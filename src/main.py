from log import Log
from look_and_model import Piece

log = Log()
log.clear()
log.print("Hello!\n")
log.write("World!\n")

log.print(f'Nought={Piece.NOUGHT}')
log.print(f'Cross ={Piece.CROSS}')
