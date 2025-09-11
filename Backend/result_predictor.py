from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib

# Load data
df = pd.read_csv("csvs/model_categories.csv")
df2 = pd.read_csv("csvs/modern.csv")
# Example engineered feature
df["PTS Margin"] = df["Home Team PTS Margin Avg"] - df["Visitor Team PTS Margin Avg"]

# Define predictors (make sure these columns exist in df)
predictors = ["PTS Margin", "W/L% Margin", "ELO Margin", "Tot EFF Margin", "Home Team PTS Avg", "Visitor Team PTS Avg"]
#predictors = ["PTS Margin", "W/L% Margin", "ELO Margin", "Tot Season EFF Avg Margin", "Home Team PTS Avg", "Visitor Team PTS Avg"]

df["Tot EFF Margin"] = df2["Home Team Tot New Season EFF Avg"] - df2["Visitor Team Tot New Season EFF Avg"]
# df["Playoff Game"] = df2["Playoff Game"]
# df["Rest Days Diff"] = df2["Home Team Rest Days"] - df2["Visitor Team Rest Days"]
df["Last 10 W/L% Margin"] = df2["Home Team Last 10 W/L%"] - df2["Visitor Team Last 10 W/L%"]
# Initialize model
# model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model = LogisticRegression(max_iter=1000)

all_predictions = []

# Walk forward year by year
years = sorted(df["Season"].unique())
for year in years:
    train = df[(df["Season"] < year) & (df["Season"] >= 1986)]
    test = df[(df["Season"] == year)]

    if train.empty or test.empty:
        continue

    X_train, y_train = train[predictors], train["Home Win"]
    X_test, y_test = test[predictors], test["Home Win"]

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    test_results = test[["Game ID", "Season"]].copy()
    test_results["Predicted"] = preds
    test_results["Actual"] = y_test.values
    all_predictions.append(test_results)

# Combine predictions
all_predictions = pd.concat(all_predictions)

joblib.dump(model, "result_predictor.pkl")
# Calculate accuracy across all years
print("Overall accuracy:", accuracy_score(all_predictions["Actual"], all_predictions["Predicted"]))
