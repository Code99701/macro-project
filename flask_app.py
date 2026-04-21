from flask import Flask, render_template, request, jsonify
import sys, os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))

from models import db, PredictionHistory
from sqlalchemy import func
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

DB_PATH = os.path.join(BASE_DIR, 'app', 'predictions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

ML_DIR     = os.path.join(BASE_DIR, 'ml')
DATA_DIR   = os.path.join(BASE_DIR, 'data')
try:
    pipe = pickle.load(open(os.path.join(ML_DIR, 'pipe.pkl'), 'rb'))
except:
    pipe = None
    print("[WARNING] pipe.pkl not loaded")

try:
    GROUND_MAP = pickle.load(open(os.path.join(ML_DIR, 'ground_map.pkl'), 'rb'))
except:
    GROUND_MAP = {}
    print("[WARNING] ground_map.pkl not loaded")

CITY_ALIASES = {
    'Bangalore':  'Bengaluru',
    'Dharamsala': 'Dharamshala',
}

TEAM_MAP = {
    'Delhi Daredevils':         'Delhi Capitals',
    'Deccan Chargers':          'Sunrisers Hyderabad',
    'Gujarat Lions':            'Kings XI Punjab',
    'Rising Pune Supergiant':   'Rajasthan Royals',
    'Rising Pune Supergiants':  'Rajasthan Royals',
    'Pune Warriors':            'Rajasthan Royals',
    'Kochi Tuskers Kerala':     'Royal Challengers Bangalore',
}

DEFAULT_BOUNDARY = 67.5

def normalize_city(city):
    return CITY_ALIASES.get(city, city)

def normalize_team(team):
    return TEAM_MAP.get(team, team)

def get_avg_boundary(city):
    return GROUND_MAP.get(normalize_city(city), DEFAULT_BOUNDARY)


def add_engineered_features(df):
    df = df.copy()
    balls_bowled = (120 - df['balls_left']).clip(1, 119)
    overs_bowled = balls_bowled / 6.0

    df['crr_rrr_ratio']    = (df['crr'] / df['rrr'].replace(0, np.nan)).fillna(3.0).clip(0, 8)
    df['balls_per_wicket'] = (df['balls_left'] / df['wickets'].replace(0, np.nan)).fillna(0).clip(0, 60)
    df['runs_per_wicket']  = (df['runs_left'] / df['wickets'].replace(0, np.nan)).fillna(df['runs_left']).clip(0, 200)
    df['phase']            = pd.cut(overs_bowled, bins=[-1, 6, 15, 20], labels=[0, 1, 2]).astype(float)

    current_score          = (df['total_runs_x'] - df['runs_left']).clip(0)
    df['score_completion'] = (current_score / df['total_runs_x']).clip(0, 1)
    df['log_target']       = np.log1p(df['total_runs_x'])
    df['wicket_rate_index']= df['crr_rrr_ratio'] * (df['wickets'] / 10.0)

    df['ground_adj_rrr']   = (df['rrr'] + (df['avg_boundary'] - 67.5) / 8.0).clip(0, 30)

    ground_bonus   = (67.5 - df['avg_boundary']) / 8.0
    phase_ceiling  = df['phase'].map({0.0: 11.0, 1.0: 9.5, 2.0: 12.5}).fillna(9.5)
    achievable     = (phase_ceiling + ground_bonus).clip(7, 16)
    df['rrr_difficulty']   = (df['ground_adj_rrr'] / achievable).clip(0, 4)

    par_score              = df['total_runs_x'] * ((balls_bowled / 120.0) ** 0.75)
    df['par_score_diff']   = ((current_score - par_score) / df['total_runs_x']).clip(-0.5, 0.5)

    df['wicket_momentum']  = (
        df['runs_per_wicket'] / (df['balls_left'] / 6.0).replace(0, np.nan)
    ).fillna(99).clip(0, 30)

    death_overs_remaining  = (20.0 - overs_bowled).clip(0, 5)
    df['slog_potential']   = death_overs_remaining * (df['wickets'] / 10.0)
    df['batting_momentum'] = df['crr_rrr_ratio'] * np.log1p(df['wickets'])

    return df


try:
    delivery   = pd.read_csv(os.path.join(DATA_DIR, 'deliveries.csv'))
    matches_df = pd.read_csv(os.path.join(DATA_DIR, 'matches.csv'))

    total_score_df = (
        delivery.groupby(['match_id', 'inning'])['total_runs'].sum().reset_index()
    )
    total_score_df = total_score_df[total_score_df['inning'] == 1]
    match_df = matches_df.merge(
        total_score_df[['match_id', 'total_runs']], left_on='id', right_on='match_id'
    )
    match_df['city'] = match_df['city'].fillna('Mumbai').apply(normalize_city)

    delivery_df = match_df.merge(delivery, on='match_id')
    delivery_df = delivery_df[delivery_df['inning'] == 2]
    delivery_df['batting_team'] = delivery_df['batting_team'].replace(TEAM_MAP)
    delivery_df['bowling_team'] = delivery_df['bowling_team'].replace(TEAM_MAP)

    delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs_y'].cumsum()
    delivery_df['runs_left']     = delivery_df['total_runs_x'] - delivery_df['current_score']
    delivery_df['balls_left']    = 120 - (delivery_df['over'] * 6 + delivery_df['ball'])

    delivery_df['player_dismissed'] = (
        delivery_df['player_dismissed'].fillna('0')
        .apply(lambda x: 0 if x == '0' else 1).astype(int)
    )
    delivery_df['wickets'] = 10 - delivery_df.groupby('match_id')['player_dismissed'].cumsum()

    balls_bowled_col = 120 - delivery_df['balls_left']
    delivery_df['crr'] = (delivery_df['current_score'] * 6) / balls_bowled_col.replace(0, np.nan)
    delivery_df['rrr'] = (delivery_df['runs_left'] * 6) / delivery_df['balls_left'].replace(0, np.nan)
    delivery_df['crr'] = delivery_df['crr'].fillna(0)
    delivery_df['rrr'] = delivery_df['rrr'].fillna(0)
    delivery_df['avg_boundary'] = delivery_df['city'].apply(get_avg_boundary)
    delivery_df = add_engineered_features(delivery_df)

    print("[OK] Datasets loaded.")
except Exception as e:
    print("[ERROR] Dataset load error: " + str(e))
    delivery_df = pd.DataFrame()
    matches_df  = pd.DataFrame()

teams = sorted([
    'Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab',
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
])

cities = sorted([
    'Abu Dhabi', 'Ahmedabad', 'Bangalore', 'Bengaluru', 'Bloemfontein',
    'Cape Town', 'Centurion', 'Chandigarh', 'Chennai', 'Cuttack', 'Delhi',
    'Dharamsala', 'Durban', 'East London', 'Hyderabad', 'Indore', 'Jaipur',
    'Johannesburg', 'Kanpur', 'Kimberley', 'Kochi', 'Kolkata', 'Mohali',
    'Mumbai', 'Nagpur', 'Port Elizabeth', 'Pune', 'Raipur', 'Rajkot',
    'Ranchi', 'Sharjah', 'Visakhapatnam'
])


def evaluate_absolute_constraints(runs_left, balls_left, wickets_left):
    """Hard cricket rules — no ML model should override these."""
    if runs_left <= 0:
        return (0, 100)
    if balls_left <= 0:
        return (100, 0)
    if wickets_left <= 0:
        return (100, 0)
    if balls_left * 6 < runs_left:
        return (100, 0)
    if balls_left == 1 and runs_left > 6:
        return (100, 0)
    if runs_left <= 1 and balls_left >= 6:
        return (0, 100)
    if runs_left <= 6 and balls_left >= 12 and wickets_left >= 2:
        return (2, 98)
    return None



def physics_calibrate(win_prob, loss_prob, crr, rrr, wickets_left, balls_left, avg_boundary, runs_left):
    """
    Tiered RRR-based calibration layer.

    Core idea: Required Run Rate is the single best predictor of remaining
    match difficulty. We map RRR buckets to realistic win probabilities, then
    fine-tune with wicket count, ball buffer, ground size, and match phase.

    Only overrides the ML model when physics_win > ML win_prob, so the
    model still governs scenarios within its training data distribution.
    """
    if balls_left <= 0 or wickets_left <= 0 or rrr <= 0:
        return win_prob, loss_prob

    ground_factor = (67.5 - avg_boundary) / 8.0   # +ve = small ground (easier scoring)
    overs_left    = balls_left / 6.0

    # ── Batting team calibration ────────────────────────────────────────────
    # Apply when RRR is not in extreme / impossible territory.
    # Condition: rrr < 10 (reachable), enough resources to matter.
    if 0 < rrr < 10.0 and wickets_left >= 3 and balls_left >= 12:

        # Tiered base probability keyed on RRR
        if   rrr < 2.0:  base = 97
        elif rrr < 3.0:  base = 95
        elif rrr < 4.5:  base = 91   # CSK case (3.90) lands here
        elif rrr < 6.0:  base = 82
        elif rrr < 7.5:  base = 70
        else:            base = 55   # 7.5–10.0

        # Wicket resource: neutral point = 5 wickets in hand
        # Each extra wicket above 5 adds confidence; below subtracts
        wkt_adj = max(-8.0, min(8.0, (wickets_left - 5) * 1.5))

        # Ball buffer: surplus balls over minimum needed at a conservative 9/over
        # Positive = batting team has time to absorb a slow patch
        min_balls = max(1.0, (runs_left * 6.0) / 9.0)
        ball_adj  = max(-5.0, min(5.0, (balls_left - min_balls) / 15.0))

        # Ground: small boundary = easier to score = slight batting boost
        ground_adj = ground_factor * 2.0

        # Phase: more overs remaining = more room to recover from a wobble
        phase_adj = 2 if overs_left > 10 else (1 if overs_left > 5 else 0)

        physics_win = max(5, min(95, int(base + wkt_adj + ball_adj + ground_adj + phase_adj)))
        if physics_win > win_prob:
            win_prob  = physics_win
            loss_prob = 100 - win_prob

    # ── Bowling team calibration (near-impossible chases) ──────────────────
    # High RRR + very few wickets + very few balls = bowling team dominates
    elif rrr >= 10.0 and wickets_left <= 4 and balls_left <= 36:
        physics_loss = min(92, int(55 + 3 * min(rrr - 10.0, 8.0) + 3 * (5 - wickets_left)))
        if physics_loss > loss_prob:
            loss_prob = physics_loss
            win_prob  = 100 - loss_prob

    return win_prob, loss_prob


def compute_single_prob(batting_team, bowling_team, city, target, score, overs, wickets_out):
    # ✅ CRITICAL FIX
    if pipe is None:
        return (50, 50)

    city_norm    = normalize_city(city)
    bat_norm     = normalize_team(batting_team)
    bowl_norm    = normalize_team(bowling_team)
    avg_boundary = get_avg_boundary(city)

    runs_left    = target - score
    balls_left   = 120 - int(round(overs * 6))
    wickets_left = 10 - wickets_out
    balls_bowled = 120 - balls_left

    crr = (score * 6) / balls_bowled if balls_bowled > 0 else 0.0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 999.0

    absolute = evaluate_absolute_constraints(runs_left, balls_left, wickets_left)
    if absolute is not None:
        return absolute

    input_df = pd.DataFrame({
        'batting_team': [bat_norm],
        'bowling_team': [bowl_norm],
        'city':         [city_norm],
        'runs_left':    [runs_left],
        'balls_left':   [balls_left],
        'wickets':      [wickets_left],
        'total_runs_x': [target],
        'crr':          [crr],
        'rrr':          [rrr],
        'avg_boundary': [avg_boundary],
    })
    input_df = add_engineered_features(input_df)

    try:
        result    = pipe.predict_proba(input_df)
        loss_prob = round(result[0][0] * 100)
        win_prob  = round(result[0][1] * 100)
        win_prob += 100 - (loss_prob + win_prob)

        win_prob, loss_prob = physics_calibrate(
            win_prob, loss_prob, crr, rrr, wickets_left, balls_left, avg_boundary, runs_left
        )
        return (loss_prob, win_prob)
    except Exception as e:
        print("[ERROR] Prediction failed:", e)
        return (50, 50)


def generate_synthetic_progression(batting_team, bowling_team, city, target, score, overs, wickets_out):
    crr         = score / overs if overs > 0 else 0
    runs_needed = target - score
    overs_left  = 20.0 - overs
    rrr         = runs_needed / overs_left if overs_left > 0 else 0

    timeline     = []
    prev_runs    = 0
    prev_wickets = 0

    for o in range(1, 21):
        if o <= overs:
            curr_runs    = (score / overs) * o if overs > 0 else 0
            curr_wickets = (wickets_out / overs) * o if overs > 0 else 0
        else:
            curr_runs    = score + (o - overs) * rrr
            curr_wickets = wickets_out

        curr_runs    = min(curr_runs, target)
        curr_wickets = min(curr_wickets, 10)

        loss_p, win_p = compute_single_prob(
            batting_team, bowling_team, city, target, curr_runs, float(o), curr_wickets
        )
        timeline.append({
            'over':      o,
            'runs':      round(max(0, curr_runs - prev_runs), 1),
            'wickets':   round(max(0, curr_wickets - prev_wickets), 1),
            'win_prob':  win_p,
            'loss_prob': loss_p,
        })
        prev_runs    = curr_runs
        prev_wickets = curr_wickets

    return timeline


@app.route('/')
def home():
    return render_template('index.html', teams=teams, cities=cities)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        batting_team = data.get('batting_team', '')
        bowling_team = data.get('bowling_team', '')
        city         = data.get('city', 'Mumbai')
        target       = int(data.get('target',  0))
        score        = int(data.get('score',   0))
        overs        = float(data.get('overs', 0.0))
        wickets_out  = int(data.get('wickets', 0))

        if not batting_team or not bowling_team:
            return jsonify({'success': False, 'error': 'Batting and bowling teams are required.'})
        if batting_team == bowling_team:
            return jsonify({'success': False, 'error': 'Batting and bowling teams must be different.'})
        if target < 2:
            return jsonify({'success': False, 'error': f'Target of {target} is invalid. Minimum T20 target is 2 runs.'})
        if target > 350:
            return jsonify({'success': False, 'error': f'Target of {target} is unrealistically high. T20 all-time record is ~278.'})
        if score < 0:
            return jsonify({'success': False, 'error': 'Current score cannot be negative.'})
        if score >= target:
            return jsonify({'success': False, 'error': f'Score ({score}) must be less than target ({target}) for an ongoing match.'})
        if wickets_out < 0 or wickets_out > 10:
            return jsonify({'success': False, 'error': 'Wickets out must be between 0 and 10.'})
        if overs < 0 or overs > 20:
            return jsonify({'success': False, 'error': 'Overs must be between 0 and 20.'})

        balls_bowled = int(round(overs * 6))

        if balls_bowled == 0 and score > 0:
            return jsonify({'success': False,
                'error': f'Score of {score} is impossible — no balls have been bowled yet. Score must be 0.'})

        if balls_bowled == 0 and wickets_out > 0:
            return jsonify({'success': False,
                'error': f'{wickets_out} wicket(s) cannot fall before a single ball is bowled.'})

        if balls_bowled > 0:
            absolute_max = balls_bowled * 6

            if score > absolute_max:
                if wickets_out > 0:
                    scoring_balls = max(0, balls_bowled - wickets_out)
                    adj_max = scoring_balls * 6
                    return jsonify({'success': False,
                        'error': (f'Score of {score} in {balls_bowled} ball(s) is physically impossible. '
                                  f'Absolute max = {absolute_max} runs ({balls_bowled}×6). '
                                  f'With {wickets_out} wicket(s), only {scoring_balls} scoring ball(s) remain — '
                                  f'wicket-adjusted max = {adj_max} runs. Score exceeds both limits.')})
                return jsonify({'success': False,
                    'error': f'Score of {score} in {balls_bowled} ball(s) is impossible. '
                             f'Maximum achievable is {absolute_max} runs ({balls_bowled} × 6).'})

            if wickets_out > 0 and wickets_out <= balls_bowled:
                scoring_balls  = balls_bowled - wickets_out
                wicket_adj_max = scoring_balls * 6

                if scoring_balls == 0 and score > 0:
                    return jsonify({'success': False,
                        'error': f'Score of {score} is impossible: all {balls_bowled} ball(s) resulted in a wicket, '
                                 f'leaving 0 balls to score from.'})

                if score > wicket_adj_max:
                    return jsonify({'success': False,
                        'error': (f'Score of {score} is not possible with {wickets_out} wicket(s) in {balls_bowled} ball(s). '
                                  f'{wickets_out} ball(s) used for dismissals → {scoring_balls} scoring ball(s) remaining. '
                                  f'Maximum = {wicket_adj_max} runs ({scoring_balls} × 6). '
                                  f'Reduce score to {wicket_adj_max} or reduce wickets.')})

            if wickets_out > balls_bowled:
                return jsonify({'success': False,
                    'error': f'{wickets_out} wickets in {balls_bowled} ball(s) is not possible. '
                             f'At most 1 wicket per ball (max {min(balls_bowled, 10)}).'})

        if balls_bowled >= 120 and score < target:
            return jsonify({'success': False,
                'error': 'All 20 overs have been bowled and the target has not been reached. The bowling team has won.'})

        loss_prob, win_prob = compute_single_prob(
            batting_team, bowling_team, city, target, score, overs, wickets_out
        )
        timeline = generate_synthetic_progression(
            batting_team, bowling_team, city, target, score, overs, wickets_out
        )

        avg_boundary = get_avg_boundary(city)
        ground_size  = 'Small' if avg_boundary < 65 else 'Large' if avg_boundary > 72 else 'Medium'

        db.session.add(PredictionHistory(
            batting_team=batting_team, bowling_team=bowling_team,
            city=city, target=target, score=score,
            overs=overs, wickets=wickets_out,
            win_probability=win_prob, loss_probability=loss_prob
        ))
        db.session.commit()

        return jsonify({
            'success':          True,
            'win_probability':  win_prob,
            'loss_probability': loss_prob,
            'batting_team':     batting_team,
            'bowling_team':     bowling_team,
            'ground_size':      ground_size,
            'avg_boundary_m':   avg_boundary,
            'timeline':         timeline,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_matches', methods=['GET'])
def get_matches():
    if matches_df.empty:
        return jsonify([])
    valid = matches_df['team1'].isin(teams) & matches_df['team2'].isin(teams)
    return jsonify([{
        'id':   int(row['id']),
        'desc': f"{row['Season']} - {row['team1']} vs {row['team2']} at {row['city']}"
    } for _, row in matches_df[valid].sort_values('Season', ascending=False).iterrows()])


@app.route('/match_analyzer/<int:match_id>', methods=['GET'])
def match_analyzer(match_id):
    if delivery_df.empty:
        return jsonify({'success': False, 'error': 'Dataset not loaded'})
    try:
        match = delivery_df[delivery_df['match_id'] == match_id]
        if match.empty:
            return jsonify({'success': False, 'error': 'No 2nd innings data for this match'})
        match = match[match['ball'] == 6]
        if match.empty:
            return jsonify({'success': False, 'error': 'No completed 6-ball overs found'})

        cols = [
            'batting_team', 'bowling_team', 'city',
            'runs_left', 'balls_left', 'wickets',
            'total_runs_x', 'crr', 'rrr', 'avg_boundary',
            'crr_rrr_ratio', 'balls_per_wicket', 'runs_per_wicket',
            'phase', 'score_completion', 'log_target', 'wicket_rate_index',
            'ground_adj_rrr', 'rrr_difficulty', 'par_score_diff',
            'wicket_momentum', 'slog_potential', 'batting_momentum'
        ]
        temp_df = match[cols].dropna()
        temp_df = temp_df[temp_df['balls_left'] > 0].copy()

        result          = pipe.predict_proba(temp_df)
        temp_df['lose'] = np.round(result.T[0] * 100, 1)
        temp_df['win']  = np.round(result.T[1] * 100, 1)
        temp_df['end_of_over'] = range(1, len(temp_df) + 1)

        target   = int(temp_df['total_runs_x'].values[0])
        runs_arr = list(temp_df['runs_left'].values)
        temp_df['runs_after_over']  = np.array([target] + runs_arr[:-1]) - np.array(runs_arr)
        wk_arr   = list(temp_df['wickets'].values)
        temp_df['wickets_in_over']  = np.array([10] + wk_arr[:-1]) - np.array(wk_arr)

        return jsonify({
            'success':      True,
            'batting_team': temp_df['batting_team'].iloc[0],
            'bowling_team': temp_df['bowling_team'].iloc[0],
            'target':       target,
            'timeline': [{
                'over':      int(row['end_of_over']),
                'runs':      float(row['runs_after_over']),
                'wickets':   float(row['wickets_in_over']),
                'win_prob':  float(row['win']),
                'loss_prob': float(row['lose']),
            } for _, row in temp_df.iterrows()],
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/analytics', methods=['GET'])
def analytics():
    top    = (db.session.query(PredictionHistory.batting_team,
                               func.count(PredictionHistory.id).label('c'))
              .group_by(PredictionHistory.batting_team)
              .order_by(db.text('c DESC')).limit(5).all())
    avg    = db.session.query(func.avg(PredictionHistory.win_probability),
                               func.avg(PredictionHistory.loss_probability)).first()
    recent = PredictionHistory.query.order_by(PredictionHistory.timestamp.desc()).limit(8).all()
    return jsonify({
        'success':   True,
        'top_teams': [{'team': t[0], 'count': t[1]} for t in top],
        'avg_win':   round(avg[0] or 0),
        'avg_loss':  round(avg[1] or 0),
        'history':   [p.to_dict() for p in recent],
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
