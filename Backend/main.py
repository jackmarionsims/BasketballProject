from typing import Annotated, Optional
from enum import Enum
import numpy as np
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field, AfterValidator
from xgboost import XGBRegressor
import pandas as pd
import joblib
from teams import NBAName, PregameStats, ScheduledGame, BoxScore, CompletedGame, row_to_completed_game, add_scheduled_game, add_completed_game, Date, get_all_elos, FilterParams, get_home_filter, get_visitor_filter
app = FastAPI()

all_cols = ['Game ID', 'Home Team', 'Visitor Team', 'Home Team Points Avg', 'Visitor Team Points Avg', 'Home Team Opp Points Avg', 'Visitor Team Opp Points Avg', 'Home Team Assists Avg', 'Visitor Team Assists Avg', 'Home Team Tot Rebounds Avg', 'Visitor Team Tot Rebounds Avg', 'Home Team Off Rebounds Avg', 'Visitor Team Off Rebounds Avg', 'Home Team Def Rebounds Avg', 'Visitor Team Def Rebounds Avg', 'Home Team Blocks Avg', 'Visitor Team Blocks Avg', 'Home Team Steals Avg', 'Visitor Team Steals Avg', 'Home Team FGA Avg', 'Visitor Team FGA Avg', 'Home Team FGM Avg', 'Visitor Team FGM Avg', 'Home Team FG% Avg', 'Visitor Team FG% Avg', 'Home Team 3PA Avg', 'Visitor Team 3PA Avg', 'Home Team 3PM Avg', 'Visitor Team 3PM Avg', 'Home Team 3P% Avg', 'Visitor Team 3P% Avg', 'Home Team FTA Avg', 'Visitor Team FTA Avg', 'Home Team FTM Avg', 'Visitor Team FTM Avg', 'Home Team FT% Avg', 'Visitor Team FT% Avg', 'Home Team Fouls Avg', 'Visitor Team Fouls Avg', 'Home Team TO Avg', 'Visitor Team TO Avg', 'Home Team ORB% Avg', 'Visitor Team ORB% Avg', 'Home Team TO% Avg', 'Visitor Team TO% Avg', 'Home Team FTM/FGA Avg', 'Visitor Team FTM/FGA Avg', 'Home Team TS% Avg', 'Visitor Team TS% Avg', 'Home Team Opp Assists Avg', 'Visitor Team Opp Assists Avg', 'Home Team Opp Tot Rebounds Avg', 'Visitor Team Opp Tot Rebounds Avg', 'Home Team Opp Off Rebounds Avg', 'Visitor Team Opp Off Rebounds Avg', 'Home Team Opp Def Rebounds Avg', 'Visitor Team Opp Def Rebounds Avg', 'Home Team Opp Blocks Avg', 'Visitor Team Opp Blocks Avg', 'Home Team Opp Steals Avg', 'Visitor Team Opp Steals Avg', 'Home Team Opp FGA Avg', 'Visitor Team Opp FGA Avg', 'Home Team Opp FGM Avg', 'Visitor Team Opp FGM Avg', 'Home Team Opp FG% Avg', 'Visitor Team Opp FG% Avg', 'Home Team Opp 3PA Avg', 'Visitor Team Opp 3PA Avg', 'Home Team Opp 3PM Avg', 'Visitor Team Opp 3PM Avg', 'Home Team Opp 3P% Avg', 'Visitor Team Opp 3P% Avg', 'Home Team Opp FTA Avg', 'Visitor Team Opp FTA Avg', 'Home Team Opp FTM Avg', 'Visitor Team Opp FTM Avg', 'Home Team Opp FT% Avg', 'Visitor Team Opp FT% Avg', 'Home Team Opp Fouls Avg', 'Visitor Team Opp Fouls Avg', 'Home Team Opp TO Avg', 'Visitor Team Opp TO Avg', 'Home Team Opp ORB% Avg', 'Visitor Team Opp ORB% Avg', 'Home Team Opp TO% Avg', 'Visitor Team Opp TO% Avg', 'Home Team Opp FTM/FGA Avg', 'Visitor Team Opp FTM/FGA Avg', 'Home Team Opp TS% Avg', 'Visitor Team Opp TS% Avg', 'Home Team W', "Home Team L", "Visitor Team W", "Visitor Team L", "Home Team W/L%", "Visitor Team W/L%", "Playoff Game", "Home Team ELO", "Visitor Team ELO", 'Date Number', 'Year', 'Date', 'Visitor Team Points', 'Home Team Points', 'Winner', 'Loser', 'Home Win', 'Home Team Assists', 'Home Team Tot Rebounds', 'Home Team Off Rebounds', 'Home Team Def Rebounds',
'Home Team Blocks', 'Home Team Steals', 'Home Team FGA', 'Home Team FGM', 'Home Team FG%',
'Home Team 3PA', 'Home Team 3PM', 'Home Team 3P%', 'Home Team FTA', 'Home Team FTM', 'Home Team FT%',
'Home Team Fouls', 'Home Team TO', 'Visitor Team Assists', 'Visitor Team Tot Rebounds',
'Visitor Team Off Rebounds', 'Visitor Team Def Rebounds', 'Visitor Team Blocks', 'Visitor Team Steals',
'Visitor Team FGA', 'Visitor Team FGM', 'Visitor Team FG%', 'Visitor Team 3PA', 'Visitor Team 3PM',
'Visitor Team 3P%', 'Visitor Team FTA', 'Visitor Team FTM', 'Visitor Team FT%', 'Visitor Team Fouls',
'Visitor Team TO', 'Home Team ORB%', 'Visitor Team ORB%', 'Home Team TO%', 'Visitor Team TO%',
'Home Team FTM/FGA', 'Visitor Team FTM/FGA', 'Home Team TS%', 'Visitor Team TS%']
finished_games = pd.read_csv("../csvs/all_games3.csv")
finished_games = finished_games[all_cols].copy()
finished_games = finished_games.loc[:, ~finished_games.columns.str.contains("^Unnamed")]
upcoming_games = pd.DataFrame()
team_elos = get_all_elos(finished_games, {})

date = Date(year=2025, month="October",day_of_week='Fri', day_num=20, season=2025)
# finished_games.to_csv("test.csv")
game = ScheduledGame(home=NBAName.BOSTON_CELTICS, visitor=NBAName.LOS_ANGELES_LAKERS, date=date, playoff=True)
sample_data = {
    'Visitor Team': ['Los Angeles Lakers'],
    'Visitor Team Points': [102],
    'Home Team': ['Boston Celtics'],
    'Home Team Points': [110],
    'Winner': ['Boston Celtics'],
    "Loser": ['Los Angeles Lakers'],
    'Home Win': [1],
    'Home Team Assists': [25],
    'Home Team Tot Rebounds': [45],
    'Home Team Off Rebounds': [12],
    'Home Team Def Rebounds': [33],
    'Home Team Blocks': [5],
    'Home Team Steals': [7],
    'Home Team FGA': [89],
    'Home Team FGM': [44],
    'Home Team FG%': [49.4],
    'Home Team 3PA': [30],
    'Home Team 3PM': [10],
    'Home Team 3P%': [33.3],
    'Home Team FTA': [20],
    'Home Team FTM': [12],
    'Home Team FT%': [60.0],
    'Home Team Fouls': [18],
    'Home Team TO': [14],
    
    'Visitor Team Assists': [20],
    'Visitor Team Tot Rebounds': [40],
    'Visitor Team Off Rebounds': [10],
    'Visitor Team Def Rebounds': [30],
    'Visitor Team Blocks': [3],
    'Visitor Team Steals': [6],
    'Visitor Team FGA': [85],
    'Visitor Team FGM': [39],
    'Visitor Team FG%': [45.9],
    'Visitor Team 3PA': [28],
    'Visitor Team 3PM': [8],
    'Visitor Team 3P%': [28.6],
    'Visitor Team FTA': [22],
    'Visitor Team FTM': [16],
    'Visitor Team FT%': [72.7],
    'Visitor Team Fouls': [16],
    'Visitor Team TO': [15],
    
    'Home Team ORB%': [55.0],
    'Visitor Team ORB%': [45.0],
    'Home Team TO%': [13.2],
    'Visitor Team TO%': [14.7],
    'Home Team FTM/FGA': [0.135],
    'Visitor Team FTM/FGA': [0.188],
    'Home Team TS%': [55.0],
    'Visitor Team TS%': [52.3],
    
    'Date Number': [739544]
}

sample_df = pd.DataFrame(sample_data)

# Instantiate the BoxScore object
sample_box_score = BoxScore(box_score=sample_df.iloc[0].to_dict())
finished_games = add_scheduled_game(finished_games, game, team_elos)
finished_games.to_csv("test_upcoming.csv")
finished_games = add_completed_game(finished_games, sample_box_score)
finished_games.to_csv("test_finished.csv")
# all_teams = df_to_teams(finished_games)

log_model = joblib.load("../logreg_model.pkl")
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


@app.get("/game/{game_id}", response_model=CompletedGame)
async def find_game(game_id: Annotated[int, Path(title="The ID of the game to get", ge=0)]):
    row = finished_games[finished_games["Game ID"] == game_id]
    if not row.empty:
        return row_to_completed_game(row)
    else:
        raise HTTPException(status_code=404, detail="No game found")

@app.put("/game/{game_id}")
async def change_game(game_id: Annotated[int, Path(title="The ID of the game to change", ge=0)], replacement: CompletedGame):
    idx = finished_games.index[finished_games["Game ID"] == game_id]
    if not idx.empty:
        new_row = replacement.to_row()
        finished_games.loc[idx[0]] = new_row
        # return {"message": f"Game {game_id} updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="No game found")
    
@app.delete("/game/{game_id}")
async def delete_game(game_id: Annotated[int, Path(title="The ID of the game to delete", ge=0)]):
    global finished_games

    if game_id not in finished_games["Game ID"].values:
        raise HTTPException(status_code=404, detail="No game found")
    finished_games = finished_games[finished_games["Game ID"] != game_id].reset_index(drop=True)

    return {"message": f"Game {game_id} deleted successfully"}
    
@app.post("/upcoming_game")
async def add_upcoming_game(game: ScheduledGame):
    global upcoming_games
    upcoming_games = add_scheduled_game(upcoming_games, game, team_elos)
    # upcoming_games = pd.concat([upcoming_games, row])
    return {"message": f"Game added successfully"}

@app.post("/finished_game")
async def add_finished_game(box_score: BoxScore):
    global finished_games
    finished_games = add_completed_game(finished_games, box_score)
    return {"message": f"Game added successfully"}

# @app.post("/prediction")
# async def predict_game(game: ScheduledGame):
#     row = game.to_row()
#     X = row.to_frame().T
#     prob = log_model.predict_proba(X)[0][1]
#     prediction = 1 if prob >= 0.5 else 0
#     home_pred = xgb_home.predict(X)
#     visitor_pred = xgb_visitor.predict(X)
#     home_rounded = np.round(home_pred).astype(int)[0]
#     visitor_rounded = np.round(visitor_pred).astype(int)[0]
#     if home_rounded == visitor_rounded:
#         if (home_pred[0] >= visitor_pred[0]):
#             home_rounded += 1
#         else:
#             visitor_rounded += 1

#     return {
#         "home_win_probability": round(prob, 4),
#         "predicted_winner": "Home" if prediction == 1 else "Visitor",
#         "predicted_home_score": int(home_rounded),
#         "predicted_visitor_score": int(visitor_rounded)
#     }

@app.get("/filter", response_model=list[CompletedGame])
async def filtered_games(home_filter: FilterParams = Depends(get_home_filter), visitor_filter: FilterParams = Depends(get_visitor_filter)):
    df = finished_games.copy()

    filters = {
        # Points
        "Home Team Points": (home_filter.pts_min, home_filter.pts_max),
        "Visitor Team Points": (visitor_filter.pts_min, visitor_filter.pts_max),

        # Assists
        "Home Team Assists": (home_filter.ast_min, home_filter.ast_max),
        "Visitor Team Assists": (visitor_filter.ast_min, visitor_filter.ast_max),

        # Total Rebounds
        "Home Team Tot Rebounds": (home_filter.trb_min, home_filter.trb_max),
        "Visitor Team Tot Rebounds": (visitor_filter.trb_min, visitor_filter.trb_max),

        # Offensive Rebounds
        "Home Team Off Rebounds": (home_filter.orb_min, home_filter.orb_max),
        "Visitor Team Off Rebounds": (visitor_filter.orb_min, visitor_filter.orb_max),

        # Defensive Rebounds
        "Home Team Def Rebounds": (home_filter.drb_min, home_filter.drb_max),
        "Visitor Team Def Rebounds": (visitor_filter.drb_min, visitor_filter.drb_max),

        # Blocks
        "Home Team Blocks": (home_filter.blk_min, home_filter.blk_max),
        "Visitor Team Blocks": (visitor_filter.blk_min, visitor_filter.blk_max),

        # Steals
        "Home Team Steals": (home_filter.stl_min, home_filter.stl_max),
        "Visitor Team Steals": (visitor_filter.stl_min, visitor_filter.stl_max),

        # Field Goals Attempted
        "Home Team FGA": (home_filter.fga_min, home_filter.fga_max),
        "Visitor Team FGA": (visitor_filter.fga_min, visitor_filter.fga_max),

        # Field Goals Made
        "Home Team FGM": (home_filter.fgm_min, home_filter.fgm_max),
        "Visitor Team FGM": (visitor_filter.fgm_min, visitor_filter.fgm_max),

        # Field Goal %
        "Home Team FG%": (home_filter.fg_pct_min, home_filter.fg_pct_max),
        "Visitor Team FG%": (visitor_filter.fg_pct_min, visitor_filter.fg_pct_max),

        # Three Pointers Attempted
        "Home Team 3PA": (home_filter.tpa_min, home_filter.tpa_max),
        "Visitor Team 3PA": (visitor_filter.tpa_min, visitor_filter.tpa_max),

        # Three Pointers Made
        "Home Team 3PM": (home_filter.tpm_min, home_filter.tpm_max),
        "Visitor Team 3PM": (visitor_filter.tpm_min, visitor_filter.tpm_max),

        # Three Point %
        "Home Team 3P%": (home_filter.tp_pct_min, home_filter.tp_pct_max),
        "Visitor Team 3P%": (visitor_filter.tp_pct_min, visitor_filter.tp_pct_max),

        # Free Throws Attempted
        "Home Team FTA": (home_filter.fta_min, home_filter.fta_max),
        "Visitor Team FTA": (visitor_filter.fta_min, visitor_filter.fta_max),

        # Free Throws Made
        "Home Team FTM": (home_filter.ftm_min, home_filter.ftm_max),
        "Visitor Team FTM": (visitor_filter.ftm_min, visitor_filter.ftm_max),

        # Free Throw %
        "Home Team FT%": (home_filter.ft_pct_min, home_filter.ft_pct_max),
        "Visitor Team FT%": (visitor_filter.ft_pct_min, visitor_filter.ft_pct_max),

        # Fouls
        "Home Team Fouls": (home_filter.fouls_min, home_filter.fouls_max),
        "Visitor Team Fouls": (visitor_filter.fouls_min, visitor_filter.fouls_max),

        # Turnovers
        "Home Team TO": (home_filter.to_min, home_filter.to_max),
        "Visitor Team TO": (visitor_filter.to_min, visitor_filter.to_max),
    }


    for column, (min_val, max_val) in filters.items():
        if min_val is not None:
            df = df[df[column] >= min_val]
        if max_val is not None:
            df = df[df[column] <= max_val]
    games = []
    for idx, row in df.iterrows():
        games.append(row_to_completed_game(row.to_frame().T))
    return games

