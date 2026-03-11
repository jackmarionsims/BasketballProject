from typing import Annotated, Optional
from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field, AfterValidator,  model_validator, ConfigDict
from typing import Dict, Any
import pandas as pd
from datetime import datetime
# from data_helpers import get_pregame_stats, calculate_avgs_for_team, calculate_elos

class NBAName(Enum):
    ATLANTA_HAWKS = 'Atlanta Hawks'
    INDIANA_PACERS = 'Indiana Pacers'
    UTAH_JAZZ = 'Utah Jazz'
    PORTLAND_TRAIL_BLAZERS = 'Portland Trail Blazers'
    DENVER_NUGGETS = 'Denver Nuggets'
    CHICAGO_BULLS = 'Chicago Bulls'
    MINNESOTA_TIMBERWOLVES = 'Minnesota Timberwolves'
    LOS_ANGELES_CLIPPERS = 'Los Angeles Clippers'
    CHARLOTTE_HORNETS = 'Charlotte Hornets'
    BOSTON_CELTICS = 'Boston Celtics'
    DETROIT_PISTONS = 'Detroit Pistons'
    MIAMI_HEAT = 'Miami Heat'
    DALLAS_MAVERICKS = 'Dallas Mavericks'
    MILWAUKEE_BUCKS = 'Milwaukee Bucks'
    NEW_YORK_KNICKS = 'New York Knicks'
    ORLANDO_MAGIC = 'Orlando Magic'
    PHILADELPHIA_76ERS = 'Philadelphia 76ers'
    PHOENIX_SUNS = 'Phoenix Suns'
    SACRAMENTO_KINGS = 'Sacramento Kings'
    SAN_ANTONIO_SPURS = 'San Antonio Spurs'
    SEATTLE_SUPERSONICS = 'Seattle SuperSonics'
    WASHINGTON_BULLETS = 'Washington Bullets'
    GOLDEN_STATE_WARRIORS = 'Golden State Warriors'
    HOUSTON_ROCKETS = 'Houston Rockets'
    LOS_ANGELES_LAKERS = 'Los Angeles Lakers'
    CLEVELAND_CAVALIERS = 'Cleveland Cavaliers'
    NEW_JERSEY_NETS = 'New Jersey Nets'
    TORONTO_RAPTORS = 'Toronto Raptors'
    VANCOUVER_GRIZZLIES = 'Vancouver Grizzlies'
    WASHINGTON_WIZARDS = 'Washington Wizards'
    MEMPHIS_GRIZZLIES = 'Memphis Grizzlies'
    NEW_ORLEANS_HORNETS = 'New Orleans Hornets'
    CHARLOTTE_BOBCATS = 'Charlotte Bobcats'
    OKLAHOMA_CITY_HORNETS = 'Oklahoma City Hornets'
    OKLAHOMA_CITY_THUNDER = 'Oklahoma City Thunder'
    BROOKLYN_NETS = 'Brooklyn Nets'
    NEW_ORLEANS_PELICANS = 'New Orleans Pelicans'


class Date(BaseModel):
    year: int
    month: str
    day_of_week: str
    day_num: int
    season: int

    def to_number(self):
        try:
            
            # Try full month name first (e.g., "August")
            try:
                month_number = datetime.strptime(self.month, "%B").month
            except ValueError:
                # If that fails, try abbreviated month name (e.g., "Aug")
                month_number = datetime.strptime(self.month, "%b").month

            dt = datetime(self.year, month_number, self.day_num)
            return dt.toordinal()
        except Exception as e:
            print(f"Failed to convert date: {self} ({e})")
            return None
        
    def to_str(self):
        return f"{self.day_of_week[:3]}, {self.month[:3]} {self.day_num}, {self.year}"



class NBATeam(BaseModel):
    name: NBAName
    
    # Basic ratings
    elo: float = Field(..., description="Current ELO rating of the team")
    
    
    stats: Dict = {}


    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.pgs])

class ScheduledGame(BaseModel):
    home: NBATeam
    visitor: NBATeam
    date: Date
    playoff: bool

    pgs: Dict[str, Any] = Field(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def compute_pgs(self) -> "ScheduledGame":
        if self.pgs is None:
            df = get_pregame_stats(self.home, self.visitor, self.date)
            self.pgs = df.iloc[0].to_dict()
        return self

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.pgs])



class BoxScore(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    box_score: Dict[str, Any]  # store row as dict instead of DataFrame

    @model_validator(mode="after")
    def validate_box_score(self) -> "BoxScore":
        required = [
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
            'Visitor Team TOV'
        ]
        # next = ['Home Team ORB%', 'Visitor Team ORB%', 'Home Team TO%', 'Visitor Team TO%',
        #     'Home Team FTM/FGA', 'Visitor Team FTM/FGA', 'Home Team TS%', 'Visitor Team TS%']

        missing = set(required) - set(self.box_score.keys())
        if missing:
            raise ValueError(f"Missing required box_score fields: {missing}")

        return self

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.box_score])



class CompletedGame(BaseModel):
    box_score: BoxScore
    scheduled_game: ScheduledGame

    def to_row(self) -> pd.DataFrame:
        combined = {**self.scheduled_game.pgs, **self.box_score.box_score}
        return pd.DataFrame([combined])
