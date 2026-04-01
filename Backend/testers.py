from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data_helpers import NAME_TO_ABBR, date_to_num, get_pregame_stats, update_pgs, box_score_update, complete_game,  CACHE_VERSION, new_season, ALL_TEAMS, driver_get_with_retry
from data_collection import add_scores, save_state, add_game_result, update_schedule
from classes2 import NBAName
import pickle
import time
from selenium.common.exceptions import WebDriverException
import os
import tempfile


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