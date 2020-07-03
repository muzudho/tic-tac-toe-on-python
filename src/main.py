from log import Log
from look_and_model import Piece, GameResult, Position, Search
from position import PositionHelper
from command_line_parser import CommandLineParser
from uxi_protocol import UxiProtocol

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
search.info_backward(pos, 1, GameResult.WIN, 'Hello!', log)

PositionHelper.do_move(pos, 1)
pos.pos(log)
PositionHelper.undo_move(pos)
pos.pos(log)
log.print(f'opponent={PositionHelper.opponent(pos)}')

p = CommandLineParser('Go to the Moon!')
log.print(f"Go to=|{p.starts_with('Go to')}|")
log.print(f"Goto =|{p.starts_with('Goto')}|")
log.print(f"p.starts=|{p.starts}|")
log.print(f"p.rest=|{p.rest}|")
p.go_next_to('Go to')
log.print(f"p.starts=|{p.starts}|")
log.print(f"p.rest=|{p.rest}|")

uxi = UxiProtocol()
log.print(f"xfen=|{uxi.to_xfen(pos)}|")
uxi.do(pos, '2', log)
pos.pos(log)
pos = UxiProtocol.from_xfen('xfen xo1/xox/oxo o', log)
pos.pos(log)
