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
# Step 1.
log = Log()
log.clear()
log.writeln('Hello, world!!')
log.println('こんにちわ、世界！！')
# こんにちわ、世界！！

# Step 2.
log.println(f'Nought=|{Piece.NOUGHT}|')
# Nought=|o|
log.println(f'Cross =|{Piece.CROSS}|')
# Cross =|x|
log.println(f'Win   =|{GameResult.WIN}|')
# Win   =|win|
log.println(f'Draw  =|{GameResult.DRAW}|')
# Draw  =|draw|
log.println(f'Lose  =|{GameResult.LOSE}|')
# Lose  =|lose|

pos = Position()
log.println(pos.pos())
# [Next 1 move(s) | Go o]
#
#         +---+---+---+
#         |   |   |   | マスを選んでください。例 `do 7`
#         +---+---+---+
#         |   |   |   |    7 8 9
#         +---+---+---+    4 5 6
#         |   |   |   |    1 2 3
#         +---+---+---+
log.println(Position.result(GameResult.WIN, Piece.NOUGHT))
# win o

search = Search(pos.friend, pos.pieces_num, True)
log.println(f'pv=|{search.pv(pos)}|')
# pv=||
log.println(Search.info_header(pos))
# info nps ...... nodes ...... pv O X O X O X O X O
# 適当な内容を入れて、入れ物として、入れた中身を見せてくれるか、チェックしろだぜ☆（＾～＾）
log.println(search.info_forward(
    123, pos, 1, 'Hello!'))
# info nps      0 nodes      0 pv                   | + [1] | ->   to height 1 |       |      | + "Hello!"
log.println(search.info_forward_leaf(456, pos, 1, GameResult.WIN, 'Hello!'))
# info nps      0 nodes      0 pv                   | + [1] | .       height 0 |       | win  | + "Hello!"
log.println(search.info_backward(789, pos,
                                 1, GameResult.WIN, 'Hello!'))
# info nps      0 nodes      0 pv                   |       | <- from height 0 | + [1] | win  | + "Hello!"

# Step 3.
PositionHelper.do_move(pos, 1)
log.println(pos.pos())
# [Next 2 move(s) | Go x]
#
#         +---+---+---+
#         |   |   |   | マスを選んでください。例 `do 7`
#         +---+---+---+
#         |   |   |   |    7 8 9
#         +---+---+---+    4 5 6
#         | o |   |   |    1 2 3
#         +---+---+---+
PositionHelper.undo_move(pos)
log.println(pos.pos())
# [Next 1 move(s) | Go o]
#
#         +---+---+---+
#         |   |   |   | マスを選んでください。例 `do 7`
#         +---+---+---+
#         |   |   |   |    7 8 9
#         +---+---+---+    4 5 6
#         |   |   |   |    1 2 3
#         +---+---+---+
log.println(f'opponent={PositionHelper.opponent(pos)}')

# Step 4.
p = CommandLineParser('Go to the Moon!')
log.println(f"Go to=|{p.starts_with('Go to')}|")
# Go to   =|True|
log.println(f"Goto =|{p.starts_with('Goto')}|")
# Goto    =|False|
log.println(f'p.starts=|{p.starts}|')
# p.starts=|0|
log.println(f'p.rest=|{p.rest}|')
# p.rest  =|Go to the Moon!|
p.go_next_to('Go to')
log.println(f'p.starts=|{p.starts}|')
# p.starts=|5|
log.println(f'p.rest=|{p.rest}|')
# p.rest  =| the Moon!|

# Step 5.
uxi = UxiProtocol()
log.println(f"xfen=|{uxi.to_xfen(pos)}|")
# xfen=|xfen 3/3/3 o|
uxi.do(pos, '2', log)
log.println(pos.pos())
# [Next 2 move(s) | Go x]
#
# +---+---+---+
# |   |   |   | マスを選んでください。例 `do 7`
# +---+---+---+
# |   |   |   |    7 8 9
# +---+---+---+    4 5 6
# |   | o |   |    1 2 3
# +---+---+---+
pos = UxiProtocol.from_xfen('xfen xo1/xox/oxo o', log)
log.println(pos.pos())
# [Next 9 move(s) | Go o]
#
# +---+---+---+
# | x | o |   | マスを選んでください。例 `do 7`
# +---+---+---+
# | x | o | x |    7 8 9
# +---+---+---+    4 5 6
# | o | x | o |    1 2 3
# +---+---+---+
pos = UxiProtocol.from_xfen('xfen 3/3/3 x moves 1 7 4 8 9 3 6 2 5', log)
log.println(pos.pos())
# win x
# [Next 10 move(s) | Go o]
#
# +---+---+---+
# | o | o | x | マスを選んでください。例 `do 7`
# +---+---+---+
# | x | x | x |    7 8 9
# +---+---+---+    4 5 6
# | x | o | o |    1 2 3
# +---+---+---+
UxiProtocol.undo(pos)
log.println(pos.pos())
# [Next 9 move(s) | Go x]
#
# +---+---+---+
# | o | o | x | マスを選んでください。例 `do 7`
# +---+---+---+
# | x |   | x |    7 8 9
# +---+---+---+    4 5 6
# | x | o | o |    1 2 3
# +---+---+---+

# Step 6.
# Step 7.
pos = UxiProtocol.from_xfen('xfen o2/xox/oxo x', log)
log.println(f'win=|{WinLoseJudgment.is_opponent_win(pos)}|')
# win=|True|
pos = UxiProtocol.from_xfen('xfen xox/oxo/oxo x', log)
log.println(f'draw=|{WinLoseJudgment.is_draw(pos)}|')
# draw=|True|

# Step 8.
# 探索してないんだから、 nodes も nps も 0 になるはずだよな☆（＾～＾）
time.sleep(1)
log.println(f'nodes={search.nodes}')
# nodes=0
log.println(f'sec  ={SearchPerformance.sec(search)}')
# sec  =1.0
log.println(f'nps  ={SearchPerformance.nps(search)}')
# nps  =0.0

# Step 9.
pos = UxiProtocol.from_xfen('xfen 3/3/3 o moves 1 5 2 3 7 4', log)
search = Search(pos.friend, pos.pieces_num, True)
(addr, result) = SearchComputer.go(pos, search, log)
# info nps ...... nodes ...... pv O X O X O X O X O
# info nps      1 nodes      1 pv 6                 | - [6] | ->   to height 8 |       |      | - "Search."
# info nps      2 nodes      2 pv 6 8               | + [8] | ->   to height 9 |       |      | + "Search."
# info nps      3 nodes      3 pv 6 8 9             | - [9] | .       height 9 |       | draw | - "It's ok."
# info nps      3 nodes      3 pv 6 8               |       | <- from height 8 | + [9] | draw |
# info nps      3 nodes      3 pv 6                 |       | <- from height 7 | - [8] | draw | - "Fmmm."
# info nps      4 nodes      4 pv 6 9               | + [9] | ->   to height 9 |       |      | + "Search."
# info nps      5 nodes      5 pv 6 9 8             | - [8] | .       height 9 |       | draw | - "It's ok."
# info nps      5 nodes      5 pv 6 9               |       | <- from height 8 | + [8] | draw |
# info nps      5 nodes      5 pv 6                 |       | <- from height 7 | - [9] | draw | - "Fmmm."
# info nps      5 nodes      5 pv                   |       | <- from height 6 | + [6] | draw | + "Fmmm."
# info nps      6 nodes      6 pv 8                 | - [8] | ->   to height 8 |       |      | - "Search."
# info nps      7 nodes      7 pv 8 6               | + [6] | .       height 8 |       | win  | + "Hooray!"
# info nps      7 nodes      7 pv 8                 |       | <- from height 7 | - [6] | win  |
# info nps      7 nodes      7 pv                   |       | <- from height 6 | + [8] | lose | + "Resign."
# info nps      8 nodes      8 pv 9                 | - [9] | ->   to height 8 |       |      | - "Search."
# info nps      9 nodes      9 pv 9 6               | + [6] | .       height 8 |       | win  | + "Hooray!"
# info nps      9 nodes      9 pv 9                 |       | <- from height 7 | - [6] | win  |
# info nps      9 nodes      9 pv                   |       | <- from height 6 | + [9] | lose | + "Resign."
log.println(f'result=|{result}|')
# result=|draw|
log.println(f'bestmove=|{addr}|')
# bestmove=|6|


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
                log.println(
                    f'info result={result} nps={SearchPerformance.nps(search)}')
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
        elif p.starts_with('quit'):
            return
        elif p.starts_with('undo'):
            UxiProtocol.undo(pos)
        elif p.starts_with('uxi'):
            log.println('uxiok tic-tac-toe v20200704.0.0')
        elif p.starts_with('xfen'):
            log.println(UxiProtocol.to_xfen(pos))
        else:
            log.println(f'Debug   | Invalid command=|{p.rest}|')


main()
