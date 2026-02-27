import pandas as pd
df = pd.read_csv(r"D:\sem 4\Macro project\IPL Matches 2008-2020 (1).csv")

# ________________________________________dataset overview_____________________________________
# print(df.shape)
# print(df.columns)
# print(df.dtypes)
# print(df.head(20))

#_________________________________________dataset inspection___________________________________
# df.info()
# print(df.describe())
# print(df.isnull().sum())

# print(df['team1'].unique())
# print(df['team2'].unique())
# print(df['result'].unique())

# print(df.duplicated().sum())

# print(df['result'].value_counts())
# print(df['toss_decision'].value_counts())

# ________________________________________MISSING value handling________________________________
# print(df.isnull().sum())


df['city'] = df['city'].fillna('Unknown')
df['player_of_match'] = df['player_of_match'].fillna('Not Awarded')
df['method'] = df['method'].fillna('Regular')
df['result_margin'] = df['result_margin'].fillna(0)

# print(df.isnull().sum())
# print((df.isnull().sum() / len(df)) * 100)

#________________________________________DATA CLEANING_______________________________________________

# print(df.duplicated().sum())
# print((df.isnull().sum() / len(df)) * 100)

df = df.drop_duplicates()

df['team1'] = df['team1'].str.strip()
df['team2'] = df['team2'].str.strip()
df['winner'] = df['winner'].str.strip()

# print(df['team1'].unique())
# print(df['result'].unique())

df['team1'] = df['team1'].replace('Old Name', 'Standard Name')
# print(df[df['winner'].isnull()])

# print(df.shape)
# print(df.isnull().sum())

# ---------------- Data Transformation ----------------

df['date'] = pd.to_datetime(df['date'])

df['match_year'] = df['date'].dt.year
df['match_month'] = df['date'].dt.month

df['neutral_venue'] = df['neutral_venue'].replace({0: 'No', 1: 'Yes'})

df['win_type'] = df['result'].fillna('No Result')

# print(df.dtypes)
# print(df.head())

# ---------------- Feature Engineering ----------------

df['margin_category'] = df['result_margin'].apply(
    lambda x: 'Big Win' if x > 50 else ('Close Win' if x > 0 else 'No Margin')
)

df['toss_impact'] = (df['toss_winner'] == df['winner']).replace({True: 'Yes', False: 'No'})

df['match_type'] = df['eliminator'].replace({'Y': 'Playoff', 'N': 'League'})

df['venue_advantage'] = (df['team1'] == df['winner']).replace({True: 'Team1', False: 'Team2'})

df['season'] = df['match_year'].astype(str)

# print(df.head())

# ---------------- Final Dataset Validation ----------------

# print(df.isnull().sum())
# print(df.duplicated().sum())
# print(df.shape)

pd.set_option('display.max_columns', None)
# print(df.head())

df.to_csv("final_preprocessed_ipl.csv", index=False)

print("Final preprocessed dataset saved successfully.")