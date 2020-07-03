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
