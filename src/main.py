import time
from log import Log
from look_and_model import Piece, GameResult, Position, Search
from position import PositionHelper
from command_line_parser import CommandLineParser
from uxi_protocol import UxiProtocol
from win_lose_judgment import WinLoseJudgment
from performance_measurement import SearchHelper

# しょっぱなにプログラムが壊れてないかテストしているぜ☆（＾～＾）
# こんなとこに書かない方がいいが、テストを毎回するのが めんどくさいんで 実行するたびにテストさせているぜ☆（＾～＾）
log = Log()
log.clear()
log.print('Hello!\n')
log.write('World!\n')

log.print(f'Nought=|{Piece.NOUGHT}|')
log.print(f'Cross =|{Piece.CROSS}|')
log.print(f'Win   =|{GameResult.WIN}|')
log.print(f'Draw  =|{GameResult.DRAW}|')
log.print(f'Lose  =|{GameResult.LOSE}|')

pos = Position()
pos.pos(log)
pos.print_result(GameResult.WIN, Piece.NOUGHT, log)

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
pos = UxiProtocol.from_xfen('xfen 3/3/3 x moves 1 7 4 8 9 3 6 2 5', log)
pos.pos(log)
UxiProtocol.undo(pos)
pos.pos(log)

pos = UxiProtocol.from_xfen('xfen o2/xox/oxo x', log)
log.print(f'win=|{WinLoseJudgment.is_opponent_win(pos)}|')
pos = UxiProtocol.from_xfen('xfen xox/oxo/oxo x', log)
log.print(f'draw=|{WinLoseJudgment.is_draw(pos)}|')

time.sleep(1)
log.print(f'sec={SearchHelper.sec(search)}')
log.print(f'nps={SearchHelper.nps(search)}')


def main():
    """最初に実行する主な関数だと思ってくれだぜ☆（＾～＾）"""

    # 説明を出そうぜ☆（＾～＾）
    log = Log()
    log.clear()

    # 最初は全部のコマンドを実装できないが、だんだん増やしていけだぜ☆（＾～＾）
    log.print("""きふわらべの〇×ゲーム

コマンド:
`do 7` - 手番のプレイヤーが、 7 番地に印を付けます。
`go` - コンピューターが次の1手を示します。
`info-off` - info出力なし。
`info-on` - info出力あり(既定)。
`pos` - 局面表示。
`position xfen 3/3/3 o moves 5 1 2 8 4 6 3 7 9` - 初期局面と棋譜を入力。
`undo` - 1手戻します。
`xfen` - 現局面のxfen文字列表示。
""")

    # 初期局面
    pos = Position()
    # TODO info_enable = True

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

            """ TODO go は後回し☆（＾～＾）
            else if p.starts_with("go"):
                search = Search: : new(pos.friend, pos.pieces_num, info_enable)
                let (addr, result) = search.go(& mut pos)
                        if let Some(addr) = addr {
                    Log:: println(&format!("info result={:?}", result))
                    Log: : println(&format!("bestmove {}", addr))
                        } else {
                    Log: : println("resign")
                        }
            elif p.starts_with('info-off'):
                info_enable = False
            elif p.starts_with('info-on'):
                info_enable = True
            """

        elif p.starts_with('position'):
            p.go_next_to('position ')
            if p.rest != '':
                pos = UxiProtocol.from_xfen(p.rest, log)
        elif p.starts_with('pos'):
            pos.pos(log)
        elif p.starts_with('undo'):
            UxiProtocol.undo(pos)
        elif p.starts_with('xfen'):
            log.print(UxiProtocol.to_xfen(pos))
        else:
            log.print(f'Debug   | Invalid command=|{p.rest}|')


main()
