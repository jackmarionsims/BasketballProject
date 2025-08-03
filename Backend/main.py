from typing import Annotated, Optional
from enum import Enum
import numpy as np
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field, AfterValidator
from xgboost import XGBRegressor
import pandas as pd
import joblib
from classes import NBATeam, NBAName, NewTeam, SeasonStats, GameStats, FilterParams, BoxScore, GameBase, FinishedGame, row_to_box_score, row_to_game, row_to_finished_game, get_home_filter, get_visitor_filter, df_to_teams
app = FastAPI()

finished_games = pd.read_csv("../csvs/all_games3.csv")
upcoming_games = pd.DataFrame()
all_teams = df_to_teams(finished_games)

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


@app.get("/game/{game_id}", response_model=FinishedGame)
async def find_game(game_id: Annotated[int, Path(title="The ID of the game to get", ge=0)]):
    row = finished_games[finished_games["Game ID"] == game_id]
    if not row.empty:
        return row_to_finished_game(row.iloc[0])
    else:
        raise HTTPException(status_code=404, detail="No game found")

@app.put("/game/{game_id}")
async def change_game(game_id: Annotated[int, Path(title="The ID of the game to change", ge=0)], replacement: FinishedGame):
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
async def add_upcoming_game(game: GameBase):
    global upcoming_games
    row = game.to_row()
    upcoming_games = pd.concat([upcoming_games, row])

@app.post("/finished_game")
async def add_finished_game(game: FinishedGame):
    global finished_games
    row = game.to_row()
    finished_games = pd.concat([finished_games, row])

@app.post("/prediction")
async def predict_game(game: GameBase):
    row = game.to_row()
    X = row.to_frame().T
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

@app.get("/filter", response_model=list[FinishedGame])
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
        games.append(row_to_finished_game(row))
    return games

