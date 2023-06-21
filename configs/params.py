# Common params
HEADERS = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
    'Referer': '',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

# LineUps
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
SEASON_TYPES_LINEUPS = ['Regular Season', 'Playoffs', 'All Star', 'PlayIn']
PER_MODES_LINEUPS = ['Totals', 
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

# Team standing
BASE_API_TEAM_STANDING = 'https://stats.nba.com/stats/leaguestandingsv3'
BASE_PARAMS_TEAM_STANDING = {
    'GroupBy': 'conf',
    'LeagueID': '00',
    'Season': '2016-17',
    'SeasonType': 'Regular Season',
    'Section': 'overall'
}