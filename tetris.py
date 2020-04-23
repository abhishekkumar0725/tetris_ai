import numpy as np

class Tetris:

    MAP_HEIGHT = 20
    MAP_WIDTH = 10
    MAP_EMPTY = 0
    MAP_TERRAIN = 1
    MAP_PLAYER = 2

    TETRIMINOS = {
        0 : { #O
            0: [(1, 0), (2, 0), (1, 1), (2, 1)],
            90: [(1, 0), (2, 0), (1, 1), (2, 1)],
            180: [(1, 0), (2, 0), (1, 1), (2, 1)],
            270: [(1, 0), (2, 0), (1, 1), (2, 1)], 
        },
        1 : { #I
            0: [(1, 0), (1, 1), (1, 2), (1, 3)],
            90: [(0, 1), (1, 1), (2, 1), (3, 1)],
            180: [(1, 0), (1, 1), (1, 2), (1, 3)],
            270: [(0, 2), (1, 2), (2, 2), (3, 2)] 
        },
        2 : { #T
            0: [(0,1), (1,0), (1,1), (1,2)],
            90: [(0,1), (1,1), (1,0), (1,2)],
            180: [(1,1), (1,2), (2,1), (0,1)],
            270: [(2,1), (1,0), (1,1), (1,2)]
        },
        3 : { #L
            0: [(1,0), (1,1), (1, 2), (2,2)],
            90: [(0,1), (1,1), (2,1), (2,0)],
            180: [(1,2), (1,1), (1,0), (0,0)],
            270: [(2,1), (0,1), (1,1), (0,2)]
        },
        4 : { #J
            0: [(1,0), (1,1), (1, 2), (0,2)],
            90: [(0,1), (1,1), (2,1), (2,2)],
            180: [(1,2), (1,1), (1,0), (2,0)],
            270: [(2,1), (0,1), (1,1), (0,0)]
        },
        5 : { #S
            0: [(2,0), (1,0), (1,1), (0,1)],
            90: [(0,0), (0,1), (1,1), (2,1)],
            180: [(0,1), (1,1), (1, 0), (2,0)],
            270: [(1,2), (0,0), (1,1), (0,1)]
        },
        6 : { #Z
            0: [(0,0), (1,0), (1,1), (2,1)],
            90: [(0,2), (0,1), (1,1), (1,0)],
            180: [(2,1), (1,1), (1,0), (0,0)],
            270: [(1,0), (1,1), (0,1), (0,2)]
        },
    }

    def __init__(self):
        self.newGame()

    def newGame(self):
        self.board= [[0 for _ in range(Tetris.MAP_WIDTH)] for _ in range(Tetris.MAP_HEIGHT)]
        self.gameOver = False
        self.score = 0
        self.nextPiece = self.selectPiece()
    
    def selectPiece(self):
        piece = int(np.random.random() * 7)     #select random piece
        self.nextState = [piece, 0]             #piece, rotation
        return Tetris.TETRIMINOS[piece][0]
    
    def newPiece(self):
        self.currentPiece = self.nextPiece
        self.currentState = self.nextState

        self.nextPiece = self.selectPiece()
        self.currentPos = [3, 0]

        if self.collision():
            self.gameOver = True
    
    def collision(self):
        for x, y in self.currentPiece:
            x += self.currentPos[0]
            y += self.currentPos[1]
            #constraints
            #Hit Wall or Already Set Piece
            if x < 0 or x >= Tetris.MAP_WIDTH or y < 0 or y >= Tetris.MAP_HEIGHT \
                or self.board[y][x] == Tetris.MAP_TERRAIN:
                return True
        return False

