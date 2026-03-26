from datetime import datetime
import pandas as pd
from classes2 import NBAName, NBATeam, Date, TEAM_RENAMES


abbrev_df = pd.read_csv("csvs/abbrevs.csv")
NAME_TO_ABBR = dict(zip(abbrev_df["Name"], abbrev_df["Abbreviation"]))
CACHE_VERSION = 1
ALL_TEAMS = {}
SCHEDULED_GAMES = pd.DataFrame()

'''
Calculations or Conversions
'''

def date_to_date(date_str: str):
     dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
     date_str = dt.strftime("%a, %b %d, %Y")
     return date_str

def date_to_num(date_str: str) -> int:
    """
    Convert a datetime string to a unique integer for that calendar day.
    Example: "Tue, Oct 21, 2025" -> 739372
    """
    #print(date_str)
    dt = datetime.strptime(date_str, "%a, %b %d, %Y")
    return dt.date().toordinal()

def date_to_num2(date_str: str) -> int:
    """
    Convert a datetime string to a unique integer for that calendar day.
    Example: "2025-06-22 20:00:00" -> 739372
    """
    # Parse string into datetime
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # Convert to unique day number
    return dt.date().toordinal()

def date_to_id(home, date):
    dt = datetime.strptime(date, "%a, %b %d, %Y")
    date_str = dt.strftime("%Y%m%d")
    team_abbr = NAME_TO_ABBR[home]
    return f"{date_str}0{team_abbr}"

def date_to_id2(home, date):
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_str = dt.strftime("%Y%m%d")
    team_abbr = NAME_TO_ABBR[home]
    return f"{date_str}0{team_abbr}"

def elo_change(home_elo, visitor_elo, margin, k=20):
    expected_home = 1 / (1 + 10 ** ((visitor_elo - home_elo) / 400))
    score = 1 if margin > 0 else 0
    elo_diff = home_elo - visitor_elo
    if margin < 0:
        margin = -margin
    mov_multiplier = ((margin + 3) ** 0.8) / (7.5 + 0.006 * elo_diff)
    # mov_multiplier = min(mov_multiplier, 2)
    return k * mov_multiplier * (score - expected_home)


'''
DataFrame Modifiers
'''
def calculate_avgs_for_team(df, nba_name: NBAName, season):
    team_name = nba_name.value
    nba_team = ALL_TEAMS[season][nba_name]

    #handle percentages differently
    cols = [
        'PTS', 'AST', 'TRB', 'ORB', 
        'DRB', 'BLK', 'STL', 
        'FGA', 'FG', '3PA', 
        '3P', 'FTA', 'FT', 
        'PF', 'TOV'
    ]
    # next = "ORB%", "TO%", "FTM/FGA", "TS%"
    season_games = df[df["Season"] == season]
    home_games = season_games[season_games["Home Team"] == team_name]
    visitor_games = season_games[season_games["Visitor Team"] == team_name]
    for stat_col in cols:
        home_stat_dict = {"total": 0, "opp total": 0, "games": 0}
        visitor_stat_dict = {"total": 0, "opp total": 0, "games": 0}

        #home calculations
        for idx, row in home_games.iterrows():
            stat = row.get(f"Home Team {stat_col}", None)
            opp_stat = row.get(f"Visitor Team {stat_col}", None)

            if pd.notna(stat):
                home_stat_dict["total"] += stat

            if pd.notna(opp_stat):
                home_stat_dict["opp total"] += opp_stat
            
            home_stat_dict["games"] += 1

        #visitor calculations
        for idx, row in visitor_games.iterrows():
            stat = row.get(f"Visitor Team {stat_col}", None)
            opp_stat = row.get(f"Home Team {stat_col}", None)

            if pd.notna(stat):
                visitor_stat_dict["total"] += stat
            if pd.notna(opp_stat):
                visitor_stat_dict["opp total"] += opp_stat
            
            visitor_stat_dict["games"] += 1


        #setting variables of NBATeam
        tot_games = home_stat_dict["games"] + visitor_stat_dict["games"]
        tot_stat = home_stat_dict["total"] + visitor_stat_dict["total"]
        tot_opp_stat = home_stat_dict["opp total"] + visitor_stat_dict["opp total"]

        nba_team.stats[f"Total {stat_col}"] = tot_stat
        nba_team.stats[f"Total Opp {stat_col}"] = tot_opp_stat

        nba_team.stats[f"Home Total {stat_col}"] = home_stat_dict["total"]
        nba_team.stats[f"Home Total Opp {stat_col}"] = home_stat_dict["opp total"]

        nba_team.stats[f"Visitor Total {stat_col}"] = visitor_stat_dict["total"]
        nba_team.stats[f"Visitor Total Opp {stat_col}"] = visitor_stat_dict["opp total"]

        # home_avg = (
        #     home_stat_dict["total"] / home_stat_dict["games"]
        #     if home_stat_dict["games"] > 0 else None
        # )
        # home_opp_avg = (
        #     home_stat_dict["opp total"] / home_stat_dict["games"]
        #     if home_stat_dict["games"] > 0 else None
        # )

        # visitor_avg = (
        #     visitor_stat_dict["total"] / visitor_stat_dict["games"]
        #     if visitor_stat_dict["games"] > 0 else None
        # )
        # visitor_opp_avg = (
        #     visitor_stat_dict["opp total"] / visitor_stat_dict["games"]
        #     if visitor_stat_dict["games"] > 0 else None
        # )

        # overall_avg = (
        #     tot_stat / tot_games
        #     if tot_games > 0 else None
        # )

        # overall_opp_avg = (
        #     tot_opp_stat / tot_games
        #     if tot_games > 0 else None
        # )

        # nba_team.stats[f"{stat_col} Avg"] = overall_avg
        # nba_team.stats[f"Opp {stat_col} Avg"] = overall_opp_avg

        # nba_team.stats[f"Home {stat_col} Avg"] = home_avg
        # nba_team.stats[f"Home Opp {stat_col} Avg"] = home_opp_avg

        # nba_team.stats[f"Visitor {stat_col} Avg"] = visitor_avg
        # nba_team.stats[f"Visitor Opp {stat_col} Avg"] = visitor_opp_avg




    #Win Loss Calculation
    home_wins = {"wins": 0, "games": 0}
    visitor_wins = {"wins": 0, "games": 0}

    #home calculations
    for idx, row in home_games.iterrows():
        win = row.get(f"Home Win", None)

        if pd.notna(win):
            home_wins["wins"] += win
            home_wins["games"] += 1

    #visitor calculations
    for idx, row in visitor_games.iterrows():
        loss = row.get(f"Home Win", None)

        if pd.notna(loss):
            visitor_wins["wins"] += (1-loss)
            visitor_wins["games"] += 1

    #setting variables of NBATeam
    tot_games = home_wins["games"] + visitor_wins["games"]
    tot_wins = home_wins["wins"] + visitor_wins["wins"]

    nba_team.stats[f"Total Games"] = tot_games
    nba_team.stats[f"Total Home Games"] = home_wins["games"]
    nba_team.stats[f"Total Visitor Games"] = visitor_wins["games"]

    nba_team.stats[f"W"] = tot_wins
    nba_team.stats[f"L"] = tot_games-tot_wins
    
    nba_team.stats[f"Home W"] = home_wins["wins"]
    nba_team.stats[f"Home L"] = home_wins["games"] - home_wins["wins"]
    nba_team.stats[f"Visitor W"] = visitor_wins["wins"]
    nba_team.stats[f"Visitor L"] = visitor_wins["games"] - visitor_wins["wins"]

    # home_wl = (
    #     home_wins["wins"] / home_wins["games"]
    #     if home_wins["games"] > 0 else None
    # )

    # visitor_wl = (
    #     visitor_wins["wins"] / visitor_wins["games"]
    #     if visitor_wins["games"] > 0 else None
    # )

    # overall_wl = (
    #     tot_stat / tot_games
    #     if tot_games > 0 else None
    # )

    # nba_team.stats[f"W/L%"] = overall_avg
    # nba_team.stats[f"Home W/L%"] = home_wl
    # nba_team.stats[f"Visitor W/L%"] = visitor_wl
    return None


def calculate_elos(df, season):
    cur_season = ALL_TEAMS[season]
    season_games = df[df["Season"] == season]
    for idx, game in season_games.iterrows():
        home = NBAName(game["Home Team"])
        visitor = NBAName(game["Visitor Team"])
        margin = game["Home Team PTS"] - game["Visitor Team PTS"]

        #for this to work must precalculate elo at start of season and only
        #call this function after creating
        home_prev = cur_season[home].elo
        visitor_prev = cur_season[visitor].elo

        delta = elo_change(home_prev+100, visitor_prev, margin)
        cur_season[home].elo = home_prev + delta
        cur_season[visitor].elo = visitor_prev - delta

def get_pregame_stats(home: NBATeam, visitor: NBATeam, date: str) -> pd.DataFrame:
    stat_cols = ['PTS', 'AST', 'TRB', 'ORB', 'DRB', 'BLK', 'STL', 
                 'FGA', 'FG', '3PA', '3P', 
                 'FTA', 'FT', 'PF', 'TOV']

    home_stats = home.stats
    visitor_stats = visitor.stats

    home_games = home_stats.get("Total Games", 0)
    visitor_games = visitor_stats.get("Total Games", 0)

    def avg(stats, col, games):
        return stats.get(f"Total {col}", 0.0) / games if games > 0 else 0.0
    
    def percentage(stats, col):
        return stats.get(f"Total {col}", 0.0) / stats.get(f"Total {col}A", 0.0) if stats.get(f"Total {col}A", 0.0) > 0 else 0.0

    # Build game ID
    game_id = date_to_id(home.name.value, date)
    team_abbr = NAME_TO_ABBR[home.name.value]

    row = {
        "Game ID": game_id, 
        "Home Team": home.name.value, 
        "Visitor Team": visitor.name.value,
        "Season": home.season,
        "Date": date,
        "Date Number": date_to_num(date)
    }

    for col in stat_cols:
        row[f"Home Team {col} Avg"]         = avg(home_stats,    col,    home_games)
        row[f"Visitor Team {col} Avg"]      = avg(visitor_stats, col,    visitor_games)
        row[f"Home Team Opp {col} Avg"]     = avg(home_stats,    f"Opp {col}", home_games)
        row[f"Visitor Team Opp {col} Avg"]  = avg(visitor_stats, f"Opp {col}", visitor_games)
        if col in ["FG", "3P", "FT"]:
            row[f"Home Team {col}% Avg"] = percentage(home_stats, col)
            row[f"Visitor Team {col}% Avg"] = percentage(visitor_stats, col)
            row[f"Home Team Opp {col}% Avg"] = percentage(home_stats, f"Opp {col}")
            row[f"Visitor Team Opp {col}% Avg"] = percentage(visitor_stats, f"Opp {col}")


    home_w  = home_stats.get("W", 0)
    home_l  = home_stats.get("L", 0)
    vis_w   = visitor_stats.get("W", 0)
    vis_l   = visitor_stats.get("L", 0)

    row.update({
        "Home Team ELO":            home.elo,
        "Visitor Team ELO":         visitor.elo,
        "Home Team Total Games":    home_games,
        "Home Team W":              home_w,
        "Home Team L":              home_l,
        "Home Team W/L%":           float(home_w / home_games) if home_games > 0 else 0.0,
        "Visitor Team Total Games": visitor_games,
        "Visitor Team W":           vis_w,
        "Visitor Team L":           vis_l,
        "Visitor Team W/L%":        float(vis_w / visitor_games) if visitor_games > 0 else 0.0,
    })

    #figure out how to determine game type
    row.update({
        "Game Type": "Regular Season",
        "Playoff Game": 0
    })
    return pd.DataFrame([row])


# def calculate_rolling_stats(df, season):
#     cols = [
#         'PTS', 'AST', 'TRB', 'ORB', 
#         'DRB', 'BLK', 'STL', 
#         'FGA', 'FG', 'FG%', '3PA', 
#         '3P', '3P%', 'FTA', 'FT', 
#         'FT%', 'Fouls', 'TOV'
#     ]
#     rows = []

#     # Process year by year
#     season_games = df[df["Season"] == season]
#     for idx, row in season_games.iterrows():
#         home = NBAName(row["Home Team"])
#         visitor = NBAName(row["Visitor Team"])
#         date = row["Date"]
#         pgs = get_pregame_stats(home, visitor, date)
#         for col in cols:
#             home_stat = row.get(f"Home Team {stat_col}", None)
#             visitor_stat = row.get(f"Visitor Team {stat_col}", None)

#             # Get current averages
#             home_data = stat_dict.get(home_team, {"total": 0, "games": 0})
#             visitor_data = stat_dict.get(visitor_team, {"total": 0, "games": 0})
#             home_opp_data = opp_stat_dict.get(home_team, {"total": 0, "games": 0})
#             visitor_opp_data = opp_stat_dict.get(visitor_team, {"total": 0, "games": 0})

#             home_avg = (
#                 home_data["total"] / home_data["games"]
#                 if home_data["games"] > 0 else None
#             )
#             visitor_avg = (
#                 visitor_data["total"] / visitor_data["games"]
#                 if visitor_data["games"] > 0 else None
#             )

#             home_opp_avg = (
#                 home_opp_data["total"] / home_opp_data["games"]
#                 if home_opp_data["games"] > 0 else None
#             )
#             visitor_opp_avg = (
#                 visitor_opp_data["total"] / visitor_opp_data["games"]
#                 if visitor_opp_data["games"] > 0 else None
#             )

#         home_averages.append(home_avg)
#         visitor_averages.append(visitor_avg)
#         home_opp_averages.append(home_opp_avg)
#         visitor_opp_averages.append(visitor_opp_avg)

#         # Update totals *after* recording current averages
#         stat_dict.setdefault(home_team, {"total": 0, "games": 0})
#         stat_dict.setdefault(visitor_team, {"total": 0, "games": 0})
#         opp_stat_dict.setdefault(home_team, {"total": 0, "games": 0})
#         opp_stat_dict.setdefault(visitor_team, {"total": 0, "games": 0})

#         if pd.notna(visitor_stat):
#             stat_dict[visitor_team]["total"] += visitor_stat
#             stat_dict[visitor_team]["games"] += 1
#             opp_stat_dict[home_team]["total"] += visitor_stat
#             opp_stat_dict[home_team]["games"] += 1

#         if pd.notna(home_stat):
#             stat_dict[home_team]["total"] += home_stat
#             stat_dict[home_team]["games"] += 1
#             opp_stat_dict[visitor_team]["total"] += home_stat
#             opp_stat_dict[visitor_team]["games"] += 1

#     # Add columns back to the original df (in order)
#     df[f"Home Team {stat_col} Avg"] = home_averages
#     df[f"Visitor Team {stat_col} Avg"] = visitor_averages
#     df[f"Home Team Opp {stat_col} Avg"] = home_opp_averages
#     df[f"Visitor Team Opp {stat_col} Avg"] = visitor_opp_averages

#     return df

'''
Season Start

check if previous season in ALL_TEAMS
initialize new season in ALL_TEAMS with correct elo and empty stats
'''
def new_season(df, season, teams):
    if season < 1985:
        raise ValueError
    cur_season = {}
    ALL_TEAMS[season] = cur_season
    for team in teams:
        nba_name = NBAName(team)
        nba_team = NBATeam(name=nba_name, season=season)
        cur_season[nba_name] = nba_team
        if season == 1985:
            nba_team.elo = 1500
        elif season-1 in ALL_TEAMS:
            prev_season = ALL_TEAMS[season-1]
            if nba_name in prev_season:
                nba_team.elo = 0.75 * prev_season[nba_name].elo + 0.25 * 1500
            else:
                prev_name = TEAM_RENAMES.get((nba_name, season))
                if prev_name and prev_name in prev_season:
                    nba_team.elo = 0.75 * prev_season[prev_name].elo + 0.25 * 1500
                    print(nba_team.elo)
                else:
                    nba_team.elo = 1500
        calculate_avgs_for_team(df, nba_name, season)
    calculate_elos(df, season)
