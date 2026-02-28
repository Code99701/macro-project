import pandas as pd
df = pd.read_csv(r"D:\sem 4\Macro project\IPL Matches 2008-2020 (1).csv")


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


# Checking missing values
# print(df.isnull().sum())

# Handling missing values
# df['city'] = df['city'].fillna('Unknown')
# df['player_of_match'] = df['player_of_match'].fillna('Not Awarded')
# df['method'] = df['method'].fillna('Regular')
# df['result_margin'] = df['result_margin'].fillna(0)

# Verifying after handling
# print(df.isnull().sum())
# print((df.isnull().sum() / len(df)) * 100)

#________________________________________DATA CLEANING_______________________________________________

# Checking duplicate records
# print(df.duplicated().sum())

# Removing duplicate rows
# df = df.drop_duplicates()

# Cleaning text fields by removing extra spaces
# df['team1'] = df['team1'].str.strip()
# df['team2'] = df['team2'].str.strip()
# df['winner'] = df['winner'].str.strip()

# Verifying cleaning results
# print(df.duplicated().sum())
# print(df['team1'].unique())
# print(df['result'].unique())

# ---------------- Data Transformation ----------------

# Converting date column to datetime format
# df['date'] = pd.to_datetime(df['date'])

# Extracting year and month from date
# df['match_year'] = df['date'].dt.year
# df['match_month'] = df['date'].dt.month

# Converting neutral venue indicator to categorical values
# df['neutral_venue'] = df['neutral_venue'].replace({0: 'No', 1: 'Yes'})

# Handling result type for clarity
# df['win_type'] = df['result'].fillna('No Result')

# Verifying data types after transformation
# print(df.dtypes)
# print(df.head())

# ---------------- Feature Engineering ----------------

# Margin Category Feature
df['margin_category'] = df['result_margin'].apply(
    lambda x: 'Big Win' if x > 50 else ('Close Win' if x > 0 else 'No Margin')
)

# Toss Impact Feature
df['toss_impact'] = (df['toss_winner'] == df['winner']).map({True: 'Yes', False: 'No'})

# Match Type Feature
df['match_type'] = df['eliminator'].map({'Y': 'Playoff', 'N': 'League'})

# Venue Advantage Feature
df['venue_advantage'] = (df['team1'] == df['winner']).map({True: 'Team1', False: 'Team2'})

# Season Feature (MAKE SURE match_year EXISTS)
if 'match_year' in df.columns:
    df['season'] = df['match_year'].astype(str)
else:
    print("Error: match_year column not found. Run data transformation first.")

print(df.head())

# ---------------- Final Dataset Validation ----------------

print(df.isnull().sum())
print(df.duplicated().sum())
print(df.shape)

# pd.set_option('display.max_columns', None)
print(df.head())

# save final Dataset
df.to_csv("final_preprocessed_ipl.csv", index=False)

print("Final preprocessed dataset saved successfully.")