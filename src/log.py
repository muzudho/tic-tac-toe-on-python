class Log:
    def __init__(self):
        self._file = 'tic-tac-toe-on-python.log'

    @property
    def file(self):
        return self._file

    def clear(self):
        """ログを空っぽにします。
        >>> from log import Log
        >>> log = Log()
        >>> log.clear()
        """
        with open(self._file, mode='w', encoding='utf-8') as f:
            f.write("")

    def writeln(self, contents: str):
        """追加書込み。
        >>> from log import Log
        >>> log = Log()
        >>> log.writeln('Hello, world!!')
        """
        with open(self._file, mode='a', encoding='utf-8') as f:
            f.write(f'{contents}\n')

    def println(self, contents: str):
        """表示かつ追加書込み。
        >>> from log import Log
        >>> log = Log()
        >>> log.println('こんにちわ、世界！！')
        こんにちわ、世界！！
        """
        # 末尾に改行が付くぜ☆（＾～＾）
        print(contents)
        self.writeln(contents)
