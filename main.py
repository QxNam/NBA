from services.game_history import GameHistory
from services.team_info import TeamInfo

if __name__ == '__main__':
    game_history = GameHistory()
    game_history.crawler()
    
    team_info = TeamInfo()
    team_info.crawler()
