import re
import requests
import time

import pandas as pd

from bs4 import BeautifulSoup
from collections import defaultdict

from configs.params import (
    HEADERS,
    BASE_URL_COACHES
)
from utils.logging import logger
from utils.utils import create_folder_if_not_existed


class Coaches:
    def __init__(
        self,
        start_year: int = 2017,
        end_year: int = 2017,
        path_data: str = './data/coaches'
    ):
        self.start_year = start_year
        self.end_year = end_year
        self.path_data = path_data

        self.headers = HEADERS
        self.base_url = BASE_URL_COACHES

        self.years = list(range(self.start_year, self.end_year+1))
        self.fields = ['coach_name', 'team', 'season', 'seas_franch', 'seas_overall', \
                       'cur_g', 'cur_w', 'cur_l', 'fr_g', 'fr_w', 'fr_l', \
                       'car_g', 'car_w', 'car_l', 'car_wpct', \
                       'cur_g_p', 'cur_w_p', 'cur_l_p', \
                       'fr_g_p', 'fr_w_p', 'fr_l_p', \
                       'car_g_p', 'car_w_p', 'car_l_p'
                    ]
        self.coaches = defaultdict(list)

        create_folder_if_not_existed(self.path_data)

    def crawler(self):
        for year in self.years:
            self.headers['Host'] = 'www.basketball-reference.com'
            self.headers['Referer'] = 'https://www.basketball-reference.com/'

            url = self.base_url.format(year=year)
            res = requests.get(url, headers=self.headers)

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                coaches_tbody = soup.find('table', id='NBA_coaches').find('tbody')
                coaches_rows = coaches_tbody.find_all('tr')

                season = f'{str(year-1)}-{str(year)[2:]}'

                for row in coaches_rows:
                    coach_name = row.find('th').text
                    coach_info_tds = row.find_all('td')
                    coach_info = [stat.text for stat in coach_info_tds \
                                if not re.search('dum-\d', stat['data-stat'])]
                    team = coach_info[0]

                    self.coaches['coach_name'].append(coach_name)
                    self.coaches['team'].append(team)
                    self.coaches['season'].append(season)
                    
                    # coach_info[0] is the team name, so we skip it
                    for col, stat in zip(self.fields[3:], coach_info[1:]):
                        self.coaches[col].append(stat)
                
                logger("success", f"Request success: '{url}'")
            else:
                logger("error", f"Request failure: '{url}'")
                
            time.sleep(2)

        self.save_data()

    def save_data(self):
        df = pd.DataFrame(self.coaches)
        df.to_csv(f'{self.path_data}/coaches.csv', index=False, encoding='utf-8')
