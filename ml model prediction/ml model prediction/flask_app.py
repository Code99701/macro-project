from flask import Flask, render_template, request, jsonify
from models import db, PredictionHistory
from sqlalchemy import func
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'predictions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context(): db.create_all()

# --- LOAD AI AND DATASETS ---
pipe = pickle.load(open('pipe.pkl', 'rb'))

try:
    delivery = pd.read_csv('deliveries.csv')
    matches_df = pd.read_csv('matches.csv')
    
    # Preprocess Full Dataset exactly like in notebook for match_progression
    total_score_df = delivery.groupby(['match_id','inning']).sum()['total_runs'].reset_index()
    total_score_df = total_score_df[total_score_df['inning'] == 1]
    match_df = matches_df.merge(total_score_df[['match_id','total_runs']],left_on='id',right_on='match_id')
    match_df['city'] = match_df['city'].fillna('Mumbai') # Simple fillna
    
    delivery_df = match_df.merge(delivery,on='match_id')
    delivery_df = delivery_df[delivery_df['inning'] == 2]
    
    # Calculate rolling targets and crr/rrr for the entire dataset
    delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs_y'].cumsum()
    delivery_df['runs_left'] = delivery_df['total_runs_x'] - delivery_df['current_score']
    delivery_df['balls_left'] = 120 - (delivery_df['over']*6 + delivery_df['ball'])
    
    delivery_df['player_dismissed'] = delivery_df['player_dismissed'].fillna("0")
    delivery_df['player_dismissed'] = delivery_df['player_dismissed'].apply(lambda x: 0 if x == "0" else 1)
    delivery_df['player_dismissed'] = delivery_df['player_dismissed'].astype('int')
    wickets = delivery_df.groupby('match_id')['player_dismissed'].cumsum()
    delivery_df['wickets'] = 10 - wickets
    
    delivery_df['crr'] = (delivery_df['current_score']*6)/(120 - delivery_df['balls_left'])
    delivery_df['rrr'] = (delivery_df['runs_left']*6)/delivery_df['balls_left']
    
    # Clean up negatives resulting from over 120 balls
    delivery_df['crr'] = delivery_df['crr'].fillna(0)
    delivery_df['rrr'] = delivery_df['rrr'].fillna(0)
    
except Exception as e:
    print("Dataset load error:", e)
    delivery_df = pd.DataFrame()
    matches_df = pd.DataFrame()

teams = ['Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab', 'Kolkata Knight Riders', 
         'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

cities = ['Abu Dhabi', 'Ahmedabad', 'Bangalore', 'Bengaluru', 'Bloemfontein', 'Cape Town', 
          'Centurion', 'Chandigarh', 'Chennai', 'Cuttack', 'Delhi', 'Dharamsala', 'Durban', 
          'East London', 'Hyderabad', 'Indore', 'Jaipur', 'Johannesburg', 'Kimberley', 'Kolkata', 
          'Mohali', 'Mumbai', 'Nagpur', 'Port Elizabeth', 'Pune', 'Raipur', 'Ranchi', 'Sharjah', 'Visakhapatnam']

def compute_single_prob(batting_team, bowling_team, city, target, score, overs, wickets):
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    wickets_left = 10 - wickets
    crr = 0 if overs == 0 else score / overs
    rrr = 0 if balls_left <= 0 else (runs_left * 6) / balls_left
    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city],
                             'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets_left],
                             'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})
    result = pipe.predict_proba(input_df)
    return round(result[0][0] * 100), round(result[0][1] * 100) # loss, win

def generate_synthetic_progression(batting_team, bowling_team, city, target, score, overs, wickets):
    crr = score / overs if overs > 0 else 0
    runs_needed = target - score
    overs_left = 20.0 - overs
    rrr = runs_needed / overs_left if overs_left > 0 else 0
    
    timeline = []
    prev_runs = 0
    prev_wickets = 0
    
    for o in range(1, 21):
        if o <= overs:
            curr_runs = (score / overs) * o if overs > 0 else 0
            curr_wickets = (wickets / overs) * o if overs > 0 else 0
        else:
            curr_runs = score + (o - overs) * rrr
            curr_wickets = wickets
            
        curr_runs = min(curr_runs, target)
        curr_wickets = min(curr_wickets, 10)
        
        runs_in_over = max(0, curr_runs - prev_runs)
        wickets_in_over = max(0, curr_wickets - prev_wickets)
        
        loss_p, win_p = compute_single_prob(batting_team, bowling_team, city, target, curr_runs, float(o), curr_wickets)
        
        if o >= 20 and curr_runs < target: win_p, loss_p = 0, 100
        if curr_runs >= target: win_p, loss_p = 100, 0
        if curr_wickets >= 10: win_p, loss_p = 0, 100
            
        timeline.append({
            'over': o,
            'runs': runs_in_over,
            'wickets': wickets_in_over,
            'win_prob': win_p,
            'loss_prob': loss_p
        })
        
        prev_runs = curr_runs
        prev_wickets = curr_wickets
        
    return timeline

# --- ENDPOINTS ---
@app.route('/')
def home():
    return render_template('index.html', teams=sorted(teams), cities=sorted(cities))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        loss_prob, win_prob = compute_single_prob(data.get('batting_team'), data.get('bowling_team'), data.get('city'), 
                                                  int(data.get('target', 0)), int(data.get('score', 0)), 
                                                  float(data.get('overs', 0.0)), int(data.get('wickets', 0)))

        timeline = generate_synthetic_progression(data.get('batting_team'), data.get('bowling_team'), data.get('city'), 
                                                  int(data.get('target', 0)), int(data.get('score', 0)), 
                                                  float(data.get('overs', 0.0)), int(data.get('wickets', 0)))

        new_pred = PredictionHistory(batting_team=data.get('batting_team'), bowling_team=data.get('bowling_team'), 
                                     city=data.get('city'), target=int(data.get('target', 0)), score=int(data.get('score', 0)), 
                                     overs=float(data.get('overs', 0.0)), wickets=int(data.get('wickets', 0)),
                                     win_probability=win_prob, loss_probability=loss_prob)
        db.session.add(new_pred)
        db.session.commit()
        return jsonify({'success': True, 'win_probability': win_prob, 'loss_probability': loss_prob, 
                        'batting_team': data.get('batting_team'), 'bowling_team': data.get('bowling_team'),
                        'timeline': timeline})
    except Exception as e: return jsonify({'success': False, 'error': str(e)})

@app.route('/get_matches', methods=['GET'])
def get_matches():
    if matches_df.empty: return jsonify([])
    # Filter only matches involving the current top 'teams' list
    valid_teams = matches_df['team1'].isin(teams) & matches_df['team2'].isin(teams)
    all_valid_matches = matches_df[valid_teams].sort_values(by='Season', ascending=False)
    
    m_list = []
    for _, row in all_valid_matches.iterrows():
        season = str(row['Season']) # 'IPL-2019'
        m_list.append({
            'id': int(row['id']),
            'desc': f"{season} - {row['team1']} vs {row['team2']} at {row['city']}"
        })
    return jsonify(m_list)

@app.route('/match_analyzer/<int:match_id>', methods=['GET'])
def match_analyzer(match_id):
    if delivery_df.empty: return jsonify({'success': False, 'error': 'Dataset not loaded'})
    try:
        match = delivery_df[delivery_df['match_id'] == match_id]
        if match.empty: return jsonify({'success': False, 'error': 'No 2nd innings data for this match'})
        
        # Exact Notebook match_progression Logic
        match = match[(match['ball'] == 6)]
        if match.empty: return jsonify({'success': False, 'error': 'No completed 6-ball overs found for rendering progression'})
        
        temp_df = match[['batting_team','bowling_team','city','runs_left','balls_left','wickets','total_runs_x','crr','rrr']].dropna()
        temp_df = temp_df[temp_df['balls_left'] != 0]
        
        result = pipe.predict_proba(temp_df)
        temp_df['lose'] = np.round(result.T[0]*100,1)
        temp_df['win'] = np.round(result.T[1]*100,1)
        temp_df['end_of_over'] = range(1,temp_df.shape[0]+1)
        
        target = temp_df['total_runs_x'].values[0]
        # Calculate Runs per over
        runs = list(temp_df['runs_left'].values)
        new_runs = runs[:]
        runs.insert(0, target)
        temp_df['runs_after_over'] = np.array(runs)[:-1] - np.array(new_runs)
        
        # Calculate Wickets per over
        wickets = list(temp_df['wickets'].values)
        new_wickets = wickets[:]
        new_wickets.insert(0, 10)
        wickets.append(0)
        w = np.array(wickets)
        nw = np.array(new_wickets)
        temp_df['wickets_in_over'] = (nw - w)[0:temp_df.shape[0]]
        
        # Format output for Chart JS
        timeline = []
        for _, row in temp_df.iterrows():
            timeline.append({
                'over': int(row['end_of_over']),
                'runs': float(row['runs_after_over']),
                'wickets': float(row['wickets_in_over']),
                'win_prob': float(row['win']),
                'loss_prob': float(row['lose'])
            })
            
        return jsonify({
            'success': True,
            'batting_team': temp_df['batting_team'].iloc[0],
            'bowling_team': temp_df['bowling_team'].iloc[0],
            'target': int(target),
            'timeline': timeline
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/analytics', methods=['GET'])
def analytics():
    top = db.session.query(PredictionHistory.batting_team, func.count(PredictionHistory.id).label('c')).group_by(PredictionHistory.batting_team).order_by(db.text('c DESC')).limit(5).all()
    avg = db.session.query(func.avg(PredictionHistory.win_probability), func.avg(PredictionHistory.loss_probability)).first()
    recent = PredictionHistory.query.order_by(PredictionHistory.timestamp.desc()).limit(8).all()
    return jsonify({'success': True, 'top_teams': [{'team': t[0], 'count': t[1]} for t in top], 'avg_win': round(avg[0] or 0), 'avg_loss': round(avg[1] or 0), 'history': [p.to_dict() for p in recent]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
