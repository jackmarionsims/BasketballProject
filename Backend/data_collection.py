from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data_helpers import calculate_avgs_for_team, calculate_elos, NAME_TO_ABBR, date_to_num, ALL_TEAMS, get_pregame_stats, new_season, CACHE_VERSION, SCHEDULED_GAMES, elo_change, date_to_id, date_to_id2, date_to_date
from classes2 import NBAName, NBATeam, BoxScore, ScheduledGame, Date, CompletedGame
import pickle
import time
from selenium.common.exceptions import WebDriverException
import os
import tempfile

def save_state(scheduled_games, completed_games):
    # Save pickle atomically
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp:
        pickle.dump(ALL_TEAMS, tmp)
        tmp_pkl = tmp.name
    os.replace(tmp_pkl, f"all_teams{CACHE_VERSION}.pkl")

    # Save CSVs atomically
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w') as tmp:
        scheduled_games.to_csv(tmp)
        tmp_sch = tmp.name
    os.replace(tmp_sch, 'scheduled_games2.csv')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w') as tmp:
        completed_games.to_csv(tmp)
        tmp_cg = tmp.name
    os.replace(tmp_cg, 'completed_games2.csv')

def driver_get_with_retry(driver, url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            driver.get(url)
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

'''
Things to maintain
1. Database mapping each team to current averages
2. Change gameID to be year + month + day + 0 + home_abbrev (Ex: Boston @ Cleveland, March 8, 2026 = 202603080CLE)
'''

'''
Workflow
1. Update Scheduled Games
2. Update Completed Games



Update Scheduled Games
- Check every scheduled game and make sure not postponed or anything, else change gameID and date, etc
- Can brute force check every game scheduled and check if already in df or else add
- Check only after last game in df

Update Completed Games
1. Take in day as argument
2. Use basketball reference to get all games played on previous day (alternative use dataframe of scheduled games)
3. For each game
    If game concluded
    a) Use basketball reference to obtain box score for game
    b) Convert box score to row in dataframe
    c) Use database to access averages to add to row
    d) Add row to completed games
    e) Remove from scheduled games
    f) Update averages

    else
    a) remove from df
'''
no_eff = [
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
    'Visitor Team W', 'Visitor Team L', 'Visitor Team W/L%'
]

#KEEP
def add_scores(date, season, scheduled_games, completed_games, driver, safe=True):
    #update schedule of day
    date_num = date_to_num(date)
    month = datetime.strptime(date, "%a, %b %d, %Y").strftime("%B").lower()
    if safe:
        scheduled_games = update_schedule(month, season, scheduled_games, driver)
    
    #update completed games
    day_games = scheduled_games[scheduled_games["Date Number"] == date_num]
    for idx, game in day_games.iterrows():
        # once indexed by gameID
        if idx in completed_games.index:
            continue
        scheduled_games, completed_games = add_game_result(game, scheduled_games, completed_games, driver)
    
    return scheduled_games, completed_games


#change how to manage the inputs depending on how you call the function
#with a specific day or month
#KEEP
def update_schedule(month, season, scheduled_games, driver):
    """
    recomputes schedule for month of day and ensures every game in the schedule is part of the scheduled games df
    """
    base_url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html"
    #obtain table of given month from basketball reference
    url = base_url.format(season, month)
    driver_get_with_retry(driver, url)
    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    game_table = soup.find(id="schedule")
    games = pd.read_html(StringIO(str(game_table)))[0]
    games = games[games["Date"] != "Date"]

    #construct scheduled game df from table
    rows = []
    for idx, game in games.iterrows():
        home_name = NBAName(game["Home/Neutral"])
        visitor_name = NBAName(game["Visitor/Neutral"])
        home = ALL_TEAMS[season][home_name]
        visitor = ALL_TEAMS[season][visitor_name]
        # print(home, visitor)
        date = game["Date"]
        row = get_pregame_stats(home, visitor, date)
        rows.append(row)

    pregame_stats = pd.concat(rows, ignore_index=True).set_index("Game ID")
    scheduled_games = pd.concat([scheduled_games, pregame_stats])
    scheduled_games = scheduled_games[~scheduled_games.index.duplicated(keep="last")]
    #scheduled_games.to_csv("scheduled_games.csv", index=False)
    #pregame_stats.to_csv("test2.csv")
    #discard previous table and set this as new one
    #either compute beginning and end of month and only change those date numbers
    #or maintain df from each individual month
    return scheduled_games

#MOVE
def add_game_result(scheduled_game, scheduled_games, completed_games, driver):
    """
    Gathers the box score of a given game from basketball reference, 
    then adds that game to completed games and remove from scheduled games
    if game not available, remove from scheduled games

    deal with making sure ALL_TEAMS is correct before calling
    updates ALL_TEAMS using new stats
    """
    id = scheduled_game.name
    scheduled_games = scheduled_games.drop(index=id)
    #SCHEDULED_GAMES = SCHEDULED_GAMES.drop(index=id)
    home_abbrev = NAME_TO_ABBR[scheduled_game["Home Team"]]
    visitor_abbrev = NAME_TO_ABBR[scheduled_game["Visitor Team"]]

    base_url = "https://www.basketball-reference.com/boxscores/{}.html"
    url = base_url.format(id)
    print(url)

    time.sleep(3)
    driver_get_with_retry(driver, url)
    page = driver.page_source
    
    base_tbl = "box-{}-game-basic"

    soup = BeautifulSoup(page, "html.parser")
    try:
        home_table = soup.find(id=base_tbl.format(home_abbrev))
        home_stats = pd.read_html(StringIO(str(home_table)), header=1)[0]
        visitor_table = soup.find(id=base_tbl.format(visitor_abbrev))
        visitor_stats = pd.read_html(StringIO(str(visitor_table)), header=1)[0]
    except Exception as e:
        print(f"Box score not available for {id}: {e}")
        return scheduled_games, completed_games
    
    home_totals = home_stats.iloc[-1]
    visitor_totals = visitor_stats.iloc[-1]


    box_score = box_score_update(scheduled_game, home_totals, visitor_totals)
    scheduled_games = update_pgs(scheduled_games, scheduled_game["Season"], scheduled_game["Home Team"], scheduled_game["Visitor Team"])
    completed_games = add_completed_game(scheduled_game, box_score, completed_games)
    return scheduled_games, completed_games
    
#MOVE
def box_score_update(scheduled_game, home_totals, visitor_totals):
    """
    update team stats for home and away team using box score of game
    """
    #also calculate elo change
    box_score = {}
    season = scheduled_game["Season"]
    home = ALL_TEAMS[season][NBAName(scheduled_game["Home Team"])]
    visitor = ALL_TEAMS[season][NBAName(scheduled_game["Visitor Team"])]

    home_points = int(home_totals["PTS"])
    visitor_points = int(visitor_totals["PTS"])
    home_win = 1 if home_points > visitor_points else 0

    #elo changes
    margin = home_points - visitor_points
    delta = elo_change(home.elo+100, visitor.elo, margin)
    home.elo += delta
    visitor.elo -= delta

    home.stats["Total Games"] += 1
    home.stats["Total Home Games"] += 1
    home.stats["W"] += home_win
    home.stats["Home W"] += home_win
    home.stats["L"] += (1-home_win)
    home.stats["Home L"] += (1-home_win)

    visitor.stats["Total Games"] += 1
    visitor.stats["Total Visitor Games"] += 1
    visitor.stats["W"] += (1-home_win)
    visitor.stats["Visitor W"] += (1-home_win)
    visitor.stats["L"] += home_win
    visitor.stats["Visitor L"] += home_win

    
    #handle percentages differently
    cols = [
        'PTS', 'AST', 'TRB', 'ORB', 
        'DRB', 'BLK', 'STL', 
        'FGA', 'FG', '3PA', 
        '3P', 'FTA', 'FT', 
        'PF', 'TOV'
    ]
    
    
    for col in cols:
        home_stat = int(home_totals[col])
        visitor_stat = int(visitor_totals[col])

        box_score[f"Home Team {col}"] = home_stat
        box_score[f"Visitor Team {col}"] = visitor_stat

        home.stats[f"Total {col}"] += home_stat
        home.stats[f"Home Total {col}"] += home_stat
        home.stats[f"Total Opp {col}"] += visitor_stat
        home.stats[f"Home Total Opp {col}"] += visitor_stat

        visitor.stats[f"Total {col}"] += visitor_stat
        visitor.stats[f"Visitor Total {col}"] += visitor_stat
        visitor.stats[f"Total Opp {col}"] += home_stat
        visitor.stats[f"Visitor Total Opp {col}"] += home_stat

    percs = ["FG%", "3P%", "FT%"]
    for perc in percs:
        home_stat = float(home_totals[perc])
        visitor_stat = float(visitor_totals[perc])
        box_score[f"Home Team {perc}"] = home_stat
        box_score[f"Visitor Team {perc}"] = visitor_stat
    
    box_score["Winner"] = home.name.value if home_win else visitor.name.value
    box_score["Loser"] = visitor.name.value if home_win else home.name.value
    box_score["Home Win"] = home_win
    
    return box_score

#MOVE
def update_pgs(scheduled_games, season, home_name, visitor_name):
    scheduled_games = scheduled_games.copy()
    teams_played = {home_name, visitor_name}
    for idx, game in scheduled_games.iterrows():
        if game["Home Team"] in teams_played or game["Visitor Team"] in teams_played:
            home = ALL_TEAMS[season][NBAName(game["Home Team"])]
            visitor = ALL_TEAMS[season][NBAName(game["Visitor Team"])]
            date = game["Date"]
            row = get_pregame_stats(home, visitor, date)
            scheduled_games.loc[idx] = row.set_index("Game ID").iloc[0]
    return scheduled_games

#MOVE
def add_completed_game(scheduled_game, box_score, completed_games):
    sg_dict = scheduled_game.to_dict()
    sg_dict["Game ID"] = scheduled_game.name
    combined = {**sg_dict, **box_score}
    # print(combined)
    new_row = pd.DataFrame([combined]).set_index("Game ID")
    completed_games = pd.concat([completed_games, new_row])
    #completed_games.to_csv("completed_games.csv", index=False)
    return completed_games


def reset_all_teams():
    modern = pd.read_csv("csvs/modern.csv")
    for season in range(1985, 2027):
        if season != 2026:
            games = modern[modern["Season"] == season]
        else:
            games = modern[modern["Season"] == 2025]
        teams = games["Home Team"].unique()
        new_season(modern, season, teams)
    
    with open(f"all_teams{CACHE_VERSION}.pkl", "wb") as f:
        pickle.dump(ALL_TEAMS, f)

def test_create_schedule(scheduled_games, driver):
    months = ["october", "november", "december", "january", "february", "march", "april"]

    try:
        for month in months:
            scheduled_games = update_schedule(month, 2026, scheduled_games, driver)
            print(month, "completed")
    finally:
        driver.quit()
    return scheduled_games

def main():
    options = Options()
    options.add_argument("--headless")
    #driver = webdriver.Chrome(options=options)
    with open(f"all_teams{CACHE_VERSION}.pkl", "rb") as f:
        loaded = pickle.load(f)
    ALL_TEAMS.update(loaded)
    print(ALL_TEAMS[2026][NBAName("New York Knicks")])
    # scheduled_games = pd.read_csv('scheduled_games.csv').set_index("Game ID")
    # completed_games = pd.read_csv('modern2.csv', index_col=0)
    # completed_games["Game ID"] = completed_games.apply(lambda row: date_to_id2(row["Home Team"], row["Date"]), axis=1)
    # completed_games["Date"] = completed_games.apply(lambda row: date_to_date(row["Date"]), axis=1)
    # completed_games = completed_games.set_index("Game ID")
    # try:
    #     scheduled_games = pd.read_csv('scheduled_games.csv').set_index("Game ID")
    #     completed_games= pd.read_csv('completed_games.csv').set_index("Game ID")

    #     before_today = scheduled_games[scheduled_games["Date Number"] < 739700]
    #     unique_dates = before_today["Date"].unique()
    #     count = 0
    #     for date in unique_dates:
    #         count += 1
    #         scheduled_games, completed_games = add_scores(date, 2026, scheduled_games, completed_games, driver, False)
    #         if count == 10:
    #             print("saving up to", date)
    #             save_state(scheduled_games, completed_games)
    #             count = 0
    #         print(date, "completed")

    #     save_state(scheduled_games, completed_games)
    # finally:
    #     driver.quit()

if __name__ == "__main__":
    main()