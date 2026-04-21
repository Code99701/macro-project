import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

ML_DIR   = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(ML_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')

CITY_ALIASES = {
    'Bangalore':  'Bengaluru',
    'Dharamsala': 'Dharamshala',
}

def normalize_city(city):
    return CITY_ALIASES.get(city, city)

def build_ground_map():
    gs = pd.read_csv(os.path.join(DATA_DIR, 'cricket_ground_sizes.csv'))
    gs['avg_boundary'] = (gs['Min_Boundary_m'] + gs['Max_Boundary_m']) / 2.0
    ground_map = dict(zip(gs['City'], gs['avg_boundary']))
    ground_map['Bangalore']  = ground_map.get('Bengaluru',   67.5)
    ground_map['Dharamsala'] = ground_map.get('Dharamshala', 75.0)
    return ground_map

GROUND_MAP       = build_ground_map()
DEFAULT_BOUNDARY = 67.5

def get_avg_boundary(city):
    return GROUND_MAP.get(city, DEFAULT_BOUNDARY)


def add_engineered_features(df):
    """
    Comprehensive cricket-aware feature engineering.

    Covers: ground size impact, phase-relative difficulty, par curve,
    wicket pressure, slog potential, and batting momentum.
    All features are bounded to prevent extrapolation instability.
    """
    df = df.copy()
    balls_bowled = (120 - df['balls_left']).clip(1, 119)
    overs_bowled = balls_bowled / 6.0

    # ── Basic rate features ──────────────────────────────────────────
    df['crr_rrr_ratio']   = (df['crr'] / df['rrr'].replace(0, np.nan)).fillna(3.0).clip(0, 8)
    df['balls_per_wicket']= (df['balls_left'] / df['wickets'].replace(0, np.nan)).fillna(0).clip(0, 60)
    df['runs_per_wicket'] = (df['runs_left'] / df['wickets'].replace(0, np.nan)).fillna(df['runs_left']).clip(0, 200)

    # ── Match phase (0=powerplay, 1=middle, 2=death) ────────────────
    df['phase'] = pd.cut(overs_bowled, bins=[-1, 6, 15, 20],
                         labels=[0, 1, 2]).astype(float)

    # ── Score completion (fraction of target already scored) ─────────
    current_score        = (df['total_runs_x'] - df['runs_left']).clip(0)
    df['score_completion']= (current_score / df['total_runs_x']).clip(0, 1)

    # ── Log-scaled target (reduce bias for rare high-target matches) ─
    df['log_target']     = np.log1p(df['total_runs_x'])

    # ── Wicket-rate composite ────────────────────────────────────────
    df['wicket_rate_index'] = df['crr_rrr_ratio'] * (df['wickets'] / 10.0)

    # ── Ground-adjusted RRR ──────────────────────────────────────────
    # Large ground (>67.5m) → harder to score → effective RRR is higher.
    # Small ground (<67.5m) → boundaries flow → effective RRR is lower.
    # Every 8m from neutral shifts effective RRR by ~1 run/over.
    df['ground_adj_rrr']  = (df['rrr'] + (df['avg_boundary'] - 67.5) / 8.0).clip(0, 30)

    # ── RRR difficulty given phase + ground ──────────────────────────
    # Maximum humanly achievable run rate varies by phase and ground size.
    # Powerplay (2 fielders out): ~12/over on small, ~10 on large.
    # Middle (4 fielders out):    ~10/over on small, ~8.5 on large.
    # Death slog (4 fielders):    ~14/over on small, ~11 on large.
    ground_bonus = (67.5 - df['avg_boundary']) / 8.0   # +ve for small, −ve for large
    phase_ceiling = df['phase'].map({0.0: 11.0, 1.0: 9.5, 2.0: 12.5}).fillna(9.5)
    achievable    = (phase_ceiling + ground_bonus).clip(7, 16)
    df['rrr_difficulty'] = (df['ground_adj_rrr'] / achievable).clip(0, 4)
    # < 1.0 → comfortable; 1.0–1.3 → stretched; > 1.5 → desperate

    # ── Par score deviation ──────────────────────────────────────────
    # T20 chases don't follow a linear scoring curve — teams accelerate.
    # Par model: par_score ≈ target × (balls_bowled/120)^0.75
    # (the 0.75 exponent captures powerplay boost and death acceleration)
    par_score       = df['total_runs_x'] * ((balls_bowled / 120.0) ** 0.75)
    df['par_score_diff'] = ((current_score - par_score) / df['total_runs_x']).clip(-0.5, 0.5)
    # Positive = batting team ahead of par → advantage
    # Negative = behind par → under pressure

    # ── Wicket-momentum pressure ──────────────────────────────────────
    # Runs needed per wicket per remaining over.
    # High value = each wicket is under huge scoring pressure.
    df['wicket_momentum'] = (
        df['runs_per_wicket'] / (df['balls_left'] / 6.0).replace(0, np.nan)
    ).fillna(99).clip(0, 30)

    # ── Slog potential ────────────────────────────────────────────────
    # Death overs (last 5) are where T20 matches turn.
    # Wickets in hand × remaining death overs = explosive finish capability.
    death_overs_remaining = (20.0 - overs_bowled).clip(0, 5)
    df['slog_potential']  = death_overs_remaining * (df['wickets'] / 10.0)

    # ── Batting momentum ──────────────────────────────────────────────
    # CRR/RRR advantage amplified by depth of batting lineup.
    # Captures: "team is cruising AND has 7 wickets left"
    df['batting_momentum'] = df['crr_rrr_ratio'] * np.log1p(df['wickets'])

    return df


def prepare_data():
    match    = pd.read_csv(os.path.join(DATA_DIR, 'matches.csv'))
    delivery = pd.read_csv(os.path.join(DATA_DIR, 'deliveries.csv'))

    total_score_df = (
        delivery.groupby(['match_id', 'inning'])['total_runs'].sum().reset_index()
    )
    total_score_df = total_score_df[total_score_df['inning'] == 1]

    match_df = match.merge(
        total_score_df[['match_id', 'total_runs']], left_on='id', right_on='match_id'
    )

    TEAM_MAP = {
        'Delhi Daredevils':         'Delhi Capitals',
        'Deccan Chargers':          'Sunrisers Hyderabad',
        'Gujarat Lions':            'Kings XI Punjab',
        'Rising Pune Supergiant':   'Rajasthan Royals',
        'Rising Pune Supergiants':  'Rajasthan Royals',
        'Pune Warriors':            'Rajasthan Royals',
        'Kochi Tuskers Kerala':     'Royal Challengers Bangalore',
    }
    for col in ['team1', 'team2']:
        match_df[col] = match_df[col].replace(TEAM_MAP)

    ACTIVE_TEAMS = [
        'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
        'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
        'Rajasthan Royals', 'Delhi Capitals'
    ]
    match_df = match_df[
        match_df['team1'].isin(ACTIVE_TEAMS) & match_df['team2'].isin(ACTIVE_TEAMS)
    ]
    match_df['city'] = match_df['city'].fillna('Mumbai').apply(normalize_city)
    match_df = match_df[match_df['dl_applied'] == 0]
    match_df = match_df[['match_id', 'city', 'winner', 'total_runs']]

    delivery_df = match_df.merge(delivery, on='match_id')
    delivery_df = delivery_df[delivery_df['inning'] == 2]
    for col in ['batting_team', 'bowling_team']:
        delivery_df[col] = delivery_df[col].replace(TEAM_MAP)

    delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs_y'].cumsum()
    delivery_df['runs_left']     = delivery_df['total_runs_x'] - delivery_df['current_score']
    delivery_df['balls_left']    = 120 - (delivery_df['over'] * 6 + delivery_df['ball'])

    delivery_df['player_dismissed'] = (
        delivery_df['player_dismissed'].fillna('0')
        .apply(lambda x: 0 if x == '0' else 1).astype(int)
    )
    delivery_df['wickets'] = 10 - delivery_df.groupby('match_id')['player_dismissed'].cumsum()

    balls_bowled = 120 - delivery_df['balls_left']
    delivery_df['crr'] = (delivery_df['current_score'] * 6) / balls_bowled.replace(0, np.nan)
    delivery_df['rrr'] = (delivery_df['runs_left'] * 6) / delivery_df['balls_left'].replace(0, np.nan)
    delivery_df['crr'] = delivery_df['crr'].fillna(0)
    delivery_df['rrr'] = delivery_df['rrr'].fillna(0)

    delivery_df['avg_boundary'] = delivery_df['city'].apply(get_avg_boundary)
    delivery_df['result'] = (delivery_df['batting_team'] == delivery_df['winner']).astype(int)

    final_df = delivery_df[[
        'batting_team', 'bowling_team', 'city',
        'runs_left', 'balls_left', 'wickets',
        'total_runs_x', 'crr', 'rrr', 'avg_boundary', 'result'
    ]].dropna()
    final_df = final_df[final_df['balls_left'] > 0]
    final_df = add_engineered_features(final_df)
    return final_df


print("Preparing data...")
df = prepare_data()
print(f"Dataset shape: {df.shape}")

X = df.drop(columns=['result'])
y = df['result']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

CAT_COLS = ['batting_team', 'bowling_team', 'city']

trf = ColumnTransformer([
    ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CAT_COLS)
], remainder='passthrough')

pipe = Pipeline(steps=[
    ('encoder', trf),
    ('model', RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        min_samples_leaf=2,
        max_features='sqrt',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    ))
])

print("Training model...")
pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)
print(f"Test Accuracy : {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=['Bowling team wins', 'Batting team wins']))

with open(os.path.join(ML_DIR, 'pipe.pkl'), 'wb') as f:
    pickle.dump(pipe, f)

with open(os.path.join(ML_DIR, 'ground_map.pkl'), 'wb') as f:
    pickle.dump(GROUND_MAP, f)

print("Saved pipe.pkl and ground_map.pkl.")