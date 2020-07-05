import time
from look_and_model import Search


class SearchPerformance():
    @staticmethod
    def sec(search: "Search"):
        """
        >>> import time
        >>> from log import Log
        >>> from look_and_model import Position, Search
        >>> from performance_measurement import SearchPerformance
        >>> pos = Position()
        >>> search = Search(pos.friend, pos.pieces_num, True)
        >>> time.sleep(1)
        >>> log.println(f'sec={SearchPerformance.sec(search)}')
        1.0

        Returns
        -------
        int
            秒
        """
        return (time.time() - search.stopwatch) // 1

    @staticmethod
    def nps(search: "Search"):
        """Node per second.
        >>> import time
        >>> from log import Log
        >>> from look_and_model import Position, Search
        >>> from performance_measurement import SearchPerformance
        >>> pos = Position()
        >>> search = Search(pos.friend, pos.pieces_num, True)
        >>> time.sleep(1)
        >>> log.println(f'nps={SearchPerformance.nps(search)}')
        0.0

        Returns
        -------
        int
            １秒間当たりの探索状態ノード数
        """
        sec = SearchPerformance.sec(search)
        if 0 < sec:
            return search.nodes // sec
        else:
            # 1秒未満で全部探索してしまった☆（＾～＾） 本当は もっと多いと思うんだが☆（＾～＾）
            return search.nodes
