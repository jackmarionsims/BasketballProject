from typing import Annotated, Optional
from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field, AfterValidator

import pandas as pd

app = FastAPI()

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
    day: int

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


def get_home_filter(
    pts_min: Optional[int] = Query(None, alias="home_pts_min"),
    pts_max: Optional[int] = Query(None, alias="home_pts_max"),
    ast_min: Optional[int] = Query(None, alias="home_ast_min"),
    ast_max: Optional[int] = Query(None, alias="home_ast_max"),
    trb_min: Optional[int] = Query(None, alias="home_trb_min"),
    trb_max: Optional[int] = Query(None, alias="home_trb_max"),
    orb_min: Optional[int] = Query(None, alias="home_orb_min"),
    orb_max: Optional[int] = Query(None, alias="home_orb_max"),
    drb_min: Optional[int] = Query(None, alias="home_drb_min"),
    drb_max: Optional[int] = Query(None, alias="home_drb_max"),
    blk_min: Optional[int] = Query(None, alias="home_blk_min"),
    blk_max: Optional[int] = Query(None, alias="home_blk_max"),
    stl_min: Optional[int] = Query(None, alias="home_stl_min"),
    stl_max: Optional[int] = Query(None, alias="home_stl_max"),
    fga_min: Optional[int] = Query(None, alias="home_fga_min"),
    fga_max: Optional[int] = Query(None, alias="home_fga_max"),
    fgm_min: Optional[int] = Query(None, alias="home_fgm_min"),
    fgm_max: Optional[int] = Query(None, alias="home_fgm_max"),
    fg_pct_min: Optional[float] = Query(None, alias="home_fg_pct_min"),
    fg_pct_max: Optional[float] = Query(None, alias="home_fg_pct_max"),
    tpa_min: Optional[int] = Query(None, alias="home_3pa_min"),
    tpa_max: Optional[int] = Query(None, alias="home_3pa_max"),
    tpm_min: Optional[int] = Query(None, alias="home_3pm_min"),
    tpm_max: Optional[int] = Query(None, alias="home_3pm_max"),
    tp_pct_min: Optional[float] = Query(None, alias="home_3pct_min"),
    tp_pct_max: Optional[float] = Query(None, alias="home_3pct_max"),
    fta_min: Optional[int] = Query(None, alias="home_fta_min"),
    fta_max: Optional[int] = Query(None, alias="home_fta_max"),
    ftm_min: Optional[int] = Query(None, alias="home_ftm_min"),
    ftm_max: Optional[int] = Query(None, alias="home_ftm_max"),
    ft_pct_min: Optional[float] = Query(None, alias="home_ft_pct_min"),
    ft_pct_max: Optional[float] = Query(None, alias="home_ft_pct_max"),
    fouls_min: Optional[int] = Query(None, alias="home_fouls_min"),
    fouls_max: Optional[int] = Query(None, alias="home_fouls_max"),
    to_min: Optional[int] = Query(None, alias="home_to_min"),
    to_max: Optional[int] = Query(None, alias="home_to_max")
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


def get_visitor_filter(
    pts_min: Optional[int] = Query(None, alias="visitor_pts_min"),
    pts_max: Optional[int] = Query(None, alias="visitor_pts_max"),
    ast_min: Optional[int] = Query(None, alias="visitor_ast_min"),
    ast_max: Optional[int] = Query(None, alias="visitor_ast_max"),
    trb_min: Optional[int] = Query(None, alias="visitor_trb_min"),
    trb_max: Optional[int] = Query(None, alias="visitor_trb_max"),
    orb_min: Optional[int] = Query(None, alias="visitor_orb_min"),
    orb_max: Optional[int] = Query(None, alias="visitor_orb_max"),
    drb_min: Optional[int] = Query(None, alias="visitor_drb_min"),
    drb_max: Optional[int] = Query(None, alias="visitor_drb_max"),
    blk_min: Optional[int] = Query(None, alias="visitor_blk_min"),
    blk_max: Optional[int] = Query(None, alias="visitor_blk_max"),
    stl_min: Optional[int] = Query(None, alias="visitor_stl_min"),
    stl_max: Optional[int] = Query(None, alias="visitor_stl_max"),
    fga_min: Optional[int] = Query(None, alias="visitor_fga_min"),
    fga_max: Optional[int] = Query(None, alias="visitor_fga_max"),
    fgm_min: Optional[int] = Query(None, alias="visitor_fgm_min"),
    fgm_max: Optional[int] = Query(None, alias="visitor_fgm_max"),
    fg_pct_min: Optional[float] = Query(None, alias="visitor_fg_pct_min"),
    fg_pct_max: Optional[float] = Query(None, alias="visitor_fg_pct_max"),
    tpa_min: Optional[int] = Query(None, alias="visitor_3pa_min"),
    tpa_max: Optional[int] = Query(None, alias="visitor_3pa_max"),
    tpm_min: Optional[int] = Query(None, alias="visitor_3pm_min"),
    tpm_max: Optional[int] = Query(None, alias="visitor_3pm_max"),
    tp_pct_min: Optional[float] = Query(None, alias="visitor_3pct_min"),
    tp_pct_max: Optional[float] = Query(None, alias="visitor_3pct_max"),
    fta_min: Optional[int] = Query(None, alias="visitor_fta_min"),
    fta_max: Optional[int] = Query(None, alias="visitor_fta_max"),
    ftm_min: Optional[int] = Query(None, alias="visitor_ftm_min"),
    ftm_max: Optional[int] = Query(None, alias="visitor_ftm_max"),
    ft_pct_min: Optional[float] = Query(None, alias="visitor_ft_pct_min"),
    ft_pct_max: Optional[float] = Query(None, alias="visitor_ft_pct_max"),
    fouls_min: Optional[int] = Query(None, alias="visitor_fouls_min"),
    fouls_max: Optional[int] = Query(None, alias="visitor_fouls_max"),
    to_min: Optional[int] = Query(None, alias="visitor_to_min"),
    to_max: Optional[int] = Query(None, alias="visitor_to_max")
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

class NBATeam(BaseModel):
    name: NBAName
    
    # Basic ratings
    elo: float = Field(..., description="Current ELO rating of the team")
    wl: float = Field(..., description="Current W/L percentage of the team")
    
    # Points
    points_avg: int = Field(..., description="Average number of points by the team")
    opp_points_avg: int = Field(..., description="Average number of points given up by the team")
    
    # Assists
    assists_avg: int = Field(..., description="Average number of assists by the team")
    opp_assists_avg: int = Field(..., description="Average number of assists given up by the team")
    
    # Rebounds
    tot_rebounds_avg: int = Field(..., description="Average number of total rebounds by the team")
    opp_tot_rebounds_avg: int = Field(..., description="Average number of total rebounds given up by the team")
    off_rebounds_avg: int = Field(..., description="Average number of offensive rebounds by the team")
    opp_off_rebounds_avg: int = Field(..., description="Average number of offensive rebounds given up by the team")
    def_rebounds_avg: int = Field(..., description="Average number of defensive rebounds by the team")
    opp_def_rebounds_avg: int = Field(..., description="Average number of defensive rebounds given up by the team")
    
    # Blocks
    blocks_avg: int = Field(..., description="Average number of blocks by the team")
    opp_blocks_avg: int = Field(..., description="Average number of blocks given up by the team")
    
    # Steals
    steals_avg: int = Field(..., description="Average number of steals by the team")
    opp_steals_avg: int = Field(..., description="Average number of steals given up by the team")
    
    # Field Goals
    fga_avg: int = Field(..., description="Average number of field goals attempted by the team")
    opp_fga_avg: int = Field(..., description="Average number of field goals attempted against the team")
    fgm_avg: int = Field(..., description="Average number of field goals made by the team")
    opp_fgm_avg: int = Field(..., description="Average number of field goals made against the team")
    fg_pct_avg: float = Field(..., description="Average field goal percentage by the team")
    opp_fg_pct_avg: float = Field(..., description="Average field goal percentage allowed by the team")
    
    # Three Pointers
    three_pa_avg: int = Field(..., description="Average number of 3-point attempts by the team")
    opp_three_pa_avg: int = Field(..., description="Average number of 3-point attempts against the team")
    three_pm_avg: int = Field(..., description="Average number of 3-point makes by the team")
    opp_three_pm_avg: int = Field(..., description="Average number of 3-point makes against the team")
    three_pct_avg: float = Field(..., description="Average 3-point percentage by the team")
    opp_three_pct_avg: float = Field(..., description="Average 3-point percentage allowed by the team")
    
    # Free Throws
    fta_avg: int = Field(..., description="Average number of free throws attempted by the team")
    opp_fta_avg: int = Field(..., description="Average number of free throws attempted against the team")
    ftm_avg: int = Field(..., description="Average number of free throws made by the team")
    opp_ftm_avg: int = Field(..., description="Average number of free throws made against the team")
    ft_pct_avg: float = Field(..., description="Average free throw percentage by the team")
    opp_ft_pct_avg: float = Field(..., description="Average free throw percentage allowed by the team")
    
    # Fouls
    fouls_avg: int = Field(..., description="Average number of fouls committed by the team")
    opp_fouls_avg: int = Field(..., description="Average number of fouls committed by the opponent")
    
    # Turnovers
    turnovers_avg: int = Field(..., description="Average number of turnovers by the team")
    opp_turnovers_avg: int = Field(..., description="Average number of turnovers forced by the team")



class BoxScore(BaseModel):
    # Points
    home_points: int = Field(..., description="Number of points by the home team")
    visitor_points: int = Field(..., description="Number of points by the visiting team")
    
    # Assists
    home_assists: int = Field(..., description="Number of assists by the home team")
    visitor_assists: int = Field(..., description="Number of assists by the visiting team")
    
    # Rebounds
    home_tot_rebounds: int = Field(..., description="Total rebounds by the home team")
    visitor_tot_rebounds: int = Field(..., description="Total rebounds by the visiting team")
    home_off_rebounds: int = Field(..., description="Offensive rebounds by the home team")
    visitor_off_rebounds: int = Field(..., description="Offensive rebounds by the visiting team")
    home_def_rebounds: int = Field(..., description="Defensive rebounds by the home team")
    visitor_def_rebounds: int = Field(..., description="Defensive rebounds by the visiting team")
    
    # Blocks & Steals
    home_blocks: int = Field(..., description="Blocks by the home team")
    visitor_blocks: int = Field(..., description="Blocks by the visiting team")
    home_steals: int = Field(..., description="Steals by the home team")
    visitor_steals: int = Field(..., description="Steals by the visiting team")
    
    # Field Goals
    home_fga: int = Field(..., description="Field goals attempted by the home team")
    visitor_fga: int = Field(..., description="Field goals attempted by the visiting team")
    home_fgm: int = Field(..., description="Field goals made by the home team")
    visitor_fgm: int = Field(..., description="Field goals made by the visiting team")
    home_fg_pct: float = Field(..., description="Field goal percentage for the home team")
    visitor_fg_pct: float = Field(..., description="Field goal percentage for the visiting team")
    
    # Three Pointers
    home_3pa: int = Field(..., description="Three-pointers attempted by the home team")
    visitor_3pa: int = Field(..., description="Three-pointers attempted by the visiting team")
    home_3pm: int = Field(..., description="Three-pointers made by the home team")
    visitor_3pm: int = Field(..., description="Three-pointers made by the visiting team")
    home_3p_pct: float = Field(..., description="Three-point percentage for the home team")
    visitor_3p_pct: float = Field(..., description="Three-point percentage for the visiting team")
    
    # Free Throws
    home_fta: int = Field(..., description="Free throws attempted by the home team")
    visitor_fta: int = Field(..., description="Free throws attempted by the visiting team")
    home_ftm: int = Field(..., description="Free throws made by the home team")
    visitor_ftm: int = Field(..., description="Free throws made by the visiting team")
    home_ft_pct: float = Field(..., description="Free throw percentage for the home team")
    visitor_ft_pct: float = Field(..., description="Free throw percentage for the visiting team")
    
    # Fouls & Turnovers
    home_fouls: int = Field(..., description="Personal fouls by the home team")
    visitor_fouls: int = Field(..., description="Personal fouls by the visiting team")
    home_to: int = Field(..., description="Turnovers by the home team")
    visitor_to: int = Field(..., description="Turnovers by the visiting team")

    def to_row(self) -> pd.Series:
        return pd.Series({
            # "Home Team": self.home.value,
            # "Visitor Team": self.visitor.value,
            # Points
            "Home Team Points": self.home_points,
            "Visitor Team Points": self.visitor_points,

            # Assists
            "Home Team Assists": self.home_assists,
            "Visitor Team Assists": self.visitor_assists,

            # Rebounds
            "Home Team Tot Rebounds": self.home_tot_rebounds,
            "Visitor Team Tot Rebounds": self.visitor_tot_rebounds,
            "Home Team Off Rebounds": self.home_off_rebounds,
            "Visitor Team Off Rebounds": self.visitor_off_rebounds,
            "Home Team Def Rebounds": self.home_def_rebounds,
            "Visitor Team Def Rebounds": self.visitor_def_rebounds,

            # Blocks & Steals
            "Home Team Blocks": self.home_blocks,
            "Visitor Team Blocks": self.visitor_blocks,
            "Home Team Steals": self.home_steals,
            "Visitor Team Steals": self.visitor_steals,

            # Field Goals
            "Home Team FGA": self.home_fga,
            "Visitor Team FGA": self.visitor_fga,
            "Home Team FGM": self.home_fgm,
            "Visitor Team FGM": self.visitor_fgm,
            "Home Team FG%": self.home_fg_pct,
            "Visitor Team FG%": self.visitor_fg_pct,

            # Three Pointers
            "Home Team 3PA": self.home_3pa,
            "Visitor Team 3PA": self.visitor_3pa,
            "Home Team 3PM": self.home_3pm,
            "Visitor Team 3PM": self.visitor_3pm,
            "Home Team 3P%": self.home_3p_pct,
            "Visitor Team 3P%": self.visitor_3p_pct,

            # Free Throws
            "Home Team FTA": self.home_fta,
            "Visitor Team FTA": self.visitor_fta,
            "Home Team FTM": self.home_ftm,
            "Visitor Team FTM": self.visitor_ftm,
            "Home Team FT%": self.home_ft_pct,
            "Visitor Team FT%": self.visitor_ft_pct,

            # Fouls & Turnovers
            "Home Team Fouls": self.home_fouls,
            "Visitor Team Fouls": self.visitor_fouls,
            "Home Team TO": self.home_to,
            "Visitor Team TO": self.visitor_to
        })

class GameBase(BaseModel):
    home: NBATeam
    visitor: NBATeam
    # date: Date

    def to_row(self) -> pd.Series:
        row = {}
        home_team = self.home
        visitor_team = self.visitor
        # Home team fields
        row["Home Team"] = home_team.name.value
        row["Home Team Home ELO"] = home_team.elo
        row["Home Team W/L%"] = home_team.wl
        row["Home Team Points Avg"] = home_team.points_avg
        row["Home Team Opp Points Avg"] = home_team.opp_points_avg
        row["Home Team Assists Avg"] = home_team.assists_avg
        row["Home Team Opp Assists Avg"] = home_team.opp_assists_avg
        row["Home Team Tot Rebounds Avg"] = home_team.tot_rebounds_avg
        row["Home Team Opp Tot Rebounds Avg"] = home_team.opp_tot_rebounds_avg
        row["Home Team Off Rebounds Avg"] = home_team.off_rebounds_avg
        row["Home Team Opp Off Rebounds Avg"] = home_team.opp_off_rebounds_avg
        row["Home Team Def Rebounds Avg"] = home_team.def_rebounds_avg
        row["Home Team Opp Def Rebounds Avg"] = home_team.opp_def_rebounds_avg
        row["Home Team Blocks Avg"] = home_team.blocks_avg
        row["Home Team Opp Blocks Avg"] = home_team.opp_blocks_avg
        row["Home Team Steals Avg"] = home_team.steals_avg
        row["Home Team Opp Steals Avg"] = home_team.opp_steals_avg
        row["Home Team FGA Avg"] = home_team.fga_avg
        row["Home Team Opp FGA Avg"] = home_team.opp_fga_avg
        row["Home Team FGM Avg"] = home_team.fgm_avg
        row["Home Team Opp FGM Avg"] = home_team.opp_fgm_avg
        row["Home Team FG% Avg"] = home_team.fg_pct_avg
        row["Home Team Opp FG% Avg"] = home_team.opp_fg_pct_avg
        row["Home Team 3PA Avg"] = home_team.three_pa_avg
        row["Home Team Opp 3PA Avg"] = home_team.opp_three_pa_avg
        row["Home Team 3PM Avg"] = home_team.three_pm_avg
        row["Home Team Opp 3PM Avg"] = home_team.opp_three_pm_avg
        row["Home Team 3P% Avg"] = home_team.three_pct_avg
        row["Home Team Opp 3P% Avg"] = home_team.opp_three_pct_avg
        row["Home Team FTA Avg"] = home_team.fta_avg
        row["Home Team Opp FTA Avg"] = home_team.opp_fta_avg
        row["Home Team FTM Avg"] = home_team.ftm_avg
        row["Home Team Opp FTM Avg"] = home_team.opp_ftm_avg
        row["Home Team FT% Avg"] = home_team.ft_pct_avg
        row["Home Team Opp FT% Avg"] = home_team.opp_ft_pct_avg
        row["Home Team Fouls Avg"] = home_team.fouls_avg
        row["Home Team Opp Fouls Avg"] = home_team.opp_fouls_avg
        row["Home Team TO Avg"] = home_team.turnovers_avg
        row["Home Team Opp TO Avg"] = home_team.opp_turnovers_avg

        # Visitor team fields
        row["Visitor Team"] = visitor_team.name.value
        row["Visitor Team ELO"] = visitor_team.elo
        row["Visitor Team W/L%"] = visitor_team.wl
        row["Visitor Team Points Avg"] = visitor_team.points_avg
        row["Visitor Team Opp Points Avg"] = visitor_team.opp_points_avg
        row["Visitor Team Assists Avg"] = visitor_team.assists_avg
        row["Visitor Team Opp Assists Avg"] = visitor_team.opp_assists_avg
        row["Visitor Team Tot Rebounds Avg"] = visitor_team.tot_rebounds_avg
        row["Visitor Team Opp Tot Rebounds Avg"] = visitor_team.opp_tot_rebounds_avg
        row["Visitor Team Off Rebounds Avg"] = visitor_team.off_rebounds_avg
        row["Visitor Team Opp Off Rebounds Avg"] = visitor_team.opp_off_rebounds_avg
        row["Visitor Team Def Rebounds Avg"] = visitor_team.def_rebounds_avg
        row["Visitor Team Opp Def Rebounds Avg"] = visitor_team.opp_def_rebounds_avg
        row["Visitor Team Blocks Avg"] = visitor_team.blocks_avg
        row["Visitor Team Opp Blocks Avg"] = visitor_team.opp_blocks_avg
        row["Visitor Team Steals Avg"] = visitor_team.steals_avg
        row["Visitor Team Opp Steals Avg"] = visitor_team.opp_steals_avg
        row["Visitor Team FGA Avg"] = visitor_team.fga_avg
        row["Visitor Team Opp FGA Avg"] = visitor_team.opp_fga_avg
        row["Visitor Team FGM Avg"] = visitor_team.fgm_avg
        row["Visitor Team Opp FGM Avg"] = visitor_team.opp_fgm_avg
        row["Visitor Team FG% Avg"] = visitor_team.fg_pct_avg
        row["Visitor Team Opp FG% Avg"] = visitor_team.opp_fg_pct_avg
        row["Visitor Team 3PA Avg"] = visitor_team.three_pa_avg
        row["Visitor Team Opp 3PA Avg"] = visitor_team.opp_three_pa_avg
        row["Visitor Team 3PM Avg"] = visitor_team.three_pm_avg
        row["Visitor Team Opp 3PM Avg"] = visitor_team.opp_three_pm_avg
        row["Visitor Team 3P% Avg"] = visitor_team.three_pct_avg
        row["Visitor Team Opp 3P% Avg"] = visitor_team.opp_three_pct_avg
        row["Visitor Team FTA Avg"] = visitor_team.fta_avg
        row["Visitor Team Opp FTA Avg"] = visitor_team.opp_fta_avg
        row["Visitor Team FTM Avg"] = visitor_team.ftm_avg
        row["Visitor Team Opp FTM Avg"] = visitor_team.opp_ftm_avg
        row["Visitor Team FT% Avg"] = visitor_team.ft_pct_avg
        row["Visitor Team Opp FT% Avg"] = visitor_team.opp_ft_pct_avg
        row["Visitor Team Fouls Avg"] = visitor_team.fouls_avg
        row["Visitor Team Opp Fouls Avg"] = visitor_team.opp_fouls_avg
        row["Visitor Team TO Avg"] = visitor_team.turnovers_avg
        row["Visitor Team Opp TO Avg"] = visitor_team.opp_turnovers_avg

        return pd.Series(row)

class FinishedGame(BaseModel):
    game_base: GameBase
    box_score: BoxScore

    def to_row(self):
        # Convert both the box score and the game averages to Series
        box_score_row = self.box_score.to_row()
        game_row = self.game_base.to_row()

        # Concatenate into a single row (Series)
        combined_row = pd.concat([game_row, box_score_row])

        return combined_row

# class UpcomingGame(GameBase):
#     elo_diff: float = Field(..., description="Current ELO difference of the teams")
#     wl_diff: float = Field(..., description="Current W/L percentage difference of the teams")
#     visitor_wl: float = Field(..., description="Current W/L percentage of the visiting team")
#     home_points_avg: int = Field(..., description="Average number of points by the home team")
#     visitor_points_avg: int = Field(..., description="Average number of points by the visiting team")
#     home_assists_avg: int = Field(..., description="Average number of assists by the home team")
#     visitor_assists_avg: int = Field(..., description="Average number of assists by the visiting team")
#     home_tot_rebounds_avg: int = Field(..., description="Average number of total rebounds by the home team")
#     visitor_tot_rebounds_avg: int = Field(..., description="Average number of total rebounds by the visiting team")
#     home_off_rebounds_avg: int = Field(..., description="Average number of offensive rebounds by the home team")
#     visitor_off_rebounds_avg: int = Field(..., description="Average number of offensive rebounds by the visiting team")
#     home_def_rebounds_avg: int = Field(..., description="Average number of defensive rebounds by the home team")
#     visitor_def_rebounds_avg: int = Field(..., description="Average number of defensive rebounds by the visiting team")


def check_is_valid_row(row: pd.Series):
    assert isinstance(row, pd.Series), "Input must be a pandas DataFrame"
    # columns = list(row.columns)
    # required = ['Visitor Team', 'Visitor Team Points', 'Home Team', 'Home Team Points',
    #             'Home Team Assists', 'Home Team Tot Rebounds', 'Home Team Off Rebounds', 'Home Team Def Rebounds', 'Visitor Team Assists', 'Visitor Team Tot Rebounds', 'Visitor Team Off Rebounds', 'Visitor Team Def Rebounds']
    # for col in required:
    #     assert col in columns
    try:
        home_team=NBAName(row["Home Team"])
        visitor_team=NBAName(row["Visitor Team"])
    except ValueError as e:
        raise ValueError(f"Invalid team name in row: {e}")

def row_to_box_score(
    row: Annotated[pd.Series, AfterValidator(check_is_valid_row)]
) -> BoxScore:
    home_stats = GameStats(
        elo=row["Home Team ELO"],
        wins=row["Home Team W"],
        points=row["Home Team Points"],
        assists=row["Home Team Assists"],
        tot_rebounds=row["Home Team Tot Rebounds"],
        off_rebounds=row["Home Team Off Rebounds"],
        def_rebounds=row["Home Team Def Rebounds"],
        blocks=row["Home Team Blocks"],
        steals=row["Home Team Steals"],
        fga=row["Home Team FGA"],
        fgm=row["Home Team FGM"],
        fg_pct=row["Home Team FG%"],
        three_pa=row["Home Team 3PA"],
        three_pm=row["Home Team 3PM"],
        three_pct=row["Home Team 3P%"],
        fta=row["Home Team FTA"],
        ftm=row["Home Team FTM"],
        ft_pct=row["Home Team FT%"],
        fouls=row["Home Team Fouls"],
        turnovers=row["Home Team TO"],
    )

    visitor_stats = GameStats(
        elo=row["Visitor Team ELO"],
        wins=row["Visitor Team W"],
        points=row["Visitor Team Points"],
        assists=row["Visitor Team Assists"],
        tot_rebounds=row["Visitor Team Tot Rebounds"],
        off_rebounds=row["Visitor Team Off Rebounds"],
        def_rebounds=row["Visitor Team Def Rebounds"],
        blocks=row["Visitor Team Blocks"],
        steals=row["Visitor Team Steals"],
        fga=row["Visitor Team FGA"],
        fgm=row["Visitor Team FGM"],
        fg_pct=row["Visitor Team FG%"],
        three_pa=row["Visitor Team 3PA"],
        three_pm=row["Visitor Team 3PM"],
        three_pct=row["Visitor Team 3P%"],
        fta=row["Visitor Team FTA"],
        ftm=row["Visitor Team FTM"],
        ft_pct=row["Visitor Team FT%"],
        fouls=row["Visitor Team Fouls"],
        turnovers=row["Visitor Team TO"],
    )

    return BoxScore(
        id=row["Game ID"],
        home=NBAName(row["Home Team"]),
        visitor=NBAName(row["Visitor Team"]),
        home_stats=home_stats,
        visitor_stats=visitor_stats,
    )



def row_to_game(row: pd.Series) -> GameBase:
    """
    Given a row from the dataset, return two NBATeam objects:
    one for the home team and one for the visitor team.
    """
    # Create home team NBATeam
    home_team = NBATeam(
        name=NBAName(row["Home Team"]),
        elo=row["Home Team Home ELO"],
        wl=row["Home Team W/L%"],
        points_avg=row["Home Team Points Avg"],
        opp_points_avg=row["Home Team Opp Points Avg"],
        assists_avg=row["Home Team Assists Avg"],
        opp_assists_avg=row["Home Team Opp Assists Avg"],
        tot_rebounds_avg=row["Home Team Tot Rebounds Avg"],
        opp_tot_rebounds_avg=row["Home Team Opp Tot Rebounds Avg"],
        off_rebounds_avg=row["Home Team Off Rebounds Avg"],
        opp_off_rebounds_avg=row["Home Team Opp Off Rebounds Avg"],
        def_rebounds_avg=row["Home Team Def Rebounds Avg"],
        opp_def_rebounds_avg=row["Home Team Opp Def Rebounds Avg"],
        blocks_avg=row["Home Team Blocks Avg"],
        opp_blocks_avg=row["Home Team Opp Blocks Avg"],
        steals_avg=row["Home Team Steals Avg"],
        opp_steals_avg=row["Home Team Opp Steals Avg"],
        fga_avg=row["Home Team FGA Avg"],
        opp_fga_avg=row["Home Team Opp FGA Avg"],
        fgm_avg=row["Home Team FGM Avg"],
        opp_fgm_avg=row["Home Team Opp FGM Avg"],
        fg_pct_avg=row["Home Team FG% Avg"],
        opp_fg_pct_avg=row["Home Team Opp FG% Avg"],
        three_pa_avg=row["Home Team 3PA Avg"],
        opp_three_pa_avg=row["Home Team Opp 3PA Avg"],
        three_pm_avg=row["Home Team 3PM Avg"],
        opp_three_pm_avg=row["Home Team Opp 3PM Avg"],
        three_pct_avg=row["Home Team 3P% Avg"],
        opp_three_pct_avg=row["Home Team Opp 3P% Avg"],
        fta_avg=row["Home Team FTA Avg"],
        opp_fta_avg=row["Home Team Opp FTA Avg"],
        ftm_avg=row["Home Team FTM Avg"],
        opp_ftm_avg=row["Home Team Opp FTM Avg"],
        ft_pct_avg=row["Home Team FT% Avg"],
        opp_ft_pct_avg=row["Home Team Opp FT% Avg"],
        fouls_avg=row["Home Team Fouls Avg"],
        opp_fouls_avg=row["Home Team Opp Fouls Avg"],
        turnovers_avg=row["Home Team TO Avg"],
        opp_turnovers_avg=row["Home Team Opp TO Avg"]
    )

    # Create visitor team NBATeam
    visitor_team = NBATeam(
        name=NBAName(row["Visitor Team"]),
        elo=row["Visitor Team ELO"],
        wl=row["Visitor Team W/L%"],
        points_avg=row["Visitor Team Points Avg"],
        opp_points_avg=row["Visitor Team Opp Points Avg"],
        assists_avg=row["Visitor Team Assists Avg"],
        opp_assists_avg=row["Visitor Team Opp Assists Avg"],
        tot_rebounds_avg=row["Visitor Team Tot Rebounds Avg"],
        opp_tot_rebounds_avg=row["Visitor Team Opp Tot Rebounds Avg"],
        off_rebounds_avg=row["Visitor Team Off Rebounds Avg"],
        opp_off_rebounds_avg=row["Visitor Team Opp Off Rebounds Avg"],
        def_rebounds_avg=row["Visitor Team Def Rebounds Avg"],
        opp_def_rebounds_avg=row["Visitor Team Opp Def Rebounds Avg"],
        blocks_avg=row["Visitor Team Blocks Avg"],
        opp_blocks_avg=row["Visitor Team Opp Blocks Avg"],
        steals_avg=row["Visitor Team Steals Avg"],
        opp_steals_avg=row["Visitor Team Opp Steals Avg"],
        fga_avg=row["Visitor Team FGA Avg"],
        opp_fga_avg=row["Visitor Team Opp FGA Avg"],
        fgm_avg=row["Visitor Team FGM Avg"],
        opp_fgm_avg=row["Visitor Team Opp FGM Avg"],
        fg_pct_avg=row["Visitor Team FG% Avg"],
        opp_fg_pct_avg=row["Visitor Team Opp FG% Avg"],
        three_pa_avg=row["Visitor Team 3PA Avg"],
        opp_three_pa_avg=row["Visitor Team Opp 3PA Avg"],
        three_pm_avg=row["Visitor Team 3PM Avg"],
        opp_three_pm_avg=row["Visitor Team Opp 3PM Avg"],
        three_pct_avg=row["Visitor Team 3P% Avg"],
        opp_three_pct_avg=row["Visitor Team Opp 3P% Avg"],
        fta_avg=row["Visitor Team FTA Avg"],
        opp_fta_avg=row["Visitor Team Opp FTA Avg"],
        ftm_avg=row["Visitor Team FTM Avg"],
        opp_ftm_avg=row["Visitor Team Opp FTM Avg"],
        ft_pct_avg=row["Visitor Team FT% Avg"],
        opp_ft_pct_avg=row["Visitor Team Opp FT% Avg"],
        fouls_avg=row["Visitor Team Fouls Avg"],
        opp_fouls_avg=row["Visitor Team Opp Fouls Avg"],
        turnovers_avg=row["Visitor Team TO Avg"],
        opp_turnovers_avg=row["Visitor Team Opp TO Avg"]
    )
    return GameBase(home=home_team, visitor=visitor_team)

def row_to_finished_game(row: pd.Series) -> FinishedGame:
    box_score = row_to_box_score(row)
    game_base = row_to_game(row)
    return FinishedGame(game_base=game_base, box_score=box_score)

def finish_game(game: GameBase, box_score: BoxScore):
    pass

def add_margin_features(df: pd.DataFrame, stat_names: list[str]) -> pd.DataFrame:
    """
    Adds both margin differences and separate for/against differences 
    for a list of stats.

    Parameters:
        df (pd.DataFrame): Must contain columns in the format:
            'Home Team {stat} Avg', 'Home Team Opp {stat} Avg',
            'Visitor Team {stat} Avg', 'Visitor Team Opp {stat} Avg'
        stat_names (list): List of stat names (e.g. ['Assists', 'Tot Rebounds'])

    Returns:
        pd.DataFrame: Original df with new features added
    """
    for stat in stat_names:
        # Create team-level margins
        df[f"Home {stat} Margin"] = df[f"Home Team {stat} Avg"] - df[f"Home Team Opp {stat} Avg"]
        df[f"Visitor {stat} Margin"] = df[f"Visitor Team {stat} Avg"] - df[f"Visitor Team Opp {stat} Avg"]
        
        # Difference in margins
        df[f"{stat} Margin Diff"] = df[f"Home {stat} Margin"] - df[f"Visitor {stat} Margin"]

        # Separate for/against differences
        df[f"{stat} Diff"] = df[f"Home Team {stat} Avg"] - df[f"Visitor Team {stat} Avg"]
        df[f"Opp {stat} Diff"] = df[f"Home Team Opp {stat} Avg"] - df[f"Visitor Team Opp {stat} Avg"]

    return df

def add_z_scores(df: pd.DataFrame,  stat_names: list[str]) -> pd.DataFrame:
    # Calculate means and stds grouped by year
    means_by_year = df.groupby("Year")[stat_names].mean().reset_index()
    stds_by_year = df.groupby("Year")[stat_names].std().reset_index()

    # Merge means and stds back into the main DataFrame
    df = df.merge(means_by_year, on="Year", suffixes=("", "_mean"))
    df = df.merge(stds_by_year, on="Year", suffixes=("", "_std"))

    # Compute z-scores
    for col in stat_names:
        mean_col = f"{col}_mean"
        std_col = f"{col}_std"
        z_col = f"{col} Z-Score"
        df[z_col] = (df[col] - df[mean_col]) / df[std_col]
    return df

def df_to_teams(df: pd.DataFrame) -> dict[NBAName, NewTeam]:
    teams: dict[NBAName, NewTeam] = {}

    # Preload arrays for speed
    game_ids = df["Game ID"].to_numpy()
    years = df["Year"].to_numpy()

    home_names = df["Home Team"].to_numpy()
    visitor_names = df["Visitor Team"].to_numpy()

    # Column groups for stats
    home_cols = [
        "Home Team ELO", "Home Team W", "Home Team Points",
        "Home Team Assists", "Home Team Tot Rebounds", "Home Team Off Rebounds",
        "Home Team Def Rebounds", "Home Team Blocks", "Home Team Steals",
        "Home Team FGA", "Home Team FGM", "Home Team FG%",
        "Home Team 3PA", "Home Team 3PM", "Home Team 3P%",
        "Home Team FTA", "Home Team FTM", "Home Team FT%",
        "Home Team Fouls", "Home Team TO"
    ]
    visitor_cols = [
        "Visitor Team ELO", "Visitor Team W", "Visitor Team Points",
        "Visitor Team Assists", "Visitor Team Tot Rebounds", "Visitor Team Off Rebounds",
        "Visitor Team Def Rebounds", "Visitor Team Blocks", "Visitor Team Steals",
        "Visitor Team FGA", "Visitor Team FGM", "Visitor Team FG%",
        "Visitor Team 3PA", "Visitor Team 3PM", "Visitor Team 3P%",
        "Visitor Team FTA", "Visitor Team FTM", "Visitor Team FT%",
        "Visitor Team Fouls", "Visitor Team TO"
    ]

    # Preload all stat arrays for home & visitor
    home_stats_arr = df[home_cols].to_numpy()
    visitor_stats_arr = df[visitor_cols].to_numpy()

    for i in range(len(df)):
        game_id = int(game_ids[i])
        year = int(years[i])

        # Create GameStats for home team
        home_stats = GameStats(
            elo=home_stats_arr[i][0],
            wins=home_stats_arr[i][1],
            points=home_stats_arr[i][2],
            assists=home_stats_arr[i][3],
            tot_rebounds=home_stats_arr[i][4],
            off_rebounds=home_stats_arr[i][5],
            def_rebounds=home_stats_arr[i][6],
            blocks=home_stats_arr[i][7],
            steals=home_stats_arr[i][8],
            fga=home_stats_arr[i][9],
            fgm=home_stats_arr[i][10],
            fg_pct=home_stats_arr[i][11],
            three_pa=home_stats_arr[i][12],
            three_pm=home_stats_arr[i][13],
            three_pct=home_stats_arr[i][14],
            fta=home_stats_arr[i][15],
            ftm=home_stats_arr[i][16],
            ft_pct=home_stats_arr[i][17],
            fouls=home_stats_arr[i][18],
            turnovers=home_stats_arr[i][19],
        )

        # Create GameStats for visitor team
        visitor_stats = GameStats(
            elo=visitor_stats_arr[i][0],
            wins=visitor_stats_arr[i][1],
            points=visitor_stats_arr[i][2],
            assists=visitor_stats_arr[i][3],
            tot_rebounds=visitor_stats_arr[i][4],
            off_rebounds=visitor_stats_arr[i][5],
            def_rebounds=visitor_stats_arr[i][6],
            blocks=visitor_stats_arr[i][7],
            steals=visitor_stats_arr[i][8],
            fga=visitor_stats_arr[i][9],
            fgm=visitor_stats_arr[i][10],
            fg_pct=visitor_stats_arr[i][11],
            three_pa=visitor_stats_arr[i][12],
            three_pm=visitor_stats_arr[i][13],
            three_pct=visitor_stats_arr[i][14],
            fta=visitor_stats_arr[i][15],
            ftm=visitor_stats_arr[i][16],
            ft_pct=visitor_stats_arr[i][17],
            fouls=visitor_stats_arr[i][18],
            turnovers=visitor_stats_arr[i][19],
        )

        # Home team entry
        home_name = NBAName(home_names[i])
        if home_name not in teams:
            teams[home_name] = NewTeam(name=home_name, stats=[])
        home_team = teams[home_name]
        home_season = next((s for s in home_team.stats if s.year == year), None)
        if home_season is None:
            home_season = SeasonStats(year=year)
            home_team.stats.append(home_season)
        home_season.add_game_stats(game_id, (home_stats, visitor_stats))

        # Visitor team entry
        visitor_name = NBAName(visitor_names[i])
        if visitor_name not in teams:
            teams[visitor_name] = NewTeam(name=visitor_name, stats=[])
        visitor_team = teams[visitor_name]
        visitor_season = next((s for s in visitor_team.stats if s.year == year), None)
        if visitor_season is None:
            visitor_season = SeasonStats(year=year)
            visitor_team.stats.append(visitor_season)
        visitor_season.add_game_stats(game_id, (visitor_stats, home_stats))

    return teams