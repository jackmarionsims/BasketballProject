from typing import Annotated, Optional
from enum import Enum
import numpy as np
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, AfterValidator
from xgboost import XGBRegressor
import pandas as pd
import joblib
from teams import NBAName, PregameStats, ScheduledGame, BoxScore, CompletedGame, row_to_completed_game, add_scheduled_game, add_completed_game, Date, get_all_elos, FilterParams, get_filter1, get_filter2

app = FastAPI()

# List of frontend origins that are allowed to access the API
origins = [
    "http://localhost:3000",  # React dev server
    # "http://localhost:8000",
    "https://your-production-frontend.com"  # production site
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Allow only specific origins (or ["*"] for all)
    allow_credentials=True,
    allow_methods=["*"],           # Allow all HTTP methods: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],           # Allow all headers
)


all_cols = [
    'Game ID', 'Date Number', 'Date', 'Game Type', 
    'Home Team', 'Visitor Team', 'Winner', 'Loser', 
    'Home Win', 'Home Team PTS', 'Home Team AST', 
    'Home Team TRB', 'Home Team ORB', 'Home Team DRB', 
    'Home Team BLK', 'Home Team STL', 'Home Team FGA', 
    'Home Team FG', 'Home Team FG%', 'Home Team 3PA', 
    'Home Team 3P', 'Home Team 3P%', 'Home Team FTA', 
    'Home Team FT', 'Home Team FT%', 'Home Team PF', 
    'Home Team TOV', 'Visitor Team PTS', 'Visitor Team AST', 
    'Visitor Team TRB', 'Visitor Team ORB', 'Visitor Team DRB', 
    'Visitor Team BLK', 'Visitor Team STL', 'Visitor Team FGA', 
    'Visitor Team FG', 'Visitor Team FG%', 'Visitor Team 3PA', 
    'Visitor Team 3P', 'Visitor Team 3P%', 'Visitor Team FTA', 
    'Visitor Team FT', 'Visitor Team FT%', 'Visitor Team PF', 
    'Visitor Team TOV', 'Playoff Game', 'Season', 
    'Home Team PTS Avg', 'Visitor Team PTS Avg', 
    'Home Team Opp PTS Avg', 'Visitor Team Opp PTS Avg', 
    'Home Team AST Avg', 'Visitor Team AST Avg', 
    'Home Team Opp AST Avg', 'Visitor Team Opp AST Avg', 
    'Home Team TRB Avg', 'Visitor Team TRB Avg', 
    'Home Team Opp TRB Avg', 'Visitor Team Opp TRB Avg', 
    'Home Team ORB Avg', 'Visitor Team ORB Avg', 
    'Home Team Opp ORB Avg', 'Visitor Team Opp ORB Avg', 
    'Home Team DRB Avg', 'Visitor Team DRB Avg', 
    'Home Team Opp DRB Avg', 'Visitor Team Opp DRB Avg', 
    'Home Team BLK Avg', 'Visitor Team BLK Avg', 
    'Home Team Opp BLK Avg', 'Visitor Team Opp BLK Avg', 
    'Home Team STL Avg', 'Visitor Team STL Avg', 
    'Home Team Opp STL Avg', 'Visitor Team Opp STL Avg', 
    'Home Team FGA Avg', 'Visitor Team FGA Avg', 
    'Home Team Opp FGA Avg', 'Visitor Team Opp FGA Avg', 
    'Home Team FG Avg', 'Visitor Team FG Avg', 
    'Home Team Opp FG Avg', 'Visitor Team Opp FG Avg', 
    'Home Team FG% Avg', 'Visitor Team FG% Avg', 
    'Home Team Opp FG% Avg', 'Visitor Team Opp FG% Avg', 
    'Home Team 3PA Avg', 'Visitor Team 3PA Avg', 
    'Home Team Opp 3PA Avg', 'Visitor Team Opp 3PA Avg', 
    'Home Team 3P Avg', 'Visitor Team 3P Avg', 
    'Home Team Opp 3P Avg', 'Visitor Team Opp 3P Avg', 
    'Home Team 3P% Avg', 'Visitor Team 3P% Avg', 
    'Home Team Opp 3P% Avg', 'Visitor Team Opp 3P% Avg', 
    'Home Team FTA Avg', 'Visitor Team FTA Avg', 
    'Home Team Opp FTA Avg', 'Visitor Team Opp FTA Avg', 
    'Home Team FT Avg', 'Visitor Team FT Avg', 
    'Home Team Opp FT Avg', 'Visitor Team Opp FT Avg', 
    'Home Team FT% Avg', 'Visitor Team FT% Avg', 
    'Home Team Opp FT% Avg', 'Visitor Team Opp FT% Avg', 
    'Home Team PF Avg', 'Visitor Team PF Avg', 
    'Home Team Opp PF Avg', 'Visitor Team Opp PF Avg', 
    'Home Team TOV Avg', 'Visitor Team TOV Avg', 
    'Home Team Opp TOV Avg', 'Visitor Team Opp TOV Avg', 
    'Home Team ELO', 'Visitor Team ELO', 
    'Home Team Total Games', 'Home Team W', 'Home Team L', 
    'Home Team W/L%', 'Visitor Team Total Games', 
    'Visitor Team W', 'Visitor Team L', 'Visitor Team W/L%', 
    'Home Team Tot Season EFF Avg', 'Home Team Tot Career EFF Avg', 
    'Visitor Team Tot Season EFF Avg', 'Visitor Team Tot Career EFF Avg'
]

# next = ['Home Team ORB%', 'Visitor Team ORB%', 'Home Team TO%', 'Visitor Team TO%',
# 'Home Team FTM/FGA', 'Visitor Team FTM/FGA', 'Home Team TS%', 'Visitor Team TS%', 'Home Team ORB% Avg', 'Visitor Team ORB% Avg', 
# 'Home Team TO% Avg', 'Visitor Team TO% Avg', 'Home Team FTM/FGA Avg', 'Visitor Team FTM/FGA Avg', 
# 'Home Team TS% Avg', 'Visitor Team TS% Avg', 'Home Team Opp ORB% Avg', 'Visitor Team Opp ORB% Avg', 
# 'Home Team Opp TO% Avg', 'Visitor Team Opp TO% Avg', 'Home Team Opp FTM/FGA Avg', 'Visitor Team Opp FTM/FGA Avg', 
# 'Home Team Opp TS% Avg', 'Visitor Team Opp TS% Avg', 'Home Team W', "Home Team L", "Visitor Team W", "Visitor Team L",
#  "Home Team ELO", "Visitor Team ELO", "Home Team W/L%", "Visitor Team W/L%"]
FINISHED_GAMES = pd.read_csv("../csvs/modern.csv")
model_cats = pd.read_csv("../csvs/model_categories.csv")
FINISHED_GAMES = FINISHED_GAMES[all_cols].copy()
FINISHED_GAMES = FINISHED_GAMES.loc[:, ~FINISHED_GAMES.columns.str.contains("^Unnamed")]
#FINISHED_GAMES = FINISHED_GAMES.set_index("Game ID")
upcoming_games = pd.DataFrame()
team_elos = get_all_elos(FINISHED_GAMES, {})

# date = Date(year=2025, month="October",day_of_week='Fri', day_num=20, season=2025)
# # finished_games.to_csv("test.csv")
# game = ScheduledGame(home=NBAName.BOSTON_CELTICS, visitor=NBAName.LOS_ANGELES_LAKERS, date=date, playoff=True)
# sample_data = {
#     'Visitor Team': ['Los Angeles Lakers'],
#     'Visitor Team Points': [102],
#     'Home Team': ['Boston Celtics'],
#     'Home Team Points': [110],
#     'Winner': ['Boston Celtics'],
#     "Loser": ['Los Angeles Lakers'],
#     'Home Win': [1],
#     'Home Team Assists': [25],
#     'Home Team Tot Rebounds': [45],
#     'Home Team Off Rebounds': [12],
#     'Home Team Def Rebounds': [33],
#     'Home Team Blocks': [5],
#     'Home Team Steals': [7],
#     'Home Team FGA': [89],
#     'Home Team FGM': [44],
#     'Home Team FG%': [49.4],
#     'Home Team 3PA': [30],
#     'Home Team 3PM': [10],
#     'Home Team 3P%': [33.3],
#     'Home Team FTA': [20],
#     'Home Team FTM': [12],
#     'Home Team FT%': [60.0],
#     'Home Team Fouls': [18],
#     'Home Team TO': [14],
    
#     'Visitor Team Assists': [20],
#     'Visitor Team Tot Rebounds': [40],
#     'Visitor Team Off Rebounds': [10],
#     'Visitor Team Def Rebounds': [30],
#     'Visitor Team Blocks': [3],
#     'Visitor Team Steals': [6],
#     'Visitor Team FGA': [85],
#     'Visitor Team FGM': [39],
#     'Visitor Team FG%': [45.9],
#     'Visitor Team 3PA': [28],
#     'Visitor Team 3PM': [8],
#     'Visitor Team 3P%': [28.6],
#     'Visitor Team FTA': [22],
#     'Visitor Team FTM': [16],
#     'Visitor Team FT%': [72.7],
#     'Visitor Team Fouls': [16],
#     'Visitor Team TO': [15],
    
#     'Home Team ORB%': [55.0],
#     'Visitor Team ORB%': [45.0],
#     'Home Team TO%': [13.2],
#     'Visitor Team TO%': [14.7],
#     'Home Team FTM/FGA': [0.135],
#     'Visitor Team FTM/FGA': [0.188],
#     'Home Team TS%': [55.0],
#     'Visitor Team TS%': [52.3],
    
#     'Date Number': [739544]
# }

# sample_df = pd.DataFrame(sample_data)

# # Instantiate the BoxScore object
# sample_box_score = BoxScore(box_score=sample_df.iloc[0].to_dict())
# finished_games = add_scheduled_game(finished_games, game, team_elos)
# finished_games.to_csv("../csvs/test_upcoming.csv")
# finished_games = add_completed_game(finished_games, sample_box_score)
# finished_games.to_csv("../csvs/test_finished.csv")
# # all_teams = df_to_teams(finished_games)

log_model = joblib.load("../result_predictor.pkl")
xgb_home = XGBRegressor()
xgb_home.load_model("../home_model_scores.json")
xgb_visitor = XGBRegressor()
xgb_visitor.load_model("../visitor_model_scores.json")

# @app.get("/items/")
# async def read_items(
#     q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

@app.get("/game/{game_id}", response_model=CompletedGame)
async def find_game(game_id: Annotated[int, Path(title="The ID of the game to get", ge=0)]):
    # if game_id not in finished_games.index:
    #     raise HTTPException(status_code=404, detail="No game found")
    # return finished_games.loc[game_id].to_dict()
    row = FINISHED_GAMES[FINISHED_GAMES["Game ID"] == game_id]
    if not row.empty:
        #change to just returning the row
        return row_to_completed_game(row)
    else:
        raise HTTPException(status_code=404, detail="No game found")

@app.put("/game/{game_id}")
async def change_game(game_id: Annotated[int, Path(title="The ID of the game to change", ge=0)], replacement: CompletedGame):
    idx = FINISHED_GAMES.index[FINISHED_GAMES["Game ID"] == game_id]
    if not idx.empty:
        new_row = replacement.to_row()
        FINISHED_GAMES.loc[idx[0]] = new_row
        # return {"message": f"Game {game_id} updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="No game found")
    
@app.delete("/game/{game_id}")
async def delete_game(game_id: Annotated[int, Path(title="The ID of the game to delete", ge=0)]):
    global FINISHED_GAMES

    if game_id not in FINISHED_GAMES["Game ID"].values:
        raise HTTPException(status_code=404, detail="No game found")
    FINISHED_GAMES = FINISHED_GAMES[FINISHED_GAMES["Game ID"] != game_id].reset_index(drop=True)

    return {"message": f"Game {game_id} deleted successfully"}
    
@app.post("/upcoming_game")
async def add_upcoming_game(game: ScheduledGame):
    global upcoming_games
    upcoming_games = add_scheduled_game(upcoming_games, game, team_elos)
    # upcoming_games = pd.concat([upcoming_games, row])
    return {"message": f"Game added successfully"}

@app.post("/finished_game")
async def add_finished_game(box_score: BoxScore):
    global FINISHED_GAMES
    FINISHED_GAMES = add_completed_game(FINISHED_GAMES, box_score)
    return {"message": f"Game added successfully"}

@app.get("/prediction/{game_id}")
async def predict_game(game_id: Annotated[int, Path(title="The ID of the game to predict", ge=0)]):
    predictors = ["PTS Margin", "W/L% Margin", "ELO Margin", "Tot Season EFF Avg Margin",
                  "Home Team PTS Avg", "Visitor Team PTS Avg"]
    row = model_cats.loc[model_cats["Game ID"] == game_id].iloc[0]
    row["PTS Margin"] = (
        float(row["Home Team PTS Margin Avg"]) - float(row["Visitor Team PTS Margin Avg"])
    )
    X = row[predictors].to_frame().T
    X = X.apply(pd.to_numeric, errors="coerce")
    prob = log_model.predict_proba(X)[0][1]
    prediction = 1 if prob >= 0.5 else 0
    home_pred = xgb_home.predict(X)
    visitor_pred = xgb_visitor.predict(X)
    home_rounded = np.round(home_pred).astype(int)[0]
    visitor_rounded = np.round(visitor_pred).astype(int)[0]
    if home_rounded == visitor_rounded:
        if (home_pred[0] >= visitor_pred[0]):
            home_rounded += 1
        else:
            visitor_rounded += 1

    return {
        "home_win_probability": round(prob, 4),
        "predicted_winner": "Home" if prediction == 1 else "Visitor",
        "predicted_home_score": int(home_rounded),
        "predicted_visitor_score": int(visitor_rounded)
    }

@app.get("/filter")
async def filtered_games(filter1: FilterParams = Depends(get_filter1), filter2: FilterParams = Depends(get_filter2)):
    df1 = FINISHED_GAMES.copy()
    df2 = FINISHED_GAMES.copy()

    filters = {
        # Points
        "Team1 Team PTS": (filter1.pts_min, filter1.pts_max),
        "Team2 Team PTS": (filter2.pts_min, filter2.pts_max),

        # Assists
        "Team1 Team AST": (filter1.ast_min, filter1.ast_max),
        "Team2 Team AST": (filter2.ast_min, filter2.ast_max),

        # Total Rebounds
        "Team1 Team TRB": (filter1.trb_min, filter1.trb_max),
        "Team2 Team TRB": (filter2.trb_min, filter2.trb_max),

        # Offensive Rebounds
        "Team1 Team ORB": (filter1.orb_min, filter1.orb_max),
        "Team2 Team ORB": (filter2.orb_min, filter2.orb_max),

        # Defensive Rebounds
        "Team1 Team DRB": (filter1.drb_min, filter1.drb_max),
        "Team2 Team DRB": (filter2.drb_min, filter2.drb_max),

        # Blocks
        "Team1 Team BLK": (filter1.blk_min, filter1.blk_max),
        "Team2 Team BLK": (filter2.blk_min, filter2.blk_max),

        # Steals
        "Team1 Team STL": (filter1.stl_min, filter1.stl_max),
        "Team2 Team STL": (filter2.stl_min, filter2.stl_max),

        # Field Goals Attempted
        "Team1 Team FGA": (filter1.fga_min, filter1.fga_max),
        "Team2 Team FGA": (filter2.fga_min, filter2.fga_max),

        # Field Goals Made
        "Team1 Team FG": (filter1.fgm_min, filter1.fgm_max),
        "Team2 Team FG": (filter2.fgm_min, filter2.fgm_max),

        # Field Goal %
        "Team1 Team FG%": (filter1.fg_pct_min, filter1.fg_pct_max),
        "Team2 Team FG%": (filter2.fg_pct_min, filter2.fg_pct_max),

        # Three Pointers Attempted
        "Team1 Team 3PA": (filter1.tpa_min, filter1.tpa_max),
        "Team2 Team 3PA": (filter2.tpa_min, filter2.tpa_max),

        # Three Pointers Made
        "Team1 Team 3P": (filter1.tpm_min, filter1.tpm_max),
        "Team2 Team 3P": (filter2.tpm_min, filter2.tpm_max),

        # Three Point %
        "Team1 Team 3P%": (filter1.tp_pct_min, filter1.tp_pct_max),
        "Team2 Team 3P%": (filter2.tp_pct_min, filter2.tp_pct_max),

        # Free Throws Attempted
        "Team1 Team FTA": (filter1.fta_min, filter1.fta_max),
        "Team2 Team FTA": (filter2.fta_min, filter2.fta_max),

        # Free Throws Made
        "Team1 Team FT": (filter1.ftm_min, filter1.ftm_max),
        "Team2 Team FT": (filter2.ftm_min, filter2.ftm_max),

        # Free Throw %
        "Team1 Team FT%": (filter1.ft_pct_min, filter1.ft_pct_max),
        "Team2 Team FT%": (filter2.ft_pct_min, filter2.ft_pct_max),

        # Fouls
        "Team1 Team PF": (filter1.fouls_min, filter1.fouls_max),
        "Team2 Team PF": (filter2.fouls_min, filter2.fouls_max),

        # Turnovers
        "Team1 Team TOV": (filter1.tov_min, filter1.tov_max),
        "Team2 Team TOV": (filter2.tov_min, filter2.tov_max),
    }

    for column, (min_val, max_val) in filters.items():
        if "Team1" in column:
            home_col = column.replace("Team1", "Home")
            if min_val is not None:
                df1 = df1[df1[home_col] >= min_val]
            if max_val is not None:
                df1 = df1[df1[home_col] <= max_val]
        else:
            visitor_col = column.replace("Team2", "Visitor")
            if min_val is not None:
                df1 = df1[df1[visitor_col] >= min_val]
            if max_val is not None:
                df1 = df1[df1[visitor_col] <= max_val]
    
    for column, (min_val, max_val) in filters.items():
        if "Team1" in column:
            visitor_col = column.replace("Team1", "Visitor")
            if min_val is not None:
                df2 = df2[df2[visitor_col] >= min_val]
            if max_val is not None:
                df2 = df2[df2[visitor_col] <= max_val]
        else:
            home_col = column.replace("Team2", "Home")
            if min_val is not None:
                df2 = df2[df2[home_col] >= min_val]
            if max_val is not None:
                df2 = df2[df2[home_col] <= max_val]
    
    df = pd.concat([df1, df2]).drop_duplicates()
    df = df.sort_values(by=["Date Number"], ascending=False)
    return df.to_dict(orient="records")

@app.get("/filter-home-visitor")
async def filtered_by_home(home_filter: FilterParams = Depends(get_filter1), visitor_filter: FilterParams = Depends(get_filter2)):
    df = FINISHED_GAMES.copy()

    filters = {
        # PTS
        "Home Team PTS": (home_filter.pts_min, home_filter.pts_max),
        "Visitor Team PTS": (visitor_filter.pts_min, visitor_filter.pts_max),

        # Assists
        "Home Team AST": (home_filter.ast_min, home_filter.ast_max),
        "Visitor Team AST": (visitor_filter.ast_min, visitor_filter.ast_max),

        # Total Rebounds
        "Home Team TRB": (home_filter.trb_min, home_filter.trb_max),
        "Visitor Team TRB": (visitor_filter.trb_min, visitor_filter.trb_max),

        # Offensive Rebounds
        "Home Team ORB": (home_filter.orb_min, home_filter.orb_max),
        "Visitor Team ORB": (visitor_filter.orb_min, visitor_filter.orb_max),

        # Defensive Rebounds
        "Home Team DRB": (home_filter.drb_min, home_filter.drb_max),
        "Visitor Team DRB": (visitor_filter.drb_min, visitor_filter.drb_max),

        # Blocks
        "Home Team BLK": (home_filter.blk_min, home_filter.blk_max),
        "Visitor Team BLK": (visitor_filter.blk_min, visitor_filter.blk_max),

        # Steals
        "Home Team STL": (home_filter.stl_min, home_filter.stl_max),
        "Visitor Team STL": (visitor_filter.stl_min, visitor_filter.stl_max),

        # Field Goals Attempted
        "Home Team FGA": (home_filter.fga_min, home_filter.fga_max),
        "Visitor Team FGA": (visitor_filter.fga_min, visitor_filter.fga_max),

        # Field Goals Made
        "Home Team FG": (home_filter.fgm_min, home_filter.fgm_max),
        "Visitor Team FG": (visitor_filter.fgm_min, visitor_filter.fgm_max),

        # Field Goal %
        "Home Team FG%": (home_filter.fg_pct_min, home_filter.fg_pct_max),
        "Visitor Team FG%": (visitor_filter.fg_pct_min, visitor_filter.fg_pct_max),

        # Three Pointers Attempted
        "Home Team 3PA": (home_filter.tpa_min, home_filter.tpa_max),
        "Visitor Team 3PA": (visitor_filter.tpa_min, visitor_filter.tpa_max),

        # Three Pointers Made
        "Home Team 3P": (home_filter.tpm_min, home_filter.tpm_max),
        "Visitor Team 3P": (visitor_filter.tpm_min, visitor_filter.tpm_max),

        # Three Point %
        "Home Team 3P%": (home_filter.tp_pct_min, home_filter.tp_pct_max),
        "Visitor Team 3P%": (visitor_filter.tp_pct_min, visitor_filter.tp_pct_max),

        # Free Throws Attempted
        "Home Team FTA": (home_filter.fta_min, home_filter.fta_max),
        "Visitor Team FTA": (visitor_filter.fta_min, visitor_filter.fta_max),

        # Free Throws Made
        "Home Team FT": (home_filter.ftm_min, home_filter.ftm_max),
        "Visitor Team FT": (visitor_filter.ftm_min, visitor_filter.ftm_max),

        # Free Throw %
        "Home Team FT%": (home_filter.ft_pct_min, home_filter.ft_pct_max),
        "Visitor Team FT%": (visitor_filter.ft_pct_min, visitor_filter.ft_pct_max),

        # Fouls
        "Home Team PF": (home_filter.fouls_min, home_filter.fouls_max),
        "Visitor Team PF": (visitor_filter.fouls_min, visitor_filter.fouls_max),

        # Turnovers
        "Home Team TOV": (home_filter.tov_min, home_filter.tov_max),
        "Visitor Team TOV": (visitor_filter.tov_min, visitor_filter.tov_max),
    }


    for column, (min_val, max_val) in filters.items():
        if min_val is not None:
            df = df[df[column] >= min_val]
        if max_val is not None:
            df = df[df[column] <= max_val]
    df = df.sort_values(by=["Date Number"], ascending=False)
    return df.to_dict(orient="records")

@app.get("/filter-winner-loser")
async def filtered_by_winner(winner_filter: FilterParams = Depends(get_filter1), loser_filter: FilterParams = Depends(get_filter2)):
    df1 = FINISHED_GAMES.copy()
    df2 = FINISHED_GAMES.copy()
    filters = {
        # PTS
        "Winning Team PTS": (winner_filter.pts_min, winner_filter.pts_max),
        "Losing Team PTS": (loser_filter.pts_min, loser_filter.pts_max),

        # Assists
        "Winning Team AST": (winner_filter.ast_min, winner_filter.ast_max),
        "Losing Team AST": (loser_filter.ast_min, loser_filter.ast_max),

        # Total Rebounds
        "Winning Team TRB": (winner_filter.trb_min, winner_filter.trb_max),
        "Losing Team TRB": (loser_filter.trb_min, loser_filter.trb_max),

        # Offensive Rebounds
        "Winning Team ORB": (winner_filter.orb_min, winner_filter.orb_max),
        "Losing Team ORB": (loser_filter.orb_min, loser_filter.orb_max),

        # Defensive Rebounds
        "Winning Team DRB": (winner_filter.drb_min, winner_filter.drb_max),
        "Losing Team DRB": (loser_filter.drb_min, loser_filter.drb_max),

        # Blocks
        "Winning Team BLK": (winner_filter.blk_min, winner_filter.blk_max),
        "Losing Team BLK": (loser_filter.blk_min, loser_filter.blk_max),

        # Steals
        "Winning Team STL": (winner_filter.stl_min, winner_filter.stl_max),
        "Losing Team STL": (loser_filter.stl_min, loser_filter.stl_max),

        # Field Goals Attempted
        "Winning Team FGA": (winner_filter.fga_min, winner_filter.fga_max),
        "Losing Team FGA": (loser_filter.fga_min, loser_filter.fga_max),

        # Field Goals Made
        "Winning Team FG": (winner_filter.fgm_min, winner_filter.fgm_max),
        "Losing Team FG": (loser_filter.fgm_min, loser_filter.fgm_max),

        # Field Goal %
        "Winning Team FG%": (winner_filter.fg_pct_min, winner_filter.fg_pct_max),
        "Losing Team FG%": (loser_filter.fg_pct_min, loser_filter.fg_pct_max),

        # Three Pointers Attempted
        "Winning Team 3PA": (winner_filter.tpa_min, winner_filter.tpa_max),
        "Losing Team 3PA": (loser_filter.tpa_min, loser_filter.tpa_max),

        # Three Pointers Made
        "Winning Team 3P": (winner_filter.tpm_min, winner_filter.tpm_max),
        "Losing Team 3P": (loser_filter.tpm_min, loser_filter.tpm_max),

        # Three Point %
        "Winning Team 3P%": (winner_filter.tp_pct_min, winner_filter.tp_pct_max),
        "Losing Team 3P%": (loser_filter.tp_pct_min, loser_filter.tp_pct_max),

        # Free Throws Attempted
        "Winning Team FTA": (winner_filter.fta_min, winner_filter.fta_max),
        "Losing Team FTA": (loser_filter.fta_min, loser_filter.fta_max),

        # Free Throws Made
        "Winning Team FT": (winner_filter.ftm_min, winner_filter.ftm_max),
        "Losing Team FT": (loser_filter.ftm_min, loser_filter.ftm_max),

        # Free Throw %
        "Winning Team FT%": (winner_filter.ft_pct_min, winner_filter.ft_pct_max),
        "Losing Team FT%": (loser_filter.ft_pct_min, loser_filter.ft_pct_max),

        # Fouls
        "Winning Team PF": (winner_filter.fouls_min, winner_filter.fouls_max),
        "Losing Team PF": (loser_filter.fouls_min, loser_filter.fouls_max),

        # Turnovers
        "Winning Team TOV": (winner_filter.tov_min, winner_filter.tov_max),
        "Losing Team TOV": (loser_filter.tov_min, loser_filter.tov_max),
    }

    for column, (min_val, max_val) in filters.items():
        if "Winning" in column:
            home_col = column.replace("Winning", "Home")
            if min_val is not None:
                df1 = df1[(df1[home_col] >= min_val) & (df1["Home Win"] == 1)]
            if max_val is not None:
                df1 = df1[(df1[home_col] <= max_val) & (df1["Home Win"] == 1)]
        else:
            visitor_col = column.replace("Losing", "Visitor")
            if min_val is not None:
                df1 = df1[(df1[visitor_col] >= min_val) & (df1["Home Win"] == 1)]
            if max_val is not None:
                df1 = df1[(df1[visitor_col] <= max_val) & (df1["Home Win"] == 1)]
    
    for column, (min_val, max_val) in filters.items():
        if "Winning" in column:
            visitor_col = column.replace("Winning", "Visitor")
            if min_val is not None:
                df2 = df2[(df2[visitor_col] >= min_val) & (df2["Home Win"] == 0)]
            if max_val is not None:
                df2 = df2[(df2[visitor_col] <= max_val) & (df2["Home Win"] == 0)]
        else:
            home_col = column.replace("Losing", "Home")
            if min_val is not None:
                df2 = df2[(df2[home_col] >= min_val) & (df2["Home Win"] == 0)]
            if max_val is not None:
                df2 = df2[(df2[home_col] <= max_val) & (df2["Home Win"] == 0)]
    
    df = pd.concat([df1, df2]).drop_duplicates()
    df = df.sort_values(by=["Date Number"], ascending=False)
    return df.to_dict(orient="records")

@app.get("/{team_name}")
async def get_team(
    team_name: Annotated[str, Path(title="The name of the team to get")],
    season: Annotated[int, Query(title="The season to access")] = 2025
):
    global FINISHED_GAMES
    season_games = FINISHED_GAMES[FINISHED_GAMES["Season"] == season]
    team_games = season_games[
        (season_games["Home Team"] == team_name) |
        (season_games["Visitor Team"] == team_name)
    ]
    if not team_games.empty:
        return team_games.to_dict(orient="records")
    else:
        raise HTTPException(status_code=404, detail="Invalid team or year")

