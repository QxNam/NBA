'''
Thong tin chan thuong cua cac cau thu trong mua giai
'''

import sys
sys.path.append('..')

from configs.params import (
    START_YEAR, 
    END_YEAR
)
from configs.nba_team import ID_TEAM_NAME
from utils.utils import (
    get_day, 
    write_csv,
    write_log,
    check_requests
)
from utils import logging
log = logging.Logger()

from bs4 import BeautifulSoup

URL_INJURY = "https://www.prosportstransactions.com/basketball/Search/SearchResults.php?Player=&Team=&BeginDate={start_day}&EndDate={end_day}&ILChkBx=yes&InjuriesChkBx=yes&Submit=Search"
trans_teams = {team_name.split(' ')[-1]:team_name for team_name in ID_TEAM_NAME.values()}

def crawler(url:str, idx, n) -> None:
    data = {'Date': [], 'Team': [], 'Acquired': [], 'Relinquished': [], 'Status': [], 'Notes': []}
    try:
        page = check_requests(url)
        if page.status_code != 200:
            print(log.status(title='injury_info', idx=idx, n=n), url.split('&')[-1], log.FAIL(), f'Status code: {page.status_code}')
            write_log('injury_info', f'[FAIL] {url.split("&")[-1]}: {page.status_code}')
            return
        print(log.status(title='injury_info', idx=idx, n=n), url.split('&')[-1], log.OK())
        write_log('injury_info', f'[OK] {url.split("&")[-1]}')
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', attrs={'class': 'datatable center'})
        tr_elements = table.find_all('tr')
        for tr in tr_elements[1:]:
            td_elements = tr.find_all('td')
            data['Date']=td_elements[0].text.strip()
            data['Team']=trans_teams[td_elements[1].text.strip()]
            data['Acquired']=td_elements[2].text.strip().replace('• ', '')
            data['Relinquished']=td_elements[3].text.strip().replace('• ', '')
            data['Status']=data['Acquired'] + data['Relinquished']
            data['Notes']=td_elements[4].text.strip()
            write_csv('injury_info.csv', data)
    except Exception as e:
        print(log.FAIL(), f': {e}')

def run():
    s_day = get_day(START_YEAR, is_start_day=True)
    e_day = get_day(END_YEAR)
    url = URL_INJURY.format(start_day=s_day, end_day=e_day)
    page = check_requests(url)
    if page.status_code != 200:
        print(log.FAIL(), f'Status code: {page.status_code}')
        return
    soup = BeautifulSoup(page.content, 'html.parser')
    n = int(soup.find_all('p', attrs={'class': 'bodyCopy'})[2].find_all('a')[-1].text)
    for page in range(n):
        link = f"{url}&start={page*25}"
        crawler(link, page, n)
    print(log.OK('--------------- Done injury_info! ---------------'))
