# import sys
# sys.path.append('..')
from utils import logging
log = logging.Logger()

from utils.utils import (
    get_url_with_params,
    get_seasons_by_year,
    write_csv,
    write_log,
    check_requests
)
from configs.nba_team import ID_TEAM_NAME
from configs.params import (
    HEADERS,
    START_YEAR,
    END_YEAR
)
from threading import Thread

# ---------------------- LineUps configs ----------------------
BASE_API_LINEUPS = 'https://stats.nba.com/stats/leaguedashlineups'
BASE_PARAMS_LINEUPS = {
    'Conference': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'GameSegment': '',
    'GroupQuantity': '5',
    'LastNGames': '0',
    'LeagueID': '00',
    'Location': '',
    'MeasureType': 'Base',
    'Month': '0',
    'OpponentTeamID': '0',
    'Outcome': '',
    'PORound': '0',
    'PaceAdjust': 'N',
    'PerMode': 'PerGame',
    'Period': '0',
    'PlusMinus': 'N',
    'Rank': 'N',
    'Season': '2016-17',
    'SeasonSegment': '',
    'SeasonType': 'Regular Season',
    'ShotClockRange': '',
    'TeamID': '0',
    'VsConference': '',
    'VsDivision': ''
}
MEASURE_TYPES_LINEUPS = ['Base', 'Advanced', 'Misc', 'Four Factors', 'Scoring', 'Opponent']
SEASON_TYPES_LINEUPS = ['Regular Season', 'Playoffs', 'PlayIn']
PER_MODES_LINEUPS = [
    'Totals', 
    'PerGame', 
    'Per100Possessions', 
    'Per100Plays', 
    'Per48', 
    'Per40', 
    'Per36', 
    'PerMinute', 
    'PerPossession', 
    'PerPlay', 
    'MinutesPer'
]
GROUP_QUANTITY_LINEUPS = [2, 3, 4, 5]
PROCESS_LINEUPS = {
    'Base': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'PTS': 'PTS',
        'FGM': 'FGM',
        'FGA': 'FGA',
        'FG%': 'FG_PCT',
        '3PA': 'FG3A',
        '3P%': 'FG3_PCT',
        'FTM': 'FTM',
        'FTA': 'FTA',
        'FT%': 'FT_PCT',
        'OREB': 'OREB',
        'DREB': 'DREB',
        'REB': 'REB',
        'AST': 'AST',
        'TOV': 'TOV',
        'STL': 'STL',
        'BLK': 'BLK',
        'BLKA': 'BLKA',
        'PF': 'PF',
        'PFD': 'PFD'
    },
    'Advanced': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'OFFRTG': 'OFF_RATING',
        'DEFRTG': 'DEF_RATING',
        'NETRTG': 'NET_RATING',
        'AST%': 'AST_PCT',
        'AST/TO': 'AST_TO',
        'AST RATIO': 'AST_RATIO',
        'OREB%': 'OREB_PCT',
        'DREB%': 'DREB_PCT',
        'REB%': 'REB_PCT',
        'TOV%': 'TM_TOV_PCT',
        'EFG%': 'EFG_PCT',
        'TS%': 'TS_PCT',
        'PACE': 'PACE',
        'PIE': 'PIE'
    },
    'Four Factors': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'EFG%': 'EFG_PCT',
        'FTA_RATE': 'FTA_RATE',
        'TOV%': 'TM_TOV_PCT',
        'OREB%': 'OREB_PCT',
        'OPP_EFG%': 'OPP_EFG_PCT',
        'OPP_FTA_RATE': 'OPP_FTA_RATE',
        'OPP_TOV%': 'OPP_TOV_PCT',
        'OPP_OREB%': 'OPP_OREB_PCT'
    },
    'Misc': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'PTS OFF TO': 'PTS_OFF_TOV',
        '2ND PTS': 'PTS_2ND_CHANCE',
        'FBPS': 'PTS_FB',
        'PITP': 'PTS_PAINT',
        'OPP PTS OFF TO': 'OPP_PTS_OFF_TOV',
        'OPP 2ND PTS': 'OPP_PTS_2ND_CHANCE',
        'OPP FBPS': 'OPP_PTS_FB',
        'OPP PITP': 'OPP_PTS_PAINT'
    },
    'Opponent': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'OPP FGM': 'OPP_FGM',
        'OPP FGA': 'OPP_FGA',
        'OPP FG%': 'OPP_FG_PCT',
        'OPP 3PM': 'OPP_FG3M',
        'OPP 3PA': 'OPP_FG3A',
        'OPP 3P%': 'OPP_FG3_PCT',
        'OPP FTM': 'OPP_FTM',
        'OPP FTA': 'OPP_FTA',
        'OPP FT%': 'OPP_FT_PCT',
        'OPP OREB': 'OPP_OREB',
        'OPP DREB': 'OPP_DREB',
        'OPP REB': 'OPP_REB',
        'OPP AST': 'OPP_AST',
        'OPP TOV': 'OPP_TOV',
        'OPP STL': 'OPP_STL',
        'OPP BLK': 'OPP_BLK',
        'OPP BLKA': 'OPP_BLKA',
        'OPP PF': 'OPP_PF',
        'OPP PFD': 'OPP_PFD',
        'OPP PTS': 'OPP_PTS'
    },
    'Scoring': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        '%FGA 2PT': 'PCT_FGA_2PT',
        '%FGA 3PT': 'PCT_FGA_3PT',
        '%PTS 2PT': 'PCT_PTS_2PT',
        '%PTS 2PT MR': 'PCT_PTS_2PT_MR',
        '%PTS 3PT': 'PCT_PTS_3PT',
        '%PTS FBPS': 'PCT_PTS_FB',
        '%PTS FT': 'PCT_PTS_FT',
        '%PTS OFFTO': 'PCT_PTS_OFF_TOV',
        '%PTS PITP': 'PCT_PTS_PAINT',
        '2FGM %AST': 'PCT_AST_2PM',
        '2FGM %UAST': 'PCT_UAST_2PM',
        '3FGM %AST': 'PCT_AST_3PM',
        '3FGM %UAST': 'PCT_UAST_3PM',
        'FGM %AST': 'PCT_AST_FGM',
        'FGM %UAST': 'PCT_UAST_FGM'
    }
}

def get_len(n = MEASURE_TYPES_LINEUPS):
    s = 0
    for measure_type in n:
        for season in get_seasons_by_year(START_YEAR, END_YEAR):
            for season_type in SEASON_TYPES_LINEUPS:
                for group_quantity in GROUP_QUANTITY_LINEUPS:
                    if measure_type in ['Advanced', 'Scoring']:
                        s+=1
                    else:
                        for per_mode in PER_MODES_LINEUPS:
                            s+=1
    return s

def process(json_data: dict) -> None:
    '''
    process json data to csv data
    '''
    parameters = json_data['parameters']
    resultSets = json_data['resultSets'][0]
    dict_lst = {k:v for v, k in enumerate(resultSets['headers'])}
    file = parameters['MeasureType']
    for result in resultSets['rowSet']:
        res = {}
        res['Team_id'] = result[3]
        res['Team_name'] = ID_TEAM_NAME[result[3]]
        res['Season'] = parameters['Season']
        res['Season Type'] = parameters['SeasonType']
        res['Per Mode'] = parameters['PerMode']
        for i in range(5):
            res[f'Player_Name{i+1}'] = None
            res[f'Player_ID{i+1}'] = None
        
        for i, player_name in enumerate(result[2].split(' - ')):
            res[f'Player_Name{i+1}'] = player_name.strip()
        for i, player_id in enumerate(result[1].split('-')[1:-1]):
            res[f'Player_ID{i+1}'] = int(player_id.strip())
        res['Lineup_Type'] = f'{parameters["GroupQuantity"]} Player Lineups'

        for p1, p2 in zip(list(PROCESS_LINEUPS[file].keys()), list(PROCESS_LINEUPS[file].values())):
            if p1.find('%')!=-1 or p1 in ['PIE']:
                res[p1] = round(result[dict_lst[p2]]*100, 3)
            else:
                res[p1] = round(result[dict_lst[p2]], 3)
        write_csv(f'lineups/{file}.csv', res)

def crawler(api, idx, n, file_name):
    '''
    Crawler data
    '''
    res = check_requests(api, HEADERS)
    if res.status_code == 200:
        print(log.status(title='lineups', idx=idx, n=n), file_name, end=' ')
        try:
            data = res.json()
            process(data)
            print(log.OK())
            write_log('lineups', f'[OK] {file_name}')
        except Exception as e:
            print(log.FAIL(f'!process: {e}'))
            write_log('lineups', f'\t !process: {e}')
    else:
        print(log.status(title='lineups', idx=idx, n=n), file_name, log.FAIL(), f'Status code: {res.status_code}')
        write_log('lineups', f'[OK] {file_name}: {res.status_code}')

def run():
    '''
    run crawler
    '''
    HEADERS['Host'] = 'stats.nba.com'
    HEADERS['Referer'] = 'https://stats.nba.com/draft/combine-anthro/'
    n = get_len()
    idx = 0
    for measure_type in MEASURE_TYPES_LINEUPS:
        BASE_PARAMS_LINEUPS['MeasureType'] = measure_type
        for season in get_seasons_by_year(START_YEAR, END_YEAR):
            BASE_PARAMS_LINEUPS['Season'] = season
            for season_type in SEASON_TYPES_LINEUPS:
                BASE_PARAMS_LINEUPS['SeasonType'] = season_type
                for group_quantity in GROUP_QUANTITY_LINEUPS:
                    BASE_PARAMS_LINEUPS['GroupQuantity'] = group_quantity
                    file_name = f"{measure_type}_{season}_{season_type}_{group_quantity}"
                    if measure_type in ['Advanced', 'Scoring']:
                        api = get_url_with_params(BASE_API_LINEUPS, BASE_PARAMS_LINEUPS)
                        crawler(api, idx, n, file_name)
                        idx += 1
                    else:
                        for per_mode in PER_MODES_LINEUPS:
                            BASE_PARAMS_LINEUPS['PerMode'] = per_mode
                            api = get_url_with_params(BASE_API_LINEUPS, BASE_PARAMS_LINEUPS)
                            crawler(api, idx, n, f'{file_name}_{per_mode}')
                            idx += 1
        print(log.OK(f'--------------- Done LineUps! ---------------'))

# --------
def setup_thread(measure_type):
    HEADERS['Host'] = 'stats.nba.com'
    HEADERS['Referer'] = 'https://stats.nba.com/draft/combine-anthro/'
    n = get_len([measure_type])
    idx = 0

    BASE_PARAMS_LINEUPS['MeasureType'] = measure_type
    for season in get_seasons_by_year(START_YEAR, END_YEAR):
        BASE_PARAMS_LINEUPS['Season'] = season
        for season_type in SEASON_TYPES_LINEUPS:
            BASE_PARAMS_LINEUPS['SeasonType'] = season_type
            for group_quantity in GROUP_QUANTITY_LINEUPS:
                BASE_PARAMS_LINEUPS['GroupQuantity'] = group_quantity
                file_name = f"{measure_type}_{season}_{season_type}_{group_quantity}"
                if measure_type in ['Advanced', 'Scoring']:
                    api = get_url_with_params(BASE_API_LINEUPS, BASE_PARAMS_LINEUPS)
                    crawler(api, idx, n, file_name)
                    idx += 1
                else:
                    for per_mode in PER_MODES_LINEUPS:
                        BASE_PARAMS_LINEUPS['PerMode'] = per_mode
                        api = get_url_with_params(BASE_API_LINEUPS, BASE_PARAMS_LINEUPS)
                        crawler(api, idx, n, f'{file_name}_{per_mode}')
                        idx += 1
    print(log.OK(f'--------------- Done LineUps: {[measure_type]} ---------------'))

def run_with_thread():
    try:
        t1 = Thread(target=setup_thread, args=('Base',))
        t2 = Thread(target=setup_thread, args=('Advanced',))
        t3 = Thread(target=setup_thread, args=('Misc',))
        t4 = Thread(target=setup_thread, args=('Four Factors',))
        t5 = Thread(target=setup_thread, args=('Scoring',))
        t6 = Thread(target=setup_thread, args=('Opponent',))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        print(log.OK('--------------- Done LineUps! ---------------'))
    except:
        print ("error")