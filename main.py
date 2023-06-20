from services.game_history import GameHistory
from services.team_info import TeamInfo
from services.line_scores import LineScores

if __name__ == '__main__':
    game_history = GameHistory()
    game_history.crawler()
    
    team_info = TeamInfo()
    team_info.crawler()

    line_scores = LineScores()
    line_scores.crawler()
