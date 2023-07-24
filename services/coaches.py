''''
Huan luyen vien
'''

# import sys
# sys.path.append('..')
from configs.params import (
    START_YEAR, 
    END_YEAR
)
from configs.nba_team import NBA_FULL_NAME
from utils.utils import (
    write_csv,
    write_log,
    get_year,
    check_requests
)
from utils import logging
log = logging.Logger()

from bs4 import BeautifulSoup

URL_COACHES = 'https://www.basketball-reference.com/leagues/NBA_{year}_coaches.html'

EXTRACT_COACHES = {
    'Coaches_Name': 'coach',
    'Coaches_Team': 'team',
    'Seasons_w/Franch_#': 'seas_num_franch',
    'Seasons_Overall_#': 'seas_num_overall',
    'Regular Season_Current Season_G': 'cur_g',
    'Regular Season_Current Season_W': 'cur_w',
    'Regular Season_Current Season_L': 'cur_l',
    'Regular Season_w/Franchise_G': 'fr_g',
    'Regular Season_w/Franchise_W': 'fr_w',
    'Regular Season_w/Franchise_L': 'fr_l',
    'Regular Season_Career_G': 'car_g',
    'Regular Season_Career_W': 'car_w',
    'Regular Season_Career_L': 'car_l',
    'Regular Season_W%': 'car_wpct',
    'Playoffs_Current Season_G': 'cur_g_p',
    'Playoffs_Current Season_W': 'cur_w_p',
    'Playoffs_Current Season_L': 'cur_l_p',
    'Playoffs_w/Franchise_G': 'fr_g_p',
    'Playoffs_w/Franchise_W': 'fr_w_p',
    'Playoffs_w/Franchise_L': 'fr_l_p',
    'Playoffs_Career_G': 'car_g_p',
    'Playoffs_Career_W': 'car_w_p',
    'Playoffs_Career_L': 'car_l_p'
}

TIMELINE = range(int(get_year(START_YEAR))+1, int(get_year(END_YEAR))+2)

def run():
    for idx, year in enumerate(TIMELINE):
        try:
            req = check_requests(URL_COACHES.format(year=year))
            if req.status_code != 200:
                print(log.status(title='Coaches', idx=idx, n=len(TIMELINE)), year, log.FAIL(), f'Status code: {req.status_code}')
                write_log('coaches', f'[FAIL] {year}: {req.status_code}')
                continue
            print(log.status(title='Coaches', idx=idx, n=len(TIMELINE)), year, log.OK())
            write_log('coaches', f'[OK] {year}')
            soup = BeautifulSoup(req.text, 'html.parser')
            trs = soup.find('table', {'id': 'NBA_coaches'}).find('tbody').find_all('tr')
            data = EXTRACT_COACHES.fromkeys(EXTRACT_COACHES.keys())
            for tr in trs:
                data['Coaches_Name'] = tr.find('th').text
                data['Coaches_Team'] = NBA_FULL_NAME[tr.find('td', {'data-stat': 'team'}).text]
                for _ in list(data.keys())[2:]:
                    in4 = tr.find('td', {'data-stat': EXTRACT_COACHES[_]}).text
                    if _.find('%') != -1:
                        data[_] = float(in4) if in4 != '' else ''
                    else:
                        data[_] = int(in4) if in4 != '' else ''
                write_csv('coaches.csv', data)
        except Exception as e:
            print(log.FAIL(), f': {e}')
    print(log.OK('--------------- Done Coaches! ---------------'))