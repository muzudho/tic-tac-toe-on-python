from enum import Enum


class Piece(Enum):
    """駒とか、石とか、そういうやつだぜ☆（＾～＾）
    >>> from log import Log
    >>> from look_and_model import Piece
    >>> log = Log()
    >>> log.print(f'Nought={Piece.NOUGHT}')
    >>> log.print(f'Cross ={Piece.CROSS}')
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
            raise ValueError(f'Invalid piece=|{self.value}|')
