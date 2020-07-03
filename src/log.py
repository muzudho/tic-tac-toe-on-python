class Log:
    def __init__(self):
        self.file = 'tic-tac-toe-on-python.log'

    def clear(self):
        """ログを空っぽにします。
        >>> from log import Log
        >>> log = Log()
        >>> log.clear()
        """
        with open(self.file, mode='w') as f:
            f.write("")

    def print(self, contents: str):
        """表示かつ追加書込み。
        >>> from log import Log
        >>> log = Log()
        >>> log.print('Hello!')
        """
        print(contents)
        self.write(contents)

    def write(self, contents: str):
        """追加書込み。
        >>> from log import Log
        >>> log = Log()
        >>> log.write('World!')
        """
        with open(self.file, mode='a') as f:
            f.write(contents)
