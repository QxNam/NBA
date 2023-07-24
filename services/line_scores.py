# import sys
# sys.path.append('..')
from utils import logging
log = logging.Logger()

from utils.utils import (
    write_csv,
    write_log,
    get_timeline,
    get_day,
    check_requests
)
from configs.params import (
    HEADERS,
    START_YEAR,
    END_YEAR,
)
from configs.nba_team import ID_TEAM_NAME
import json

# congig
URL_LINESCORES = "https://global.nba.com/statsm2/scores/daily.json?gameDate={date}"
EXTRACT_DATA = {
    'GameID': 'gameId',
    'GameDate': '',
    'Location': {
        'arena_name': 'arenaName',
        'arena_location': 'arenaLocation'
    },
    'Attendance':'attendance',
    'Team': 'id',
    'Score': 'score',
    'Q1': 'q1Score',
    'Q2': 'q2Score',
    'Q3': 'q3Score',
    'Q4': 'q4Score',
    'OT1': 'ot1Score',
    'OT2': 'ot2Score',
    'OT3': 'ot3Score',
    'OTOthers': '',
    'PITP': 'pointsInPaint',
    'FB_PTS': 'fastBreakPoints',
    'BIG_LD': 'biggestLead'
}

def process(game_data: dict, day: str) -> None:
    payload = game_data['payload']

    if payload['date'] == None:
        print('No match in this day!')
        write_log('line_scores', '+ No match in this day!')
        return

    list_games = payload['date']['games']
    #.fromkeys(EXTRACT_DATA.keys(), '')

    for idx_game, game in enumerate(list_games):
        data = {}
        print(f'{idx_game+1}/{len(list_games)}', end=' ')
        try:
        # Game ID
            data['GameID']=game['profile'][EXTRACT_DATA['GameID']]

            # Year, Date of game
            data['GameDate']=day

            # Get location
            arena_name = game['profile'][EXTRACT_DATA['Location']['arena_name']]
            arena_location = game['profile'][EXTRACT_DATA['Location']['arena_location']]
            data['Location'] = f'{arena_name}_{arena_location}'

            # Get attendance
            data['Attendance'] = int(game['boxscore'][EXTRACT_DATA['Attendance']].replace(',', ''))

            # get each team
            others_ot_score_keys = [f'ot{times}Score' for times in range(4, 11)]
            for idx, team_key in enumerate(['awayTeam', 'homeTeam']):
                team = game[team_key]
                team_id = int(team['profile'][EXTRACT_DATA['Team']])
                data[f'Team_{idx+1}_id']=team_id
                if team_id in ID_TEAM_NAME.keys():
                    data[f'Team_{idx+1}_name']=ID_TEAM_NAME[team_id]
                else:
                    data[f'Team_{idx+1}_name']=team["profile"]["name"]
                    print(log.WARN(), f'{team_id}: {team["profile"]["name"]}', end=' ')
                    write_log('line_scores', f'---> {team_id}: {team["profile"]["name"]}')
                team_score = team['score']
                data[f'Team_{idx+1}_Score']=team_score[EXTRACT_DATA['Score']]
                data[f'Team_{idx+1}_Q1']=team_score[EXTRACT_DATA['Q1']]
                data[f'Team_{idx+1}_Q2']=team_score[EXTRACT_DATA['Q2']]
                data[f'Team_{idx+1}_Q3']=team_score[EXTRACT_DATA['Q3']]
                data[f'Team_{idx+1}_Q4']=team_score[EXTRACT_DATA['Q4']]
                data[f'Team_{idx+1}_OT1']=team_score[EXTRACT_DATA['OT1']]
                data[f'Team_{idx+1}_OT2']=team_score[EXTRACT_DATA['OT2']]
                data[f'Team_{idx+1}_OT3']=team_score[EXTRACT_DATA['OT3']]
                data[f'Team_{idx+1}_OTOthers']=sum([team_score[score_key] for score_key in others_ot_score_keys])
                data[f'Team_{idx+1}_PITP']=team_score[EXTRACT_DATA['PITP']]
                data[f'Team_{idx+1}_FB_PTS']=team_score[EXTRACT_DATA['FB_PTS']]
                data[f'Team_{idx+1}_BIG_LD']=team_score[EXTRACT_DATA['BIG_LD']]
            write_csv(f'line_scores.csv', data)
            print(log.OK('OK'), end=', ')
            write_log('line_scores', f'+ ({idx_game+1}/{len(list_games)}) [OK]')
        except Exception as e:
            print(log.FAIL('FAIL'), f': {e}', end=', ')
            write_log('line_scores', f'+ ({idx_game+1}/{len(list_games)}) [FAIL]: {e}')
            continue
    print()

        


def run():
    HEADERS['Host'] = 'global.nba.com'
    HEADERS['Referer'] = 'https://global.nba.com/scores/'
    timeline = get_timeline(get_day(START_YEAR, is_start_day=True), get_day(END_YEAR))
    for idx, time_step in enumerate(timeline):
        date_str = time_step.strftime("%Y-%m-%d")
        api = URL_LINESCORES.format(date=date_str)
        res = check_requests(api, HEADERS)
        if res.status_code == 200:
            res = json.loads(res.text)
            print(log.status(title='line_scores', idx=idx, n=len(timeline)), date_str, log.OK(), end = ' -> ')
            write_log('line_scores', f'[OK] {date_str}')
        else:
            print(log.status(title='line_scores', idx=idx, n=len(timeline)), date_str, log.FAIL(), f'Status code: {res.status_code}')
            write_log('line_scores', f'[FAIL] {date_str}: {res.status_code}')
            continue
        process(res, date_str)
    print(log.OK('--------------- Done line_scores! ---------------'))

# def debug(day='2016-02-13'):
#     HEADERS['Host'] = 'global.nba.com'
#     HEADERS['Referer'] = 'https://global.nba.com/scores/'
#     api = URL_LINESCORES.format(date=day)
#     res = check_requests(api, HEADERS)
#     if res.status_code == 200:
#         res = json.loads(res.text)
#         process(res, day)
#     else:
#         print(res.status_code)