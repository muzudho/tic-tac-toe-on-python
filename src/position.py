from look_and_model import Piece, Position


class PositionHelper():
    """ポジション☆（＾～＾）局面とか言われるやつだぜ☆（＾～＾）"""

    @staticmethod
    def do_move(pos: "Position", addr: int):
        """１手指すぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from position import PositionHelper
        >>> log = Log()
        >>> pos = Position()
        >>> PositionHelper.do_move(pos, 1)
        >>> print(pos.pos())
        [Next 2 move(s) | Go x]

        +---+---+---+
        |   |   |   | マスを選んでください。例 `do 7`
        +---+---+---+
        |   |   |   |    7 8 9
        +---+---+---+    4 5 6
        | o |   |   |    1 2 3
        +---+---+---+

        """

        # 石を置くぜ☆（＾～＾）
        pos.board[addr] = pos.friend

        # 棋譜に記すぜ☆（＾～＾）
        pos.history[pos.pieces_num] = addr

        # 棋譜に記した後にカウンターを増やすぜ☆（＾～＾）
        pos.pieces_num += 1

        # 手番は交代だぜ☆（＾～＾）
        pos.friend = PositionHelper.opponent(pos)

    @staticmethod
    def undo_move(pos: "Position"):
        """１手戻すぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from position import PositionHelper
        >>> log = Log()
        >>> pos = Position()
        >>> PositionHelper.undo_move(pos, 1)
        >>> print(pos.pos())
        [Next 1 move(s) | Go o]

        +---+---+---+
        |   |   |   | マスを選んでください。例 `do 7`
        +---+---+---+
        |   |   |   |    7 8 9
        +---+---+---+    4 5 6
        |   |   |   |    1 2 3
        +---+---+---+

        """

        # 手番は交代だぜ☆（＾～＾）
        pos.friend = PositionHelper.opponent(pos)

        # 手数は次の要素を指しているんで、先に戻してから、配列の中身を取り出せだぜ☆（＾～＾）
        pos.pieces_num -= 1

        # 置いたところの石は削除な☆（＾～＾）

        addr = pos.history[pos.pieces_num]
        pos.board[addr] = None

    @staticmethod
    def opponent(pos: "Position"):
        """
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from position import PositionHelper
        >>> log = Log()
        >>> pos = Position()
        >>> log.println(f'opponent=|{PositionHelper.opponent(pos)}|')
        opponent=|x|

        Returns
        -------
        "Piece"
            相手番☆（＾～＾）
        """
        if pos.friend == Piece.NOUGHT:
            return Piece.CROSS
        elif pos.friend == Piece.CROSS:
            return Piece.NOUGHT
        else:
            raise ValueError(f'Invalid friend={pos.friend}')
