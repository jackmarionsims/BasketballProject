from typing import Annotated, Optional
from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field, AfterValidator,  model_validator, ConfigDict
import pandas as pd
from datetime import datetime

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
    NEW_ORLEANS_OKLAHOMA_CITY_HORNETS = 'New Orleans/Oklahoma City Hornets'
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



class ScheduledGame(BaseModel):
    home: NBAName
    visitor: NBAName
    # id: int
    date: Date
    playoff: bool

from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, model_validator
import pandas as pd

class BoxScore(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    box_score: Dict[str, Any]  # store row as dict instead of DataFrame

    @model_validator(mode="after")
    def validate_box_score(self) -> "BoxScore":
        required = [  # same required columns
            'Visitor Team', 'Visitor Team Points', 'Home Team', 'Home Team Points', 'Winner', 'Loser', 'Home Win',
            'Home Team Assists', 'Home Team Tot Rebounds', 'Home Team Off Rebounds', 'Home Team Def Rebounds',
            'Home Team Blocks', 'Home Team Steals', 'Home Team FGA', 'Home Team FGM', 'Home Team FG%',
            'Home Team 3PA', 'Home Team 3PM', 'Home Team 3P%', 'Home Team FTA', 'Home Team FTM', 'Home Team FT%',
            'Home Team Fouls', 'Home Team TO', 'Visitor Team Assists', 'Visitor Team Tot Rebounds',
            'Visitor Team Off Rebounds', 'Visitor Team Def Rebounds', 'Visitor Team Blocks', 'Visitor Team Steals',
            'Visitor Team FGA', 'Visitor Team FGM', 'Visitor Team FG%', 'Visitor Team 3PA', 'Visitor Team 3PM',
            'Visitor Team 3P%', 'Visitor Team FTA', 'Visitor Team FTM', 'Visitor Team FT%', 'Visitor Team Fouls',
            'Visitor Team TO', 'Home Team ORB%', 'Visitor Team ORB%', 'Home Team TO%', 'Visitor Team TO%',
            'Home Team FTM/FGA', 'Visitor Team FTM/FGA', 'Home Team TS%', 'Visitor Team TS%'
        ]

        missing = set(required) - set(self.box_score.keys())
        if missing:
            raise ValueError(f"Missing required box_score fields: {missing}")

        return self

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.box_score])


class PregameStats(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pgs: Dict[str, Any]

    @model_validator(mode="after")
    def validate_pgs(self) -> "PregameStats":
        required = ['Home Team', 'Visitor Team', 'Home Team Points Avg', 'Visitor Team Points Avg', 'Home Team Opp Points Avg', 'Visitor Team Opp Points Avg', 'Home Team Assists Avg', 'Visitor Team Assists Avg', 'Home Team Tot Rebounds Avg', 'Visitor Team Tot Rebounds Avg', 'Home Team Off Rebounds Avg', 'Visitor Team Off Rebounds Avg', 'Home Team Def Rebounds Avg', 'Visitor Team Def Rebounds Avg', 'Home Team Blocks Avg', 'Visitor Team Blocks Avg', 'Home Team Steals Avg', 'Visitor Team Steals Avg', 'Home Team FGA Avg', 'Visitor Team FGA Avg', 'Home Team FGM Avg', 'Visitor Team FGM Avg', 'Home Team FG% Avg', 'Visitor Team FG% Avg', 'Home Team 3PA Avg', 'Visitor Team 3PA Avg', 'Home Team 3PM Avg', 'Visitor Team 3PM Avg', 'Home Team 3P% Avg', 'Visitor Team 3P% Avg', 'Home Team FTA Avg', 'Visitor Team FTA Avg', 'Home Team FTM Avg', 'Visitor Team FTM Avg', 'Home Team FT% Avg', 'Visitor Team FT% Avg', 'Home Team Fouls Avg', 'Visitor Team Fouls Avg', 'Home Team TO Avg', 'Visitor Team TO Avg', 'Home Team ORB% Avg', 'Visitor Team ORB% Avg', 'Home Team TO% Avg', 'Visitor Team TO% Avg', 'Home Team FTM/FGA Avg', 'Visitor Team FTM/FGA Avg', 'Home Team TS% Avg', 'Visitor Team TS% Avg', 'Home Team Opp Assists Avg', 'Visitor Team Opp Assists Avg', 'Home Team Opp Tot Rebounds Avg', 'Visitor Team Opp Tot Rebounds Avg', 'Home Team Opp Off Rebounds Avg', 'Visitor Team Opp Off Rebounds Avg', 'Home Team Opp Def Rebounds Avg', 'Visitor Team Opp Def Rebounds Avg', 'Home Team Opp Blocks Avg', 'Visitor Team Opp Blocks Avg', 'Home Team Opp Steals Avg', 'Visitor Team Opp Steals Avg', 'Home Team Opp FGA Avg', 'Visitor Team Opp FGA Avg', 'Home Team Opp FGM Avg', 'Visitor Team Opp FGM Avg', 'Home Team Opp FG% Avg', 'Visitor Team Opp FG% Avg', 'Home Team Opp 3PA Avg', 'Visitor Team Opp 3PA Avg', 'Home Team Opp 3PM Avg', 'Visitor Team Opp 3PM Avg', 'Home Team Opp 3P% Avg', 'Visitor Team Opp 3P% Avg', 'Home Team Opp FTA Avg', 'Visitor Team Opp FTA Avg', 'Home Team Opp FTM Avg', 'Visitor Team Opp FTM Avg', 'Home Team Opp FT% Avg', 'Visitor Team Opp FT% Avg', 'Home Team Opp Fouls Avg', 'Visitor Team Opp Fouls Avg', 'Home Team Opp TO Avg', 'Visitor Team Opp TO Avg', 'Home Team Opp ORB% Avg', 'Visitor Team Opp ORB% Avg', 'Home Team Opp TO% Avg', 'Visitor Team Opp TO% Avg', 'Home Team Opp FTM/FGA Avg', 'Visitor Team Opp FTM/FGA Avg', 'Home Team Opp TS% Avg', 'Visitor Team Opp TS% Avg', 'Home Team W', "Home Team L", "Visitor Team W", "Visitor Team L", "Home Team W/L%", "Visitor Team W/L%", "Playoff Game", "Home Team ELO", "Visitor Team ELO", 'Date Number', 'Year', 'Date']

        missing = set(required) - set(self.pgs.keys())
        if missing:
            raise ValueError(f"Missing required pgs fields: {missing}")

        return self

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame([self.pgs])


class CompletedGame(BaseModel):
    box_score: BoxScore
    pregame_stats: PregameStats

    def to_row(self) -> pd.DataFrame:
        combined = {**self.pregame_stats.pgs, **self.box_score.box_score}
        return pd.DataFrame([combined])

class FilterParams(BaseModel):
    # Points
    pts_min: Optional[int] = None
    pts_max: Optional[int] = None

    # Assists
    ast_min: Optional[int] = None
    ast_max: Optional[int] = None

    # Total rebounds
    trb_min: Optional[int] = None
    trb_max: Optional[int] = None

    # Offensive rebounds
    orb_min: Optional[int] = None
    orb_max: Optional[int] = None

    # Defensive rebounds
    drb_min: Optional[int] = None
    drb_max: Optional[int] = None

    # Blocks
    blk_min: Optional[int] = None
    blk_max: Optional[int] = None

    # Steals
    stl_min: Optional[int] = None
    stl_max: Optional[int] = None

    # Field goals attempted
    fga_min: Optional[int] = None
    fga_max: Optional[int] = None

    # Field goals made
    fgm_min: Optional[int] = None
    fgm_max: Optional[int] = None

    # Field goal %
    fg_pct_min: Optional[float] = None
    fg_pct_max: Optional[float] = None

    # Three-point attempts
    tpa_min: Optional[int] = None
    tpa_max: Optional[int] = None

    # Three-point makes
    tpm_min: Optional[int] = None
    tpm_max: Optional[int] = None

    # Three-point %
    tp_pct_min: Optional[float] = None
    tp_pct_max: Optional[float] = None

    # Free throw attempts
    fta_min: Optional[int] = None
    fta_max: Optional[int] = None

    # Free throw makes
    ftm_min: Optional[int] = None
    ftm_max: Optional[int] = None

    # Free throw %
    ft_pct_min: Optional[float] = None
    ft_pct_max: Optional[float] = None

    # Fouls
    fouls_min: Optional[int] = None
    fouls_max: Optional[int] = None

    # Turnovers
    to_min: Optional[int] = None
    to_max: Optional[int] = None


def get_filter1(
    pts_min: Optional[int] = Query(None, alias="team1_pts_min"),
    pts_max: Optional[int] = Query(None, alias="team1_pts_max"),
    ast_min: Optional[int] = Query(None, alias="team1_ast_min"),
    ast_max: Optional[int] = Query(None, alias="team1_ast_max"),
    trb_min: Optional[int] = Query(None, alias="team1_trb_min"),
    trb_max: Optional[int] = Query(None, alias="team1_trb_max"),
    orb_min: Optional[int] = Query(None, alias="team1_orb_min"),
    orb_max: Optional[int] = Query(None, alias="team1_orb_max"),
    drb_min: Optional[int] = Query(None, alias="team1_drb_min"),
    drb_max: Optional[int] = Query(None, alias="team1_drb_max"),
    blk_min: Optional[int] = Query(None, alias="team1_blk_min"),
    blk_max: Optional[int] = Query(None, alias="team1_blk_max"),
    stl_min: Optional[int] = Query(None, alias="team1_stl_min"),
    stl_max: Optional[int] = Query(None, alias="team1_stl_max"),
    fga_min: Optional[int] = Query(None, alias="team1_fga_min"),
    fga_max: Optional[int] = Query(None, alias="team1_fga_max"),
    fgm_min: Optional[int] = Query(None, alias="team1_fgm_min"),
    fgm_max: Optional[int] = Query(None, alias="team1_fgm_max"),
    fg_pct_min: Optional[float] = Query(None, alias="team1_fg_pct_min"),
    fg_pct_max: Optional[float] = Query(None, alias="team1_fg_pct_max"),
    tpa_min: Optional[int] = Query(None, alias="team1_3pa_min"),
    tpa_max: Optional[int] = Query(None, alias="team1_3pa_max"),
    tpm_min: Optional[int] = Query(None, alias="team1_3pm_min"),
    tpm_max: Optional[int] = Query(None, alias="team1_3pm_max"),
    tp_pct_min: Optional[float] = Query(None, alias="team1_3pct_min"),
    tp_pct_max: Optional[float] = Query(None, alias="team1_3pct_max"),
    fta_min: Optional[int] = Query(None, alias="team1_fta_min"),
    fta_max: Optional[int] = Query(None, alias="team1_fta_max"),
    ftm_min: Optional[int] = Query(None, alias="team1_ftm_min"),
    ftm_max: Optional[int] = Query(None, alias="team1_ftm_max"),
    ft_pct_min: Optional[float] = Query(None, alias="team1_ft_pct_min"),
    ft_pct_max: Optional[float] = Query(None, alias="team1_ft_pct_max"),
    fouls_min: Optional[int] = Query(None, alias="team1_fouls_min"),
    fouls_max: Optional[int] = Query(None, alias="team1_fouls_max"),
    to_min: Optional[int] = Query(None, alias="team1_to_min"),
    to_max: Optional[int] = Query(None, alias="team1_to_max")
) -> FilterParams:
    return FilterParams(
        pts_min=pts_min, pts_max=pts_max,
        ast_min=ast_min, ast_max=ast_max,
        trb_min=trb_min, trb_max=trb_max,
        orb_min=orb_min, orb_max=orb_max,
        drb_min=drb_min, drb_max=drb_max,
        blk_min=blk_min, blk_max=blk_max,
        stl_min=stl_min, stl_max=stl_max,
        fga_min=fga_min, fga_max=fga_max,
        fgm_min=fgm_min, fgm_max=fgm_max,
        fg_pct_min=fg_pct_min, fg_pct_max=fg_pct_max,
        tpa_min=tpa_min, tpa_max=tpa_max,
        tpm_min=tpm_min, tpm_max=tpm_max,
        tp_pct_min=tp_pct_min, tp_pct_max=tp_pct_max,
        fta_min=fta_min, fta_max=fta_max,
        ftm_min=ftm_min, ftm_max=ftm_max,
        ft_pct_min=ft_pct_min, ft_pct_max=ft_pct_max,
        fouls_min=fouls_min, fouls_max=fouls_max,
        to_min=to_min, to_max=to_max
    )


def get_filter2(
    pts_min: Optional[int] = Query(None, alias="team2_pts_min"),
    pts_max: Optional[int] = Query(None, alias="team2_pts_max"),
    ast_min: Optional[int] = Query(None, alias="team2_ast_min"),
    ast_max: Optional[int] = Query(None, alias="team2_ast_max"),
    trb_min: Optional[int] = Query(None, alias="team2_trb_min"),
    trb_max: Optional[int] = Query(None, alias="team2_trb_max"),
    orb_min: Optional[int] = Query(None, alias="team2_orb_min"),
    orb_max: Optional[int] = Query(None, alias="team2_orb_max"),
    drb_min: Optional[int] = Query(None, alias="team2_drb_min"),
    drb_max: Optional[int] = Query(None, alias="team2_drb_max"),
    blk_min: Optional[int] = Query(None, alias="team2_blk_min"),
    blk_max: Optional[int] = Query(None, alias="team2_blk_max"),
    stl_min: Optional[int] = Query(None, alias="team2_stl_min"),
    stl_max: Optional[int] = Query(None, alias="team2_stl_max"),
    fga_min: Optional[int] = Query(None, alias="team2_fga_min"),
    fga_max: Optional[int] = Query(None, alias="team2_fga_max"),
    fgm_min: Optional[int] = Query(None, alias="team2_fgm_min"),
    fgm_max: Optional[int] = Query(None, alias="team2_fgm_max"),
    fg_pct_min: Optional[float] = Query(None, alias="team2_fg_pct_min"),
    fg_pct_max: Optional[float] = Query(None, alias="team2_fg_pct_max"),
    tpa_min: Optional[int] = Query(None, alias="team2_3pa_min"),
    tpa_max: Optional[int] = Query(None, alias="team2_3pa_max"),
    tpm_min: Optional[int] = Query(None, alias="team2_3pm_min"),
    tpm_max: Optional[int] = Query(None, alias="team2_3pm_max"),
    tp_pct_min: Optional[float] = Query(None, alias="team2_3pct_min"),
    tp_pct_max: Optional[float] = Query(None, alias="team2_3pct_max"),
    fta_min: Optional[int] = Query(None, alias="team2_fta_min"),
    fta_max: Optional[int] = Query(None, alias="team2_fta_max"),
    ftm_min: Optional[int] = Query(None, alias="team2_ftm_min"),
    ftm_max: Optional[int] = Query(None, alias="team2_ftm_max"),
    ft_pct_min: Optional[float] = Query(None, alias="team2_ft_pct_min"),
    ft_pct_max: Optional[float] = Query(None, alias="team2_ft_pct_max"),
    fouls_min: Optional[int] = Query(None, alias="team2_fouls_min"),
    fouls_max: Optional[int] = Query(None, alias="team2_fouls_max"),
    to_min: Optional[int] = Query(None, alias="team2_to_min"),
    to_max: Optional[int] = Query(None, alias="team2_to_max")
) -> FilterParams:
    return FilterParams(
        pts_min=pts_min, pts_max=pts_max,
        ast_min=ast_min, ast_max=ast_max,
        trb_min=trb_min, trb_max=trb_max,
        orb_min=orb_min, orb_max=orb_max,
        drb_min=drb_min, drb_max=drb_max,
        blk_min=blk_min, blk_max=blk_max,
        stl_min=stl_min, stl_max=stl_max,
        fga_min=fga_min, fga_max=fga_max,
        fgm_min=fgm_min, fgm_max=fgm_max,
        fg_pct_min=fg_pct_min, fg_pct_max=fg_pct_max,
        tpa_min=tpa_min, tpa_max=tpa_max,
        tpm_min=tpm_min, tpm_max=tpm_max,
        tp_pct_min=tp_pct_min, tp_pct_max=tp_pct_max,
        fta_min=fta_min, fta_max=fta_max,
        ftm_min=ftm_min, ftm_max=ftm_max,
        ft_pct_min=ft_pct_min, ft_pct_max=ft_pct_max,
        fouls_min=fouls_min, fouls_max=fouls_max,
        to_min=to_min, to_max=to_max
    )
# class BoxScore(BaseModel):
#     model_config = ConfigDict(arbitrary_types_allowed=True)

#     box_score: pd.DataFrame

#     # This runs automatically after the model is created
#     @model_validator(mode="after")
#     def validate_box_score(self) -> "BoxScore":
#         required = [
#             'Visitor Team', 'Visitor Team Points', 'Home Team', 'Home Team Points', 'Winner', 'Loser', 'Home Win',
#             'Home Team Assists', 'Home Team Tot Rebounds', 'Home Team Off Rebounds', 'Home Team Def Rebounds',
#             'Home Team Blocks', 'Home Team Steals', 'Home Team FGA', 'Home Team FGM', 'Home Team FG%',
#             'Home Team 3PA', 'Home Team 3PM', 'Home Team 3P%', 'Home Team FTA', 'Home Team FTM', 'Home Team FT%',
#             'Home Team Fouls', 'Home Team TO', 'Visitor Team Assists', 'Visitor Team Tot Rebounds',
#             'Visitor Team Off Rebounds', 'Visitor Team Def Rebounds', 'Visitor Team Blocks', 'Visitor Team Steals',
#             'Visitor Team FGA', 'Visitor Team FGM', 'Visitor Team FG%', 'Visitor Team 3PA', 'Visitor Team 3PM',
#             'Visitor Team 3P%', 'Visitor Team FTA', 'Visitor Team FTM', 'Visitor Team FT%', 'Visitor Team Fouls',
#             'Visitor Team TO', 'Home Team ORB%', 'Visitor Team ORB%', 'Home Team TO%', 'Visitor Team TO%',
#             'Home Team FTM/FGA', 'Visitor Team FTM/FGA', 'Home Team TS%', 'Visitor Team TS%'
#         ]

#         df = self.box_score
#         if not isinstance(df, pd.DataFrame):
#             raise TypeError("box_score must be a pandas DataFrame")
#         if df.shape[0] != 1:
#             raise ValueError(f"Expected exactly 1 row, got {df.shape[0]}")

#         actual = list(df.columns)

#         missing = set(required) - set(actual)
#         if missing:
#             raise ValueError(f"Missing required columns: {missing}")

#         # extra = set(actual) - set(required)
#         # if extra:
#         #     raise ValueError(f"Unexpected extra columns: {extra}")

#         # Validate team names
#         single_row = df.iloc[0]
#         try:
#             _ = NBAName(single_row["Home Team"])
#             _ = NBAName(single_row["Visitor Team"])
#         except ValueError as e:
#             raise ValueError(f"Invalid team name in row: {e}")

#         return self

#     def to_row(self) -> pd.DataFrame:
#         """Return the single row as a Pandas DataFrame"""
#         return self.box_score


# class PregameStats(BaseModel):
#     model_config = ConfigDict(arbitrary_types_allowed=True)
#     pgs: pd.DataFrame

#     # This runs automatically after the model is created
#     @model_validator(mode="after")
#     def validate_pgs(self) -> "PregameStats":
#         required = ['Home Team', 'Visitor Team', 'Home Team Points Avg', 'Visitor Team Points Avg', 'Home Team Opp Points Avg', 'Visitor Team Opp Points Avg', 'Home Team Assists Avg', 'Visitor Team Assists Avg', 'Home Team Tot Rebounds Avg', 'Visitor Team Tot Rebounds Avg', 'Home Team Off Rebounds Avg', 'Visitor Team Off Rebounds Avg', 'Home Team Def Rebounds Avg', 'Visitor Team Def Rebounds Avg', 'Home Team Blocks Avg', 'Visitor Team Blocks Avg', 'Home Team Steals Avg', 'Visitor Team Steals Avg', 'Home Team FGA Avg', 'Visitor Team FGA Avg', 'Home Team FGM Avg', 'Visitor Team FGM Avg', 'Home Team FG% Avg', 'Visitor Team FG% Avg', 'Home Team 3PA Avg', 'Visitor Team 3PA Avg', 'Home Team 3PM Avg', 'Visitor Team 3PM Avg', 'Home Team 3P% Avg', 'Visitor Team 3P% Avg', 'Home Team FTA Avg', 'Visitor Team FTA Avg', 'Home Team FTM Avg', 'Visitor Team FTM Avg', 'Home Team FT% Avg', 'Visitor Team FT% Avg', 'Home Team Fouls Avg', 'Visitor Team Fouls Avg', 'Home Team TO Avg', 'Visitor Team TO Avg', 'Home Team ORB% Avg', 'Visitor Team ORB% Avg', 'Home Team TO% Avg', 'Visitor Team TO% Avg', 'Home Team FTM/FGA Avg', 'Visitor Team FTM/FGA Avg', 'Home Team TS% Avg', 'Visitor Team TS% Avg', 'Home Team Opp Assists Avg', 'Visitor Team Opp Assists Avg', 'Home Team Opp Tot Rebounds Avg', 'Visitor Team Opp Tot Rebounds Avg', 'Home Team Opp Off Rebounds Avg', 'Visitor Team Opp Off Rebounds Avg', 'Home Team Opp Def Rebounds Avg', 'Visitor Team Opp Def Rebounds Avg', 'Home Team Opp Blocks Avg', 'Visitor Team Opp Blocks Avg', 'Home Team Opp Steals Avg', 'Visitor Team Opp Steals Avg', 'Home Team Opp FGA Avg', 'Visitor Team Opp FGA Avg', 'Home Team Opp FGM Avg', 'Visitor Team Opp FGM Avg', 'Home Team Opp FG% Avg', 'Visitor Team Opp FG% Avg', 'Home Team Opp 3PA Avg', 'Visitor Team Opp 3PA Avg', 'Home Team Opp 3PM Avg', 'Visitor Team Opp 3PM Avg', 'Home Team Opp 3P% Avg', 'Visitor Team Opp 3P% Avg', 'Home Team Opp FTA Avg', 'Visitor Team Opp FTA Avg', 'Home Team Opp FTM Avg', 'Visitor Team Opp FTM Avg', 'Home Team Opp FT% Avg', 'Visitor Team Opp FT% Avg', 'Home Team Opp Fouls Avg', 'Visitor Team Opp Fouls Avg', 'Home Team Opp TO Avg', 'Visitor Team Opp TO Avg', 'Home Team Opp ORB% Avg', 'Visitor Team Opp ORB% Avg', 'Home Team Opp TO% Avg', 'Visitor Team Opp TO% Avg', 'Home Team Opp FTM/FGA Avg', 'Visitor Team Opp FTM/FGA Avg', 'Home Team Opp TS% Avg', 'Visitor Team Opp TS% Avg', 'Home Team W', "Home Team L", "Visitor Team W", "Visitor Team L", "Home Team W/L%", "Visitor Team W/L%", "Playoff Game", "Home Team ELO", "Visitor Team ELO", 'Date Number', 'Year', 'Date']

#         df = self.pgs
#         if not isinstance(df, pd.DataFrame):
#             raise TypeError("pregame_stats must be a pandas DataFrame")
#         if df.shape[0] != 1:
#             raise ValueError(f"Expected exactly 1 row, got {df.shape[0]}")

#         actual = list(df.columns)

#         missing = set(required) - set(actual)
#         if missing:
#             raise ValueError(f"Missing required columns: {missing}")

#         extra = set(actual) - set(required)
#         if extra:
#             raise ValueError(f"Unexpected extra columns: {extra}")

#         # Validate team names
#         single_row = df.iloc[0]
#         try:
#             _ = NBAName(single_row["Home Team"])
#             _ = NBAName(single_row["Visitor Team"])
#         except ValueError as e:
#             raise ValueError(f"Invalid team name in row: {e}")

#         return self

#     def to_row(self):
#         return self.pgs


# class CompletedGame(BaseModel):
#     box_score: BoxScore
#     pregame_stats: PregameStats

#     def to_row(self) -> pd.DataFrame:
#         # Convert both to single-row DataFrames
#         box_score_row = self.box_score.to_row()
#         game_row = self.pregame_stats.to_row()

#         # Convert both to dicts, box_score overwrites any overlaps
#         combined_data = {**game_row.iloc[0].to_dict(), **box_score_row.iloc[0].to_dict()}

#         # Return as a single-row DataFrame
#         return pd.DataFrame([combined_data])


def row_to_completed_game(row: pd.DataFrame):
    bs_df = row[[
            'Visitor Team', 'Visitor Team Points', 'Home Team', 'Home Team Points', 'Winner', 'Loser', 'Home Win',
            'Home Team Assists', 'Home Team Tot Rebounds', 'Home Team Off Rebounds', 'Home Team Def Rebounds',
            'Home Team Blocks', 'Home Team Steals', 'Home Team FGA', 'Home Team FGM', 'Home Team FG%',
            'Home Team 3PA', 'Home Team 3PM', 'Home Team 3P%', 'Home Team FTA', 'Home Team FTM', 'Home Team FT%',
            'Home Team Fouls', 'Home Team TO', 'Visitor Team Assists', 'Visitor Team Tot Rebounds',
            'Visitor Team Off Rebounds', 'Visitor Team Def Rebounds', 'Visitor Team Blocks', 'Visitor Team Steals',
            'Visitor Team FGA', 'Visitor Team FGM', 'Visitor Team FG%', 'Visitor Team 3PA', 'Visitor Team 3PM',
            'Visitor Team 3P%', 'Visitor Team FTA', 'Visitor Team FTM', 'Visitor Team FT%', 'Visitor Team Fouls',
            'Visitor Team TO', 'Home Team ORB%', 'Visitor Team ORB%', 'Home Team TO%', 'Visitor Team TO%',
            'Home Team FTM/FGA', 'Visitor Team FTM/FGA', 'Home Team TS%', 'Visitor Team TS%'
        ]]
    pgs_df = row[['Home Team', 'Visitor Team', 'Home Team Points Avg', 'Visitor Team Points Avg', 'Home Team Opp Points Avg', 'Visitor Team Opp Points Avg', 'Home Team Assists Avg', 'Visitor Team Assists Avg', 'Home Team Tot Rebounds Avg', 'Visitor Team Tot Rebounds Avg', 'Home Team Off Rebounds Avg', 'Visitor Team Off Rebounds Avg', 'Home Team Def Rebounds Avg', 'Visitor Team Def Rebounds Avg', 'Home Team Blocks Avg', 'Visitor Team Blocks Avg', 'Home Team Steals Avg', 'Visitor Team Steals Avg', 'Home Team FGA Avg', 'Visitor Team FGA Avg', 'Home Team FGM Avg', 'Visitor Team FGM Avg', 'Home Team FG% Avg', 'Visitor Team FG% Avg', 'Home Team 3PA Avg', 'Visitor Team 3PA Avg', 'Home Team 3PM Avg', 'Visitor Team 3PM Avg', 'Home Team 3P% Avg', 'Visitor Team 3P% Avg', 'Home Team FTA Avg', 'Visitor Team FTA Avg', 'Home Team FTM Avg', 'Visitor Team FTM Avg', 'Home Team FT% Avg', 'Visitor Team FT% Avg', 'Home Team Fouls Avg', 'Visitor Team Fouls Avg', 'Home Team TO Avg', 'Visitor Team TO Avg', 'Home Team ORB% Avg', 'Visitor Team ORB% Avg', 'Home Team TO% Avg', 'Visitor Team TO% Avg', 'Home Team FTM/FGA Avg', 'Visitor Team FTM/FGA Avg', 'Home Team TS% Avg', 'Visitor Team TS% Avg', 'Home Team Opp Assists Avg', 'Visitor Team Opp Assists Avg', 'Home Team Opp Tot Rebounds Avg', 'Visitor Team Opp Tot Rebounds Avg', 'Home Team Opp Off Rebounds Avg', 'Visitor Team Opp Off Rebounds Avg', 'Home Team Opp Def Rebounds Avg', 'Visitor Team Opp Def Rebounds Avg', 'Home Team Opp Blocks Avg', 'Visitor Team Opp Blocks Avg', 'Home Team Opp Steals Avg', 'Visitor Team Opp Steals Avg', 'Home Team Opp FGA Avg', 'Visitor Team Opp FGA Avg', 'Home Team Opp FGM Avg', 'Visitor Team Opp FGM Avg', 'Home Team Opp FG% Avg', 'Visitor Team Opp FG% Avg', 'Home Team Opp 3PA Avg', 'Visitor Team Opp 3PA Avg', 'Home Team Opp 3PM Avg', 'Visitor Team Opp 3PM Avg', 'Home Team Opp 3P% Avg', 'Visitor Team Opp 3P% Avg', 'Home Team Opp FTA Avg', 'Visitor Team Opp FTA Avg', 'Home Team Opp FTM Avg', 'Visitor Team Opp FTM Avg', 'Home Team Opp FT% Avg', 'Visitor Team Opp FT% Avg', 'Home Team Opp Fouls Avg', 'Visitor Team Opp Fouls Avg', 'Home Team Opp TO Avg', 'Visitor Team Opp TO Avg', 'Home Team Opp ORB% Avg', 'Visitor Team Opp ORB% Avg', 'Home Team Opp TO% Avg', 'Visitor Team Opp TO% Avg', 'Home Team Opp FTM/FGA Avg', 'Visitor Team Opp FTM/FGA Avg', 'Home Team Opp TS% Avg', 'Visitor Team Opp TS% Avg', 'Home Team W', "Home Team L", "Visitor Team W", "Visitor Team L", "Home Team W/L%", "Visitor Team W/L%", "Playoff Game", "Home Team ELO", "Visitor Team ELO", 'Date Number', 'Year', 'Date']]
    box_score = BoxScore(box_score=bs_df.iloc[0].to_dict())
    pgs = PregameStats(pgs=pgs_df.iloc[0].to_dict())
    return CompletedGame(box_score=box_score, pregame_stats=pgs)


def calculate_rolling_stat_per_year(df, stat_col, date_col="Date Number"):
    home_averages = []
    visitor_averages = []
    home_opp_averages = []
    visitor_opp_averages = []

    # Process year by year
    for year, group in df.groupby("Year"):
        stat_dict = {}  # Reset each year
        opp_stat_dict = {}
        for idx, row in group.sort_values(date_col).iterrows():
            home_team = row["Home Team"]
            visitor_team = row["Visitor Team"]
            home_stat = row.get(f"Home Team {stat_col}", None)
            visitor_stat = row.get(f"Visitor Team {stat_col}", None)

            # Get current averages
            home_data = stat_dict.get(home_team, {"total": 0, "games": 0})
            visitor_data = stat_dict.get(visitor_team, {"total": 0, "games": 0})
            home_opp_data = opp_stat_dict.get(home_team, {"total": 0, "games": 0})
            visitor_opp_data = opp_stat_dict.get(visitor_team, {"total": 0, "games": 0})

            home_avg = (
                home_data["total"] / home_data["games"]
                if home_data["games"] > 0 else None
            )
            visitor_avg = (
                visitor_data["total"] / visitor_data["games"]
                if visitor_data["games"] > 0 else None
            )

            home_opp_avg = (
                home_opp_data["total"] / home_opp_data["games"]
                if home_opp_data["games"] > 0 else None
            )
            visitor_opp_avg = (
                visitor_opp_data["total"] / visitor_opp_data["games"]
                if visitor_opp_data["games"] > 0 else None
            )

            home_averages.append(home_avg)
            visitor_averages.append(visitor_avg)
            home_opp_averages.append(home_opp_avg)
            visitor_opp_averages.append(visitor_opp_avg)

            # Update totals *after* recording current averages
            stat_dict.setdefault(home_team, {"total": 0, "games": 0})
            stat_dict.setdefault(visitor_team, {"total": 0, "games": 0})
            opp_stat_dict.setdefault(home_team, {"total": 0, "games": 0})
            opp_stat_dict.setdefault(visitor_team, {"total": 0, "games": 0})

            if pd.notna(visitor_stat):
                stat_dict[visitor_team]["total"] += visitor_stat
                stat_dict[visitor_team]["games"] += 1
                opp_stat_dict[home_team]["total"] += visitor_stat
                opp_stat_dict[home_team]["games"] += 1

            if pd.notna(home_stat):
                stat_dict[home_team]["total"] += home_stat
                stat_dict[home_team]["games"] += 1
                opp_stat_dict[visitor_team]["total"] += home_stat
                opp_stat_dict[visitor_team]["games"] += 1

    # Add columns back to the original df (in order)
    df[f"Home Team {stat_col} Avg"] = home_averages
    df[f"Visitor Team {stat_col} Avg"] = visitor_averages
    df[f"Home Team Opp {stat_col} Avg"] = home_opp_averages
    df[f"Visitor Team Opp {stat_col} Avg"] = visitor_opp_averages

    return df

def calculate_avgs_for_team(df: pd.DataFrame, game: ScheduledGame, team_elos:  dict[tuple[NBAName, int], float]) -> PregameStats:
    home = game.home
    visitor = game.visitor
    new_row = pd.DataFrame([{
    "Home Team": home.value,
    "Visitor Team": visitor.value,
    "Date": game.date.to_str(),
    "Date Number": game.date.to_number(),
    "Year": game.date.season,
    "Playoff Game": 1 if game.playoff else 0,
    "Home Team ELO": team_elos[(home, game.date.season)],
    "Visitor Team ELO": team_elos[(visitor, game.date.season)],
    }])
    stat_dict = {}
    opp_stat_dict = {}
    cols = ['Points', 'Assists', 'Tot Rebounds', 'Off Rebounds', 
              'Def Rebounds', 'Blocks', 'Steals', 
              'FGA', 'FGM', 'FG%', '3PA', 
              '3PM', '3P%', 'FTA', 'FTM', 
              'FT%', 'Fouls', 'TO', 
              "ORB%", "TO%", "FTM/FGA", "TS%"]
    for stat_col in cols:
        for idx, row in df.iterrows():
            home_team = row["Home Team"]
            visitor_team = row["Visitor Team"]
            home_stat = row.get(f"Home Team {stat_col}", None)
            visitor_stat = row.get(f"Visitor Team {stat_col}", None)

            # Update totals *after* recording current averages
            stat_dict.setdefault(home_team, {"total": 0, "games": 0})
            stat_dict.setdefault(visitor_team, {"total": 0, "games": 0})
            opp_stat_dict.setdefault(home_team, {"total": 0, "games": 0})
            opp_stat_dict.setdefault(visitor_team, {"total": 0, "games": 0})

            if pd.notna(visitor_stat):
                stat_dict[visitor_team]["total"] += visitor_stat
                stat_dict[visitor_team]["games"] += 1
                opp_stat_dict[home_team]["total"] += visitor_stat
                opp_stat_dict[home_team]["games"] += 1

            if pd.notna(home_stat):
                stat_dict[home_team]["total"] += home_stat
                stat_dict[home_team]["games"] += 1
                opp_stat_dict[visitor_team]["total"] += home_stat
                opp_stat_dict[visitor_team]["games"] += 1

        home_data = stat_dict.get(home.value, {"total": 0, "games": 0})
        visitor_data = stat_dict.get(visitor.value, {"total": 0, "games": 0})
        home_opp_data = opp_stat_dict.get(home.value, {"total": 0, "games": 0})
        visitor_opp_data = opp_stat_dict.get(visitor.value, {"total": 0, "games": 0})

        home_avg = (
            home_data["total"] / home_data["games"]
            if home_data["games"] > 0 else None
        )
        visitor_avg = (
            visitor_data["total"] / visitor_data["games"]
            if visitor_data["games"] > 0 else None
        )

        home_opp_avg = (
            home_opp_data["total"] / home_opp_data["games"]
            if home_opp_data["games"] > 0 else None
        )
        visitor_opp_avg = (
            visitor_opp_data["total"] / visitor_opp_data["games"]
            if visitor_opp_data["games"] > 0 else None
        )
        new_row[f"Home Team {stat_col} Avg"] = home_avg
        new_row[f"Visitor Team {stat_col} Avg"] = visitor_avg
        new_row[f"Home Team Opp {stat_col} Avg"] = home_opp_avg
        new_row[f"Visitor Team Opp {stat_col} Avg"] = visitor_opp_avg
    stat_dict = {}
    for idx, row in df.iterrows():
        home_team = row["Home Team"]
        visitor_team = row["Visitor Team"]
        home_win = row.get(f"Home Win", None)

        # Update totals *after* recording current averages
        stat_dict.setdefault(home_team, {"wins": 0, "games": 0})
        stat_dict.setdefault(visitor_team, {"wins": 0, "games": 0})

        if pd.notna(home_win):
            stat_dict[visitor_team]["wins"] += 1-home_win
            stat_dict[visitor_team]["games"] += 1
            stat_dict[home_team]["wins"] += home_win
            stat_dict[home_team]["games"] += 1

    home_data = stat_dict.get(home.value, {"wins": 0, "games": 0})
    visitor_data = stat_dict.get(visitor.value, {"wins": 0, "games": 0})

    home_wl = (
        home_data["wins"] / home_data["games"]
        if home_data["games"] > 0 else None
    )
    visitor_wl = (
        visitor_data["wins"] / visitor_data["games"]
        if visitor_data["games"] > 0 else None
    )

    new_row[f"Home Team W"] = home_data["wins"]
    new_row[f"Visitor Team W"] = visitor_data["wins"]
    new_row[f"Home Team L"] = home_data['games'] - home_data["wins"]
    new_row[f"Visitor Team L"] = visitor_data['games'] - visitor_data["wins"]
    new_row[f"Home Team W/L%"] = home_wl
    new_row[f"Visitor Team W/L%"] = visitor_wl
    return PregameStats(pgs=new_row.iloc[0].to_dict())

def add_scheduled_game(df: pd.DataFrame, game: ScheduledGame, team_elos:  dict[tuple[NBAName, int], float]) -> pd.DataFrame:
    season = game.date.season
    date_num = game.date.to_number()
    previous_games = df[(df["Year"] == season) & (df["Date Number"] < date_num)]
    pgs = calculate_avgs_for_team(previous_games, game, team_elos)
    df = pd.concat([df, pgs.to_row()], ignore_index=True)
    return df

def add_completed_game(df: pd.DataFrame, box_score: BoxScore) -> pd.DataFrame:
    # Convert BoxScore to a single-row DataFrame
    bs = box_score.to_row()
    bs_row = bs.iloc[0]
    home = bs_row["Home Team"]
    visitor = bs_row["Visitor Team"]
    date_num = bs_row["Date Number"]

    # Find matching row
    match = df[
        (df["Home Team"] == home) &
        (df["Visitor Team"] == visitor) &
        (df["Date Number"] == date_num)
    ]
    if match.empty:
        raise ValueError("Matching pregame row not found in DataFrame.")
    idx = match.index[0]             # label index
    pos = df.index.get_loc(idx)      # integer position (for .iloc use)
    for col in bs_row.index:
        df.at[idx, col] = bs_row[col]
    df["Game ID"] = list(range(len(df)))
    return df

def get_id(df: pd.DataFrame, home: NBAName, visitor: NBAName, date_num: int) -> int:
    mask = (
        (df["Home Team"] == home) &
        (df["Visitor Team"] == visitor) &
        (df["Date Number"] == date_num)
    )
    if not mask.any():
        raise ValueError("Matching pregame row not found in DataFrame.")
    else:
        row = df.loc[mask].iloc[0]
        return row["Game ID"]

def elo_change(home_elo, visitor_elo, margin, k=20):
    expected_home = 1 / (1 + 10 ** ((visitor_elo - home_elo) / 400))
    score = 1 if margin > 0 else 0
    elo_diff = home_elo - visitor_elo
    if margin < 0:
        margin = -margin
    mov_multiplier = ((margin + 3) ** 0.8) / (7.5 + 0.006 * elo_diff)
    # mov_multiplier = min(mov_multiplier, 2)
    return k * mov_multiplier * (score - expected_home)

def get_all_elos(df: pd.DataFrame, team_elos: dict[tuple[NBAName, int], float], base_elo: int =1500) -> dict[tuple[NBAName, int], float]:
    base_elo = 1500

    for idx, game in df.iterrows():
        home_team = NBAName(game["Home Team"])
        visitor_team = NBAName(game["Visitor Team"])
        year = game["Year"]
        date_number = game["Date Number"]
        margin = game["Home Team Points"] - game["Visitor Team Points"]

        # Get raw (unadjusted) Elo from previous year or base
        raw_home_elo = team_elos.get((home_team, year - 1), base_elo)
        raw_visitor_elo = team_elos.get((visitor_team, year - 1), base_elo)

        # Check if first game of this team this year
        is_first_home_game = (home_team, year) not in team_elos
        is_first_visitor_game = (visitor_team, year) not in team_elos

        # Apply seasonal decay BEFORE storing
        if is_first_home_game:
            home_elo = 0.75 * raw_home_elo + 0.25 * base_elo
            team_elos[(home_team, year)] = home_elo  # initialize season
        else:
            home_elo = team_elos[(home_team, year)]

        if is_first_visitor_game:
            visitor_elo = 0.75 * raw_visitor_elo + 0.25 * base_elo
            team_elos[(visitor_team, year)] = visitor_elo
        else:
            visitor_elo = team_elos[(visitor_team, year)]


        # Calculate Elo change
        delta = elo_change(home_elo+100, visitor_elo, margin)
        # Update Elo for next game
        team_elos[(home_team, year)] += delta
        team_elos[(visitor_team, year)] -= delta
    # print(team_elos)
    return team_elos