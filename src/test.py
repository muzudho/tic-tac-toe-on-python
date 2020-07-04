"""
ほんとは src ディレクトリの下に test を置くべきではないんだが、
Python は `ValueError: attempted relative import beyond top-level package` というエラーが出るんで
src ディレクトリの下に test を置いてるんだぜ☆（＾～＾）
"""
import unittest
from log import Log
from look_and_model import Piece, GameResult, Position


class TestLog(unittest.TestCase):

    def test_clear(self):
        log = Log()
        log.clear()
        with open(log.file, mode='r', encoding='utf-8') as f:
            s = f.read()
        self.assertEqual(s, '')

    def test_println(self):
        log = Log()
        log.clear()
        log.println('Hello!')
        with open(log.file, mode='r', encoding='utf-8') as f:
            s = f.read()
        self.assertEqual(s, 'Hello!\n')

    def test_writeln(self):
        log = Log()
        log.clear()
        log.writeln('World!')
        with open(log.file, mode='r', encoding='utf-8') as f:
            s = f.read()
        self.assertEqual(s, 'World!\n')


class TestLookAndModel(unittest.TestCase):

    def test_piece(self):
        self.assertEqual(f'{Piece.NOUGHT}', 'o')
        self.assertEqual(f'{Piece.CROSS}', 'x')

    def test_game_result(self):
        self.assertEqual(f'{GameResult.WIN}', 'win')
        self.assertEqual(f'{GameResult.DRAW}', 'draw')
        self.assertEqual(f'{GameResult.LOSE}', 'lose')

    def test_position_pos(self):
        pos = Position()
        self.assertEqual(pos.pos(), """[Next 1 move(s) | Go o]

        +---+---+---+
        |   |   |   | マスを選んでください。例 `do 7`
        +---+---+---+
        |   |   |   |    7 8 9
        +---+---+---+    4 5 6
        |   |   |   |    1 2 3
        +---+---+---+""")


if __name__ == '__main__':
    unittest.main()
