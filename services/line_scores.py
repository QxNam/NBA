import os
import json
import time
import requests

import pandas as pd

from collections import defaultdict
from services.processing import processing_line_scores
from utils.logging import logger
from utils.utils import get_timeline


class LineScores:
    def __init__(
        self,
        start_date: str = "2016-01-01",
        end_date: str = "2016-01-01",
        path_data: str = "./data/line_scores",
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.path_data = path_data
        self.timeline = get_timeline(start_date, end_date)

        self.games_data = defaultdict(list)

        if not os.path.exists(path_data):
            logger("info", f"Create path {path_data}")
            os.makedirs(path_data)
    
    @staticmethod
    def get_api_by_date(date: str="2016-01-01"):
        return f"https://global.nba.com/statsm2/scores/daily.json?gameDate={date}"
    
    def crawler(self):
        for time_step in self.timeline:
            flag = True
            date_str = time_step.strftime("%Y-%m-%d")
            api = self.get_api_by_date(date_str)
            response = requests.get(api)

            if response.status_code == 200:
                if response.text != '':
                    response_data = json.loads(response.text)
                    processed_data = processing_line_scores(response_data)

                    if processed_data:
                        if not any(self.games_data.values()):
                            self.games_data = processed_data
                        else:
                            [self.games_data[key].extend(processed_data[key]) \
                             for key in self.games_data.keys()]
                    else:
                        flag = False
                        logger("warning", "API URL: '{api}' No game in day!")

                    if flag:
                        logger("success", f"API URL: '{api}' done!")
                else:
                    logger("warning", f"API URL: '{api}' return empty data!")
            else:
                logger("warning", "API URL: '{api}' return status code: {response.status_code}")

            if time_step.is_month_end or date_str == self.end_date:
                df = pd.DataFrame(self.games_data)
                df.to_csv(f'{self.path_data}/line_scores_{date_str}.csv', index=False, encoding='utf-8')
                logger("success", f"Save data at: '{self.path_data}/line_scores_{date_str}.csv' saved!")

            time.sleep(1)