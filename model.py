import pandas as pd
import pickle

# Load dataset
df = pd.read_csv("final_preprocessed_ipl.csv")

# Load trained model
rf_model = pickle.load(open("rf_model.pkl", "rb"))
encoders = pickle.load(open("encoders.pkl", "rb"))

# Feature order used during training
features = [
    'team1',
    'team2',
    'toss_winner',
    'toss_decision',
    'venue',
    'match_type',
    'toss_impact',
    'margin_category'
]

# Team encoding (same as training)
team_to_code = {
    "Chennai Super Kings": 0,
    "Deccan Chargers": 1,
    "Delhi Capitals": 2,
    "Delhi Daredevils": 3,
    "Gujarat Lions": 4,
    "Kings XI Punjab": 5,
    "Kochi Tuskers Kerala": 6,
    "Kolkata Knight Riders": 7,
    "Mumbai Indians": 8,
    "Pune Warriors": 9,
    "Rajasthan Royals": 10,
    "Rising Pune Supergiant": 11,
    "Rising Pune Supergiants": 12,
    "Royal Challengers Bangalore": 13,
    "Sunrisers Hyderabad": 14
}

# Reverse mapping
code_to_team = {v: k for k, v in team_to_code.items()}


def predict_winner(team1, team2):

    # default match values
    toss_winner = team1
    toss_decision = "bat"
    venue = "M Chinnaswamy Stadium"
    match_type = "League"
    toss_impact = 1
    margin_category = 2

    input_data = pd.DataFrame([[
        team1,
        team2,
        toss_winner,
        toss_decision,
        venue,
        match_type,
        toss_impact,
        margin_category
    ]], columns=features)

    # encode categorical columns using trained encoders
    categorical_cols = [
        "team1",
        "team2",
        "toss_winner",
        "toss_decision",
        "venue",
        "match_type"
    ]

    for col in categorical_cols:
        if col in encoders:
            input_data[col] = encoders[col].transform(input_data[col])

    # prediction
    prediction = rf_model.predict(input_data)

    # convert predicted label back to team name
    winner = encoders["winner"].inverse_transform(prediction)

    return winner[0]