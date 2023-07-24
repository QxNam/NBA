import os
import json
import pandas as pd
import datetime
import requests
import csv

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
    if start_year==end_year:
        return [f'{start_year-1}-{str(start_year)[2:]}']
    return [f'{year-1}-{str(year)[2:]}' for year in range(start_year, end_year+1)][1:]


def create_folder_if_not_existed(path_data: str):
    if not os.path.exists(path_data):
        logger("info", f"Create directory: {path_data}")
        os.makedirs(path_data)

def save_json(path, data, mode = 'w'):
    # check path, if not exist then create
    if path.find('/') != -1:
        os.makedirs(f'data/{"/".join(path.split("/")[:-1])}', exist_ok=True)
    with open(f'data/{path}.json', mode=mode, encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# ----
def write_csv(path: str, data: dict, mode = 'a') -> None:
    '''
    write data to csv file
    '''
    # check path, if not exist then create
    if path.find('/') != -1:
        os.makedirs(f'data/{"/".join(path.split("/")[:-1])}', exist_ok=True)
    with open(f'data/{path}', mode, newline='') as f:
        columns = [col.upper() for col in data.keys()]
        writer = csv.writer(f)
        # check data in csv file, if empty then write header
        if os.stat(f'data/{path}').st_size == 0:
            writer.writerow(columns)
        writer.writerow(data.values())
        f.close()

def get_folder_size(folder_path):
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            file_path = os.path.join(path, f)
            total_size += os.path.getsize(file_path)
    size_in_kb = total_size / 1024
    size_in_mb = size_in_kb / 1024
    size_in_gb = size_in_mb / 1024
    return {'KB': size_in_kb, 'MB': size_in_mb, 'GB': size_in_gb}

def get_year(year):
    year_now = datetime.datetime.now().year
    if year_now <= year:
        return int(datetime.datetime.now().strftime('%Y'))
    return int(year)

def get_day(year, format_day = '%Y-%m-%d', is_start_day=False):
    year_now = datetime.datetime.now().year
    if year_now <= year:
        if is_start_day:
            return datetime.datetime(year, 1, 1).strftime(format_day)
        return datetime.datetime.now().strftime(format_day)
    return datetime.datetime(year, 1, 1).strftime(format_day)

def check_requests(url, HEADERS=None):
    check_out = 3
    res = None
    while check_out > 0:
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200: 
            break
        check_out -= 1
    return res

def write_log(file, text='', mode ='a'):
    with open(f'log/{file}.txt', mode) as f:
        f.write(str(text) + '\n')
        f.close()

def process_data(data, col_name:str):
    if data is None:
        return None
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, int):
        return data
    if col_name.find('%') != -1:
        return round(data*100, 3)
    return round(data, 3)