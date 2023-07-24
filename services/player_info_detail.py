from utils import logging
log = logging.Logger()

from utils.utils import (
    get_url_with_params,
    get_year,
    get_seasons_by_year,
    write_csv,
    write_log,
    check_requests
)
from configs.params import (
    HEADERS,
    START_YEAR,
    END_YEAR
)

URL = 'https://stats.nba.com/stats/draftcombineplayeranthro'
HEADERS['Host'] = 'stats.nba.com'
HEADERS['Referer'] = 'https://www.nba.com/'
params = {
    'LeagueID': '00',
    'SeasonYear': '2023-24'
}
process = {
    'PLAYER_ID': 'PLAYER_ID',
    'PLAYER_NAME': 'PLAYER_NAME',
    'POSITION': 'POSITION',
    'HEIGHT_WO_SHOES': 'HEIGHT_WO_SHOES',
    'HEIGHT_WO_SHOES_FT_IN': 'HEIGHT_WO_SHOES_FT_IN',
    'HEIGHT_W_SHOES': 'HEIGHT_W_SHOES',
    'HEIGHT_W_SHOES_FT_IN': 'HEIGHT_W_SHOES_FT_IN',
    'WEIGHT': 'WEIGHT',
    'WINGSPAN': 'WINGSPAN',
    'WINGSPAN_FT_IN': 'WINGSPAN_FT_IN',
    'STANDING_REACH': 'STANDING_REACH',
    'STANDING_REACH_FT_IN': 'STANDING_REACH_FT_IN',
    'BODY_FAT_%': 'BODY_FAT_PCT',
    'HAND_LENGTH': 'HAND_LENGTH',
    'HAND_WIDTH': 'HAND_WIDTH'
} 

def crawl():
    s_year = get_year(START_YEAR)+1
    e_year = get_year(END_YEAR)+1
    seasons = get_seasons_by_year(s_year, e_year)
    for idx, season in enumerate(seasons):
        params['SeasonYear'] = season
        try:
            url = get_url_with_params(url=URL, params=params)
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title='Player_info_detail', idx=idx, n=len(seasons)), season, log.FAIL(), f'Status code: {req.status_code}')
                write_log('Player_info_detail', f'[OK] {season}: {req.status_code}')
                continue
            json_data = req.json()
            resultSets = json_data['resultSets'][0]
            dict_lst = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data = {
                    'Season': season
                }
                for key, value in process.items():
                    data[key] = result[dict_lst[value]]
                write_csv('team_info_detail.csv', data)
            print(log.status(title=f'Team_info_detail', idx=idx, n=len(seasons)), season, log.OK())
            write_log('Player_info', 'f{season} [OK]')
        except Exception as e:
            print(log.status(title='Team_info_detail', idx=idx, n=len(seasons)), season, log.FAIL(e))
            write_log('Team_info_detail', season, f'[FAIL] {e}')
def run():
    crawl()