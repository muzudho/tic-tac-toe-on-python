import copy
from enum import Enum
from log import Log
from look_and_model import Piece, Position
from position import PositionHelper
from win_lose_judgment import WinLoseJudgment


class UxiProtocol():
    """局面データを文字列にしたり、文字列を局面データに復元するのに使うぜ☆（＾～＾）"""

    @staticmethod
    def to_xfen(pos: "Position"):
        """現局面を xfen に変換するぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from uxi_protocol import UxiProtocol
        >>> log = Log()
        >>> pos = Position()
        >>> uxi = UxiProtocol()
        >>> log.print(f"xfen=|{uxi.to_xfen(pos)}|")
        xfen=|xfen 3/3/3 o|

        Returns
        -------
        str
            現局面のXFEN。
        """
        xfen = 'xfen '

        # StartingBoard
        spaces = 0
        for addr in [7, 8, 9, 4, 5, 6, 1, 2, 3]:
            piece = pos.starting_board[addr]
            if piece is None:
                spaces += 1
            else:
                if 0 < spaces:
                    xfen += str(spaces)
                    spaces = 0

                xfen += str(piece)

            if addr == 9 or addr == 6:
                if 0 < spaces:
                    xfen += str(spaces)
                    spaces = 0
                xfen += '/'

        # 残ってるスペースの flush を忘れないぜ☆（＾～＾）
        if 0 < spaces:
            xfen += str(spaces)

        # Phase
        xfen += f' {pos.friend}'

        # Moves
        if 0 < pos.pieces_num - pos.starting_pieces_num:
            xfen += ' moves'
            for i in range(pos.starting_pieces_num, pos.pieces_num):
                xfen += f' {pos.history[i]}'

        return xfen

    @staticmethod
    def from_xfen(xfen: str, log: "Log"):
        """xfen を board に変換するぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from uxi_protocol import UxiProtocol
        >>> log = Log()
        >>> pos = UxiProtocol.from_xfen('xfen xo1/xox/oxo o', log)
        >>> pos.pos(log)
        >>> pos = UxiProtocol.from_xfen('xfen 3/3/3 x moves 1 7 4 8 9 3 6 2 5', log)
        >>> pos.pos(log)
        [Next 10 move(s) | Go o]

        +---+---+---+
        | o | o | x | マスを選んでください。例 `do 7`
        +---+---+---+
        | x | x | x |    7 8 9
        +---+---+---+    4 5 6
        | x | o | o |    1 2 3
        +---+---+---+

        Returns
        -------
        "Position"
            または None
        """
        if not xfen.startswith("xfen "):
            return None

        pos = Position()

        # 文字数☆（＾～＾）
        starts = 0

        # 番地☆（＾～＾） 0 は未使用☆（＾～＾）
        # 7 8 9
        # 4 5 6
        # 1 2 3
        addr = 7

        class MachineState(Enum):
            # 最初☆（＾～＾）
            START = 1
            # 初期局面の盤上を解析中☆（＾～＾）
            STARTING_BOARD = 2
            # 手番の解析中☆（＾～＾）
            PHASE = 3
            # ` moves ` 読取中☆（＾～＾）
            MOVES_LABEL = 4
            # 棋譜の解析中☆（＾～＾）
            MOVES = 5

        machine_state = MachineState.START
        # 1文字ずつ舐めていくぜ☆（＾～＾）
        for (i, ch) in enumerate(xfen):
            if machine_state == MachineState.START:
                if i + 1 == len("xfen "):
                    # 先頭のキーワードを読み飛ばしたら次へ☆（＾～＾）
                    machine_state = MachineState.STARTING_BOARD

            elif machine_state == MachineState.STARTING_BOARD:
                if ch == 'x':
                    # 手番の順ではないので、手番は分からないぜ☆（＾～＾）
                    pos.starting_board[addr] = Piece.CROSS
                    pos.pieces_num += 1
                    addr += 1
                elif ch == 'o':
                    # 手番の順ではないので、手番は分からないぜ☆（＾～＾）
                    pos.starting_board[addr] = Piece.NOUGHT
                    pos.pieces_num += 1
                    addr += 1
                elif ch == '1':
                    addr += 1
                elif ch == '2':
                    addr += 2
                elif ch == '3':
                    addr += 3
                elif ch == '/':
                    addr -= 6
                elif ch == ' ':
                    # 明示的にクローン☆（＾～＾）
                    pos.board = copy.deepcopy(pos.starting_board)
                    pos.starting_pieces_num = pos.pieces_num
                    machine_state = MachineState.PHASE
                else:
                    log.print(f'Error   | xfen starting_board error: {ch}')
                    return None

            elif machine_state == MachineState.PHASE:
                if ch == 'x':
                    pos.friend = Piece.CROSS
                elif ch == 'o':
                    pos.friend = Piece.NOUGHT
                else:
                    log.print(f'Error   | xfen phase error: {ch}')
                    return None

                # 一時記憶。
                starts = i
                machine_state = MachineState.MOVES_LABEL

            elif machine_state == MachineState.MOVES_LABEL:
                if starts + len(" moves ") <= i:
                    machine_state = MachineState.MOVES

            elif machine_state == MachineState.MOVES:
                if ch != ' ':
                    UxiProtocol.do(pos, ch, log)

        return pos

    @staticmethod
    def do(pos: "Position", arg_str: str, log: "Log"):
        """未来へ駒を置くぜ☆（＾～＾） 最初は、合法手判定や勝敗判定をせずに　とりあえず動かせだぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from uxi_protocol import UxiProtocol
        >>> log = Log()
        >>> pos = Position()
        >>> uxi = UxiProtocol()
        >>> uxi.do(pos, '2', log)
        >>> pos.pos(log)
        [Next 2 move(s) | Go x]

        +---+---+---+
        |   |   |   | マスを選んでください。例 `do 7`
        +---+---+---+
        |   |   |   |    7 8 9
        +---+---+---+    4 5 6
        |   | o |   |    1 2 3
        +---+---+---+

        Parameters
        ----------
        arg_str :
            コマンドラインの残り。ここでは駒を置く場所。 `1` とか `7` など。
        log :
            ロガー。
        """
        try:
            addr = int(arg_str)
        except ValueError:
            log.print(f'Error   | `do 数字` で入力してくれだぜ☆（＾～＾） 引数=|{arg_str}|')
            return

        """
        # TODO 合法手判定☆（＾～＾）移動先のマスに駒があってはダメ☆（＾～＾）
        if addr < 1 or 9 < addr:
            log.print(f'Error   | 1～9 で指定してくれだぜ☆（＾～＾） 番地={addr}')
            return
        elif pos.board[addr] is not None:
            log.print(f'Error   | 移動先のマスに駒があってはダメだぜ☆（＾～＾） 番地={addr}')
            return
        """

        PositionHelper.do_move(pos, addr)

        # 勝ち負け判定☆（*＾～＾*）
        if WinLoseJudgment.is_opponent_win(pos):
            log.print(f'win {pos.friend}')
        elif WinLoseJudgment.is_draw(pos):
            log.print(f'draw')

    @staticmethod
    def undo(pos: "Position"):
        """未来の駒を１つ戻すぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position
        >>> from uxi_protocol import UxiProtocol
        >>> log = Log()
        >>> pos = UxiProtocol.from_xfen('xfen 3/3/3 x moves 1 7 4 8 9 3 6 2 5', log)
        >>> UxiProtocol.undo(pos)
        >>> pos.pos(log)
        [Next 9 move(s) | Go x]

        +---+---+---+
        | o | o | x | マスを選んでください。例 `do 7`
        +---+---+---+
        | x |   | x |    7 8 9
        +---+---+---+    4 5 6
        | x | o | o |    1 2 3
        +---+---+---+

        """
        PositionHelper.undo_move(pos)
