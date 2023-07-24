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
    get_url_with_params
)
from utils import logging
log = logging.Logger()

# from threading import Thread

# -- set config param
URL = 'https://stats.nba.com/stats/{stats}'
# - header
HEADERS['Host'] = 'stats.nba.com'
HEADERS['Referer'] = 'https://www.nba.com/'
# - type stats
type_stats = {
    'General': 'leaguedashteamstats',
    'Genaral_Estimated Advanced': 'teamestimatedmetrics',
    'Clutch': 'leaguedashteamclutch',
    'Playtype': 'synergyplaytypes',
    'Tracking': 'leaguedashptstats',
    'Defense Dashboard': 'leaguedashptteamdefend',
    'Shot Dashboard': 'leaguedashteamptshot',
    'Box Score': 'leaguegamelog',
    'Advanced Box Scores': 'teamgamelogs',
    'Shooting': 'leaguedashteamshotlocations',
    'Opponent Shooting': 'leaguedashoppptshot',
    'Hustle': 'leaguehustlestatsteam',
    'Box Outs': 'leaguehustlestatsteam'
}
# - general
params_general = {
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
measuretypes_general = {
    'Traditional': 'Base',
    'Advanced': 'Advanced',
    'Misc': 'Misc',
    'Four Factors': 'Four Factors',
    'Scoring': 'Scoring',
    'Opponent': 'Opponent',
    'Defense': 'Defense'
    # 'Estimated Advanced': 'Estimated Advanced'
}
seasontypes_general = {
    'Playoffs': 'Playoffs',
    'Pre Season': 'Pre Season',
    'Regular Season': 'Regular Season',
    'PlayIn': 'PlayIn'
}
permodes_general = {
    'Per Game': 'PerGame',
    'Totals': 'Totals',
    'Per 100 Pos': 'Per100Possessions',
    'Per 100 Plays': 'Per100Plays',
    'Per 48 Minutes': 'Per48',
    'Per 40 Minutes': 'Per40',
    'Per 36 Minutes': 'Per36',
    'Per 1 Minute': 'PerMinute',
    'Per 1 poss': 'PerPossession',
    'Per 1 play': 'PerPlay',
    'Minutes Per': 'MinutesPer'
}
process_general = {
    'Traditional': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'WIN%': 'W_PCT',
        'MIN': 'MIN',
        'PTS': 'PTS',
        'FGM': 'FGM',
        'FGA': 'FGA',
        'FG%': 'FG_PCT',
        '3PM': 'FG3M',
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
        'PFD': 'PFD',
        '+/-': 'PLUS_MINUS'
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
        'PIE': 'PIE',
        'POSS': 'POSS'
    },
    'Four Factors': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'WIN%': 'W_PCT',
        'MIN': 'MIN',
        'EFG%': 'EFG_PCT',
        'FTA RATE': 'FTA_RATE',
        'TOV%': 'TM_TOV_PCT',
        'OREB%': 'OREB_PCT',
        'OPP EFG%': 'OPP_EFG_PCT',
        'OPP FTA RATE': 'OPP_FTA_RATE',
        'OPP TOV%': 'OPP_TOV_PCT',
        'OPP OREB%': 'OPP_OREB_PCT'
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
    'Scoring': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        '%FGA 2PT': 'PCT_FGA_2PT',
        '%FGA 3PT': 'PCT_FGA_3PT',
        '%PTS 2PT': 'PCT_PTS_2PT',
        '%PTS 2PT- MR': 'PCT_PTS_2PT_MR',
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
        'OPP PTS': 'OPP_PTS',
        '+/-': 'PLUS_MINUS'
    },
    'Defense': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'DEF RTG': 'DEF_RATING',
        'DREB': 'DREB',
        'DREB%': 'DREB_PCT',
        'STL': 'STL',
        'BLK': 'BLK',
        'OPP PTS OFF TOV': 'OPP_PTS_OFF_TOV',
        'OPP PTS 2ND CHANCE': 'OPP_PTS_2ND_CHANCE',
        'OPP PTS FB': 'OPP_PTS_FB',
        'OPP PTS PAINT': 'OPP_PTS_PAINT'
    },
    'Estimated Advanced': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'EST.  OFFRTG': 'E_OFF_RATING',
        'EST.  DEFRTG': 'E_DEF_RATING',
        'EST.  NETRTG': 'E_NET_RATING',
        'EST.  AST RATIO': 'E_AST_RATIO',
        'EST.  OREB%': 'E_OREB_PCT',
        'EST.  DREB%': 'E_DREB_PCT',
        'EST.  REB%': 'E_REB_PCT',
        'EST.  TOV%': 'E_TM_TOV_PCT',
        'EST.  PACE': 'E_PACE'
    }
}

# - clutch
params_clutch = {
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
measuretypes_clutch = {
    'Traditional': 'Base',
    'Advanced': 'Advanced',
    'Misc': 'Misc',
    'Four Factors': 'Four Factors',
    'Scoring': 'Scoring',
    'Opponent': 'Opponent'
}
seasontypes_clutch = {
    'Playoffs': 'Playoffs',
    'PreSeason': 'Pre Season',
    'Regular Season': 'Regular Season',
    'PlayIn': 'PlayIn'
}
permodes_clutch = {
    'Per Game': 'PerGame',
    'Totals': 'Totals',
    'Per 100 Pos': 'Per100Possessions',
    'Per 100 Plays': 'Per100Plays',
    'Per 48 Minutes': 'Per48',
    'Per 40 Minutes': 'Per40',
    'Per 36 Minutes': 'Per36',
    'Per 1 Minute': 'PerMinute',
    'Per 1 poss': 'PerPossession',
    'Per 1 play': 'PerPlay',
    'Minutes Per': 'MinutesPer'
}
# use param process for general

# - playtype
params_playtype = {
    'LeagueID': '00',
    'PerMode': 'PerGame',
    'PlayType': 'Isolation',
    'PlayerOrTeam': 'T',
    'SeasonType': 'Playoffs',
    'SeasonYear': '2022-23',
    'TypeGrouping': 'offensive'
}
measuretypes_playtype = {
    'Isolation': 'Isolation',
    'Transition': 'Transition',
    'Pick & Roll Ball Handler': 'PRBallHandler',
    'Pick & Roll Roll Man': 'PRRollman',
    'Post up': 'Postup',
    'Spot up': 'Spotup',
    'Handoff': 'Handoff',
    'Cut': 'Cut',
    'Off Screen': 'OffScreen',
    'Putbacks': 'OffRebound',
    'Misc': 'Misc'
}
seasontypes_playtype = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season'
}
permodes_clutch = {
    'Per Game': 'PerGame',
    'Totals': 'Totals',
}
process_playtype = {
    'GP': 'GP',
    'POSS': 'POSS',
    'FREQ%': 'POSS_PCT',
    'PPP': 'PPP',
    'PTS': 'PTS',
    'FGM': 'FGM',
    'FGA': 'FGA',
    'FG%': 'FG_PCT',
    'EFG%': 'EFG_PCT',
    'FT FREQ%': 'FT_POSS_PCT',
    'TOV FREQ%': 'TOV_POSS_PCT',
    'SF FREQ%': 'SF_POSS_PCT',
    'AND ONE FREQ%': 'PLUSONE_POSS_PCT',
    'SCORE FREQ%': 'SCORE_POSS_PCT',
    'PERCENTILE': 'PERCENTILE'
}

# - tracking
params_tracking = {
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
measuretypes_tracking = {
    # 'Drives': 'Drives',
    # 'Defensive Impact': 'Defense',
    # 'Catch & Shoot': 'CatchShoot',
    'Passing': 'Passing',
    'Touches': 'Possessions',
    'Pull Up Shooting': 'PullUpShot',
    'Rebounding': 'Rebounding', # Offensive Rebounding, Defensive Rebounding is same
    'Shooting Efficiency': 'Efficiency',
    'Speed & Distance': 'SpeedDistance',
    'Elbow Touches': 'ElbowTouch',
    'Post Ups': 'PostTouch',
    'Paint Touches': 'PaintTouch'
}
seasontypes_tracking = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Play In': 'PlayIn'
}
permodes_tracking = {
    'Per Game': 'PerGame',
    'Totals': 'Totals'
}
process_tracking = {
    'Drives': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'DRIVES': 'DRIVES',
        'FGM': 'DRIVE_FGM',
        'FGA': 'DRIVE_FGA',
        'FG%': 'DRIVE_FG_PCT',
        'FTM': 'DRIVE_FTM',
        'FTA': 'DRIVE_FTA',
        'FT%': 'DRIVE_FT_PCT',
        'PTS': 'DRIVE_PTS',
        'PTS%': 'DRIVE_PTS_PCT',
        'PASS': 'DRIVE_PASSES',
        'PASS%': 'DRIVE_PASSES_PCT',
        'AST': 'DRIVE_AST',
        'AST%': 'DRIVE_AST_PCT',
        'TO': 'DRIVE_TOV',
        'TOV%': 'DRIVE_TOV_PCT',
        'PF': 'DRIVE_PF',
        'PF%': 'DRIVE_PF_PCT'
    },
    'Defensive Impact': {
        'GP': 'GP',
        'MIN': 'W',
        'W': 'L',
        'L': 'MIN',
        'STL': 'STL',
        'BLK': 'BLK',
        'DREB': 'DREB',
        'DFGM': 'DEF_RIM_FGM',
        'DFGA': 'DEF_RIM_FGA',
        'DFG%': 'DEF_RIM_FG_PCT'
    },
    'Catch & Shoot': {
        'GP': 'GP',
        'MIN': 'MIN',
        'PTS': 'CATCH_SHOOT_PTS',
        'FGM': 'CATCH_SHOOT_FGM',
        'FGA': 'CATCH_SHOOT_FGA',
        'FG%': 'CATCH_SHOOT_FG_PCT',
        '3PM': 'CATCH_SHOOT_FG3M',
        '3PA': 'CATCH_SHOOT_FG3A',
        '3P%': 'CATCH_SHOOT_FG3_PCT',
        'EFG%': 'CATCH_SHOOT_EFG_PCT'
    },
    'Passing': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'PASSES MADE': 'PASSES_MADE',
        'PASSES RECEIVED': 'PASSES_RECEIVED',
        'AST': 'AST',
        'SECONDARY AST': 'SECONDARY_AST',
        'POTENTIAL AST': 'POTENTIAL_AST',
        'AST PTS CREATED': 'AST_POINTS_CREATED',
        'AST ADJ': 'AST_ADJ',
        'AST TO PASS%': 'AST_TO_PASS_PCT',
        'AST TO PASS% ADJ': 'AST_TO_PASS_PCT_ADJ'
    },
    'Touches': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'PTS': 'POINTS',
        'TOUCHES': 'TOUCHES',
        'FRONT CT TOUCHES': 'FRONT_CT_TOUCHES',
        'TIME OF POSS': 'TIME_OF_POSS',
        'AVG SEC PER TOUCH': 'AVG_SEC_PER_TOUCH',
        'AVG DRIB PER TOUCH': 'AVG_DRIB_PER_TOUCH',
        'PTS PER TOUCH': 'PTS_PER_TOUCH',
        'ELBOW TOUCHES': 'ELBOW_TOUCHES',
        'POST UPS': 'POST_TOUCHES',
        'PAINT TOUCHES': 'PAINT_TOUCHES',
        'PTS PER ELBOW TOUCH': 'PTS_PER_ELBOW_TOUCH',
        'PTS PER POST TOUCH': 'PTS_PER_POST_TOUCH',
        'PTS PER PAINT TOUCH': 'PTS_PER_PAINT_TOUCH'
    },
    'Pull Up Shooting': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'PTS': 'PULL_UP_PTS',
        'FGM': 'PULL_UP_FGM',
        'FGA': 'PULL_UP_FGA',
        'FG%': 'PULL_UP_FG_PCT',
        '3PM': 'PULL_UP_FG3M',
        '3PA': 'PULL_UP_FG3A',
        '3P%': 'PULL_UP_FG3_PCT',
        'EFG%': 'PULL_UP_EFG_PCT'
    },
    'Rebounding': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'REB': 'REB',
        'CONTESTED REB': 'REB_CONTEST',
        'CONTESTED REB%': 'REB_CONTEST_PCT',
        'REB CHANCES': 'REB_CHANCES',
        'REB CHANCE%': 'REB_CHANCE_PCT',
        'DEFERRED REB CHANCES': 'REB_CHANCE_DEFER',
        'ADJUSTED REB CHANCE%': 'REB_CHANCE_PCT_ADJ'
    },
    'Shooting Efficiency': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'PTS': 'POINTS',
        'DRIVE PTS': 'DRIVE_PTS',
        'DRIVE FG%': 'DRIVE_FG_PCT',
        'C&S PTS': 'CATCH_SHOOT_PTS',
        'C&S FG%': 'CATCH_SHOOT_FG_PCT',
        'PULL UP PTS': 'PULL_UP_PTS',
        'PULL UP FG%': 'PULL_UP_FG_PCT',
        'PAINT TOUCH PTS': 'PAINT_TOUCH_PTS',
        'PAINT TOUCH FG%': 'PAINT_TOUCH_FG_PCT',
        'POST TOUCH PTS': 'POST_TOUCH_PTS',
        'POST TOUCH FG%': 'POST_TOUCH_FG_PCT',
        'ELBOW TOUCH PTS': 'ELBOW_TOUCH_PTS',
        'ELBOW TOUCH FG%': 'ELBOW_TOUCH_FG_PCT',
        'EFG%': 'EFF_FG_PCT'
    },
    'Speed & Distance': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'DIST. FEET': 'DIST_FEET',
        'DIST. MILES': 'DIST_MILES',
        'DIST. MILES OFF': 'DIST_MILES_OFF',
        'DIST. MILES DEF': 'DIST_MILES_DEF',
        'AVG SPEED': 'AVG_SPEED',
        'AVG SPEED OFF': 'AVG_SPEED_OFF',
        'AVG SPEED DEF': 'AVG_SPEED_DEF'
    },
    'Elbow Touches': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'TOUCHES': 'TOUCHES',
        'ELBOW TOUCHES': 'ELBOW_TOUCHES',
        'FGM': 'ELBOW_TOUCH_FGM',
        'FGA': 'ELBOW_TOUCH_FGA',
        'FG%': 'ELBOW_TOUCH_FG_PCT',
        'FTM': 'ELBOW_TOUCH_FTM',
        'FTA': 'ELBOW_TOUCH_FTA',
        'FT%': 'ELBOW_TOUCH_FT_PCT',
        'PTS': 'ELBOW_TOUCH_PTS',
        'PTS%': 'ELBOW_TOUCH_PTS_PCT',
        'PASS': 'ELBOW_TOUCH_PASSES',
        'PASS%': 'ELBOW_TOUCH_PASSES_PCT',
        'AST': 'ELBOW_TOUCH_AST',
        'AST%': 'ELBOW_TOUCH_AST_PCT',
        'TO': 'ELBOW_TOUCH_TOV',
        'TOV%': 'ELBOW_TOUCH_TOV_PCT',
        'PF': 'ELBOW_TOUCH_FOULS',
        'PF%': 'ELBOW_TOUCH_FOULS_PCT'
    },
    'Post Ups': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'TOUCHES': 'TOUCHES',
        'POST UPS': 'POST_TOUCHES',
        'FGM': 'POST_TOUCH_FGM',
        'FGA': 'POST_TOUCH_FGA',
        'FG%': 'POST_TOUCH_FG_PCT',
        'FTM': 'POST_TOUCH_FTM',
        'FTA': 'POST_TOUCH_FTA',
        'FT%': 'POST_TOUCH_FT_PCT',
        'PTS': 'POST_TOUCH_PTS',
        'PTS%': 'POST_TOUCH_PTS_PCT',
        'PASS': 'POST_TOUCH_PASSES',
        'PASS%': 'POST_TOUCH_PASSES_PCT',
        'AST': 'POST_TOUCH_AST',
        'AST%': 'POST_TOUCH_AST_PCT',
        'TO': 'POST_TOUCH_TOV',
        'TOV%': 'POST_TOUCH_TOV_PCT',
        'PF': 'POST_TOUCH_FOULS',
        'PF%': 'POST_TOUCH_FOULS_PCT'
    },
    'Paint Touches': {
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN',
        'TOUCHES': 'TOUCHES',
        'PAINT TOUCHES': 'PAINT_TOUCHES',
        'FGM': 'PAINT_TOUCH_FGM',
        'FGA': 'PAINT_TOUCH_FGA',
        'FG%': 'PAINT_TOUCH_FG_PCT',
        'FTM': 'PAINT_TOUCH_FTM',
        'FTA': 'PAINT_TOUCH_FTA',
        'FT%': 'PAINT_TOUCH_FT_PCT',
        'PTS': 'PAINT_TOUCH_PTS',
        'PTS%': 'PAINT_TOUCH_PTS_PCT',
        'PASS': 'PAINT_TOUCH_PASSES',
        'PASS%': 'PAINT_TOUCH_PASSES_PCT',
        'AST': 'PAINT_TOUCH_AST',
        'AST%': 'PAINT_TOUCH_AST_PCT',
        'TO': 'PAINT_TOUCH_TOV',
        'TOV%': 'PAINT_TOUCH_TOV_PCT',
        'PF': 'PAINT_TOUCH_FOULS',
        'PF%': 'PAINT_TOUCH_FOULS_PCT'
    }
}

# - defense dashboard
params_defense_dashboard = {
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
measuretypes_defense_dashboard = {
    'Overall': 'Overall',
    '3 Pointers': '3 Pointers',
    '2 Pointers': '2 Pointers',
    'Less Than 6Ft': 'Less Than 6Ft',
    'Less Than 10Ft': 'Less Than 10Ft',
    'Greater Than 15Ft': 'Greater Than 15Ft'
}
seasontypes_defense_dashboard = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Play In': 'PlayIn'
}
process_defense_dashboard = {
    'Overall': {
        'GP': 'GP',
        'G': 'G',
        'FREQ': 'FREQ',
        'DFGM': 'D_FGM',
        'DFGA': 'D_FGA',
        'DFG%': 'D_FG_PCT',
        'FG%': 'NORMAL_FG_PCT',
        'DIFF%': 'PCT_PLUSMINUS'
    },
    '3 Pointers': {
        'GP': 'GP',
        'G': 'G',
        'FREQ': 'FREQ',
        'DFGM': 'FG3M',
        'DFGA': 'FG3A',
        'DFG%': 'FG3_PCT',
        'FG%': 'NS_FG3_PCT',
        'DIFF%': 'PLUSMINUS'
    },
    '2 Pointers': {
        'GP': 'GP',
        'G': 'G',
        'FREQ': 'FREQ',
        'DFGM': 'FG2M',
        'DFGA': 'FG2A',
        'DFG%': 'FG2_PCT',
        'FG%': 'NS_FG2_PCT',
        'DIFF%': 'PLUSMINUS'
    },
    'Less Than 6Ft': {
        'GP': 'GP',
        'G': 'G',
        'FREQ': 'FREQ',
        'DFGM': 'FGM_LT_06',
        'DFGA': 'FGA_LT_06',
        'DFG%': 'LT_06_PCT',
        'FG%': 'NS_LT_06_PCT',
        'DIFF%': 'PLUSMINUS'
    },
    'Less Than 10Ft': {
        'GP': 'GP',
        'G': 'G',
        'FREQ': 'FREQ',
        'DFGM': 'FGM_LT_10',
        'DFGA': 'FGA_LT_10',
        'DFG%': 'LT_10_PCT',
        'FG%': 'NS_LT_10_PCT',
        'DIFF%': 'PLUSMINUS'
    },
    'Greater Than 15Ft': {
        'GP': 'GP',
        'G': 'G',
        'FREQ': 'FREQ',
        'DFGM': 'FGM_GT_15',
        'DFGA': 'FGA_GT_15',
        'DFG%': 'GT_15_PCT',
        'FG%': 'NS_GT_15_PCT',
        'DIFF%': 'PLUSMINUS'
    }
}

# - Shot Dashboard
params_shot_dashboard = {
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
    'GeneralRange': 'Overall',
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
measuretypes_shot_dashboard = {
    'General': 'General',
    'Shotclock': 'ShotClock',
    'Dribbles': 'Dribble',
    'Touch Time': 'TouchTime',
    'Closest Defender': 'ClosestDef',
    'Closest Defender +10': 'ClosestDef10',
}
seasontypes_shot_dashboard = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Preseason': 'Pre Season',
    'Play In': 'PlayIn'
}
permodes_shot_dashboard = {
    'Per Game': 'PerGame',
    'Totals': 'Totals'
}
process_shot_dashboard = {
    'GP': 'GP',
    'G': 'G',
    'FREQ%': 'FGA_FREQUENCY',
    'FGM': 'FGM',
    'FGA': 'FGA',
    'FG%': 'FG_PCT',
    'EFG%': 'EFG_PCT',
    '2FG FREQ%': 'FG2A_FREQUENCY',
    '2FGM': 'FG2M',
    '2FGA': 'FG2A',
    '2FG%': 'FG2_PCT',
    '3FG FREQ%': 'FG3A_FREQUENCY',
    '3PM': 'FG3M',
    '3PA': 'FG3A',
    '3P%': 'FG3_PCT'
}

# - Box Score
params_box_score = {
    'Counter': '1000',
    'DateFrom': '',
    'DateTo': '',
    'Direction': 'DESC',
    'LeagueID': '00',
    'PlayerOrTeam': 'T',
    'Season': '2022-23',
    'SeasonType': 'Playoffs',
    'Sorter': 'DATE'
}
seasontypes_box_score = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Preseason': 'Pre Season',
    'Play In': 'PlayIn'
}
process_box_score = {
    'MIN': 'MIN',
    'PTS': 'PTS',
    'FGM': 'FGM',
    'FGA': 'FGA',
    'FG%': 'FG_PCT',
    '3PM': 'FG3M',
    '3PA': 'FG3A',
    '3P%': 'FG3_PCT',
    'FTM': 'FTM',
    'FTA': 'FTA',
    'FT%': 'FT_PCT',
    'OREB': 'OREB',
    'DREB': 'DREB',
    'REB': 'REB',
    'AST': 'AST',
    'STL': 'STL',
    'BLK': 'BLK',
    'TOV': 'TOV',
    'PF': 'PF',
    '+/-': 'PLUS_MINUS'
}

# - Advanced Box Scores
params_advanced_box_scores = {
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
    'SeasonType': 'Playoffs',
    'ShotClockRange': '',
    'VsConference': '',
    'VsDivision': ''
}
measuretypes_advanced_box_scores = {
    'Traditional': 'Base',
    'Advanced': 'Advanced',
    'Misc': 'Misc',
    'Four Factors': 'Four Factors',
    'Misc': 'Misc',
    'Scoring': 'Scoring'
}
seasontypes_advanced_box_scores = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Preseason': 'Pre Season',
    'Play In': 'PlayIn'
}
process_advance_box_scores = {
    'Traditional': {
        'MIN': 'MIN',
        'PTS': 'PTS',
        'FGM': 'FGM',
        'FGA': 'FGA',
        'FG%': 'FG_PCT',
        '3PM': 'FG3M',
        '3PA': 'FG3A',
        '3P%': 'FG3_PCT',
        'FTM': 'FTM',
        'FTA': 'FTA',
        'FT%': 'FT_PCT',
        'OREB': 'OREB',
        'DREB': 'DREB',
        'REB': 'REB',
        'AST': 'AST',
        'STL': 'STL',
        'BLK': 'BLK',
        'TOV': 'TOV',
        'PF': 'PF',
        '+/-': 'PLUS_MINUS'
    },
    'Advanced': {
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
        'MIN': 'MIN',
        'EFG%': 'EFG_PCT',
        'FTA RATE': 'FTA_RATE',
        'TOV%': 'TM_TOV_PCT',
        'OREB%': 'OREB_PCT',
        'OPP EFG%': 'OPP_EFG_PCT',
        'OPP FTA RATE': 'OPP_FTA_RATE',
        'OPP TOV%': 'OPP_TOV_PCT',
        'OPP OREB%': 'OPP_OREB_PCT'
    },
    'Misc': {
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
    'Scoring': {
        'MIN': 'MIN',
        '%FGA 2PT': 'PCT_FGA_2PT',
        '%FGA 3PT': 'PCT_FGA_3PT',
        '%PTS 2PT': 'PCT_PTS_2PT',
        '%PTS 2PT MR': 'PCT_PTS_2PT_MR',
        '%PTS 3PT': 'PCT_PTS_3PT',
        '%PTS FBPS': 'PCT_PTS_FB',
        '%PTS FT': 'PCT_PTS_FT',
        '%PTS OFF TO': 'PCT_PTS_OFF_TOV',
        '%PTS PITP': 'PCT_PTS_PAINT',
        '2FGM %AST': 'PCT_AST_2PM',
        '2FGM %UAST': 'PCT_UAST_2PM',
        '3FGM %AST': 'PCT_AST_3PM',
        '3FGM %UAST': 'PCT_UAST_3PM',
        'FGM %AST': 'PCT_AST_FGM',
        'FGM %UAST': 'PCT_UAST_FGM'
    }
}

# - Shooting
params_shooting = {
    'Conference': '',
    'DateFrom': '',
    'DateTo': '',
    'DistanceRange': '5ft Range',
    'Division': '',
    'GameScope': '',
    'GameSegment': '',
    'LastNGames': '0',
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
seasontypes_shooting = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Preseason': 'Pre Season',
    'Play In': 'PlayIn'
}
permodes_shooting = {
    'Per Game': 'PerGame',
    'Totals': 'Totals'
}
distance_ranges_shooting = {
    '5ft Range': '5ft Range',
    '8ft Range': '8ft Range',
    'By Zone': 'By Zone'
}
process_shooting = {
    # 'Team_id': 0,
    # 'Team_name': 1,
    '5ft Range': {
        'FGM (LESS THAN 5FT.)': 2,
        'FGA (LESS THAN 5FT.)': 3,
        'FG% (LESS THAN 5FT.)': 4,
        'FGM (5-9 FT.)': 5,
        'FGA (5-9 FT.)': 6,
        'FG% (5-9 FT.)': 7,
        'FGM (10-14 FT.)': 8,
        'FGA (10-14 FT.)': 9,
        'FG% (10-14 FT.)': 10,
        'FGM (15-19 FT.)': 11,
        'FGA (15-19 FT.)': 12,
        'FG% (15-19 FT.)': 13,
        'FGM (20-24 FT.)': 14,
        'FGA (20-24 FT.)': 15,
        'FG% (20-24 FT.)': 16,
        'FGM (25-29 FT.)': 17,
        'FGA (25-29 FT.)': 18,
        'FG% (25-29 FT.)': 19
    },
    '8ft Range': {
        'FGM (LESS THAN 8FT.)': 2,
        'FGA (LESS THAN 8FT.)': 3,
        'FG% (LESS THAN 8FT.)': 4,
        'FGM (8-16 FT.)': 5,
        'FGA (8-16 FT.)': 6,
        'FG% (8-16 FT.)': 7,
        'FGM (16-24 FT.)': 8,
        'FGA (16-24 FT.)': 9,
        'FG% (16-24 FT.)': 10,
        'FGM (24+ FT.)': 11,
        'FGA (24+ FT.)': 12,
        'FG% (24+ FT.)': 13,
        'FGM (BACK COURT SHOT)': 14,
        'FGA (BACK COURT SHOT)': 15,
        'FG% (BACK COURT SHOT)': 16
    },
    'By Zone': {
        'FGM (RESTRICTED AREA)': 2,
        'FGA (RESTRICTED AREA)': 3,
        'FG% (RESTRICTED AREA)': 4,
        'FGM (IN THE PAINT (NON-RA))': 5,
        'FGA (IN THE PAINT (NON-RA))': 6,
        'FG% (IN THE PAINT (NON-RA))': 7,
        'FGM (MID-RANGE)': 8,
        'FGA (MID-RANGE)': 9,
        'FG% (MID-RANGE)': 10,
        'FGM (LEFT CORNER 3.)': 11,
        'FGA (LEFT CORNER 3.)': 12,
        'FG% (LEFT CORNER 3.)': 13,
        'FGM (RIGHT CORNER 3.)': 14,
        'FGA (RIGHT CORNER 3.)': 15,
        'FG% (RIGHT CORNER 3.)': 16,
        'FGM (CORNER 3)': 23,
        'FGA (CORNER 3)': 24,
        'FG% (CORNER 3)': 25,
        'FGM (ABOVE THE BREAK 3.)': 17,
        'FGA (ABOVE THE BREAK 3.)': 18,
        'FG% (ABOVE THE BREAK 3.)': 19
    }
}

# - Opponent Shooting
params_opponent_shooting = {
    'SeasonSegment': '',
    'GameSegment': '',
    'PerMode': 'PerGame',
    'PORound': '0',
    'OpponentTeamID': '0',
    'Division': '',
    'VsConference': '',
    'Month': '0',
    'Season': '2022-23',
    'TeamID': '0',
    'PlayerExperience': '',
    'VsDivision': '',
    'Conference': '',
    'DateTo': '',
    'Outcome': '',
    'PlayerPosition': '',
    'LastNGames': '0',
    'Period': '0',
    'Location': '',
    'DateFrom': '',
    'SeasonType': 'Playoffs'
}
measuretypes_opponent_shooting = {
    'Overall Opponent Shooting': 'Opponent',
    'General': 'General',
    'Shotclock': 'ShotClock',
    'Dribbles': 'Dribble',
    'Touch Time': 'TouchTime',
    'Closest Defender': 'ClosestDef',
    'Closest Defender +10': 'ClosestDef10'
}
seasontypes_opponent_shooting = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Play In': 'PlayIn'
}
permodes_opponent_shooting = {
    'Per Game': 'PerGame',
    'Totals': 'Totals'
}

# distance use distance_ranges_shooting
shot_opponent_shooting = {
    'Overall': 'Overall',
    'Catch and Shoot': 'Catch and Shoot',
    'Pullups': 'Pullups',
    'Less Than 10 ft': 'Less Than 10 ft'
}
shot_clock_opponent_shooting = {
    '24-22': '24-22',
    '22-18 Very Early': '22-18 Very Early',
    '18-15 Early': '18-15 Early',
    '15-7 Average': '15-7 Average',
    '7-4 Late': '7-4 Late',
    '4-0 Very Late': '4-0 Very Late'
}
dribble_opponent_shooting = {
    '0 Dribbles': '0 Dribbles',
    '1 Dribble': '1 Dribble',
    '2 Dribbles': '2 Dribbles',
    '3-6 Dribbles': '3-6 Dribbles',
    '7+ Dribbles': '7+ Dribbles'
}
touch_opponent_shooting = {
    '0-2 Seconds': 'Touch < 2 Seconds',
    '2-6 Seconds': 'Touch 2-6 Seconds',
    '6+ Seconds': 'Touch 6+ Seconds'
}
closest_opponent_shooting = {
    '0-2 Feet (Very Tight)': '0-2 Feet - Very Tight',
    '2-4 Feet (Tight)': '2-4 Feet - Tight',
    '4-6 Feet (Open)': '4-6 Feet - Open',
    '6+ Feet (Wide Open)': '6+ Feet - Wide Open'
}
closest10_opponent_shooting = {
    '0-2 Feet (Very Tight)': '0-2 Feet - Very Tight',
    '2-4 Feet (Tight)': '2-4 Feet - Tight',
    '4-6 Feet (Open)': '4-6 Feet - Open',
    '6+ Feet (Wide Open)': '6+ Feet - Wide Open'
}
# using process_shot_dashboard and process_shooting
ranges = {
    'Overall Opponent Shooting': 'Distance_range',
    'General': 'Shot_range',
    'Shotclock': 'Shot_clock_range',
    'Dribbles': 'Dribble_range',
    'Touch Time': 'Touch_time_range',
    'Closest Defender': 'Closest_defender_distance_range',
    'Closest Defender +10': 'Closest_defender_distance_range',
}

# - Hustle
params_hustle = {
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
seasontypes_hustle = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Play In': 'PlayIn'
}
permodes_hustle = {
    'Per Game': 'PerGame',
    'Totals': 'Totals',
    'Per 48 Minutes': 'Per48',
    'Per 40 Minutes': 'Per40',
    'Per 36 Minutes': 'Per36',
    'Per 1 Minute': 'PerMinute'
}
process_hustle = {
    'MIN': 'MIN',
    'SCREEN ASSISTS': 'SCREEN_ASSISTS',
    'SCREEN ASSISTS PTS': 'SCREEN_AST_PTS',
    'DEFLECTIONS': 'DEFLECTIONS',
    'OFF LOOSE BALLS RECOVERED': 'OFF_LOOSE_BALLS_RECOVERED',
    'DEF LOOSE BALLS RECOVERED': 'DEF_LOOSE_BALLS_RECOVERED',
    'LOOSE BALLS RECOVERED': 'LOOSE_BALLS_RECOVERED',
    '% LOOSE BALLS RECOVERED OFF': 'PCT_LOOSE_BALLS_RECOVERED_OFF',
    '% LOOSE BALLS RECOVERED DEF': 'PCT_LOOSE_BALLS_RECOVERED_DEF',
    'CHARGES DRAWN': 'CHARGES_DRAWN',
    'CONTESTED 2PT SHOTS': 'CONTESTED_SHOTS_2PT',
    'CONTESTED 3PT SHOTS': 'CONTESTED_SHOTS_3PT',
    'CONTESTED SHOTS': 'CONTESTED_SHOTS'
}

# - Box Outs
params_box_outs = {
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
seasontypes_box_outs = {
    'Playoffs': 'Playoffs',
    'Regular Season': 'Regular Season',
    'Play In': 'PlayIn'
}
permodes_box_outs = {
    'Per Game': 'PerGame',
    'Totals': 'Totals',
    'Per 48 Minutes': 'Per48',
    'Per 40 Minutes': 'Per40',
    'Per 36 Minutes': 'Per36',
    'Per 1 Minute': 'PerMinute'
}
process_box_outs = {
    'MIN': 'MIN',
    'BOX OUTS': 'BOX_OUTS',
    'OFF BOX OUTS': 'OFF_BOXOUTS',
    'DEF BOX OUTS': 'DEF_BOXOUTS',
    '% BOX OUTS OFF': 'PCT_BOX_OUTS_OFF',
    '% BOX OUTS DEF': 'PCT_BOX_OUTS_DEF'
}

def get_urls(type: str):
    s = []
    seasons = get_seasons_by_year(START_YEAR, END_YEAR)
    title = f'Team_stats/{type}'

    if type == 'General':
        for measuretype in measuretypes_general:
            params_general['MeasureType'] = measuretypes_general[measuretype]
            for season in seasons:
                params_general['Season'] = season
                for seasontype in seasontypes_general:
                    params_general['SeasonType'] = seasontype
                    for permode in permodes_general:
                        params_general['PerMode'] = permodes_general[permode]
                        url = get_url_with_params(URL.format(stats=type_stats[type]), params_general)
                        path_file = f'{measuretype}/{season}_{seasontype}_{permode}'
                        s.append((url, title, path_file))
        # Estimated Advanced
        param = {'LeagueID': '00', 'Season': '2022-23', 'SeasonType': 'Playoffs'}
        for season in seasons:
            param['Season'] = season
            for seasontype in seasontypes_general:
                param['SeasonType'] = seasontype
                url = get_url_with_params(URL.format(stats=type_stats['Genaral_Estimated Advanced']), param)
                path_file = f'Estimated Advanced/{season}_{seasontype}_'
                s.append((url, title, path_file))

    elif type == 'Clutch':
        for measuretype in measuretypes_clutch:
            params_clutch['MeasureType'] = measuretypes_clutch[measuretype]
            for season in seasons:
                params_clutch['Season'] = season
                for seasontype in seasontypes_clutch:
                    params_clutch['SeasonType'] = seasontype
                    for permode in permodes_clutch:
                        params_clutch['PerMode'] = permodes_clutch[permode]
                        url = get_url_with_params(URL.format(stats=type_stats[type]), params_clutch)
                        path_file = f'{measuretype}/{season}_{seasontype}_{permode}'
                        s.append((url, title, path_file))

    elif type == 'Playtype':
        for measuretype in measuretypes_playtype:
            params_playtype['PlayType'] = measuretypes_playtype[measuretype]
            for season in seasons:
                params_playtype['SeasonYear'] = season
                for seasontype in seasontypes_playtype:
                    params_playtype['SeasonType'] = seasontype
                    for permode in permodes_clutch:
                        params_playtype['PerMode'] = permodes_clutch[permode]
                        url = get_url_with_params(URL.format(stats=type_stats[type]), params_playtype)
                        path_file = f'{measuretype}/{season}_{seasontype}_{permode}'
                        s.append((url, title, path_file))

    elif type == 'Tracking':
        for measuretype in measuretypes_tracking:
            params_tracking['PtMeasureType'] = measuretypes_tracking[measuretype]
            for season in seasons:
                params_tracking['Season'] = season
                for seasontype in seasontypes_tracking:
                    params_tracking['SeasonType'] = seasontype
                    for permode in permodes_tracking:
                        params_tracking['PerMode'] = permodes_tracking[permode]
                        url = get_url_with_params(URL.format(stats=type_stats[type]), params_tracking)
                        path_file = f'{measuretype}/{season}_{seasontype}_{permode}'
                        s.append((url, title, path_file))
    
    elif type == 'Defense Dashboard':
        for measuretype in measuretypes_defense_dashboard:
            params_defense_dashboard['DefenseCategory'] = measuretypes_defense_dashboard[measuretype]
            for season in seasons:
                params_defense_dashboard['Season'] = season
                for seasontype in seasontypes_defense_dashboard:
                    params_defense_dashboard['SeasonType'] = seasontype
                    url = get_url_with_params(URL.format(stats=type_stats[type]), params_defense_dashboard)
                    path_file = f'{measuretype}/{season}_{seasontype}'
                    s.append((url, title, path_file))

    elif type == 'Shot Dashboard':
        for measuretype in measuretypes_shot_dashboard:
            params_shot_dashboard['GeneralRange'] = measuretypes_shot_dashboard[measuretype]
            for season in seasons:
                params_shot_dashboard['Season'] = season
                for seasontype in seasontypes_shot_dashboard:
                    params_shot_dashboard['SeasonType'] = seasontype
                    for permode in permodes_shot_dashboard:
                        params_shot_dashboard['PerMode'] = permodes_shot_dashboard[permode]
                        url = get_url_with_params(URL.format(stats=type_stats[type]), params_shot_dashboard)
                        path_file = f'{measuretype}/{season}_{seasontype}_{permode}'
                        s.append((url, title, path_file))

    elif type == 'Box Score':
        for season in seasons:
            params_box_score['Season'] = season
            for seasontype in seasontypes_box_score:
                params_box_score['SeasonType'] = seasontypes_box_score[seasontype]
                url = get_url_with_params(URL.format(stats=type_stats[type]), params_box_score)
                path_file = f'{season}_{seasontype}'
                s.append((url, title, path_file))
            
    elif type == 'Advanced Box Scores':
        for measuretype in measuretypes_advanced_box_scores:
            params_advanced_box_scores['MeasureType'] = measuretypes_advanced_box_scores[measuretype]
            for season in seasons:
                params_advanced_box_scores['Season'] = season
                for seasontype in seasontypes_advanced_box_scores:
                    params_advanced_box_scores['SeasonType'] = seasontypes_advanced_box_scores[seasontype]
                    url = get_url_with_params(URL.format(stats=type_stats[type]), params_advanced_box_scores)
                    path_file = f'{measuretype}/{season}_{seasontype}'
                    s.append((url, title, path_file))

    elif type == 'Shooting':
        for season in seasons:
            params_shooting['Season'] = season
            for seasontype in seasontypes_shooting:
                params_shooting['SeasonType'] = seasontypes_shooting[seasontype]
                for permode in permodes_shooting:
                    params_shooting['PerMode'] = permodes_shooting[permode]
                    for distance_range in distance_ranges_shooting:
                        params_shooting['DistanceRange'] = distance_ranges_shooting[distance_range]
                        url = get_url_with_params(URL.format(stats=type_stats[type]), params_shooting)
                        path_file = f'{season}_{seasontype}_{permode}_{distance_range}'
                        s.append((url, title, path_file))

    elif type == 'Opponent Shooting':
        sstype = seasontypes_opponent_shooting
        for measuretype in measuretypes_opponent_shooting:
            if measuretype == 'Overall Opponent Shooting':
                sstype = seasontypes_shooting
            for season in seasons:
                for seasontype in sstype:
                    for permode in permodes_opponent_shooting:
                        params = params_opponent_shooting.copy()
                        url = URL.format(stats=type_stats[type])
                        if measuretype == 'Overall Opponent Shooting':
                            url = URL.format(stats=type_stats['Shooting'])
                            params.update({
                                'DistanceRange': '5ft Range',
                                'PaceAdjust': 'N',
                                'Rank': 'N',
                                'StarterBench': '',
                                'PlusMinus': 'N',
                                'ShotClockRange': '',
                                'MeasureType': 'Opponent',
                                'GameScope': ''
                            })
                            for distance_range in distance_ranges_shooting:
                                params_shooting['DistanceRange'] = distance_ranges_shooting[distance_range]
                                url_ = get_url_with_params(url, params_shooting)
                                path_file = f'{measuretype}/{season}_{seasontype}_{permode}_{distance_range}'
                                s.append((url_, title, path_file))
                        if measuretype == 'General':
                            params.update({
                                'LeagueID': '00', 
                                'GeneralRange': ''
                            })
                            for shot in shot_opponent_shooting:
                                params['GeneralRange'] = shot_opponent_shooting[shot]
                                url_ = get_url_with_params(url, params)
                               
                                path_file = f'{measuretype}/{season}_{seasontype}_{permode}_{shot}'
                                s.append((url_, title, path_file))
                            break

                        elif measuretype == 'Shotclock':
                            params.update({
                                'LeagueID': '00', 
                                'ShotClockRange': ''
                            })
                            for shotclock in shot_clock_opponent_shooting:
                                params['ShotClockRange'] = shot_clock_opponent_shooting[shotclock]
                                url_ = get_url_with_params(url, params)
                                path_file = f'{measuretype}/{season}_{seasontype}_{permode}_{shotclock}'
                                s.append((url_, title, path_file))
                            break

                        elif measuretype == 'Dribbles':
                            params.update({
                                'LeagueID': '00', 
                                'DribbleRange': ''
                            })
                            for dribble in dribble_opponent_shooting:
                                params['DribbleRange'] = dribble_opponent_shooting[dribble]
                                url_ = get_url_with_params(url, params)
                                path_file = f'{measuretype}/{season}_{seasontype}_{permode}_{dribble}'
                                s.append((url_, title, path_file))
                            break

                        elif measuretype == 'Touch Time':
                            params.update({
                                'LeagueID': '00', 
                                'TouchTimeRange': ''
                            })
                            for touch in touch_opponent_shooting:
                                params['TouchTimeRange'] = touch_opponent_shooting[touch]
                                url_ = get_url_with_params(url, params)
                                path_file = f'{measuretype}/{season}_{seasontype}_{permode}_{touch}'
                                s.append((url_, title, path_file))
                            break

                        elif measuretype == 'Closest Defender':
                            params.update({
                                'LeagueID': '00', 
                                'CloseDefDistRange': ''
                            })
                            for closest in closest_opponent_shooting:
                                params['CloseDefDistRange'] = closest_opponent_shooting[closest]
                                url_ = get_url_with_params(url, params)
                                path_file = f'{measuretype}/{season}_{seasontype}_{permode}_{closest}'
                                s.append((url_, title, path_file))
                            break

                        elif measuretype == 'Closest Defender +10':
                            params.update({
                                'LeagueID': '00', 
                                'CloseDefDistRange': '', 
                                'ShotDistRange': '>=10.0'
                            })
                            for closest10 in closest10_opponent_shooting:
                                params['CloseDefDistRange'] = closest10_opponent_shooting[closest10]
                                url_ = get_url_with_params(url, params)
                                path_file = f'{measuretype}/{season}_{seasontype}_{permode}_{closest10}'
                                s.append((url_, title, path_file))
                            break
            
    elif type == 'Hustle':
        for season in seasons:
            params_hustle['Season'] = season
            for seasontype in seasontypes_hustle:
                params_hustle['SeasonType'] = seasontypes_hustle[seasontype]
                for permode in permodes_hustle:
                    params_hustle['PerMode'] = permodes_hustle[permode]
                    url = get_url_with_params(URL.format(stats=type_stats[type]), params_hustle)
                    path_file = f'{season}_{seasontype}_{permode}'
                    s.append((url, title, path_file))

    elif type == 'Box Outs':
        for season in seasons:
            params_box_outs['Season'] = season
            for seasontype in seasontypes_box_outs:
                params_box_outs['SeasonType'] = seasontypes_box_outs[seasontype]
                for permode in permodes_hustle:
                    params_box_outs['PerMode'] = permodes_box_outs[permode]
                    url = get_url_with_params(URL.format(stats=type_stats[type]), params_box_outs)
                    path_file = f'{season}_{seasontype}_{permode}'
                    s.append((url, title, path_file))

    return s

def crawl_general():
    urls = get_urls('General')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            ss, sst, pm = params.split('_')
            resultSets = None
            if pm != '':
                data['Per_Mode'] = pm
                resultSets = data_json['resultSets'][0]
            else:
                resultSets = data_json['resultSet']
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                attrs = process_general[file]
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_clutch():
    urls = get_urls('Clutch')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            ss, sst, pm = params.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Per_Mode'] = pm
                attrs = process_general[file]
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_playtype():
    urls = get_urls('Playtype')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            ss, sst, pm = params.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Per_Mode'] = pm
                attrs = process_playtype
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_tracking():
    urls = get_urls('Tracking')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            ss, sst, pm = params.split('_')
            resultSets = data_json['resultSets'][0]
            attrs = process_tracking[file]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for i in headers_idx.keys():
                if i == 'AST_PTS_CREATED':
                    attrs['AST PTS CREATED'] = i
                    break
                elif i == 'AST_POINTS_CREATED':
                    attrs['AST PTS CREATED'] = i
                    break
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Per_Mode'] = pm
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_defense_dashboard():
    urls = get_urls('Defense Dashboard')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            ss, sst = params.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                attrs = process_defense_dashboard[file]
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_shot_dashboard():
    urls = get_urls('Shot Dashboard')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            ss, sst, pm = params.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Per_Mode'] = pm
                attrs = process_shot_dashboard
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_box_score():
    urls = get_urls('Box Score')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file = title.split('/')[-1]
            title = title.split('/')[0]
            ss, sst = path_file.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Team'] = result[headers_idx['TEAM_ABBREVIATION']]
                data['Match_up'] = result[headers_idx['MATCHUP']]
                data['Game_date'] = result[headers_idx['GAME_DATE']]
                data['W/L'] = result[headers_idx['WL']]
                attrs = process_box_score
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{file}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{file}] {path_file}, [FAIL]: {e}')

def crawl_advanced_box_scores():
    urls = get_urls('Advanced Box Scores')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            ss, sst = params.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Team'] = result[headers_idx['TEAM_ABBREVIATION']]
                data['Match_up'] = result[headers_idx['MATCHUP']]
                data['Game_date'] = result[headers_idx['GAME_DATE']]
                data['W/L'] = result[headers_idx['WL']]
                attrs = process_advance_box_scores[file]
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_shooting():
    urls = get_urls('Shooting')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file = title.split('/')[-1]
            title = title.split('/')[0]
            ss, sst, pm, dist = path_file.split('_')
            resultSets = data_json['resultSets']
            attrs = process_shooting[dist]
            for result in resultSets['rowSet']:
                data['Team_id'] = result[0]
                data['Team_name'] = result[1]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Per_mode'] = pm
                data['Distance_range'] = dist
                for attr in attrs:
                    num = result[attrs[attr]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)
                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_opponent_shooting():
    urls = get_urls('Opponent Shooting')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file, params = path_file.split('/')
            if file == 'Overall Opponent Shooting':
                ss, sst, pm, dist = params.split('_')
                resultSets = data_json['resultSets']
                attrs = process_shooting[dist]
                for result in resultSets['rowSet']:
                    data['Team_id'] = result[0]
                    data['Team_name'] = result[1]
                    data['Season'] = ss
                    data['Season_type'] = sst
                    data['Per_mode'] = pm
                    data['Distance_range'] = dist
                    for attr in attrs:
                        num = result[attrs[attr]]
                        if num is None:
                            data[attr] = None
                        else:
                            if attr.find('%') != -1:
                                data[attr] = round(num*100, 3)
                            else:
                                data[attr] = round(num, 3)

                    write_csv(f'{title}/{file}.csv', data)
            else:
                ss, sst, pm, range_ = params.split('_')
                resultSets = data_json['resultSets'][0]
                headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
                for result in resultSets['rowSet']:
                    data['Team_id'] = result[headers_idx['TEAM_ID']]
                    data['Team_name'] = result[headers_idx['TEAM_NAME']]
                    data['Season'] = ss
                    data['Season_type'] = sst
                    data['Per_Mode'] = pm
                    data[ranges[file]] = range_
                    attrs = process_shot_dashboard
                    for attr in attrs:
                        num = result[headers_idx[attrs[attr]]]
                        if num is None:
                            data[attr] = None
                        else:
                            if attr.find('%') != -1:
                                data[attr] = round(num*100, 3)
                            else:
                                data[attr] = round(num, 3)

                    write_csv(f'{title}/{file}.csv', data)
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{title}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{title}] {path_file}, [FAIL]: {e}')

def crawl_hustle():
    urls = get_urls('Hustle')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file = title.split('/')[-1]
            title = title.split('/')[0]
            ss, sst, pm = path_file.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Per_Mode'] = pm
                attrs = process_hustle
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{file}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{file}] {path_file}, [FAIL]: {e}')

def crawl_box_outs():
    urls = get_urls('Box Outs')
    for idx, (url, title, path_file) in enumerate(urls):
        try:
            req = check_requests(url, HEADERS)
            if req.status_code != 200:
                print(log.status(title=title, idx=idx, n=len(urls)), path_file, log.FAIL(f'status_code: {req.status_code}'))
                write_log('Team_stats', f'{title}/{path_file}, [FAIL] status_code: {req.status_code}')
                continue
            data_json = req.json()
            # -- process
            data = {}
            file = title.split('/')[-1]
            title = title.split('/')[0]
            ss, sst, pm = path_file.split('_')
            resultSets = data_json['resultSets'][0]
            headers_idx = {k:v for v, k in enumerate(resultSets['headers'])}
            for result in resultSets['rowSet']:
                data['Team_id'] = result[headers_idx['TEAM_ID']]
                data['Team_name'] = result[headers_idx['TEAM_NAME']]
                data['Season'] = ss
                data['Season_type'] = sst
                data['Per_Mode'] = pm
                attrs = process_box_outs
                for attr in attrs:
                    num = result[headers_idx[attrs[attr]]]
                    if num is None:
                        data[attr] = None
                    else:
                        if attr.find('%') != -1:
                            data[attr] = round(num*100, 3)
                        else:
                            data[attr] = round(num, 3)

                write_csv(f'{title}/{file}.csv', data)

            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.OK())
            write_log('Team_stats', f'[{file}] {path_file} [OK]')
        except Exception as e:
            print(log.status(title=f'{"Team_stats"}/{file}', idx=idx, n=len(urls)), path_file, log.FAIL(e)) 
            write_log('Team_stats', f'[{file}] {path_file}, [FAIL]: {e}')
        

# --- run all
def run():
    crawl_general()
    crawl_clutch()
    crawl_playtype()
    crawl_tracking()
    crawl_defense_dashboard()
    crawl_shot_dashboard()
    crawl_box_score()
    crawl_advanced_box_scores()
    crawl_shooting()
    crawl_opponent_shooting()
    crawl_hustle()
    crawl_box_outs()
    # try:
    #     t1 = Thread(target=crawl_general)
    #     t2 = Thread(target=crawl_clutch)
    #     t3 = Thread(target=crawl_playtype)
    #     t4 = Thread(target=crawl_tracking)
    #     t5 = Thread(target=crawl_defense_dashboard)
    #     t6 = Thread(target=crawl_shot_dashboard)
    #     t7 = Thread(target=crawl_box_score)
    #     t8 = Thread(target=crawl_advanced_box_scores)
    #     t9 = Thread(target=crawl_shooting)
    #     t10 = Thread(target=crawl_opponent_shooting)
    #     t11 = Thread(target=crawl_hustle)
    #     t12 = Thread(target=crawl_box_outs)
    #     t1.start()
    #     t2.start()
    #     t3.start()
    #     t4.start()
    #     t5.start()
    #     t6.start()
    #     t7.start()
    #     t8.start()
    #     t9.start()
    #     t10.start()
    #     t11.start()
    #     t12.start()
    #     t1.join()
    #     t2.join()
    #     t3.join()
    #     t4.join()
    #     t5.join()
    #     t6.join()
    #     t7.join()
    #     t8.join()
    #     t9.join()
    #     t10.join()
    #     t11.join()
    #     t12.join()
    #     print(log.OK('--------------- Done Team stats! ---------------'))
    # except:
    #     print ("error")