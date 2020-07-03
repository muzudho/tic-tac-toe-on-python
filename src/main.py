from log import Log
from look_and_model import Piece, GameResult, Position, Search

log = Log()
log.clear()
log.print("Hello!\n")
log.write("World!\n")

log.print(f'Nought=|{Piece.NOUGHT}|')
log.print(f'Cross =|{Piece.CROSS}|')
log.print(f'Win   =|{GameResult.WIN}|')
log.print(f'Draw  =|{GameResult.DRAW}|')
log.print(f'Lose  =|{GameResult.LOSE}|')

pos = Position()
pos.pos(log)

search = Search(pos.friend, pos.pieces_num, True)
log.print(f'pv=|{search.pv(pos)}|')
Search.info_header(pos, log)
search.info_forward(pos, 1, 'Hello!', log)
search.info_forward_leaf(pos, 1, GameResult.WIN, 'Hello!', log)
