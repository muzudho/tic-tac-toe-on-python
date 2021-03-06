from enum import Enum
import time


class Piece(Enum):
    """駒とか、石とか、そういうやつだぜ☆（＾～＾）
    >>> from look_and_model import Piece
    >>> print(f'Nought=|{Piece.NOUGHT}|')
    Nought=|o|
    >>> print(f'Cross =|{Piece.CROSS}|')
    Cross =|x|
    """

    # 文字もセットできるんだが、0を除く自然数を入れるほうが一般的かだぜ☆（＾～＾）？
    # o
    NOUGHT = 1

    # x
    CROSS = 2

    def __str__(self):
        if self.value == 1:
            return 'o'
        elif self.value == 2:
            return 'x'
        else:
            raise ValueError(f'Invalid Piece=|{self.value}|')


class GameResult(Enum):
    """〇×ゲームは完全解析できるから、評価ではなくて、ゲームの結果が分かるんだよな☆（＾～＾）
    >>> from log import Log
    >>> from look_and_model import GameResult
    >>> log = Log()
    >>> log.println(f'Win =|{GameResult.WIN}|')
    Win   =|win|
    >>> log.println(f'Draw=|{GameResult.DRAW}|')
    Draw  =|draw|
    >>> log.println(f'Lose=|{GameResult.LOSE}|')
    Lose  =|lose|
    """

    # 勝ち☆（＾～＾）
    WIN = 1

    # 引き分け☆（＾～＾）
    DRAW = 2

    # 負け☆（＾～＾）
    LOSE = 3

    def __str__(self):
        if self.value == 1:
            return 'win'
        elif self.value == 2:
            return 'draw'
        elif self.value == 3:
            return 'lose'
        else:
            raise ValueError(f'Invalid GameResult=|{self.value}|')


# Python に定数は無いから、定数の気分で使ってくれだぜ☆（＾～＾）
#
# 1スタートで9まで☆（＾～＾） 配列には0番地もあるから、要素数は10だぜ☆（＾～＾）
BOARD_LEN = 10

# 盤上に置ける最大の駒数だぜ☆（＾～＾） ９マスしか置くとこないから９だぜ☆（＾～＾）
SQUARES_NUM = 9


class Position():
    """
    局面☆（＾～＾）ゲームデータをセーブしたり、ロードしたりするときの保存されてる現状だぜ☆（＾～＾）
    """

    def __init__(self):
        """
        規定値☆（＾～＾）
        """

        """
        次に盤に置く駒☆（＾～＾）
        英語では 手番は your turn, 相手版は your opponent's turn なんで 手番という英語は無い☆（＾～＾）
        自分という意味の単語はプログラム用語と被りまくるんで、
        あまり被らない 味方(friend) を手番の意味で たまたま使ってるだけだぜ☆（＾～＾）
        """
        self.friend = Piece.NOUGHT

        """開始局面の盤の各マス☆（＾～＾） [0] は未使用☆（＾～＾）"""
        self.starting_board = [None] * BOARD_LEN

        """盤の上に最初から駒が何個置いてあったかだぜ☆（＾～＾）"""
        self.starting_pieces_num = 0

        """現状の盤の各マス☆（＾～＾） [0] は未使用☆（＾～＾）"""
        self.board = [None] * BOARD_LEN

        """棋譜だぜ☆（＾～＾）駒を置いた番地を並べてけだぜ☆（＾～＾）"""
        self.history = [0] * SQUARES_NUM

        """盤の上に駒が何個置いてあるかだぜ☆（＾～＾）"""
        self.pieces_num = 0

    def pos(self):
        """局面を表示するぜ☆（＾～＾）
        >>> from look_and_model import Position
        >>> pos = Position()
        >>> print(pos.pos())
        [Next 1 move(s) | Go o]

        +---+---+---+
        |   |   |   | マスを選んでください。例 `do 7`
        +---+---+---+
        |   |   |   |    7 8 9
        +---+---+---+    4 5 6
        |   |   |   |    1 2 3
        +---+---+---+

        Returns
        -------
        str:
            局面
        """

        def cell(index: int):
            """
            Returns
            -------
            str
                マスの横幅に合わせた石、または空欄。
            """
            if self.board[index] is None:
                return "   "
            else:
                return f" {self.board[index]} "

        s = f'[Next {self.pieces_num + 1} move(s) | Go {self.friend}]\n\n'
        s += """+---+---+---+
|{0}|{1}|{2}| マスを選んでください。例 `do 7`
+---+---+---+
|{3}|{4}|{5}|    7 8 9
+---+---+---+    4 5 6
|{6}|{7}|{8}|    1 2 3
+---+---+---+""".format(
            cell(7),
            cell(8),
            cell(9),
            cell(4),
            cell(5),
            cell(6),
            cell(1),
            cell(2),
            cell(3)
        )
        return s

    @staticmethod
    def result(result: "GameResult", winner: "Piece"):
        """着いていれば勝敗を表示するぜ☆（＾～＾） 負けが表示されるケースは無い☆（＾～＾）
        >>> from look_and_model import Position
        >>> print(Position.result(GameResult.WIN, Piece.NOUGHT))
        win o

        Returns
        -------
        str:
            着いていれば、勝敗
        """
        if result == GameResult.WIN:
            return f'win {winner}'
        elif result == GameResult.DRAW:
            return f'draw'
        else:
            None


class Search():
    """探索部☆（＾～＾）"""

    def __init__(self, friend: "Piece", start_pieces_num: int, info_enable: bool):
        """初期値
        Parameters
        ----------
        friend :
            この探索を始めたのはどっち側か☆（＾～＾）
        start_pieces_num :
            この探索を始めたときに石はいくつ置いてあったか☆（＾～＾）
        info_enable :
            info の出力の有無
        """

        self.start_friend = friend
        self.start_pieces_num = start_pieces_num
        """探索した状態ノード数☆（＾～＾）"""
        self.nodes = 0
        """この構造体を生成した時点からストップ・ウォッチを開始するぜ☆（＾～＾）
        [Stopwatch In Python](https://stackoverflow.com/questions/5890304/stopwatch-in-python)
        """
        self.stopwatch = time.time()
        self.info_enable = info_enable

    def pv(self, pos: "Position"):
        """Principal variation.
        >>> from log import Log
        >>> from look_and_model import Position, Search
        >>> log = Log()
        >>> pos = Position()
        >>> search = Search(pos.friend,pos.pieces_num,True)
        >>> log.println(f'pv={search.pv(pos)}')
        pv=||

        Returns
        -------
        str
            今読んでる読み筋☆（＾～＾）
        """

        pv = ""
        for t in range(self.start_pieces_num, pos.pieces_num):
            pv += f'{pos.history[t]} '
        return pv.rstrip()

    @staticmethod
    def info_header(pos: "Position"):
        """ヘッダー☆（＾～＾）
        >>> from look_and_model import Position, Search
        >>> pos = Position()
        >>> print(Search.info_header(pos))
        info nps ...... nodes ...... pv O X O X O X O X O

        Returns
        -------
        str:
            info
        """
        if pos.friend == Piece.NOUGHT:
            return 'info nps ...... nodes ...... pv O X O X O X O X O'
        elif pos.friend == Piece.CROSS:
            return 'info nps ...... nodes ...... pv X O X O X O X O X'
        else:
            raise ValueError(f'Invalid friend=|{pos.friend}|')

    def info_forward(self, nps: int, pos: "Position", addr: int, comment: str):
        """前向き探索中だぜ☆（＾～＾）
        >>> from look_and_model import Position, Search
        >>> pos = Position()
        >>> println(search.info_forward(0, pos, 1, 'Hello!'))
        info nps      0 nodes      0 pv                   | + [1] | ->   to height 1 |       |      | + "Hello!"

        Returns
        -------
        str:
            info
        """
        nodes = self.nodes
        pv = self.pv(pos)
        friend_str = '+' if pos.friend == self.start_friend else '-'
        height = 'none    ' if SQUARES_NUM < pos.pieces_num + \
            1 else f'height {pos.pieces_num + 1}'
        if comment is not None:
            comment_str = f' {friend_str} "{comment}"'
        else:
            comment_str = ""

        return f'info nps {nps: >6.0f} nodes {nodes: >6} pv {pv: <17} | {friend_str} [{addr}] | ->   to {height} |       |      |{comment_str}'

    def info_forward_leaf(self, nps: int, pos: "Position", addr: int, result: "GameResult", comment: str):
        """前向き探索で葉に着いたぜ☆（＾～＾）
        >>> from look_and_model import Position, Search
        >>> pos = Position()
        >>> println(search.info_forward_leaf(0, pos, 1, GameResult.WIN, 'Hello!'))
        info nps      0 nodes      0 pv                   | + [1] | .       height 0 |       | win  | + "Hello!"

        Returns
        -------
        str:
            info
        """
        nodes = self.nodes
        pv = self.pv(pos)
        friend_str = '+' if pos.friend == self.start_friend else '-'
        height = 'none    ' if SQUARES_NUM < pos.pieces_num else f'height {pos.pieces_num}'
        if result == GameResult.WIN:
            result_str = ' win  '
        elif result == GameResult.DRAW:
            result_str = ' draw '
        elif result == GameResult.LOSE:
            result_str = ' lose '
        else:
            raise ValueError(f'Invalid GameResult={result}')
        if comment is not None:
            comment_str = f' {friend_str} "{comment}"'
        else:
            comment_str = ""

        return f'info nps {nps: >6.0f} nodes {nodes: >6} pv {pv: <17} | {friend_str} [{addr}] | .       {height} |       |{result_str}|{comment_str}'

    def info_backward(self, nps: int, pos: "Position", addr: int, result: "GameResult", comment: str):
        """後ろ向き探索のときの表示だぜ☆（＾～＾）
        >>> from look_and_model import Position, Search
        >>> pos = Position()
        >>> println(search.info_backward(0, pos, 1, GameResult.WIN, 'Hello!'))
        info nps      0 nodes      0 pv                   |       | <- from height 0 | + [1] | win  | + "Hello!"

        Returns
        -------
        str:
            info
        """
        nodes = self.nodes
        pv = self.pv(pos)
        height = 'none    ' if SQUARES_NUM < pos.pieces_num else f'height {pos.pieces_num}'
        friend_str = '+' if pos.friend == self.start_friend else '-'
        if result == GameResult.WIN:
            result_str = ' win  '
        elif result == GameResult.DRAW:
            result_str = ' draw '
        elif result == GameResult.LOSE:
            result_str = ' lose '
        else:
            raise ValueError(f'Invalid GameResult={result}')
        if comment is not None:
            comment_str = f' {friend_str} "{comment}"'
        else:
            comment_str = ""

        return f'info nps {nps: >6.0f} nodes {nodes: >6} pv {pv: <17} |       | <- from {height} | {friend_str} [{addr}] |{result_str}|{comment_str}'
