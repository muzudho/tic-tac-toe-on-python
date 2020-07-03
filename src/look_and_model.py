from enum import Enum


class Piece(Enum):
    """駒とか、石とか、そういうやつだぜ☆（＾～＾）
    >>> from log import Log
    >>> from look_and_model import Piece
    >>> log = Log()
    >>> log.print(f'Nought=|{Piece.NOUGHT}|')
    Nought=|o|
    >>> log.print(f'Cross =|{Piece.CROSS}|')
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
    >>> log.print(f'Win =|{GameResult.WIN}|')
    Win   =|win|
    >>> log.print(f'Draw=|{GameResult.DRAW}|')
    Draw  =|draw|
    >>> log.print(f'Lose=|{GameResult.LOSE}|')
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

        """
        開始局面の盤の各マス☆（＾～＾） [0] は未使用☆（＾～＾）
        """
        self.starting_board = [None] * BOARD_LEN

        """
        現状の盤の各マス☆（＾～＾） [0] は未使用☆（＾～＾）
        """
        self.board = [None] * BOARD_LEN

        """
        棋譜だぜ☆（＾～＾）駒を置いた番地を並べてけだぜ☆（＾～＾）
        """
        self.history = [0] * SQUARES_NUM

        """
        盤の上に駒が何個置いてあるかだぜ☆（＾～＾）
        """
        self.pieces_num = 0

    def pos(self, log: "Log"):
        """局面を表示するぜ☆（＾～＾）
        >>> from look_and_model import Position
        >>> pos = Position()
        >>> pos.pos()
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

        log.print(
            f'[Next {self.pieces_num + 1} move(s) | Go {self.friend}]\n')
        log.print(
            """+---+---+---+
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
            ))
