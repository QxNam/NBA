from collections import defaultdict

def processing_game_leader_info(game_data: dict) -> dict:
    payload = game_data['payload']

    if payload['date'] == None:
        return {}
    
    list_games = payload['date']['games']
    points = defaultdict(list)

    for game in list_games:
        # Game ID
        points['gameID'].append(game['profile']['gameId'])

        # Year, Date of game
        game_date_time = game['profile']['dateTimeEt']
        season_year = game_date_time.split('-')[0]
        game_date = game_date_time.split('T')[0]

        points['seasonYear'].append(season_year)
        points['gameDate'].append(game_date)

        team_keys = ['awayTeam', 'homeTeam']
        game_leader_keys = ['pointGameLeader', 'reboundGameLeader', 'assistGameLeader']

        for team_key in team_keys:
            team = game[team_key]

            points[team_key + 'Name'].append(team['profile']['name'])

            for game_leader_key in game_leader_keys:
                game_leader = team[game_leader_key]

                if game_leader == None:
                    leader_name = ''
                    leader_pts = ''
                    leader_reb = ''
                    leader_ast = ''
                else:
                    leader_name = game_leader['profile']['displayName']
                    game_leader_stats = game_leader['statTotal']
                    leader_pts = game_leader_stats['points']
                    leader_reb = game_leader_stats['rebs']
                    leader_ast = game_leader_stats['assists']
                
                points[team_key + 'Name' + game_leader_key].append(leader_name)

                if game_leader_key == 'pointGameLeader':
                    points[team_key + game_leader_key].append(leader_pts)
                elif game_leader_key == 'reboundGameLeader':
                    points[team_key + game_leader_key].append(leader_reb)
                else:
                    points[team_key + game_leader_key].append(leader_ast)
        
    data_processed = {
        'game_id': points['gameID'],
        'year': points['seasonYear'],
        'date': points['gameDate'],
        'away_team_name': points['awayTeamName'],
        'home_team_name': points['homeTeamName'],
        'away_team_name_pts': points['awayTeamNamepointGameLeader'],
        'away_team_pts_pts': points['awayTeampointGameLeader'],
        'away_team_name_reb': points['awayTeamNamereboundGameLeader'],
        'away_team_pts_reb': points['awayTeamreboundGameLeader'],
        'away_team_name_ast': points['awayTeamNameassistGameLeader'],
        'away_team_pts_ast': points['awayTeamassistGameLeader'],
        'home_team_name_pts': points['homeTeamNamepointGameLeader'],
        'home_team_pts_pts': points['homeTeampointGameLeader'],
        'home_team_name_reb': points['homeTeamNamereboundGameLeader'],
        'home_team_pts_reb': points['homeTeamreboundGameLeader'],
        'home_team_name_ast': points['homeTeamNameassistGameLeader'],
        'home_team_pts_ast': points['homeTeamassistGameLeader']
    }

    return data_processed


def processing_line_scores(game_data: dict) -> dict:
    payload = game_data['payload']

    if payload['date'] == None:
        return {}
    
    list_games = payload['date']['games']
    data_line_scores = defaultdict(list)

    for game in list_games:
        # Game ID
        data_line_scores['gameID'].append(game['profile']['gameId'])

        # Year, Date of game
        game_date_time = game['profile']['dateTimeEt']
        game_date = game_date_time.split('T')[0]
        data_line_scores['gameDate'].append(game_date)

        # Get location
        location_pattern = '{arena_name} {arena_location}'
        arena_name = game['profile']['arenaName']
        arena_location = game['profile']['arenaLocation']
        location = location_pattern.format(arena_name=arena_name, arena_location=arena_location)
        data_line_scores['location'].append(location)

        # Get attendance
        attendance = game['boxscore']['attendance']
        data_line_scores['attendance'].append(attendance)

        team_keys = ['awayTeam', 'homeTeam']

        others_ot_score_keys = [f'ot{times}Score' for times in range(4, 11)]

        for team_key in team_keys:
            team = game[team_key]

            data_line_scores[team_key + 'Name'].append(team['profile']['name'])

            team_score = team['score']
            data_line_scores[team_key + 'Score'].append(team_score['score'])
            data_line_scores[team_key + 'Q1'].append(team_score['q1Score'])
            data_line_scores[team_key + 'Q2'].append(team_score['q2Score'])
            data_line_scores[team_key + 'Q3'].append(team_score['q3Score'])
            data_line_scores[team_key + 'Q4'].append(team_score['q4Score'])
            data_line_scores[team_key + 'OT1'].append(team_score['ot1Score'])
            data_line_scores[team_key + 'OT2'].append(team_score['ot2Score'])
            data_line_scores[team_key + 'OT3'].append(team_score['ot3Score'])
            data_line_scores[team_key + 'OTOthers'].append(
                sum([team_score[score_key] for score_key in others_ot_score_keys])
            )
            data_line_scores[team_key + 'PITP'].append(team_score['pointsInPaint'])
            data_line_scores[team_key + 'FB_PTS'].append(team_score['fastBreakPoints'])
            data_line_scores[team_key + 'BIG_LD'].append(team_score['biggestLead'])

    data_processed = {
        'game_id': data_line_scores['gameID'],
        'date': data_line_scores['gameDate'],
        'location': data_line_scores['location'],
        'attendance': data_line_scores['attendance'],
        'away_team': data_line_scores['awayTeamName'],
        'home_team': data_line_scores['homeTeamName'],
        'away_team_score': data_line_scores['awayTeamScore'],
        'home_team_score': data_line_scores['homeTeamScore'],
        'away_team_q1': data_line_scores['awayTeamQ1'],
        'away_team_q2': data_line_scores['awayTeamQ2'],
        'away_team_q3': data_line_scores['awayTeamQ3'],
        'away_team_q4': data_line_scores['awayTeamQ4'],
        'away_team_ot1': data_line_scores['awayTeamOT1'],
        'away_team_ot2': data_line_scores['awayTeamOT2'],
        'away_team_ot3': data_line_scores['awayTeamOT3'],
        'away_team_ot_other': data_line_scores['awayTeamOTOthers'],
        'away_team_pitp': data_line_scores['awayTeamPITP'],
        'away_team_fb_pts': data_line_scores['awayTeamFB_PTS'],
        'away_team_big_ld': data_line_scores['awayTeamBIG_LD'],
        'home_team_q1': data_line_scores['homeTeamQ1'],
        'home_team_q2': data_line_scores['homeTeamQ2'],
        'home_team_q3': data_line_scores['homeTeamQ3'],
        'home_team_q4': data_line_scores['homeTeamQ4'],
        'home_team_ot1': data_line_scores['homeTeamOT1'],
        'home_team_ot2': data_line_scores['homeTeamOT2'],
        'home_team_ot3': data_line_scores['homeTeamOT3'],
        'home_team_ot_other': data_line_scores['homeTeamOTOthers'],
        'home_team_pitp': data_line_scores['homeTeamPITP'],
        'home_team_fb_pts': data_line_scores['homeTeamFB_PTS'],
        'home_team_big_ld': data_line_scores['homeTeamBIG_LD']
    }
    
    return data_processed