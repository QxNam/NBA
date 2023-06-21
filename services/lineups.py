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
    BASE_API_LINEUPS,
    BASE_PARAMS_LINEUPS,
    MEASURE_TYPES_LINEUPS,
    SEASON_TYPES_LINEUPS,
    PER_MODES_LINEUPS,
    GROUP_QUANTITY_LINEUPS
)

class LineUps:
    def __init__(
        self,
        start_year: int = 2017,
        end_year: int = 2017,
        path_data: str = './data/lineups'
    ):
        self.start_year = start_year
        self.end_year = end_year
        self.path_data = path_data
        self.seasons = get_seasons_by_year(start_year, end_year)

        self.header = HEADERS
        self.base_api = BASE_API_LINEUPS
        self.base_params = BASE_PARAMS_LINEUPS
        self.measure_types = MEASURE_TYPES_LINEUPS
        self.season_types = SEASON_TYPES_LINEUPS
        self.per_modes = PER_MODES_LINEUPS
        self.group_quantity = GROUP_QUANTITY_LINEUPS
        
        create_folder_if_not_existed(self.path_data)

    def crawler(self):
        self.header['Host'] = 'stats.nba.com'
        self.header['Referer'] = 'https://stats.nba.com/draft/combine-anthro/'
        
        for measure_type in self.measure_types:
            self.base_params['MeasureType'] = measure_type

            for season in self.seasons:
                self.base_params['Season'] = season

                for season_type in self.season_types:
                    self.base_params['SeasonType'] = season_type

                    for per_mode in self.per_modes:
                        self.base_params['PerMode'] = per_mode

                        for group_quantity in self.group_quantity:
                            self.base_params['GroupQuantity'] = group_quantity

                            api = get_url_with_params(self.base_api, self.base_params)
                            res = requests.get(api, headers=self.header)

                            path_file = f"{self.path_data}/{measure_type}/{season}/{season_type}/{per_mode}/"
                            file_name = f"{measure_type}_{season}_{season_type}_{per_mode}_{group_quantity}.json"

                            if res.status_code == 200:
                                data = res.json()

                                create_folder_if_not_existed(path_file)
                                with open(path_file + file_name, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, ensure_ascii=False, indent=4)
                                    logger("success", f"Saved data at: '{file_name}'")
                            else:
                                logger("error", f"Request failure: {file_name}")

                            time.sleep(2)
