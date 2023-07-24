from configs.params import (
    START_YEAR, 
    END_YEAR,
    HEADERS
)
from utils.utils import (
    write_csv,
    write_log,
    check_requests,
    get_seasons_by_year,
    get_url_with_params,
    get_year,
    process_data,
    save_json
)
from utils import logging
log = logging.Logger()

# - set configs params

URL = 'https://stats.nba.com/stats/leaguestandingsv3?GroupBy=conf&LeagueID=00&Season={season}&SeasonType=Regular Season&Section=overall'
HEADERS['Host'] = 'stats.nba.com'
HEADERS['Referer'] = 'https://www.nba.com/'
group_by = {
    'Conference': {
        'Rank': 'PlayoffRank',
        'GB': 'ConferenceGamesBack',
        'Conference': 'Conference'
    },
    'Division': {
        'Rank': 'DivisionRank',
        'GB': 'DivisionGamesBack',
        'Division': 'Division'
    }
}
sections = {
    'Overall': 'overall',
    'Streaks': 'streaks',
    'Ahead_or_behind': 'ab',
    'Margins_and_stats': 'margins',
    'vs div_or_conf': 'vs'
}
process = {
    'Overall': {
        'CONF': 'vsEast',
        'DIV': 'vsAtlantic',
        'HOME': 'HOME',
        'ROAD': 'ROAD',
        'OT': 'OT',
        'LAST10': 'L10',
        'STREAK': 'strCurrentStreak'
    },
    'Streaks': {
        'CURRENT': 'strCurrentStreak',
        'HOME': 'strCurrentHomeStreak',
        'ROAD': 'strCurrentRoadStreak',
        'LAST10': 'L10',
        'L10 HOME': 'Last10Home',
        'L10 ROAD': 'Last10Road',
        'HOME LONG': 'strLongHomeStreak',
        'ROAD LONG': 'strLongRoadStreak'
    },
    'Ahead_or_behind': {
        'AHEAD HALF': 'AheadAtHalf',
        'BEHIND HALF': 'BehindAtHalf',
        'TIED HALF': 'TiedAtHalf',
        'AHEAD 3RD': 'AheadAtThird',
        'BEHIND 3RD': 'BehindAtThird',
        'TIED 3RD': 'TiedAtThird',
        'PTS/G': 'PointsPG',
        'PA/G': 'OppPointsPG',
        '+/-': 'DiffPointsPG'
    },
    'Margins_and_stats': {
        '3PTS OR LESS': 'ThreePTSOrLess',
        '10PTS OR MORE': 'TenPTSOrMore',
        'SCORE 100+': 'Score100PTS',
        'OPP SCORE100+': 'OppScore100PTS',
        'OPP .500+': 'OppOver500',
        'LEAD FG%': 'LeadInFGPCT',
        'LEAD REB': 'LeadInReb',
        'FEWER TOV': 'FewerTurnovers'
    },
    'vs div_or_conf': {
        'EAST': 'vsEast',
        'WEST': 'vsWest',
        'ATLANTIC': 'vsAtlantic',
        'CENTRAL': 'vsCentral',
        'SOUTHEAST': 'vsSoutheast',
        'NORTHWEST': 'vsNorthwest',
        'PACIFIC': 'vsPacific',
        'SOUTHWEST': 'vsSouthwest'
    }
}
def get_urls():
    urls = []
    seasons = get_seasons_by_year(START_YEAR, END_YEAR)
    for season in seasons:
        urls.append((URL.format(season=season), season))
    return urls
def crawler():
    urls = get_urls()
    for idx, (url, season) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title='Team_standing', idx=idx, n=len(urls)), log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_standing', f'{season}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for section in sections:
                data = {}
                for rowset in resultSets['rowSet']:
                    team_id = rowset[headers_idx['TeamID']]
                    team_name = rowset[headers_idx['TeamName']]
                    team_city = rowset[headers_idx['TeamCity']]
                    data['Team_id'] = team_id
                    data['Team_name'] = f'{team_city} {team_name}'
                    data['W'] = rowset[headers_idx['WINS']]
                    data['L'] = rowset[headers_idx['LOSSES']]
                    data['WIN%'] = round(rowset[headers_idx['WinPCT']]*100, 3)
                    for i in process[section]:
                        num =  rowset[headers_idx[process[section][i]]]
                        if i.find('%') != -1:
                            data[i] = process_data(num, percent=True)
                        else:
                            data[i] = process_data(num)
                    for i in group_by:
                        data['Group_by'] = i
                        for j in group_by[i]:
                            data[j] = rowset[headers_idx[group_by[i][j]]]
                    write_csv(f'Team_standing/{section}.csv', data)
                print(log.status(title=f'Team_standing/{section}', idx=idx, n=len(urls)), log.OK(f'{season}'))
                write_log('Team_standing', f'[{section}] {season}, [OK]')
        except Exception as e:
            print(log.status(title='Team_standing', idx=idx, n=len(urls)), f'{season}', log.FAIL(e))
            write_log('Team_standing', f'[{section}] {season}, [FAIL] {e}')

def run():
    crawler()