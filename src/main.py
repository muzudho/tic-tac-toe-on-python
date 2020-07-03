from log import Log
from look_and_model import Piece, GameResult

log = Log()
log.clear()
log.print("Hello!\n")
log.write("World!\n")

log.print(f'Nought=|{Piece.NOUGHT}|')
log.print(f'Cross =|{Piece.CROSS}|')
log.print(f'Win   =|{GameResult.WIN}|')
log.print(f'Draw  =|{GameResult.DRAW}|')
log.print(f'Lose  =|{GameResult.LOSE}|')
