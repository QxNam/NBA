import time
import pandas as pd

from collections import defaultdict
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from configs.nba_team import NBA_FULL_NAME
from utils.logging import logger
from utils.utils import (
    is_ready,
    create_folder_if_not_existed
)


class TeamInfo:
    def __init__(
        self,
        start_year: int = 2017,
        end_year: int = 2017,
        path_data: str = './data/team_info',
    ):
        self.start_year = start_year
        self.end_year = end_year
        self.path_data = path_data

        self.service = ChromeService(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--incognito')

        self.years = list(range(self.start_year, self.end_year + 1))
        self.keys_roster = ['no.', 'player', 'pos', 'height', 'weight', 'birth_date', 'country', 'exp', 'college']
        self.keys_salary = ['player', 'salary']

        create_folder_if_not_existed(self.path_data)
    
    @staticmethod
    def get_page_by_name_year(short_name: str = 'ATL', year: int = 2017):
        return f'https://www.basketball-reference.com/teams/{short_name}/{year}.html'
    

    def get_roster(self, soup: BeautifulSoup, team_name, year, year_str):
        roster = defaultdict(list)

        # Table Roster
        table_roster = soup.find('table', {'id': 'roster'})
        tbody_roster = table_roster.find('tbody')
        rows_roster = tbody_roster.find_all('tr')

        for row in rows_roster:
            clothers_number = row.find('th')
            if clothers_number.text.strip() == 'No.':
                continue
            
            roster['no.'].append(clothers_number.text.strip())
            roster['team_name'].append(team_name)
            roster['year'].append(year)
            roster['year_str'].append(year_str)
            
            cells_roster = row.find_all('td')
            for key, cell in zip(self.keys_roster[1:], cells_roster):
                roster[key].append(cell.text.strip())
        
        return roster
    
    def get_salary(self, soup: BeautifulSoup):
        salary = defaultdict(list)

       # Table Salary
        table_salary = soup.find('table', {'id': 'salaries2'})
        rows_salary = table_salary.find_all('tr')
        for row in rows_salary:
            cells_salary = row.find_all('td')
            for key, cell in zip(self.keys_salary, cells_salary):
                salary[key].append(cell.text.strip())
        
        return salary

    def crawler(self):
        browser = webdriver.Chrome(service=self.service, options=self.options)
        
        for key_full_name in NBA_FULL_NAME.keys():
            data_team = pd.DataFrame()

            for year in self.years:
                roster = defaultdict(list)
                salary = defaultdict(list)

                year_str = f'{year - 1}-' + str(year)[2:]
                link = self.get_page_by_name_year(short_name=key_full_name, year=year)

                browser.get(link)
                WebDriverWait(browser, 10).until(is_ready)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(browser, 10).until(is_ready)

                html_content = browser.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                
                team_name = NBA_FULL_NAME[key_full_name]

                roster = self.get_roster(soup=soup, team_name=team_name, year=year, year_str=year_str)
                salary = self.get_salary(soup=soup)
                
                df_roster = pd.DataFrame(roster)
                df_salary = pd.DataFrame(salary)

                df = pd.merge(df_roster, df_salary, on='player', how='left')
                data_team = pd.concat([data_team, df], ignore_index=True)
                
                logger("success", f"Page: '{link}' done!")
                time.sleep(2)

            data_team.to_csv(f'{self.path_data}/{team_name}.csv', index=False)
            logger("success", f"Saved data at: '{self.path_data}/{team_name}.csv'")
    
        browser.quit()
