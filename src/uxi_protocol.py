from log import Log
from look_and_model import Piece, Position
from position import PositionHelper


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
        if 0 < pos.pieces_num:
            xfen += ' moves'
            for i in range(0, pos.pieces_num):
                xfen += f' {pos.history[i]}'

        return xfen

    """
    // / xfen を board に変換するぜ☆（＾～＾）
    pub fn from_xfen(xfen: & str) -> Option < Position > {
        if !xfen.starts_with("xfen ") {
            return None; }

        let mut pos = Position:: default();

        // 文字数☆（＾～＾）
        let mut starts = 0usize;
        // 番地☆（＾～＾） 0 は未使用☆（＾～＾）
        // 7 8 9
        // 4 5 6
        // 1 2 3
        let mut addr = 7;

        # [derive(Debug)]
        enum MachineState {
            // / 最初☆（＾～＾）
            Start,
            // / 初期局面の盤上を解析中☆（＾～＾）
            StartingBoard,
            // / 手番の解析中☆（＾～＾）
            Phase,
            // / ` moves ` 読取中☆（＾～＾）
            MovesLabel,
            // / 棋譜の解析中☆（＾～＾）
            Moves,
        }
        let mut machine_state = MachineState:: Start;
        // Rust言語では文字列に配列のインデックスを使ったアクセスはできないので、
        // 一手間かけるぜ☆（＾～＾）
        for (i, ch) in xfen.chars().enumerate() {
            match machine_state {
                MachineState: : Start = > {
                    if i + 1 == "xfen ".len() {
                        // 先頭のキーワードを読み飛ばしたら次へ☆（＾～＾）
                        machine_state = MachineState: : StartingBoard;                     }
                }
                MachineState: : StartingBoard = > match ch {
                    'x' = > {
                        pos.starting_board[addr] = Some(Piece:: Cross);
                        pos.pieces_num += 1;
                        addr += 1; }
                    'o' = > {
                        pos.starting_board[addr] = Some(Piece:: Nought);
                        pos.pieces_num += 1;
                        addr += 1; }
                    '1' = > addr += 1,
                    '2' = > addr += 2,
                    '3' = > addr += 3,
                    '/' = > addr -= 6,
                    ' ' = > {
                        // 明示的にクローン☆（＾～＾）
                        pos.board = pos.starting_board.clone();
                        machine_state = MachineState: : Phase;                     }
                    _ = > {
                        Log:: println(&format!("Error   | xfen starting_board error: {}", ch));
                        return None; }
                },
                MachineState: : Phase = > {
                    match ch {
                        'x' = > {
                            pos.friend = Piece: : Cross;                         }
                        'o' = > {
                            pos.friend = Piece: : Nought;                         }
                        _ = > {
                            Log:: println(&format!("Error   | xfen phase error: {}", ch));
                            return None; }
                    }
                    // 一時記憶。
                    starts = i;
                    machine_state = MachineState: : MovesLabel;                 }
                MachineState: : MovesLabel = > {
                    if starts + " moves ".len() <= i {
                        machine_state = MachineState: : Moves;                     }
                }
                MachineState: : Moves = > {
                    if ch == ' ' {
                    } else {
                        pos.do_(&ch.to_string()); }
                }
            }
        }

        Some(pos)
    }
    """

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
        # 合法手判定☆（＾～＾）移動先のマスに駒があってはダメ☆（＾～＾）
        if addr < 1 or 9 < addr:
            log.print(f'Error   | 1～9 で指定してくれだぜ☆（＾～＾） 番地={addr}')
            return
        elif pos.board[addr] is not None:
            log.print(f'Error   | 移動先のマスに駒があってはダメだぜ☆（＾～＾） 番地={addr}')
            return
        """

        PositionHelper.do_move(pos, addr)

        """
        # 勝ち負け判定☆（*＾～＾*）
        if pos.is_opponent_win():
            log.print(f'win {pos.friend}')
        elif pos.is_draw():
            log.print(f'draw')
        """

    """
    // / 未来の駒を１つ戻す
    pub fn undo(& mut self) {
        self.undo_move(); }


    }
    """
