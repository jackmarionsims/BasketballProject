from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np
from scipy.stats import norm

predictors = ['W/L% Diff Z-Score', 'Avg Points Margin Diff Z-Score', 'Avg TS% Margin Diff Z-Score', 'Location ELO Diff Z-Score', 'Avg FGM Margin Diff Z-Score', 'Avg FG% Margin Diff Z-Score', 'Total Starters Career EFF Diff',
'Total Starters Season EFF Diff']
predictors = ['W/L% Diff Z-Score', 'Avg Points Margin Diff Z-Score', 'Avg TS% Margin Diff Z-Score', 'Location ELO Diff Z-Score', 'Avg FGM Margin Diff Z-Score', 'Avg FG% Margin Diff Z-Score', 'Total Starters Career EFF Diff',
'Total Starters Season EFF Diff']
predictors = ["Visitor Team Points Avg",
        "Home Team Points Avg", "Home Team Assists Avg", "Home Team Tot Rebounds Avg", "Home Team Off Rebounds Avg", "Home Team Def Rebounds Avg",
        "Visitor Team Assists Avg", "Visitor Team Tot Rebounds Avg",
        "Visitor Team Off Rebounds Avg", "Visitor Team Def Rebounds Avg",
        "Home Team Home ELO","Visitor Team ELO", "Home Team W/L%",
        "Visitor Team W/L%",]
df = pd.read_csv("csvs/team_effs.csv")
df = pd.read_csv("csvs/all_games2.csv")
# Assume you have columns 'Home Points' and 'Visitor Points' in your df
home_model = XGBRegressor()
visitor_model = XGBRegressor()

# Use the same predictor variables
X = df[predictors]
y_home = df["Home Team Points"]
y_visitor = df["Visitor Team Points"]
years = range(1991, 2026)
for year in years:
    all_train = df[df["Year"] < year]
    all_test = df[df["Year"] == year]

    X_train = all_train[predictors]
    y_home_train = all_train["Home Team Points"]
    y_visitor_train = all_train["Visitor Team Points"]

    X_test = all_test[predictors]
    y_home_test = all_test["Home Team Points"]
    y_visitor_test = all_test["Visitor Team Points"]

    home_model.fit(X_train, y_home_train)
    visitor_model.fit(X_train, y_visitor_train)

    home_model.save_model("home_model_scores.json")
    visitor_model.save_model("visitor_model_scores.json")

    # home_train_preds = home_model.predict(X_train)
    # visitor_train_preds = visitor_model.predict(X_train)

    # home_residuals = y_home_train - home_train_preds
    # visitor_residuals = y_visitor_train - visitor_train_preds

    # # Fit normal distributions to residuals
    # home_mu, home_sigma = norm.fit(home_residuals)
    # visitor_mu, visitor_sigma = norm.fit(visitor_residuals)

    home_preds_mean = home_model.predict(X_test)
    visitor_preds_mean = visitor_model.predict(X_test)
    # home_preds_sampled = home_preds_mean + np.random.normal(home_mu, home_sigma, size=len(home_preds_mean))
    # visitor_preds_sampled = visitor_preds_mean + np.random.normal(visitor_mu, visitor_sigma, size=len(visitor_preds_mean))


    # home_rounded = np.round(home_preds_sampled).astype(int)
    # visitor_rounded = np.round(visitor_preds_sampled).astype(int)
    home_rounded = np.round(home_preds_mean).astype(int)
    visitor_rounded = np.round(visitor_preds_mean).astype(int)
    for i in range(len(home_rounded)):
        if home_rounded[i] == visitor_rounded[i]:
            if (home_preds_mean[i] >= visitor_preds_mean[i]):
                home_rounded[i] += 1
            else:
                visitor_rounded[i] += 1

    # Combine results with test data
    all_test = all_test.copy()
    preds = all_test[["Visitor Team", "Home Team", "Visitor Points", "Home Points"]]
    preds["Predicted Visitor Score"] = visitor_rounded
    preds["Predicted Home Score"] = home_rounded
    preds["Date Number"] = all_test["Date Number"]
    preds["Year"] = all_test["Year"]

    # Optional: save predictions each year
    if year == years[0]:
        all_predictions = preds
    else:
        all_predictions = pd.concat([all_predictions, preds], ignore_index=True)

# Save all predictions
predicted_wins = [1 if row["Predicted Home Score"] > row["Predicted Visitor Score"] else 0 for _, row in all_predictions.iterrows()]
# years_predicted = df[df["Year"] >= 1996]
# print(accuracy_score(years_predicted["Home Win"], predicted_wins ))
# all_predictions.to_csv("score_predictions.csv", index=False)
