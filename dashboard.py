import streamlit as st
import pandas as pd
from model import predict_winner

# Load dataset
df = pd.read_csv(r"D:\sem 4\MAcro project\final_preprocessed_ipl.csv")

st.title("🏏 IPL Data Analytics Dashboard")

st.write("Interactive dashboard for IPL match insights")

st.dataframe(df.head())

st.subheader("Team Wins")

team_wins = df['winner'].value_counts()

st.bar_chart(team_wins)

st.subheader("Toss Decision Distribution")

toss_counts = df['toss_decision'].value_counts()

st.bar_chart(toss_counts)

st.subheader("Matches by Venue")

venue_counts = df['venue'].value_counts().head(10)

st.bar_chart(venue_counts)

st.subheader("Match Winner Prediction")

team1 = st.selectbox("Select Team 1", df['team1'].unique())
team2 = st.selectbox("Select Team 2", df['team2'].unique())

if st.button("Predict Winner"):

    winner = predict_winner(team1, team2)

    st.success(f"Predicted Winner: {winner}")