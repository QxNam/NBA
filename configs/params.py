# Common params configs
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

# LineUps configs
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

# Team standing configs
BASE_API_TEAM_STANDING = 'https://stats.nba.com/stats/leaguestandingsv3'
BASE_PARAMS_TEAM_STANDING = {
    'GroupBy': 'conf',
    'LeagueID': '00',
    'Season': '2016-17',
    'SeasonType': 'Regular Season',
    'Section': 'overall'
}

# Coaches configs
BASE_URL_COACHES = 'https://www.basketball-reference.com/leagues/NBA_{year}_coaches.html'

# All configs below for Team stats
TEAM_STATS_API_NAMES = ['General', 'Clutch', 'Playtype', 'Tracking', 'DefenseDashboard', 'ShotDashboard', \
                        'Shooting', 'OpponentShooting', 'Hustle', 'BoxScores', 'AdvancedBoxScores']
# General configs
BASE_API_GENERAL = 'https://stats.nba.com/stats/leaguedashteamstats'
BASE_PARAMS_GENERAL = {
    'Conference': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'GameScope': '',
    'GameSegment': '',
    'Height': '',
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
    'PlayerExperience': '',
    'PlayerPosition': '',
    'PlusMinus': 'N',
    'Rank': 'N',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'ShotClockRange': '',
    'StarterBench': '',
    'TeamID': '0',
    'TwoWay': '0',
    'VsConference': '',
    'VsDivision': ''
}
MEASURE_TYPES_GENERAL = ['Base', 'Advanced', 'Four Factors', 'Misc', 'Scoring', 'Opponent', 'Defense']
SEASON_TYPES_GENERAL = ['Pre Season', 'Regular Season', 'Playoffs', 'All Star', 'PlayIn']
PER_MODES_GENERAL = ['Totals', 'PerGame', 'Per100Possessions', 'Per100Plays', 'Per48', 'Per40', 'Per36', \
                     'PerMinute', 'PerPossession', 'PerPlay', 'MinutesPer']

# Clutch configs
BASE_API_CLUTCH = 'https://stats.nba.com/stats/leaguedashteamclutch'
BASE_PARAMS_CLUTCH = {
    'AheadBehind': 'Ahead or Behind',
    'ClutchTime': 'Last 5 Minutes',
    'College': '',
    'Conference': '',
    'Country': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'DraftPick': '',
    'DraftYear': '',
    'GameScope': '',
    'GameSegment': '',
    'Height': '',
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
    'PlayerExperience': '',
    'PlayerPosition': '',
    'PlusMinus': 'N',
    'PointDiff': '5',
    'Rank': 'N',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'ShotClockRange': '',
    'StarterBench': '',
    'TeamID': '0',
    'VsConference': '',
    'VsDivision': '',
    'Weight': ''
}
MEASURE_TYPES_CLUTCH = ['Base', 'Advanced', 'Four Factors', 'Misc', 'Scoring', 'Opponent']
SEASON_TYPES_CLUTCH = ['Pre Season', 'Regular Season', 'Playoffs', 'All Star', 'PlayIn']
PER_MODES_CLUTCH = ['Totals', 'PerGame', 'Per100Possessions', 'Per100Plays', 'Per48', 'Per40', 'Per36', \
                    'PerMinute', 'PerPossession', 'PerPlay', 'MinutesPer']

# Playtype configs
BASE_API_PLAYTYPE = 'https://stats.nba.com/stats/synergyplaytypes'
BASE_PARAMS_PLAYTYPE = {
    'LeagueID': '00',
    'PerMode': 'PerGame',
    'PlayType': 'Isolation',
    'PlayerOrTeam': 'T',
    'SeasonType': 'Playoffs',
    'SeasonYear': '2022-23',
    'TypeGrouping': 'offensive'
}
PLAYTYPES = ['Isolation', 'Transition', 'PRBallHandler', 'PRRollman', 'Postup', 'Spotup', \
              'Handoff', 'Cut', 'OffScreen', 'OffRebound', 'Misc']
SEASON_TYPES_PLAYTYPE  = ['Regular Season', 'Playoffs']
PER_MODES_PLAYTYPE = ['Totals', 'PerGame']
OFF_DEF = ['offensive', 'defensive']

# Tracking configs
BASE_API_TRACKING = 'https://stats.nba.com/stats/leaguedashptstats'
BASE_PARAMS_TRACKING = {
    'College': '',
    'Conference': '',
    'Country': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'DraftPick': '',
    'DraftYear': '',
    'GameScope': '',
    'Height': '',
    'LastNGames': '0',
    'LeagueID': '00',
    'Location': '',
    'Month': '0',
    'OpponentTeamID': '0',
    'Outcome': '',
    'PORound': '0',
    'PerMode': 'PerGame',
    'PlayerExperience': '',
    'PlayerOrTeam': 'Team',
    'PlayerPosition': '',
    'PtMeasureType': 'Drives',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'StarterBench': '',
    'TeamID': '0',
    'VsConference': '',
    'VsDivision': '',
    'Weight': ''
}
# Defensive Impact: Defense
# Touches: Possessions
# Post Up: PostTouch
PT_MEASURE_TYPES = ['Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', \
                    'Rebounding', 'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch']
SEASON_TYPES_TRACKING = ['Regular Season', 'Playoffs', 'All Star', 'PlayIn']
PER_MODES_TRACKING = ['Totals', 'PerGame']

# Defense Dashboard configs
BASE_API_DEFENSE = 'https://stats.nba.com/stats/leaguedashptteamdefend'
BASE_PARAMS_DEFENSE = {
    'Conference': '',
    'DateFrom': '',
    'DateTo': '',
    'DefenseCategory': 'Overall',
    'Division': '',
    'GameSegment': '',
    'LastNGames': '0',
    'LeagueID': '00',
    'Location': '',
    'Month': '0',
    'OpponentTeamID': '0',
    'Outcome': '',
    'PORound': '0',
    'PerMode': 'PerGame',
    'Period': '0',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'TeamID': '0',
    'VsConference': '',
    'VsDivision': ''
}
DEFENSE_CATEGORIES = ['Overall', '3 Pointers', '2 Pointers', 'Less Than 6Ft', 'Less Than 10Ft', 'Greater Than 15Ft']
SEASON_TYPES_DEFENSE = ['Regular Season', 'Playoffs', 'All Star', 'PlayIn']

# Shot Dashboard configs
BASE_API_SHOT = 'https://stats.nba.com/stats/leaguedashteamptshot'
BASE_PARAMS_SHOT = {
    'CloseDefDistRange': '',
    'College': '',
    'Conference': '',
    'Country': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'DraftPick': '',
    'DraftYear': '',
    'DribbleRange': '',
    'GameScope': '',
    'GameSegment': '',
    'GeneralRange': '',
    'Height': '',
    'LastNGames': '0',
    'LeagueID': '00',
    'Location': '',
    'Month': '0',
    'OpponentTeamID': '0',
    'Outcome': '',
    'PORound': '0',
    'PaceAdjust': 'N',
    'PerMode': 'PerGame',
    'Period': '0',
    'PlayerExperience': '',
    'PlayerPosition': '',
    'PlusMinus': 'N',
    'Rank': 'N',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'ShotClockRange': '',
    'ShotDistRange': '',
    'StarterBench': '',
    'TeamID': '0',
    'TouchTimeRange': '',
    'VsConference': '',
    'VsDivision': '',
    'Weight': ''
}
SHOT_TYPES = ['General', 'ShotClock', 'Dribble', 'TouchTime', 'ClosestDef', 'ClosestDef10']
SEASON_TYPES_SHOT = ['Regular Season', 'Playoffs', 'All Star', 'PlayIn']
GENERAL_RANGE = ['Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10Ft']
SHOT_CLOCK_RANGE = ['24-22', '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late']
DRIBBLE_RANGE = ['0 Dribbles', '1 Dribbles', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles']
TOUCH_TIME_RANGE = ['Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds']
CLOSEST_DEF_RANGE = ['0-2 Feet - Very Tight', '2-4 Feet - Tight', '4-6 Feet - Open', '6+ Feet - Wide Open']
PER_MODES_SHOT = ['Totals', 'PerGame']

# Shooting configs
BASE_API_SHOOTING = 'https://stats.nba.com/stats/leaguedashteamshotlocations'
BASE_PARAMS_SHOOTING = {
    'Conference': '',
    'DateFrom': '',
    'DateTo': '',
    'DistanceRange': '5ft Range',
    'Division': '',
    'GameScope': '',
    'GameSegment': '',
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
    'PlayerExperience': '',
    'PlayerPosition': '',
    'PlusMinus': 'N',
    'Rank': 'N',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'ShotClockRange': '',
    'StarterBench': '',
    'TeamID': '0',
    'VsConference': '',
    'VsDivision': ''
}
SEASON_TYPES_SHOOTING = ['Pre Season', 'Regular Season', 'Playoffs', 'All Star', 'PlayIn']
PER_MODES_SHOOTING = ['Totals', 'PerGame']
DISTANCE_RANGE = ['5ft Range', '8ft Range', 'By Zone']

# Opponent Shooting configs
BASE_API_OPP_SHOOTING = 'https://stats.nba.com/stats/leaguedashoppptshot'
OPP_SHOOTING_MEASURE_TYPES = ['Opponent', 'General', 'ShotClock', 'Dribble', 'TouchTime', 'ClosestDef', 'ClosestDef10']

# Hustle configs
BASE_API_HUSTLE = 'https://stats.nba.com/stats/leaguehustlestatsteam'
BASE_PARAMS_HUSTLE = {
    'College': '',
    'Conference': '',
    'Country': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'DraftPick': '',
    'DraftYear': '',
    'GameScope': '',
    'Height': '',
    'LastNGames': '0',
    'LeagueID': '00',
    'Location': '',
    'Month': '0',
    'OpponentTeamID': '0',
    'Outcome': '',
    'PORound': '0',
    'PaceAdjust': 'N',
    'PerMode': 'PerGame',
    'PlayerExperience': '',
    'PlayerPosition': '',
    'PlusMinus': 'N',
    'Rank': 'N',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Playoffs',
    'ShotClockRange': '',
    'TeamID': '0',
    'VsConference': '',
    'VsDivision': '',
    'Weight': ''
}
SEASON_TYPES_HUSTLE = ['Regular Season', 'Playoffs', 'All Star', 'PlayIn']
PER_MODES_HUSTLE = ['Totals', 'PerGame', 'Per48', 'Per40', 'Per36', 'PerMinute']

# Box Scores configs
BASE_API_BOX_SCORES = 'https://stats.nba.com/stats/leaguegamelog'
BASE_PARAMS_BOX_SCORES = {
    'Counter': '1000',
    'DateFrom': '',
    'DateTo': '',
    'Direction': 'DESC',
    'LeagueID': '00',
    'PlayerOrTeam': 'P',
    'Season': '2022-23',
    'SeasonType': 'Playoffs',
    'Sorter': 'DATE'
}
SEASON_TYPES_BOX_SCORES = ['Pre Season', 'Regular Season', 'Playoffs', 'All Star', 'PlayIn']

# Advanced Box Scores configs
BASE_API_ADVANCED_BOX_SCORES = 'https://stats.nba.com/stats/playergamelogs'
BASE_PARAMS_ADVANCED_BOX_SCORES = {
    'DateFrom': '',
    'DateTo': '',
    'GameSegment': '',
    'LastNGames': '0',
    'LeagueID': '00',
    'Location': '',
    'MeasureType': 'Base',
    'Month': '0',
    'OpponentTeamID': '0',
    'Outcome': '',
    'PORound': '0',
    'PaceAdjust': 'N',
    'PerMode': 'Totals',
    'Period': '0',
    'PlusMinus': 'N',
    'Rank': 'N',
    'Season': '2022-23',
    'SeasonSegment': '',
    'SeasonType': 'Regular Season',
    'ShotClockRange': '',
    'VsConference': '',
    'VsDivision': ''
}
MEASURE_TYPES_ADVANCED_BOX_SCORES  = ['Base', 'Advanced', 'Misc', 'Scoring', 'Usage']
SEASON_TYPES_ADVANCED_BOX_SCORES = ['Pre Season', 'Regular Season', 'Playoffs', 'PlayIn']
