from look_and_model import Position, BOARD_LEN
from position import PositionHelper


class WinLoseJudgment():
    """勝敗判定☆（＾～＾）"""

    @staticmethod
    def is_opponent_win(pos: "Position"):
        """石を置いてから 勝敗判定をするので、
        反対側の手番のやつが 石を３つ並べてたかどうかを調べるんだぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from uxi_protocol import UxiProtocol
        >>> from win_lose_judgment import WinLoseJudgment
        >>> log = Log()
        >>> pos = UxiProtocol.from_xfen('xfen o2/xox/oxo x', log)
        >>> log.println(f'win=|{WinLoseJudgment.is_opponent_win(pos)}|')
        win=|True|

        Returns
        -------
        bool
            反対側の手番の勝ち。
        """

        # 8パターンしかないので、全部チェックしてしまおうぜ☆（＾～＾）
        opponent = PositionHelper.opponent(pos)

        """
        (1) (2) (3) (4) (5) (6) (7) (8)
        xxx ... ... x.. .x. ..x x.. ..x
        ... xxx ... x.. .x. ..x .x. .x.
        ... ... xxx x.. .x. ..x ..x x..
        """
        return (opponent == pos.board[7] and opponent == pos.board[8] and opponent == pos.board[9]) or (
            opponent == pos.board[4] and opponent == pos.board[5] and opponent == pos.board[6]) or (
            opponent == pos.board[1] and opponent == pos.board[2] and opponent == pos.board[3]) or (
            opponent == pos.board[7] and opponent == pos.board[4] and opponent == pos.board[1]) or (
            opponent == pos.board[8] and opponent == pos.board[5] and opponent == pos.board[2]) or (
            opponent == pos.board[9] and opponent == pos.board[6] and opponent == pos.board[3]) or (
            opponent == pos.board[7] and opponent == pos.board[5] and opponent == pos.board[3]) or (
            opponent == pos.board[9] and opponent == pos.board[5] and opponent == pos.board[1])

    @staticmethod
    def is_draw(pos: "Position"):
        """石を置いてから 引き分け判定をするので、
        反対側の手番のやつが 勝ってなくて、
        かつ、全てのマスが埋まってたら引き分けだぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from uxi_protocol import UxiProtocol
        >>> from win_lose_judgment import WinLoseJudgment
        >>> log = Log()
        >>> pos = UxiProtocol.from_xfen('xfen xox/oxo/oxo x', log)
        >>> log.println(f'draw=|{WinLoseJudgment.is_draw(pos)}|')
        draw=|True|

        """
        if WinLoseJudgment.is_opponent_win(pos):
            return False

        for addr in range(1, BOARD_LEN):
            if pos.board[addr] is None:
                return False

        return True
