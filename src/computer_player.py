
from look_and_model import GameResult, Position, Search, BOARD_LEN, SQUARES_NUM
from position import PositionHelper
from win_lose_judgment import WinLoseJudgment
from performance_measurement import SearchPerformance


class SearchComputer():
    """
    サーチ☆（＾～＾）探索部とか言われてるやつだぜ☆（＾～＾）
    """

    @staticmethod
    def go(pos: "Position", search: "Search", log: "Log"):
        """最善の番地を返すぜ☆（＾～＾）
        >>> from log import Log
        >>> from look_and_model import Position, Search
        >>> from computer_player import SearchComputer
        >>> log = Log()
        >>> pos = UxiProtocol.from_xfen('xfen 3/3/3 o moves 1 5 2 3 7 4', log)
        >>> search = Search(pos.friend, pos.pieces_num, True)
        >>> (addr, result) = SearchComputer.go(pos, search, log)
        >>> log.println(f'result=|{result}|')
        >>> log.println(f'bestmove=|{addr}|')
        info nps ...... nodes ...... pv X O X O X O X O X
        info nps      0 nodes      1 pv 6                 | - [6] | ->   to height 8 |       |      | - "Search."
        info nps      0 nodes      2 pv 6 8               | + [8] | ->   to height 9 |       |      | + "Search."
        info nps      0 nodes      3 pv 6 8 9             | - [9] | .       height 9 |       | draw | - "It's ok."
        info nps      0 nodes      3 pv 6 8               |       | <- from height 8 | + [9] | draw | + "None"
        info nps      0 nodes      3 pv 6                 |       | <- from height 7 | - [8] | draw | - "Fmmm."
        info nps      0 nodes      4 pv 6 9               | + [9] | ->   to height 9 |       |      | + "Search."
        info nps      0 nodes      5 pv 6 9 8             | - [8] | .       height 9 |       | draw | - "It's ok."
        info nps      0 nodes      5 pv 6 9               |       | <- from height 8 | + [8] | draw | + "None"
        info nps      0 nodes      5 pv 6                 |       | <- from height 7 | - [9] | draw | - "Fmmm."
        info nps      0 nodes      5 pv                   |       | <- from height 6 | + [6] | win  | + "Ok."
        result=|win|
        bestmove=|6|

        Returns
        -------
        int :
        "GameResult" :
        """
        if search.info_enable:
            log.println(Search.info_header(pos))

        return SearchComputer.node(pos, search, log)

    @staticmethod
    def node(pos: "Position", search: "Search", log: "Log"):
        """
        手番が来たぜ☆（＾～＾）いわゆる search だぜ☆（＾～＾）

        Returns
        -------
        int :
        "GameResult" :
        """

        best_addr = None
        best_result = GameResult.LOSE

        for addr in range(1, BOARD_LEN):
            # 空きマスがあれば
            if pos.board[addr] is None:
                # とりあえず置いてみようぜ☆（＾～＾）
                PositionHelper.do_move(pos, addr)
                search.nodes += 1

                # 前向き探索というのは、葉っぱの方に進んでるとき☆（＾～＾）
                # 後ろ向き探索というのは、根っこの方に戻ってるとき☆（＾～＾）
                #
                # 勝ったかどうか判定しようぜ☆（＾～＾）？
                if WinLoseJudgment.is_opponent_win(pos):
                    # 勝ったなら☆（＾～＾）
                    # 前向き探索情報を出して、置いた石は戻して、後ろ向き探索情報を出して、探索終了だぜ☆（＾～＾）
                    if search.info_enable:
                        log.println(search.info_forward_leaf(
                            SearchPerformance.nps(search),
                            pos,
                            addr,
                            GameResult.WIN,
                            "Hooray!",
                        ))
                    PositionHelper.undo_move(pos)
                    if search.info_enable:
                        log.println(search.info_backward(
                            SearchPerformance.nps(search),
                            pos, addr, GameResult.WIN, None))

                    return (addr, GameResult.WIN)
                elif SQUARES_NUM <= pos.pieces_num:
                    # 勝っていなくて、深さ上限に達したら、〇×ゲームでは 他に置く場所もないから引き分け確定だぜ☆（＾～＾）
                    # 前向き探索情報を出して、置いた石は戻して、後ろ向き探索情報を出して、探索終了だぜ☆（＾～＾）
                    if search.info_enable:
                        log.println(search.info_forward_leaf(
                            SearchPerformance.nps(search),
                            pos,
                            addr,
                            GameResult.DRAW,
                            "It's ok.",
                        ))

                    PositionHelper.undo_move(pos)
                    if search.info_enable:
                        log.println(search.info_backward(
                            SearchPerformance.nps(search),
                            pos, addr, GameResult.DRAW, None))

                    return (addr, GameResult.DRAW)
                else:
                    # まだ続きがあるぜ☆（＾～＾）
                    if search.info_enable:
                        log.println(search.info_forward(
                            SearchPerformance.nps(search),
                            pos, addr, "Search."))

                # 相手の番だぜ☆（＾～＾）
                (_opponent_address, opponent_game_result) = SearchComputer.node(
                    pos, search, log)

                # 自分が置いたところを戻そうぜ☆（＾～＾）？
                PositionHelper.undo_move(pos)

                if opponent_game_result == GameResult.LOSE:
                    # 相手の負けなら、この手で勝ちだぜ☆（＾～＾）後ろ向き探索情報を出して、探索終わり☆（＾～＾）
                    if search.info_enable:
                        log.println(search.info_backward(
                            SearchPerformance.nps(search),
                            pos, addr, GameResult.WIN, "Ok."))
                    return (addr, GameResult.WIN)
                elif opponent_game_result == GameResult.DRAW:
                    # 勝ち負けがずっと見えてないなら☆（＾～＾）後ろ向き探索情報を出して、探索を続けるぜ☆（＾～＾）
                    if search.info_enable:
                        log.println(search.info_backward(
                            SearchPerformance.nps(search),
                            pos,
                            addr,
                            GameResult.DRAW,
                            "Fmmm.",
                        ))
                    if best_result == GameResult.LOSE:
                        # 更新
                        best_addr = addr
                        best_result = GameResult.DRAW
                elif opponent_game_result == GameResult.WIN:
                    # 相手が勝つ手を選んではダメだぜ☆（＾～＾）後ろ向き探索情報を出して、探索を続けるぜ☆（＾～＾）
                    if search.info_enable:
                        log.println(search.info_backward(
                            SearchPerformance.nps(search),
                            pos,
                            addr,
                            GameResult.LOSE,
                            "Resign.",
                        ))

        return (best_addr, best_result)
