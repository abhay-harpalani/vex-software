import numpy as np
from random import choice, sample
from time import sleep

empty = 2
white = 0
black = 1

initial_pos = [[empty] * 8 for i in range(8)]
initial_pos[3][3] = initial_pos[4][4] = white
initial_pos[3][4] = initial_pos[4][3] = black

piece_to_emoji = {
  empty: "🔲",
  black: "⚫",
  white: "⚪"
}

def initializeBoard(): return np.array(initial_pos)
def getTurn(turn): return piece_to_emoji[turn]

def printBoard(board):
  for row in board:
    print(" ".join(piece_to_emoji[piece] for piece in row))
    
def isTrapped(board, turn, r, c, r_incr, c_incr):
  r += r_incr
  c += c_incr
  if not (0 <= r < 8 and 0 <= c < 8) or board[r,c] != 1 - turn:
    return False
  r += r_incr
  c += c_incr
  while 0 <= r < 8 and 0 <= c < 8:
    if board[r,c] == empty:
      return False
    elif board[r,c] == turn:
      return True
    r += r_incr
    c += c_incr
  return False

def generateMoves(board, turn):
  moves = []
  full = True
  for r in range(8):
    for c in range(8):
      if board[r,c] == empty:
        if isTrapped(board, turn, r, c, 1, 0)        \
          or isTrapped(board, turn, r, c, -1, 0)      \
          or isTrapped(board, turn, r, c, 0, 1)        \
          or isTrapped(board, turn, r, c, 0, -1)        \
          or isTrapped(board, turn, r, c, 1, 1)          \
          or isTrapped(board, turn, r, c, 1, -1)          \
          or isTrapped(board, turn, r, c, -1, 1)           \
          or isTrapped(board, turn, r, c, -1, -1)           \
        :
          moves.append((r, c))
        full = False
  return None if full else moves

def flipPieces(board, turn, r, c, r_incr, c_incr):
  if isTrapped(board, turn, r, c, r_incr, c_incr):
    r += r_incr
    c += c_incr
    while 0 <= r < 8 and 0 <= c < 8:
      if board[r,c] == 1 - turn:
        board[r,c] = turn
        r += r_incr
        c += c_incr
      else:
        break
    
def playMove(board, turn, move):
  r, c = move
  board[r,c] = turn
  flipPieces(board, turn, r, c, 1, 0)
  flipPieces(board, turn, r, c, -1, 0)
  flipPieces(board, turn, r, c, 0, 1)
  flipPieces(board, turn, r, c, 0, -1)
  flipPieces(board, turn, r, c, 1, 1)
  flipPieces(board, turn, r, c, 1, -1)
  flipPieces(board, turn, r, c, -1, 1)
  flipPieces(board, turn, r, c, -1, -1)
  
def getResult(board):
  return np.sum(board == white) - np.sum(board == black)

# Main function to run game
def runGame(board=None, turn=black, print_enabled=True):
  if board is None:
    board = initializeBoard()
  passed_turns = 0
  while True:
    if print_enabled:
      print(f"Turn: {getTurn(turn)}")
      printBoard(board)

    moves = generateMoves(board, turn)
    if moves is None or passed_turns == 2:
      yield board, turn, None, getResult(board)
    elif len(moves) == 0:
      passed_turns += 1
      turn = 1 - turn
      print("PASSING.")
      continue
    else:
      passed_turns = 0

    played_move = yield board.copy(), turn, moves, None
    playMove(board, turn, played_move)
    turn = 1 - turn

def runRandomGame(delay=0.01):
  game = runGame()
  board, turn, moves, result = next(game)
  while moves is not None:
    random_move = choice(moves)
    print("Move:", random_move)
    board, turn, moves, result = game.send(random_move)
    sleep(delay)
  else:
    print("Game Over")
    print("Result:", result)
  game.close()
  
for i in range(1):
  runRandomGame(0.0001)