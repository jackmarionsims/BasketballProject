from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data_helpers import calculate_avgs_for_team, calculate_elos, NAME_TO_ABBR, date_to_num, ALL_TEAMS, get_pregame_stats
from classes2 import NBAName, NBATeam, BoxScore, ScheduledGame, Date, CompletedGame



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


def add_scores(day):
    #update schedule of day
    #update completed games
    pass


def check_game(game):
    """
    check if a given scheduled game is still being played on that day, else remove from scheduled games
    """
    pass


#change how to manage the inputs depending on how you call the function
#with a specific day or month
def update_schedule(month, season, driver):
    """
    recomputes schedule for month of day and ensures every game in the schedule is part of the scheduled games df
    """
    base_url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html"
    #obtain table of given month from basketball reference
    url = base_url.format(season, month)
    driver.get(url)
    page = driver.page_source
    driver.quit()
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

    pregame_stats = pd.concat(rows, ignore_index=True)

    pregame_stats.to_csv("test2.csv")
    #discard previous table and set this as new one
    #either compute beginning and end of month and only change those date numbers
    #or maintain df from each individual month
    return

def add_game_result(game):
    """
    Gathers the box score of a given game from basketball reference, 
    then adds that game to completed games and remove from scheduled games
    if game not available, remove from scheduled games
    """
    id = game["New Game ID"]
    home_abbrev = NAME_TO_ABBR[game["Home Team"]]
    visitor_abbrev = NAME_TO_ABBR[game["Visitor Team"]]
    base_url = "https://www.basketball-reference.com/boxscores/{}.html"
    url = base_url.format(id)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page = driver.page_source
    driver.quit()

    base_tbl = "box-{}-game-basic"

    soup = BeautifulSoup(page, "html.parser")
    home_table = soup.find(id=base_tbl.format(home_abbrev))
    home_stats = pd.read_html(StringIO(str(home_table)))[0]

    visitor_table = soup.find(id=base_tbl.format(visitor_abbrev))
    visitor_stats = pd.read_html(StringIO(str(visitor_table)))[0]
    
    # retrieve previous team stats


    # create row using previous stats and box score


    # update team stats

    # home_stats.to_csv("home_stats.csv")
    # visitor_stats.to_csv("visitor_stats.csv")

def update_team_stats(box_score):
    """
    update team stats for home and away team using box score of game
    """
    pass


def main():
    # Code to run when the script is executed directly
    #Game ID,Date Number,Date,Game Type,Home Team,Visitor Team

    # ag = pd.read_csv("csvs/modern.csv")
    # all_cols = ag.columns
    # print(all_cols)
    #update_schedule("march", 2026)
    modern = pd.read_csv("csvs/modern.csv")
    teams = modern["Home Team"].unique()
    ALL_TEAMS[2025] = {}
    for team in teams:
        nba_name = NBAName(team)
        ALL_TEAMS[2025][nba_name] = NBATeam(name=nba_name, elo=1500)
        calculate_avgs_for_team(modern, nba_name, 2025)

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        update_schedule("february", 2025, driver)
    finally:
        driver.quit()
    #add_game_result(games.iloc[0])


if __name__ == "__main__":
    main()