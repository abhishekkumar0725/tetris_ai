import numpy as np
import time
import cv2
from PIL import Image


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

    COLORS = [
        #R G B
        (255, 255, 255),
        (74, 226, 239),
        (255, 86, 102)
    ]

    def __init__(self):
        self.newGame()
        Tetris.COLORS = [color[::-1] for color in Tetris.COLORS]
        self.round = 1

    def newGame(self):
        self.board= [[0 for _ in range(Tetris.MAP_WIDTH)] for _ in range(Tetris.MAP_HEIGHT)]
        self.gameOver = False
        self.score = 0
        self.nextPiece = self.selectPiece()
        self.newPiece()
        return self.getFeautres()

    def selectPiece(self):
        piece = int(np.random.random() * 7)     #select random piece
        self.nextState = [piece, 0]             #piece, rotation
        return Tetris.TETRIMINOS[piece][0]

    def newPiece(self):
        self.currentPiece = self.nextPiece
        self.currentState = self.nextState

        self.nextPiece = self.selectPiece()
        self.currentPos = [4, 0]

        if self.collision():
            self.gameOver = True

    def collision(self):
        return self.potentialCollision(self.currentPiece, self.currentPos)
    
    def potentialCollision(self, piece, pos):
        for x, y in piece:
            x += pos[0]
            y += pos[1]
            #constraints
            #Hit Wall or Already Set Piece
            if x < 0 or x >= Tetris.MAP_WIDTH or y < 0 or y >= Tetris.MAP_HEIGHT \
                or self.board[y][x] == Tetris.MAP_TERRAIN:
                return True
        return False

    def placePiece(self):
        locX, locY= self.currentPos
        for x, y in self.currentPiece:
            self.board[y+locY][x+locX] = Tetris.MAP_TERRAIN

    def moveLeft(self):
        self.currentPos[0] -= 1
        if self.collision():
            self.currentPos += 1

    def moveRight(self):
        self.currentPos[0] += 1
        if self.collision():
            self.currentPos -= 1

    def rotateCW(self):
        self.currentState[1] = (self.currentState[1] + 90) % 360
        self.currentPiece = Tetris.TETRIMINOS[self.currentState[0]][self.currentState[1]]

    def rotateCCW(self):
        self.currentState[1] = (self.currentState[1] - 90) % 360
        self.currentPiece = Tetris.TETRIMINOS[self.currentState[0]][self.currentState[1]]

    def clearLines(self, board=None):
        if board == None:
            board = self.board
        lines  = [row for row in range(Tetris.MAP_HEIGHT) if sum(board[row])==Tetris.MAP_WIDTH]
        if lines == None:
            return 0
        lines.sort(reverse=True)
        for line in lines:
            board.pop(line)
            board.insert(0, [0 for _ in range(Tetris.MAP_WIDTH)])
        if board == None:
            self.board=board
        return len(lines)

    def getRenderBoard(self):
        display = []
        display = [row[:] for row in self.board]
        locX, locY = self.currentPos
        for x, y in self.currentPiece:
            display[y+locY][x+locX] = Tetris.MAP_PLAYER
        return display

    def render(self):
        #Render numpy array
        display = self.getRenderBoard()
        img = []
        for row in display:
            img.append([Tetris.COLORS[square] for square in row])
        img = np.array(img).reshape(Tetris.MAP_HEIGHT, Tetris.MAP_WIDTH, 3).astype(np.uint8)
        img = Image.fromarray(img, 'RGB')
        img = np.array(img.resize((Tetris.MAP_HEIGHT*20, Tetris.MAP_WIDTH*70)))
        cv2.putText(img, str(self.score), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        cv2.imshow('image', img)
        cv2.waitKey(1)

    def getHeights(self, board=None):
        if board == None:
            board  = self.board
        heights = []
        for column in zip(*board):
            if Tetris.MAP_TERRAIN not in column:
                heights.append(0)
                continue
            top = column.index(Tetris.MAP_TERRAIN)
            heights.append(Tetris.MAP_HEIGHT-top)

        return heights

    def getBumpiness(self, board=None):
        if board == None:
            board = self.board
        heights = self.getHeights(board)
        bumps = []
        for i in range(len(heights)-1):
            bumps.append(abs(heights[i+1]-heights[i]))
        return bumps

    def numHoles(self, board=None):
        if board == None:
            board  = self.board
        totalHoles = 0
        for column in zip(*board):
            i = 0
            while i < Tetris.MAP_HEIGHT and column[i] != Tetris.MAP_TERRAIN:
                i += 1
            totalHoles += len([x for x in column[i+1:] if x == Tetris.MAP_EMPTY])

        return totalHoles

    def getFeautres(self, board=None):
        if board == None:
            board = self.board
        holes = self.numHoles(board)
        height = self.getHeights(board)
        bumps = self.getBumpiness(board)
        lines = self.clearLines(board)
        if max(height) > 17:
            return [lines, holes, sum(bumps), sum(height)**2]
        return [lines, holes, sum(bumps), sum(height)]

    def getLegalActions(self):
        states= {}
        def potentialBoard(piece, pos):
            board = []
            board = [row[:] for row in self.board]
            locX, locY = pos
            for x, y in piece:
                xPos = x+locX
                yPos = y+locY
                board[yPos][xPos] = Tetris.MAP_TERRAIN
            return board

        for i in range(4):
            piece = Tetris.TETRIMINOS[self.currentState[0]][self.currentState[1] + 90*i]
            lowerX = min([p[0] for p in self.currentPiece])
            upperX = max([p[0] for p in self.currentPiece])

            for xLoc in range(-1*lowerX, Tetris.MAP_WIDTH - upperX):
                pos = [xLoc, 0]
                while not self.potentialCollision(piece, pos):
                    pos[1] += 1
                pos[1] -= 1
                
                if pos[1] >= 0:
                    newBoard = potentialBoard(piece, pos)
                    features = self.getFeautres(board=newBoard)
                    states[(xLoc, 90*i)] = features
        return states

    def play(self, xLoc=None, degrees=None, render = False):
        if xLoc != None:
            self.currentPos = [xLoc, 0]
        if degrees != None:
            while self.currentState[1] != degrees:
                self.rotateCW()

        #plays individual round
        while not self.collision():
            if render:
                self.render()
                time.sleep(.01) #Renders .01 second time
            self.currentPos[1] += 1
        self.currentPos[1] -= 1

        self.placePiece()
        cleared = self.clearLines()
        score = 1 + 4**cleared #scoring is exponential, but we can change
        self.score += score
        print(self.score)
        self.newPiece()
        return score, self.gameOver

    def stupidPlay(self):
        while not self.gameOver:
            self.play(render=True)
