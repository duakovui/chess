import pygame as p
import sys
import ChessEngine
import bot

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = 64
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE));

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('cHeSS')
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False

    loadImages() #only do this once, before the while loop
    sqSelected = () #no square is selected, keep track of the last click of the user
    playerClicks = [] #keep track of player clicks
    gameOver = False

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # human's turn
            if gs.whiteToMove:
                # mouse handle
                if e.type == p.MOUSEBUTTONDOWN:
                    if not gameOver:
                        location = p.mouse.get_pos()  # x, y location of mouse
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if sqSelected == (row, col):  # the user clicked the same square twice
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()  # reset user clicks
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]

                        if gs.checkMate:
                            gameOver = True
                            if gs.whiteToMove:
                                drawText(screen, "BLACK WINS")
                            else:
                                drawText(screen, "WHITE WINS")
                        elif gs.staleMate:
                            gameOver = True
                            drawText(screen, "STALEMATE")

                # key handle
                if e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        gs.undoMove()
                        gs.undoMove()
                        moveMade = True
                        animate = False
                    if e.key == p.K_r:  # reset the board when 'r' is pressed
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False

                if moveMade:
                    if animate:
                        animateMove(gs.moveLog[-1], screen, gs.board, clock)
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    animate = False
            else:
                if not gameOver:
                    ai = bot.Engine(gs, 3, "b")
                    gs.makeMove(ai.getBestMove())
                    animateMove(gs.moveLog[-1], screen, gs.board, clock)
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    animate = False

                    if gs.checkMate:
                        gameOver = True
                        if gs.whiteToMove:
                            drawText(screen, "BLACK WINS")
                        else:
                            drawText(screen, "WHITE WINS")
                    elif gs.staleMate:
                        gameOver = True
                        drawText(screen, "STALEMATE")

        drawGameState(screen, gs, validMoves, sqSelected)

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    hightlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def hightlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be move
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transperancy value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight move from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawPieces(screen, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if(piece != "__"):
                screen.blit(IMAGES[piece], (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    colors = [p.Color("white"), p.Color("gray")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto retangle
        if move.pieceCaptured != "__":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()