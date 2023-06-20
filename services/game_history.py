import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from configs.nba_team import NBA_TEAM_SHORT_NAME
from utils.logging import logger
from utils.utils import get_timeline, is_ready


class GameHistory:
    def __init__(
        self, 
        start_date: str = "2016-01-01", 
        end_date: str = "2016-01-01", 
        path_data: str = "./data/game_history"
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.path_data = path_data
        self.timeline = get_timeline(self.start_date, self.end_date)

        self.service = ChromeService(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--incognito')

        self.game_ids = []
        self.years = []
        self.dates = []
        self.away_teams_name = []
        self.home_teams_name = []
        self.periods = []
        self.game_periods = []
        self.away_teams_score = []
        self.home_teams_score = []
        self.series_scores = []
        self.away_teams_leader = []
        self.home_teams_leader = []

        if not os.path.exists(self.path_data):
            logger("info", f"Create directory: {self.path_data}")
            os.makedirs(self.path_data)

    def get_game_id(self, game_card_element: WebElement):
        xpath_game_link = ".//section[@class='GameCard_gcMain__q1lUW']/a"
        game_link = game_card_element.find_element(By.XPATH, xpath_game_link)
        game_id = game_link.get_attribute('href').split('/')[-1].split('-')[-1]
        
        return game_id
    
    def get_team_name(self, game_card_element: WebElement):
        xpath_team_name = ".//span[@class='MatchupCardTeamName_teamName__9YaBA']"
        teams_name = game_card_element.find_elements(By.XPATH, xpath_team_name)
        away_team_name = teams_name[0].text
        home_team_name = teams_name[1].text

        return away_team_name, home_team_name
    
    def get_team_score(self, game_card_element: WebElement):
        xpath_total_scores = ".//p[@class='MatchupCardScore_p__dfNvc GameCardMatchup_matchupScoreCard__owb6w']"
        total_scores = game_card_element.find_elements(By.XPATH, xpath_total_scores)
        away_team_score = total_scores[0].text
        home_team_score = total_scores[1].text

        return away_team_score, home_team_score
    
    def get_team_leader(self, game_card_element: WebElement, away_team_name: str, home_team_name: str):
        # Try to get all game leaders
        xpath_table_game_card_leader = ".//table[@class='GameCardLeaders_gclTable__iiNs9']"
        xpath_trow_game_card_leader = ".//tr[@class='GameCardLeaders_gclRow__VMSee']"
        table_game_card_leader = game_card_element.find_element(By.XPATH, xpath_table_game_card_leader)
        trow_game_card_leader = table_game_card_leader.find_elements(By.XPATH, xpath_trow_game_card_leader)

        # Each rows have 2 game leader, for each row has 4 cell (Player name, pts, reb, ast)
        game_leaders = {
            'away_team': {},
            'home_team': {}
        }

        for row in trow_game_card_leader:
            tds_game_card_leader = row.find_elements(By.XPATH, ".//td")

            try:
                xpath_leader_name = ".//p[@class='GameCardLeaders_gclName__Oh5iE']"
                xpath_team_name_short = ".//p[@class='GameCardLeaders_gclInfo__6QvJ_']"
                leader_name = tds_game_card_leader[0].find_element(By.XPATH, xpath_leader_name).text
                team_name_short = tds_game_card_leader[0].find_element(By.XPATH, xpath_team_name_short).text
                # Sample: ORL | #5 | G
                team_name_short = team_name_short.split('|')[0].strip()

                leader_pts = tds_game_card_leader[1].text
                leader_reb = tds_game_card_leader[2].text
                leader_ast = tds_game_card_leader[3].text

                if team_name_short not in NBA_TEAM_SHORT_NAME.keys():
                    logger("warning", f"No team name short: '{team_name_short}'")

                if NBA_TEAM_SHORT_NAME[team_name_short] == away_team_name:
                    team_key = 'away_team'
                elif NBA_TEAM_SHORT_NAME[team_name_short] == home_team_name:
                    team_key = 'home_team'
                else:
                    logger("warning", f"No team full name for '{team_name_short}' " \
                            f"match with '{away_team_name}' or '{home_team_name}'")
                    continue

                game_leaders[team_key]['name'] = leader_name
                game_leaders[team_key]['pts'] = leader_pts
                game_leaders[team_key]['reb'] = leader_reb
                game_leaders[team_key]['ast'] = leader_ast
            except:
                logger("warning", "No game leader!")
            
        return game_leaders

    def get_period(self, game_card_element: WebElement):
        try:
            xpath_period = ".//p[@class='GameCardMatchup_gamePlayoffRoundText__Sy2Tn']"
            period = game_card_element.find_element(By.XPATH, xpath_period).text
        except:
            period = ''

        return period
    
    def get_game_period_sscore(self, game_card_element: WebElement):
        try:
            xpath_game_period = ".//p[@class='GameCardMatchup_gameSeriesText__zqvUF']"
            game_period = game_card_element.find_element(By.XPATH, xpath_game_period).text
            if game_period[-1].isnumeric():
                sscore = game_period.split(' ')[-1]
            else:
                sscore = ''
        except:
            game_period = ''
            sscore = ''
        
        return game_period, sscore
    
    @staticmethod
    def get_page_by_date(date: str = "2016-01-01") -> str:
        return f"https://www.nba.com/games?date={date}"

    def crawler(self):
        browser = webdriver.Chrome(service=self.service, options=self.options)

        for time_step in self.timeline:
            date_str = time_step.strftime("%Y-%m-%d")
            link = self.get_page_by_date(date_str)

            browser.get(link)
            WebDriverWait(browser, 10).until(is_ready)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(browser, 10).until(is_ready)

            # Inspect the page to get elements
            xpath_game_card_mapper = "//div[@class='GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg']"
            game_card_mapper = browser.find_elements(By.XPATH, xpath_game_card_mapper)

            flag = True
            if len(game_card_mapper) == 0:
                flag = False
                logger("warning", f"Page: '{link}' No game in day!")
            
            for game_card in game_card_mapper:
                try:
                    xpath_preseason = ".//span[@class='GameCardMatchupStatusText_gcsPre__rnEtg']"
                    preseason = game_card.find_element(By.XPATH, xpath_preseason)
                    if preseason.text.lower() == "preseason":
                        logger("warning", f"Page: '{link}' Preseason game!")
                        continue
                except:
                    pass

                game_id = self.get_game_id(game_card)
                away_team_name, home_team_name = self.get_team_name(game_card)
                away_team_score, home_team_score = self.get_team_score(game_card)
                game_leaders = self.get_team_leader(game_card, away_team_name, home_team_name)
                period = self.get_period(game_card)
                game_period, sscore = self.get_game_period_sscore(game_card)

                self.game_ids.append(game_id)
                self.years.append(time_step.year)
                self.dates.append(date_str)
                self.away_teams_name.append(away_team_name)
                self.home_teams_name.append(home_team_name)
                self.periods.append(period)
                self.game_periods.append(game_period)
                self.away_teams_score.append(away_team_score)
                self.home_teams_score.append(home_team_score)
                self.series_scores.append(sscore)

                game_leader_str_pattern = "{name} ({pts}, {reb}, {ast})"
                # Check empty game leader dict
                if not any(game_leaders.values()):
                    self.away_teams_leader.append('')
                    self.home_teams_leader.append('')
                elif game_leaders['away_team'] == {}:
                    self.away_teams_leader.append('')
                    self.home_teams_leader.append(game_leader_str_pattern.format(**game_leaders['home_team']))
                elif game_leaders['home_team'] == {}:
                    self.away_teams_leader.append(game_leader_str_pattern.format(**game_leaders['away_team']))
                    self.home_teams_leader.append('')
                else:
                    self.away_teams_leader.append(game_leader_str_pattern.format(**game_leaders['away_team']))
                    self.home_teams_leader.append(game_leader_str_pattern.format(**game_leaders['home_team']))

            if flag:
                logger("info", f"Page: '{link}' Done!")
                flag = True

            if time_step.is_month_end:
                self.save_dataframe(f"{self.path_data}/game_history_{date_str}.csv")

            time.sleep(2)

    def save_dataframe(self, path):
        df = pd.DataFrame({
            'game_id': self.game_ids,
            'year': self.years,
            'date': self.dates,
            'away_team_name': self.away_teams_name,
            'home_team_name': self.home_teams_name,
            'period': self.periods,
            'game_period': self.game_periods,
            'away_team_score': self.away_teams_score,
            'home_team_score': self.home_teams_score,
            'series_score': self.series_scores,
            'away_team_leader': self.away_teams_leader,
            'home_team_leader': self.home_teams_leader
        })

        if df.empty:
            logger("warning", "Empty dataframe!")
            return
        
        df.to_csv(path, index=False, encoding='utf-8')
        logger("success", f"Save dataframe to: {path}")