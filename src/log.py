class Log:
    def __init__(self):
        self.file = 'tic-tac-toe-on-python.log'

    def clear(self):
        """ログを空っぽにします。
        >>> from log import Log
        >>> log = Log()
        >>> log.clear()
        """
        with open(self.file, mode='w', encoding='utf-8') as f:
            f.write("")

    def println(self, contents: str):
        """表示かつ追加書込み。
        >>> from log import Log
        >>> log = Log()
        >>> log.println('Hello!')
        """
        # 末尾に改行が付くぜ☆（＾～＾）
        print(contents)
        self.writeln(contents)

    def writeln(self, contents: str):
        """追加書込み。
        >>> from log import Log
        >>> log = Log()
        >>> log.writeln('World!')
        """
        with open(self.file, mode='a', encoding='utf-8') as f:
            f.write(f'{contents}\n')
