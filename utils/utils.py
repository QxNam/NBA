import os
import json
import pandas as pd

from urllib.parse import urlencode
from utils.logging import logger


def get_timeline(start_date: str, end_date: str):
    return pd.date_range(start_date, end_date)


def is_ready(browser):
    return browser.execute_script(r"""
        return document.readyState === 'complete'
    """)


def get_url_with_params(url: str, params: dict):
    return url + '?' + urlencode(params)


def get_seasons_by_year(start_year: int = 2017, end_year: int = 2017):
    return [f'{year-1}-{str(year)[2:]}' for year in range(start_year, end_year+1)]


def create_folder_if_not_existed(path_data: str):
    if not os.path.exists(path_data):
        logger("info", f"Create directory: {path_data}")
        os.makedirs(path_data)

def save_json(data, path_file):
    with open(path_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        logger("success", f"Saved data at: {path_file}")
