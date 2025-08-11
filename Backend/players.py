from typing import Annotated, Optional, Dict, Any
from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field, AfterValidator,  model_validator, ConfigDict
import pandas as pd
from datetime import datetime
from teams import Date

class PlayerBoxScore(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    box_score: Dict[str, Any]

    @model_validator(mode="after")
    def validate_box_score(self) -> "PlayerBoxScore":
        required = [  'Minutes', 'Points', 'Assists', 'Blocks', 'Steals', 'FGA', 'FGM', 'FG%',
       '3PA', '3PM', '3P%', 'FTA', 'FTM', 'FT%', 'Def Rebounds',
       'Off Rebounds', 'Tot Rebounds', 'Fouls', 'Turnovers', 'Plus Minus',
       'Date Number', 'Player Name', 'Team', 'Opp Team'
        ]

        missing = set(required) - set(self.box_score.keys())
        if missing:
            raise ValueError(f"Missing required box_score fields: {missing}")

        return self

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.box_score])

class PlayerSeasonStats(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pgs: Dict[str, Any]

    @model_validator(mode="after")
    def validate_pgs(self) -> "PlayerSeasonStats":
        required = ['Date Number', 'Player Name', 'Team', 'Opp Team', 'Year', 'Home',
       'Game ID', 'Minutes Avg', 'Points Avg', 'Assists Avg', 'Blocks Avg',
       'Steals Avg', 'FGA Avg', 'FGM Avg', '3PA Avg', '3PM Avg', 'FTA Avg',
       'FTM Avg', 'Def Rebounds Avg', 'Off Rebounds Avg', 'Tot Rebounds Avg',
       'Fouls Avg', 'Turnovers Avg', 'Plus Minus Avg', 'Overall FG%',
       'Overall FT%', 'Overall 3P%', 'Player EFF']

        missing = set(required) - set(self.pgs.keys())
        if missing:
            raise ValueError(f"Missing required pgs fields: {missing}")

        return self

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.pgs])

class PlayerCareerStats(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pgs: Dict[str, Any]

    @model_validator(mode="after")
    def validate_pgs(self) -> "PlayerCareerStats":
        required = ['Date Number', 'Team', 'Opp Team', 'Year', 'Player Name',
       'Career Minutes Avg', 'Career Points Avg', 'Career Assists Avg',
       'Career Blocks Avg', 'Career Steals Avg', 'Career FGA Avg',
       'Career FGM Avg', 'Career 3PA Avg', 'Career 3PM Avg', 'Career FTA Avg',
       'Career FTM Avg', 'Career Def Rebounds Avg', 'Career Off Rebounds Avg',
       'Career Tot Rebounds Avg', 'Career Fouls Avg', 'Career Turnovers Avg',
       'Career Plus Minus Avg', 'Career FG%', 'Career FT%', 'Career 3P%',
       'Career Player EFF']

        missing = set(required) - set(self.pgs.keys())
        if missing:
            raise ValueError(f"Missing required pgs fields: {missing}")

        return self

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.pgs])

class PlayerCompletedGame(BaseModel):
    box_score: PlayerBoxScore
    pregame_stats: PlayerSeasonStats
    career_stats: PlayerCareerStats

    def to_row(self) -> pd.DataFrame:
        combined = {**self.pregame_stats.pgs, **self.box_score.box_score}
        return pd.DataFrame([combined])