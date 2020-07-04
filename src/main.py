import time
from log import Log
from look_and_model import Piece, GameResult, Position, Search
from position import PositionHelper
from command_line_parser import CommandLineParser
from uxi_protocol import UxiProtocol
from win_lose_judgment import WinLoseJudgment
from performance_measurement import SearchPerformance
from computer_player import SearchComputer

# しょっぱなにプログラムが壊れてないかテストしているぜ☆（＾～＾）
# こんなとこに書かない方がいいが、テストを毎回するのが めんどくさいんで 実行するたびにテストさせているぜ☆（＾～＾）
log = Log()
log.clear()
log.println('Hello!\n')
log.writeln('World!\n')

log.println(f'Nought=|{Piece.NOUGHT}|')
log.println(f'Cross =|{Piece.CROSS}|')
log.println(f'Win   =|{GameResult.WIN}|')
log.println(f'Draw  =|{GameResult.DRAW}|')
log.println(f'Lose  =|{GameResult.LOSE}|')

pos = Position()
log.println(pos.pos())
pos.print_result(GameResult.WIN, Piece.NOUGHT, log)

search = Search(pos.friend, pos.pieces_num, True)
log.println(f'pv=|{search.pv(pos)}|')
log.println(Search.info_header(pos))
log.println(search.info_forward(
    SearchPerformance.nps(search), pos, 1, 'Hello!'))
log.println(search.info_forward_leaf(SearchPerformance.nps(
    search), pos, 1, GameResult.WIN, 'Hello!'))
log.println(search.info_backward(SearchPerformance.nps(search), pos,
                                 1, GameResult.WIN, 'Hello!'))

PositionHelper.do_move(pos, 1)
log.println(pos.pos())
PositionHelper.undo_move(pos)
log.println(pos.pos())
log.println(f'opponent={PositionHelper.opponent(pos)}')

p = CommandLineParser('Go to the Moon!')
log.println(f"Go to=|{p.starts_with('Go to')}|")
log.println(f"Goto =|{p.starts_with('Goto')}|")
log.println(f"p.starts=|{p.starts}|")
log.println(f"p.rest=|{p.rest}|")
p.go_next_to('Go to')
log.println(f"p.starts=|{p.starts}|")
log.println(f"p.rest=|{p.rest}|")

uxi = UxiProtocol()
log.println(f"xfen=|{uxi.to_xfen(pos)}|")
uxi.do(pos, '2', log)
log.println(pos.pos())
pos = UxiProtocol.from_xfen('xfen xo1/xox/oxo o', log)
log.println(pos.pos())
pos = UxiProtocol.from_xfen('xfen 3/3/3 x moves 1 7 4 8 9 3 6 2 5', log)
log.println(pos.pos())
UxiProtocol.undo(pos)
log.println(pos.pos())

pos = UxiProtocol.from_xfen('xfen o2/xox/oxo x', log)
log.println(f'win=|{WinLoseJudgment.is_opponent_win(pos)}|')
pos = UxiProtocol.from_xfen('xfen xox/oxo/oxo x', log)
log.println(f'draw=|{WinLoseJudgment.is_draw(pos)}|')

time.sleep(1)
log.println(f'sec={SearchPerformance.sec(search)}')
log.println(f'nps={SearchPerformance.nps(search)}')

pos = UxiProtocol.from_xfen('xfen 3/3/3 o moves 1 5 2 3 7 4', log)
search = Search(pos.friend, pos.pieces_num, True)
(addr, result) = SearchComputer.go(pos, search, log)
log.println(f'result=|{result}|')
log.println(f'bestmove=|{addr}|')


def main():
    """最初に実行する主な関数だと思ってくれだぜ☆（＾～＾）"""

    # 説明を出そうぜ☆（＾～＾）
    log = Log()
    log.clear()

    # 最初は全部のコマンドを実装できないが、だんだん増やしていけだぜ☆（＾～＾）
    log.println("""きふわらべの〇×ゲーム

コマンド:
`do 7` - 手番のプレイヤーが、 7 番地に印を付けます。
`go` - コンピューターが次の1手を示します。
`info-off` - info出力なし。
`info-on` - info出力あり(既定)。
`pos` - 局面表示。
`position xfen 3/3/3 o moves 5 1 2 8 4 6 3 7 9` - 初期局面と棋譜を入力。
`undo` - 1手戻します。
`uxi` - 'uxiok tic-tac-toe {protocol-version}' を返します。
`xfen` - 現局面のxfen文字列表示。
""")

    # 初期局面
    pos = Position()

    # info_enable は 'computer_player.py' を実装してから、ここに追加しろだぜ☆（＾～＾）
    info_enable = True

    # [Ctrl]+[C] でループを終了
    while True:
        # まず最初に、コマンドライン入力を待機しろだぜ☆（＾～＾）
        line = input()

        # コマンドライン☆（＾～＾） p は parser の意味で使ってるぜ☆（＾～＾）
        p = CommandLineParser(line)

        # 本当は よく使うコマンド順に並べた方が高速だが、先に見つけた方が選ばれるので後ろの方を漏らしやすくて むずかしいし、
        # だから、アルファベット順に並べた方が見やすいぜ☆（＾～＾）
        if p.starts_with('do'):
            p.go_next_to('do ')
            if p.rest != '':
                UxiProtocol.do(pos, p.rest, log)

        # go は 'computer_player.py' を実装してから、ここに追加しろだぜ☆（＾～＾）
        elif p.starts_with("go"):
            search = Search(pos.friend, pos.pieces_num, info_enable)
            (addr, result) = SearchComputer.go(pos, search, log)
            if addr is not None:
                log.println(f'info result={result}')
                log.println(f'bestmove {addr}')
            else:
                log.println('resign')

        # info-off は 'computer_player.py' を実装してから、ここに追加しろだぜ☆（＾～＾）
        elif p.starts_with('info-off'):
            info_enable = False
        # info-on は 'computer_player.py' を実装してから、ここに追加しろだぜ☆（＾～＾）
        elif p.starts_with('info-on'):
            info_enable = True

        elif p.starts_with('position'):
            p.go_next_to('position ')
            if p.rest != '':
                pos = UxiProtocol.from_xfen(p.rest, log)
        elif p.starts_with('pos'):
            log.println(pos.pos())
        elif p.starts_with('undo'):
            UxiProtocol.undo(pos)
        elif p.starts_with('uxi'):
            log.println('uxiok tic-tac-toe v20200704.0.0')
        elif p.starts_with('xfen'):
            log.println(UxiProtocol.to_xfen(pos))
        else:
            log.println(f'Debug   | Invalid command=|{p.rest}|')


main()
