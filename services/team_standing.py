import json
import requests
import time

from utils.logging import logger
from utils.utils import (
    get_url_with_params,
    get_seasons_by_year,
    create_folder_if_not_existed
)

from configs.params import (
    HEADERS,
    BASE_API_TEAM_STANDING,
    BASE_PARAMS_TEAM_STANDING
)

class TeamStanding:
    def __init__(
        self,
        start_year: int = 2017,
        end_year: int = 2017,
        path_data: str = './data/team_standing'
    ):
        self.start_year = start_year
        self.end_year = end_year
        self.path_data = path_data
        self.seasons = get_seasons_by_year(start_year, end_year)

        self.header = HEADERS
        self.base_api = BASE_API_TEAM_STANDING
        self.base_params = BASE_PARAMS_TEAM_STANDING
        
        create_folder_if_not_existed(self.path_data)

    def crawler(self):
        self.header['Host'] = 'stats.nba.com'
        self.header['Referer'] = 'https://www.nba.com/'

        for season in self.seasons:
            self.base_params['Season'] = season
            api = get_url_with_params(self.base_api, self.base_params)
            res = requests.get(api, headers=self.header)

            path_file = f"{self.path_data}/"
            file_name = f"team_standing_{season}.json"

            if res.status_code == 200:
                data = res.json()

                with open(path_file + file_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    logger("success", f"Saved data at: {file_name}")
            else:
                logger("error", f"Request failure: {file_name}")
            
            time.sleep(2)
