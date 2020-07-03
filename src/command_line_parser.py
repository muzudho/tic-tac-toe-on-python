class CommandLineParser():
    """入力されたコマンドを、読み取る手伝いをするぜ☆（＾～＾）"""

    def __init__(self, line: str):
        """初期値"""
        # 末尾の改行を除こうぜ☆（＾～＾）
        self.line = line.rstrip()
        # 文字数を調べようぜ☆（＾～＾）
        self.len = len(line)
        self._starts = 0

    @property
    def starts(self):
        return self._starts

    @property
    def rest(self):
        """
        >>> from log import Log
        >>> from command_line_parser import CommandLineParser
        >>> log = Log()
        >>> p = CommandLineParser('Go to the Moon!')
        >>> log.print(f"p.rest=|{p.rest}|")
        p.rest=|Go to the Moon!|
        >>> p.go_next_to('Go to')
        >>> log.print(f"p.rest=|{p.rest}|")
        p.rest=| the Moon!|

        Returns
        -------
        str
            残りの文字列
        """
        if self._starts < len(self.line):
            return self.line[self._starts:]
        else:
            return ""

    def starts_with(self, expected: str):
        """
        >>> from log import Log
        >>> from command_line_parser import CommandLineParser
        >>> log = Log()
        >>> p = CommandLineParser('Go to the Moon!')
        >>> log.print(f"Go to=|{p.starts_with('Go to')}|")
        Go to=|True|
        >>> log.print(f"Goto =|{p.starts_with('Goto')}|")
        Goto =|False|

        Returns
        -------
        bool
            開始の文字列が一致しているか。
        """
        len2 = len(expected)
        return len2 <= self.len and self.line[self._starts:len2] == expected

    def go_next_to(self, expected: str):
        """カーソルを進めるぜ☆（＾～＾）
        >>> from log import Log
        >>> from command_line_parser import CommandLineParser
        >>> log = Log()
        >>> p = CommandLineParser('Go to the Moon!')
        >>> log.print(f"p.starts=|{p.starts}|")
        p.starts=|0|
        >>> p.go_next_to('Go to')
        >>> log.print(f"p.starts=|{p.starts}|")
        p.starts=|5|
        """
        self._starts += len(expected)

    def __str__(self):
        """デバッグ用の文字列☆（＾～＾）
        文字列を タテボウで クォートする(挟む)のは わたしの癖で、
        |apple|banana|cherry| のように区切れる☆（＾～＾）
        そのうち めんどくさくなったら お前もこうなる☆ｍ９（＾～＾）
        """
        return f'line=|{self.line}| len={self.len} starts={self._starts}'
