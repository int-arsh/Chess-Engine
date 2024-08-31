import pygame as p
import asyncio
import ChessEngine, aimove, button
from multiprocessing import Process, Queue


p.init()

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT

DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION  # 64
MAX_FPS = 15
IMAGES = {}

FONT_COLOR = (0, 0, 0)
font = p.font.Font(None, 20)

# Load sound files
start_sound = p.mixer.Sound('sounds/game-start.ogg')
move_sound = p.mixer.Sound('sounds/move-self.ogg')
move_sound_opponent = p.mixer.Sound('sounds/move-opponent.ogg')
castle_sound = p.mixer.Sound('sounds/castle.ogg')
capture_sound = p.mixer.Sound('sounds/capture.ogg')
check_sound = p.mixer.Sound('sounds/move-check.ogg')
promote_sound = p.mixer.Sound('sounds/promote.ogg')
game_end_sound = p.mixer.Sound('sounds/game-end.ogg')


async def mainMenu():
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    p.display.set_caption("Main Menu")
    clock = p.time.Clock()


    bg_image = p.image.load("images-menu/theme3.jpeg").convert()  # Adjust the path as necessary
    bg_image = p.transform.scale(bg_image, (BOARD_HEIGHT, BOARD_WIDTH))  # Scale the image to fit the screen

    # screen.fill(p.Color("blue"))

    # load button images
    quit_img = p.image.load("images-menu/quit.png").convert_alpha()
    back_img = p.image.load("images-menu/back.png").convert_alpha()
    vsAI_img = p.image.load("images-menu/vsAI.png").convert_alpha()
    white_img = p.image.load("images-menu/white.png").convert_alpha()
    black_img = p.image.load("images-menu/black.png").convert_alpha()
    playas_img = p.image.load("images-menu/playas.png").convert_alpha()
    passnplay_img = p.image.load("images-menu/passnplay.png").convert_alpha()
    options_img = p.image.load("images-menu/options.png").convert_alpha()
    play_img = p.image.load("images-menu/play.png").convert_alpha()

    # create button instances
    play_button = button.Button(75, 70, play_img, 1)
    options_button = button.Button(75, 160, options_img, 1)
    quit_button = button.Button(75, 250, quit_img, 1)

    passnplay_button = button.Button(55, 70, passnplay_img, 1)
    vsAI_button = button.Button(75, 160, vsAI_img, 1)
    back_button = button.Button(75, 250, back_img, 1)

    playas_button = button.Button(55, 155, playas_img, 1)

    white_button = button.Button(75, 100, white_img, 1)
    black_button = button.Button(75, 170, black_img, 1)

    menu_state = "main"
    clicked = False

    run = True
    while run:
        # screen.fill(p.Color("light blue"))
        screen.blit(bg_image, (0, 0))


        if menu_state == "main":
            if play_button.draw(screen) and not clicked:
                menu_state = "play"
                clicked = True
                p.time.delay(150)
            if quit_button.draw(screen):
                run = False
                clicked = True
            if options_button.draw(screen):
                menu_state = "options"
                clicked = True
                p.time.delay(150)


        if menu_state == "play":
            if passnplay_button.draw(screen) and not clicked:
                run = False
                await main(True, True)
                clicked = True
                p.time.delay(150)
            if vsAI_button.draw(screen) and not clicked:
                menu_state = "AI"
                clicked = True
                p.time.delay(150)
            if back_button.draw(screen) and not clicked:
                menu_state = "main"
                clicked = True
                p.time.delay(150)

        if menu_state == "options":
            if back_button.draw(screen) and not clicked:
                menu_state = "main"
                clicked = True
                p.time.delay(150)

        if menu_state == "AI":
            if playas_button.draw(screen) and not clicked:
                menu_state = "playas"
                clicked = True
                p.time.delay(150)
            if back_button.draw(screen) and not clicked:
                menu_state = "play"
                clicked = True
                p.time.delay(150)

        if menu_state == "playas":
            if white_button.draw(screen) and not clicked:
                clicked = True
                run = False
                p.time.delay(150)
                await main(True, False)
            if black_button.draw(screen) and not clicked:
                clicked = True
                run = False
                await main(False, True)
                p.time.delay(150)
            if back_button.draw(screen) and not clicked:
                menu_state = "AI"
                clicked = True
                p.time.delay(150)

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            if event.type == p.MOUSEBUTTONDOWN:
                clicked = False

        p.display.flip()
        clock.tick(MAX_FPS)
        await asyncio.sleep(0)



def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (SQ_SIZE, SQ_SIZE))
    # print(IMAGES)

async def main(playerOne=True, playerTwo=False):
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    p.display.set_caption("Main")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Aerial", 18, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    gameOver = False
    animate = False  # flag variable for when we should animate a move
    loadImages()
    sqSelected = ()
    playerClicks = []
    # playerOne = True  # If a Human is playing white, then True. If an AI is playing, then False
    # playerTwo = False  # Same as above but for black
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False
    gameEndSoundPlayed = False
    running = True
    start_sound.play()
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:  # if you click the same square twice or user clicked mouse log
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append 1st and 2nd click
                    if len(playerClicks) == 2 and humanTurn:  # after second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                if move.isPawnPromotion:
                                    gs.makeMove(validMoves[i], getPromotionChoice, screen)
                                else:
                                    gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()  # reset user clicks
                                playerClicks = []
                                if gs.inCheck():
                                    check_sound.play()
                                elif move.pieceCaptured == "--":
                                    if not gs.whiteToMove:
                                        move_sound.play()
                                    else:
                                        move_sound_opponent.play()
                                else:
                                    capture_sound.play()
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    gameEndSoundPlayed = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

        # AI move finder
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("thinking...")
                returnQueue = Queue()  # used to pass data between threads
                moveFinderProcess = Process(target=aimove.findBestMove, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start()  # call findBestMove(gs, validMoves, returnQueue)

            if not moveFinderProcess.is_alive():
                print("done thinking")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = aimove.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                if gs.inCheck():
                    check_sound.play()
                elif move.pieceCaptured == "--":
                    move_sound_opponent.play()
                else:
                    capture_sound.play()
                moveMade = True
                animate = True
                AIThinking = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate or gs.staleMate:
            gameOver = True
            if not gameEndSoundPlayed:
                game_end_sound.play()
                gameEndSoundPlayed = True
            text = 'Stalemate!' if gs.staleMate else 'Black wins by checkmate!' if gs.whiteToMove else 'White wins by checkmate!'
            drawEndGameText(screen, text)

        clock.tick(MAX_FPS)
        await asyncio.sleep(0)
        p.display.flip()
    await mainMenu()


def drawPromotionMenu(screen, move):
    width = SQ_SIZE
    height = 4*SQ_SIZE  # Adjusted height to fit four pieces
    if move.endRow > 3:
        menu_rect = p.Rect(move.endCol * SQ_SIZE, (move.endRow - 3) * SQ_SIZE, width, height)
    else:
        menu_rect = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, width, height)
    # Drawing the rectangle for the menu
    p.draw.rect(screen, p.Color('white'), menu_rect)

    # Load images for promotion options
    piece_options = ['Q', 'R', 'B', 'N']
    images = {
        'Q': p.transform.scale(p.image.load(f'images/{move.pieceMoved[0]}Q.png'), (SQ_SIZE, SQ_SIZE)),
        'R': p.transform.scale(p.image.load(f'images/{move.pieceMoved[0]}R.png'), (SQ_SIZE, SQ_SIZE)),
        'B': p.transform.scale(p.image.load(f'images/{move.pieceMoved[0]}B.png'), (SQ_SIZE, SQ_SIZE)),
        'N': p.transform.scale(p.image.load(f'images/{move.pieceMoved[0]}N.png'), (SQ_SIZE, SQ_SIZE)),
    }

    # Draw each image in the vertical menu
    for i, piece in enumerate(piece_options):
        screen.blit(images[piece], (menu_rect.x, menu_rect.y + i * SQ_SIZE))

    p.display.flip()
    return piece_options, menu_rect


def getPromotionChoice(screen, move):
    piece_options, menu_rect = drawPromotionMenu(screen, move)
    while True:
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                if menu_rect.collidepoint(x, y):
                    index = (y - menu_rect.y) // 64  # Determine which option was clicked
                    if 0 <= index < len(piece_options):
                        return piece_options[index]


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


'''
Highlight square selected and moves for piece selected 
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value (0, 255)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

            # Draw column labels (a, b, c, ...)
            if r == 7:
                col_label = font.render(chr(97 + c), True, FONT_COLOR)
                screen.blit(col_label, (c * SQ_SIZE + 54, 500))

            # Draw row labels (1, 2, 3, ...)
            if c == 0:
                row_label = font.render(str(DIMENSION - r), True, FONT_COLOR)
                screen.blit(row_label, (5, r * SQ_SIZE + 5))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draws the move log
'''
def drawMoveLog(screen, gs, font2):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):  # make sure black made a move
            moveString += str(moveLog[i+1]) + "  "
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font2.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    distance = abs(dR) + abs(dC)
    framesPerSquare = max(3, 10 - distance)  # frames to move one square
    frameCount = distance * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece into rectangle
        if move.pieceCaptured != '--' and not move.isEnpassantMove:
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font2 = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font2.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font2.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == '__main__':
    asyncio.run(mainMenu())
