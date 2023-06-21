from services.game_history import GameHistory
from services.team_info import TeamInfo
from services.line_scores import LineScores
from services.lineups import LineUps
from services.team_standing import TeamStanding
from services.coaches import Coaches


if __name__ == '__main__':
    game_history = GameHistory()
    game_history.crawler()
    
    team_info = TeamInfo()
    team_info.crawler()

    line_scores = LineScores()
    line_scores.crawler()

    line_ups = LineUps()
    line_ups.crawler()

    team_standing = TeamStanding()
    team_standing.crawler()

    coaches = Coaches()
    coaches.crawler()
