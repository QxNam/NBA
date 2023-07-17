import requests
import time

from utils.logging import logger
from utils.utils import (
    get_url_with_params,
    get_seasons_by_year,
    create_folder_if_not_existed,
    save_json
)

from configs.params import (
    HEADERS,
    TEAM_STATS_API_NAMES
)
from configs.params import (
    BASE_API_GENERAL,
    BASE_PARAMS_GENERAL,
    MEASURE_TYPES_GENERAL,
    SEASON_TYPES_GENERAL,
    PER_MODES_GENERAL
)
from configs.params import (
    BASE_API_CLUTCH,
    BASE_PARAMS_CLUTCH,
    MEASURE_TYPES_CLUTCH,
    SEASON_TYPES_CLUTCH,
    PER_MODES_CLUTCH
)
from configs.params import (
    BASE_API_PLAYTYPE,
    BASE_PARAMS_PLAYTYPE,
    PLAYTYPES,
    SEASON_TYPES_PLAYTYPE,
    PER_MODES_PLAYTYPE,
    OFF_DEF
)
from configs.params import (
    BASE_API_TRACKING,
    BASE_PARAMS_TRACKING,
    PT_MEASURE_TYPES,
    SEASON_TYPES_TRACKING,
    PER_MODES_TRACKING
)
from configs.params import (
    BASE_API_DEFENSE,
    BASE_PARAMS_DEFENSE,
    DEFENSE_CATEGORIES,
    SEASON_TYPES_DEFENSE,
)    
from configs.params import (
    BASE_API_SHOT,
    BASE_PARAMS_SHOT,
    SHOT_TYPES,
    SEASON_TYPES_SHOT,
    GENERAL_RANGE,
    SHOT_CLOCK_RANGE,
    DRIBBLE_RANGE,
    TOUCH_TIME_RANGE,
    CLOSEST_DEF_RANGE,
    PER_MODES_SHOT
)
from configs.params import (
    BASE_API_SHOOTING,
    BASE_PARAMS_SHOOTING,
    SEASON_TYPES_SHOOTING,
    PER_MODES_SHOOTING,
    DISTANCE_RANGE
)
from configs.params import (
    BASE_API_OPP_SHOOTING,
    OPP_SHOOTING_MEASURE_TYPES
)
from configs.params import (
    BASE_API_HUSTLE,
    BASE_PARAMS_HUSTLE,
    SEASON_TYPES_HUSTLE,
    PER_MODES_HUSTLE
)
from configs.params import (
    BASE_API_BOX_SCORES,
    BASE_PARAMS_BOX_SCORES,
    SEASON_TYPES_BOX_SCORES
)
from configs.params import (
    BASE_API_ADVANCED_BOX_SCORES,
    BASE_PARAMS_ADVANCED_BOX_SCORES,
    MEASURE_TYPES_ADVANCED_BOX_SCORES,
    SEASON_TYPES_ADVANCED_BOX_SCORES
)

class TeamStats:
    def __init__(
        self,
        start_year: int = 2017,
        end_year: int = 2017,
        path_data: str = './data/team_stats'
    ):
        self.start_year = start_year
        self.end_year = end_year
        self.path_data = path_data
        self.seasons = get_seasons_by_year(start_year, end_year)

        self.headers = HEADERS
        self.api_names = TEAM_STATS_API_NAMES

        self.headers['Host'] = 'stats.nba.com'
        self.headers['Referer'] = 'https://www.nba.com/'

        self.base_api_general = BASE_API_GENERAL
        self.base_params_general = BASE_PARAMS_GENERAL
        self.measure_types_general = MEASURE_TYPES_GENERAL
        self.season_types_general = SEASON_TYPES_GENERAL
        self.per_modes_general = PER_MODES_GENERAL

        self.base_api_clutch = BASE_API_CLUTCH
        self.base_params_clutch = BASE_PARAMS_CLUTCH
        self.measure_types_clutch = MEASURE_TYPES_CLUTCH
        self.season_types_clutch = SEASON_TYPES_CLUTCH
        self.per_modes_clutch = PER_MODES_CLUTCH

        self.base_api_playtype = BASE_API_PLAYTYPE
        self.base_params_playtype = BASE_PARAMS_PLAYTYPE
        self.playtype = PLAYTYPES
        self.season_types_playtype = SEASON_TYPES_PLAYTYPE
        self.per_modes_playtype = PER_MODES_PLAYTYPE
        self.off_def = OFF_DEF

        self.base_api_tracking = BASE_API_TRACKING
        self.base_params_tracking = BASE_PARAMS_TRACKING
        self.pt_measure_types = PT_MEASURE_TYPES
        self.season_types_tracking = SEASON_TYPES_TRACKING
        self.per_modes_tracking = PER_MODES_TRACKING

        self.base_api_defense = BASE_API_DEFENSE
        self.base_params_defense = BASE_PARAMS_DEFENSE
        self.defense_categories = DEFENSE_CATEGORIES
        self.season_types_defense = SEASON_TYPES_DEFENSE

        self.base_api_shot = BASE_API_SHOT
        self.base_params_shot = BASE_PARAMS_SHOT
        self.shot_types = SHOT_TYPES
        self.season_types_shot = SEASON_TYPES_SHOT
        self.general_range = GENERAL_RANGE
        self.shot_clock_range = SHOT_CLOCK_RANGE
        self.dribble_range = DRIBBLE_RANGE
        self.touch_time_range = TOUCH_TIME_RANGE
        self.closest_def_range = CLOSEST_DEF_RANGE
        self.per_modes_shot = PER_MODES_SHOT

        self.base_api_shooting = BASE_API_SHOOTING
        self.base_params_shooting = BASE_PARAMS_SHOOTING
        self.season_types_shooting = SEASON_TYPES_SHOOTING
        self.per_modes_shooting = PER_MODES_SHOOTING
        self.distance_range = DISTANCE_RANGE

        self.base_api_opp_shooting = BASE_API_OPP_SHOOTING
        self.opp_shooting_measure_types = OPP_SHOOTING_MEASURE_TYPES

        self.base_api_hustle = BASE_API_HUSTLE
        self.base_params_hustle = BASE_PARAMS_HUSTLE
        self.season_types_hustle = SEASON_TYPES_HUSTLE
        self.per_modes_hustle = PER_MODES_HUSTLE

        self.base_api_box_scores = BASE_API_BOX_SCORES
        self.base_params_box_scores = BASE_PARAMS_BOX_SCORES
        self.season_types_box_scores = SEASON_TYPES_BOX_SCORES

        self.base_api_advanced_box_scores = BASE_API_ADVANCED_BOX_SCORES
        self.base_params_advanced_box_scores = BASE_PARAMS_ADVANCED_BOX_SCORES
        self.measure_types_advanced_box_scores = MEASURE_TYPES_ADVANCED_BOX_SCORES
        self.season_types_advanced_box_scores = SEASON_TYPES_ADVANCED_BOX_SCORES

    def get_general_clutch_data(self, api_name: str):
        if api_name == 'General':
            base_api = self.base_api_general
            base_params = self.base_params_general
            measure_types = self.measure_types_general
            season_types = self.season_types_general
            per_modes = self.per_modes_general
        else:
            base_api = self.base_api_clutch
            base_params = self.base_params_clutch
            measure_types = self.measure_types_clutch
            season_types = self.season_types_clutch
            per_modes = self.per_modes_clutch

        for measure_type in measure_types:
            base_params['MeasureType'] = measure_type

            for season in self.seasons:
                base_params['Season'] = season

                for season_type in season_types:
                    base_params['SeasonType'] = season_type

                    for per_mode in per_modes:
                        base_params['PerMode'] = per_mode

                        api = get_url_with_params(base_api, base_params)
                        res = requests.get(api, headers=HEADERS)

                        if res.status_code == 200:
                            data = res.json()

                            path_file = f'{self.path_data}/{api_name}/{measure_type}/{season}/{season_type}/'
                            file_name = f'{api_name}_{measure_type}_{season}_{season_type}_{per_mode}.json'
                            create_folder_if_not_existed(path_file)

                            save_json(data, path_file + file_name)
                        else:
                            logger("error", f"Request failure: {file_name}")

                        time.sleep(2)
    
    def get_playtype_data(self, api_name: str):
        for playtype in self.playtype:
            self.base_params_playtype['PlayType'] = playtype

            for season in self.seasons:
                self.base_params_playtype['SeasonYear'] = season

                for season_type in self.season_types_playtype:
                    self.base_params_playtype['SeasonType'] = season_type

                    for per_mode in self.per_modes_playtype:
                        self.base_params_playtype['PerMode'] = per_mode

                        for off_def in self.off_def:
                            self.base_params_playtype['TypeGrouping'] = off_def

                            api = get_url_with_params(self.base_api_playtype, self.base_params_playtype)
                            res = requests.get(api, headers=HEADERS)

                            if res.status_code == 200:
                                data = res.json()

                                path_file = f'{self.path_data}/{api_name}/{playtype}/{season}/{season_type}/'
                                file_name = f'{api_name}_{playtype}_{season}_{season_type}_{per_mode}_{off_def}.json'
                                create_folder_if_not_existed(path_file)

                                save_json(data, path_file + file_name)
                            else:
                                logger("error", f"Request failure: {file_name}")

                            time.sleep(2)

    def get_tracking_data(self, api_name: str):
        for pt in self.pt_measure_types:
            self.base_params_tracking['PtMeasureType'] = pt

            for season in self.seasons:
                self.base_params_tracking['Season'] = season

                for season_type in self.season_types_tracking:
                    self.base_params_tracking['SeasonType'] = season_type

                    for per_mode in self.per_modes_tracking:
                        self.base_params_tracking['PerMode'] = per_mode

                        api = get_url_with_params(self.base_api_tracking, self.base_params_tracking)
                        res = requests.get(api, headers=HEADERS)

                        if res.status_code == 200:
                            data = res.json()

                            path_file = f'{self.path_data}/{api_name}/{pt}/{season}/{season_type}/'
                            file_name = f'{api_name}_{pt}_{season}_{season_type}_{per_mode}.json'
                            create_folder_if_not_existed(path_file)

                            save_json(data, path_file + file_name)
                        else:
                            logger("error", f"Request failure: {file_name}")

                        time.sleep(2)

    def get_defense_dashboard_data(self, api_name: str):
        for defense_category in self.defense_categories:
            self.base_params_defense['DefenseCategory'] = defense_category

            for season in self.seasons:
                self.base_params_defense['Season'] = season

                for season_type in self.season_types_defense:
                    self.base_params_defense['SeasonType'] = season_type

                    api = get_url_with_params(self.base_api_defense, self.base_params_defense)
                    res = requests.get(api, headers=HEADERS)

                    if res.status_code == 200:
                        data = res.json()

                        path_file = f'{self.path_data}/{api_name}/{defense_category}/{season}/{season_type}/'
                        file_name = f'{api_name}_{defense_category}_{season}_{season_type}.json'
                        create_folder_if_not_existed(path_file)

                        save_json(data, path_file + file_name)
                    else:
                        logger("error", f"Request failure: {file_name}")

                    time.sleep(2)

    def get_shot_dashboard_data(self, api_name: str):
        for shot_type in self.shot_types:
            for season in self.seasons:
                self.base_params_shot['Season'] = season

                for season_type in self.season_types_shot:
                    self.base_params_shot['SeasonType'] = season_type

                    for per_mode in self.per_modes_shot:
                        self.base_params_shot['PerMode'] = per_mode

                        if shot_type == 'General':
                            ranges = GENERAL_RANGE
                        elif shot_type == 'ShotClock':
                            ranges = SHOT_CLOCK_RANGE
                        elif shot_type == 'Dribble':
                            ranges = DRIBBLE_RANGE
                        elif shot_type == 'TouchTime':
                            ranges = TOUCH_TIME_RANGE
                        elif shot_type == 'ClosestDef':
                            ranges = CLOSEST_DEF_RANGE
                        elif shot_type == 'ClosestDef10':
                            ranges = CLOSEST_DEF_RANGE

                        for shot_range in ranges:
                            if shot_type == 'General':
                                self.base_params_shot['GeneralRange'] = shot_range
                            elif shot_type == 'ShotClock':
                                self.base_params_shot['ShotClockRange'] = shot_range
                            elif shot_type == 'Dribble':
                                self.base_params_shot['DribbleRange'] = shot_range
                            elif shot_type == 'TouchTime':
                                self.base_params_shot['TouchTimeRange'] = shot_range
                            elif shot_type == 'ClosestDef':
                                self.base_params_shot['CloseDefDistRange'] = shot_range
                            elif shot_type == 'ClosestDef10':
                                self.base_params_shot['CloseDefDistRange'] = shot_range

                            api = get_url_with_params(self.base_api_shot, self.base_params_shot)
                            res = requests.get(api, headers=HEADERS)

                            if res.status_code == 200:
                                data = res.json()

                                path_file = f'{self.path_data}/{api_name}/{shot_type}/{season}/{season_type}/{per_mode}/'
                                file_name = f'{api_name}_{shot_type}_{season}_{season_type}_{per_mode}_{shot_range}.json'
                                create_folder_if_not_existed(path_file)

                                save_json(data, path_file + file_name)
                            else:
                                logger("error", f"Request failure: {file_name}")

                            time.sleep(2)

    def get_shooting_data(self, api_name: str):
        for season in self.seasons:
            self.base_params_shooting['Season'] = season

            for season_type in self.season_types_shooting:
                self.base_params_shooting['SeasonType'] = season_type

                for per_mode in self.per_modes_shooting:
                    self.base_params_shooting['PerMode'] = per_mode

                    for distance in self.distance_range:
                        self.base_params_shooting['DistanceRange'] = distance

                        api = get_url_with_params(self.base_api_shooting, self.base_params_shooting)
                        res = requests.get(api, headers=HEADERS)

                        if res.status_code == 200:
                            data = res.json()

                            path_file = f'{self.path_data}/{api_name}/{season}/{season_type}/{per_mode}/'
                            file_name = f'{api_name}_{season}_{season_type}_{per_mode}_{distance}.json'
                            create_folder_if_not_existed(path_file)

                            save_json(data, path_file + file_name)
                        else:
                            logger("error", f"Request failure: {file_name}")

                        time.sleep(2)

    def get_opponent_shooting_data(self, api_name: str):
        for opp in self.opp_shooting_measure_types:
            if opp == 'Opponent':
                base_api = self.base_api_shooting
                base_params = self.base_params_shooting
                base_params['MeasureType'] = opp
                season_types = self.season_types_shooting
                ranges = self.distance_range
            else:
                base_api = self.base_api_opp_shooting
                base_params = self.base_params_shot
                season_types = self.season_types_shot

                if opp == 'General':
                    ranges = GENERAL_RANGE
                elif opp == 'ShotClock':
                    ranges = SHOT_CLOCK_RANGE
                elif opp == 'Dribble':
                    ranges = DRIBBLE_RANGE
                elif opp == 'TouchTime':
                    ranges = TOUCH_TIME_RANGE
                elif opp == 'ClosestDef' or opp == 'ClosestDef10':
                    ranges = CLOSEST_DEF_RANGE

            for season in self.seasons:
                base_params['Season'] = season

                for season_type in season_types:
                    base_params['SeasonType'] = season_type

                    for per_mode in self.per_modes_shot:
                        base_params['PerMode'] = per_mode

                        for shot_range in ranges:
                            if opp == 'Opponent':
                                base_params['DistanceRange'] = shot_range
                            elif opp == 'General':
                                base_params['GeneralRange'] = shot_range
                            elif opp == 'ShotClock':
                                base_params['ShotClockRange'] = shot_range
                            elif opp == 'Dribble':
                                base_params['DribbleRange'] = shot_range
                            elif opp == 'TouchTime':
                                base_params['TouchTimeRange'] = shot_range
                            elif opp == 'ClosestDef' or opp == 'ClosestDef10':
                                base_params['CloseDefDistRange'] = shot_range

                            api = get_url_with_params(base_api, base_params)
                            res = requests.get(api, headers=HEADERS)

                            if res.status_code == 200:
                                data = res.json()

                                path_file = f'{self.path_data}/{api_name}/{opp}/{season}/{season_type}/{per_mode}/'
                                file_name = f'{api_name}_{opp}_{season}_{season_type}_{per_mode}_{shot_range}.json'
                                create_folder_if_not_existed(path_file)

                                save_json(data, path_file + file_name)
                            else:
                                logger("error", f"Request failure: {file_name}")

                            time.sleep(2)

    def get_hustle_data(self, api_name: str):
        for season in self.seasons:
            self.base_params_hustle['Season'] = season

            for season_type in self.season_types_hustle:
                self.base_params_hustle['SeasonType'] = season_type

                for per_mode in self.per_modes_hustle:
                    self.base_params_hustle['PerMode'] = per_mode

                    api = get_url_with_params(self.base_api_hustle, self.base_params_hustle)
                    res = requests.get(api, headers=HEADERS)

                    if res.status_code == 200:
                        data = res.json()

                        path_file = f'{self.path_data}/{api_name}/{season}/{season_type}/'
                        file_name = f'{api_name}_{season}_{season_type}_{per_mode}.json'
                        create_folder_if_not_existed(path_file)

                        save_json(data, path_file + file_name)
                    else:
                        logger("error", f"Request failure: {file_name}")

                    time.sleep(2)

    def get_box_scores_data(self, api_name: str):
        for season in self.seasons:
            self.base_params_box_scores['Season'] = season

            for season_type in self.season_types_box_scores:
                self.base_params_box_scores['SeasonType'] = season_type

                api = get_url_with_params(self.base_api_box_scores, self.base_params_box_scores)
                res = requests.get(api, headers=HEADERS)

                if res.status_code == 200:
                    data = res.json()

                    path_file = f'{self.path_data}/{api_name}/{season}/'
                    file_name = f'{api_name}_{season}_{season_type}.json'
                    create_folder_if_not_existed(path_file)

                    save_json(data, path_file + file_name)
                else:
                    logger("error", f"Request failure: {file_name}")

                time.sleep(2)

    def get_advanced_box_scores_data(self, api_name: str):
        for measure_type in self.measure_types_advanced_box_scores:
            self.base_params_advanced_box_scores['MeasureType'] = measure_type

            for season in self.seasons:
                self.base_params_advanced_box_scores['Season'] = season

                for season_type in self.season_types_advanced_box_scores:
                    self.base_params_advanced_box_scores['SeasonType'] = season_type

                    api = get_url_with_params(self.base_api_advanced_box_scores, self.base_params_advanced_box_scores)
                    res = requests.get(api, headers=HEADERS)

                    if res.status_code == 200:
                        data = res.json()

                        path_file = f'{self.path_data}/{api_name}/{measure_type}/{season}/{season_type}/'
                        file_name = f'{api_name}_{measure_type}_{season}_{season_type}.json'
                        create_folder_if_not_existed(path_file)

                        save_json(data, path_file + file_name)
                    else:
                        logger("error", f"Request failure: {file_name}")

                    time.sleep(2)

    def crawler(self):
        for api_name in self.api_names:
            if api_name == 'General' or api_name == 'Clutch':
                self.get_general_clutch_data(api_name)
            elif api_name == 'Playtype':
                self.get_playtype_data(api_name)
            elif api_name == 'Tracking':
                self.get_tracking_data(api_name)
            elif api_name == 'DefenseDashboard':
                self.get_defense_dashboard_data(api_name)
            elif api_name == 'ShotDashboard':
                self.get_shot_dashboard_data(api_name)
            elif api_name == 'Shooting':
                self.get_shooting_data(api_name)
            elif api_name == 'OpponentShooting':
                self.get_opponent_shooting_data(api_name)
            elif api_name == 'Hustle':
                self.get_hustle_data(api_name)
            elif api_name == 'BoxScores':
                self.get_box_scores_data(api_name)
            elif api_name == 'AdvancedBoxScores':
                self.get_advanced_box_scores_data(api_name)
            else:
                logger("error", f"API name not found: {api_name}")
