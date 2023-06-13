import random as rd

class Engine:

    def __init__(self, gamestate, maxDepth, color):
        self.gamestate = gamestate
        self.color = color
        self.maxDepth = maxDepth
        self.best_move = None
        self.queen_locations = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.1],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]
        self.rook_locations = [
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        self.bishop_locations = [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
            [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
            [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
            [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        ]
        self.knight_location = [
            [-5.0, -2.0, -3.0, -3.0, -3.0, -3.0, -2.0, -5.0],
            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        ]
        self.pawn_locations = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def getBestMove(self):
        ai = self.engine(float("-inf"), float("inf"), 1)
        return self.best_move

    def evalFunct(self):
        compt = 0
        # Sums up the material values
        for i in range(8):
            for j in range(8):
                compt += self.squareResPoints(self.gamestate.board[i][j], i, j)
        compt += self.mateOpportunity() + 0.001 * rd.random()
        return compt

    def mateOpportunity(self):
        valid_moves = self.gamestate.getValidMoves()
        if len(valid_moves) == 0:
            if (self.gamestate.whiteToMove and self.color=="w") or (not self.gamestate.whiteToMove and self.color=="b"):
                return -999
            else:
                return 999
        else:
            return 0

    # Takes a square as input and
    # returns the corresponding Hans Berliner's
    # system value of it's resident
    def squareResPoints(self, square, i, j):
        square_value = 0
        if square[1] == "p":
            if square[0] == self.color:
                square_value += 1 + self.pawn_locations[i][j]
            else:
                square_value += -1
        if square[1] == "R":
            if square[0] == self.color:
                square_value += 5 + self.rook_locations[i][j]
            else:
                square_value += -5
        if square[1] == "N":
            if square[0] == self.color:
                square_value += 3.1 + self.knight_location[i][j]
            else:
                square_value += -3.1
        if square[1] == "B":
            if square[0] == self.color:
                square_value += 3.2 + self.bishop_locations[i][j]
            else:
                square_value += -3.2
        if square[1] == "Q":
            if square[0] == self.color:
                square_value += 9 + self.queen_locations[i][j]
            else:
                square_value += -9
        return square_value

    def engine(self, alpha, beta, depth):
        moveList = self.gamestate.getValidMoves()
        # reached max depth of search or no possible moves
        if depth == self.maxDepth or len(moveList) == 0:
            return self.evalFunct()

        if depth % 2 != 0:
            for i in moveList:
                self.gamestate.makeMove(i)
                val = self.engine(alpha, beta, depth + 1)
                if val > alpha:
                    alpha = val
                    if depth == 1:
                        self.best_move = i
                if alpha >= beta:
                    self.gamestate.undoMove()
                    break
                self.gamestate.undoMove()
            return alpha
        else:
            for i in moveList:
                self.gamestate.makeMove(i)
                val = self.engine(alpha, beta, depth + 1)
                if val < beta:
                    beta = val
                if alpha >= beta:
                    self.gamestate.undoMove()
                    break
                self.gamestate.undoMove()
            return beta












