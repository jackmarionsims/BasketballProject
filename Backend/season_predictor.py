from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression
import numpy as np

def elo_change(home_elo, visitor_elo, home_win, margin, k=20):
    expected_home = 1 / (1 + 10 ** ((visitor_elo - home_elo) / 400))
    score = 1 if home_win else 0
    elo_diff = home_elo - visitor_elo
    mov_multiplier = ((margin + 3) ** 0.8) / (7.5 + 0.006 * elo_diff)
    # mov_multiplier = min(mov_multiplier, 2)
    return k * mov_multiplier * (score - expected_home)


predictors = ['Home Team Home PPG', 'Home Team PPG', 'Visitor Team Visiting PPG', 'Visitor Team PPG', 'Home Team Home Opp PPG', "Home Team Opp PPG", "Visitor Team Visiting Opp PPG", "Visitor Team Opp PPG", "Home Team W/L%", "Home Team Home W/L%", "Visitor Team W/L%", "Visitor Team Visiting W/L%", "Home Team Home ELO", "Visitor Team ELO"]
df = pd.read_csv("../csvs/all_games.csv")
# Assume you have columns 'Home Points' and 'Visitor Points' in your df
home_model = XGBRegressor()
visitor_model = XGBRegressor()

# Use the same predictor variables
X = df[predictors]
y_home = df["Home Points"]
y_visitor = df["Visitor Points"]
years = range(1996, 2026)
for year in [2025]:
    all_train = df[df["Year"] < year]
    all_test = df[df["Year"] == year]

    X_train = all_train[predictors]
    y_home_train = all_train["Home Points"]
    y_visitor_train = all_train["Visitor Points"]

    X_test = all_test[predictors]
    y_home_test = all_test["Home Points"]
    y_visitor_test = all_test["Visitor Points"]

    home_model.fit(X_train, y_home_train)
    visitor_model.fit(X_train, y_visitor_train)

    home_train_preds = home_model.predict(X_train)
    visitor_train_preds = visitor_model.predict(X_train)

    home_residuals = y_home_train - home_train_preds
    visitor_residuals = y_visitor_train - visitor_train_preds

    # Fit normal distributions to residuals
    home_mu, home_sigma = norm.fit(home_residuals)
    visitor_mu, visitor_sigma = norm.fit(visitor_residuals)

all_stats = {}
for i in range(100):
    team_stats = {}
    predictions = all_test[["Visitor Team", "Home Team", "Date Number"]].copy()

    for idx, game in all_test.iterrows():
        home_team = game["Home Team"]
        visitor_team = game["Visitor Team"]

        # Initialize teams if not already present
        for team in [home_team, visitor_team]:
            if team not in team_stats:
                if team not in all_stats:
                    all_stats[team] = 0
                team_stats[team] = {
                    "elo": game[f"{'Home' if team == home_team else 'Visitor'} Team ELO"],
                    "wins_h": 0, "wins_v": 0,
                    "points_h": 0, "points_v": 0,
                    "opp_points_h": 0, "opp_points_v": 0,
                    "games_h": 0, "games_v": 0,
                }

        # Shorthands for readability
        h = team_stats[home_team]
        v = team_stats[visitor_team]

        total_h = h["games_h"] + h["games_v"]
        total_v = v["games_h"] + v["games_v"]

        # --- Home team stats ---
        if total_h == 0:
            predictions.loc[idx, "Home Team W/L%"] = game["Home Team W/L%"]
            predictions.loc[idx, "Home Team PPG"] = game["Home Team PPG"]
            predictions.loc[idx, "Home Team Opp PPG"] = game["Home Team Opp PPG"]
            predictions.loc[idx, "Home Team ELO"] = game["Home Team ELO"]
        else:
            predictions.loc[idx, "Home Team W/L%"] = (h["wins_h"] + h["wins_v"]) / total_h
            predictions.loc[idx, "Home Team PPG"] = (h["points_h"] + h["points_v"]) / total_h
            predictions.loc[idx, "Home Team Opp PPG"] = (h["opp_points_h"] + h["opp_points_v"]) / total_h
            predictions.loc[idx, "Home Team ELO"] = h["elo"]

        if h["games_h"] == 0:
            predictions.loc[idx, "Home Team Home W/L%"] = game["Home Team Home W/L%"]
            predictions.loc[idx, "Home Team Home PPG"] = game["Home Team Home PPG"]
            predictions.loc[idx, "Home Team Home Opp PPG"] = game["Home Team Home Opp PPG"]
            predictions.loc[idx, "Home Team Home ELO"] = game["Home Team Home ELO"]
        else:
            predictions.loc[idx, "Home Team Home W/L%"] = h["wins_h"] / h["games_h"]
            predictions.loc[idx, "Home Team Home PPG"] = h["points_h"] / h["games_h"]
            predictions.loc[idx, "Home Team Home Opp PPG"] = h["opp_points_h"] / h["games_h"]
            predictions.loc[idx, "Home Team Home ELO"] = h["elo"] + 100

        # --- Visitor team stats ---
        if total_v == 0:
            predictions.loc[idx, "Visitor Team W/L%"] = game["Visitor Team W/L%"]
            predictions.loc[idx, "Visitor Team PPG"] = game["Visitor Team PPG"]
            predictions.loc[idx, "Visitor Team Opp PPG"] = game["Visitor Team Opp PPG"]
            predictions.loc[idx, "Visitor Team ELO"] = game["Visitor Team ELO"]
        else:
            predictions.loc[idx, "Visitor Team W/L%"] = (v["wins_h"] + v["wins_v"]) / total_v
            predictions.loc[idx, "Visitor Team PPG"] = (v["points_h"] + v["points_v"]) / total_v
            predictions.loc[idx, "Visitor Team Opp PPG"] = (v["opp_points_h"] + v["opp_points_v"]) / total_v
            predictions.loc[idx, "Visitor Team ELO"] = v["elo"]

        if v["games_v"] == 0:
            predictions.loc[idx, "Visitor Team Visiting W/L%"] = game["Visitor Team Visiting W/L%"]
            predictions.loc[idx, "Visitor Team Visiting PPG"] = game["Visitor Team Visiting PPG"]
            predictions.loc[idx, "Visitor Team Visiting Opp PPG"] = game["Visitor Team Visiting Opp PPG"]
        else:
            predictions.loc[idx, "Visitor Team Visiting W/L%"] = v["wins_v"] / v["games_v"]
            predictions.loc[idx, "Visitor Team Visiting PPG"] = v["points_v"] / v["games_v"]
            predictions.loc[idx, "Visitor Team Visiting Opp PPG"] = v["opp_points_v"] / v["games_v"]



        if game["Playoff Game"] == 0:

            home_preds_mean = home_model.predict(predictions.loc[[idx], predictors])
            visitor_preds_mean = visitor_model.predict(predictions.loc[[idx], predictors])

            home_preds_sampled = home_preds_mean + np.random.normal(home_mu, home_sigma, size=len(home_preds_mean))
            visitor_preds_sampled = visitor_preds_mean + np.random.normal(visitor_mu, visitor_sigma, size=len(visitor_preds_mean))


            home_rounded = np.round(home_preds_sampled).astype(int)
            visitor_rounded = np.round(visitor_preds_sampled).astype(int)
            # home_rounded = np.round(home_preds_mean).astype(int)
            # visitor_rounded = np.round(visitor_preds_mean).astype(int)

            home_points = home_rounded.item()
            visitor_points = visitor_rounded.item()
            if home_points == visitor_points:
                if (home_preds_sampled.item() >= visitor_preds_sampled.item()):
                    home_points += 1
                else:
                    visitor_points += 1
            
            predictions.loc[idx, "Visitor Points"] = game["Visitor Points"]
            predictions.loc[idx, "Visitor Predictions"] = visitor_points
            predictions.loc[idx, "Home Points"] = game["Home Points"]
            predictions.loc[idx, "Home Predictions"] = home_points

            h["games_h"] += 1
            v["games_v"] += 1

            # Update points scored
            h["points_h"] += home_points
            v["points_v"] += visitor_points

            # Update opponent points
            h["opp_points_h"] += visitor_points
            v["opp_points_v"] += home_points

            # Update wins
            if home_points > visitor_points:
                h["wins_h"] += 1
                elo_c = elo_change(h["elo"] + 100, v["elo"], True, home_points - visitor_points)
                h["elo"] += elo_c
                v["elo"] -= elo_c
            else:
                v["wins_v"] += 1
                elo_c = elo_change(h["elo"] + 100, v["elo"], False, visitor_points - home_points)
                h["elo"] += elo_c
                v["elo"] -= elo_c
        
    for team in team_stats.keys():
        all_stats[team] += team_stats[team]["wins_h"] + team_stats[team]["wins_v"]

for team in all_stats.keys():
    print(team, all_stats[team] / 100)

predictions.to_csv("season_predictions.csv", index=False)
