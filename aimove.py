import random
import numpy as np

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]])

bishopScores = np.array([[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]])

queenScores = np.array([[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]])

rockScores = np.array([[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]])

whitePawnScores = np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]])

blackPawnScores = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]])

whiteKingScores = np.array([[3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [2, 3, 3, 4, 4, 3, 3, 2],
                   [1, 2, 2, 2, 2, 2, 2, 1],
                   [2, 2, 0, 0, 0, 0, 2, 2],
                   [2, 3, 1, 0, 0, 1, 3, 2]])

blackKingScores = np.array([[2, 3, 1, 0, 0, 1, 3, 2],
                   [2, 2, 0, 0, 0, 0, 2, 2],
                   [1, 2, 2, 2, 2, 2, 2, 1],
                   [2, 3, 3, 4, 4, 3, 3, 2],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3]])



piecePositionScores = {"N": knightScores, "Q": queenScores, "B": bishopScores, "R": rockScores, "wp": whitePawnScores,
                       "bp": blackPawnScores, "wK": whiteKingScores, "bK": blackKingScores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMove(validMoves):
    return random.choice(validMoves)

# Minmax without recursion

def findBestMoveMinMaxNoRecursion(gs, validMoves):  # called for AI move
    turnMultiplier = 1 if gs.whiteToMove else -1  # say -1 as AI move (black)
    opponentMinMaxScore = CHECKMATE  # 1000
    bestPlayerMove = None
    random.shuffle(validMoves)  # shuffle's black(ai moves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)  # for one of valid black move
        opponentsMoves = gs.getValidMoves()  # we get all possible white moves
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE  # -1000
        else:
            opponentMaxScore = -CHECKMATE  # -1000
            for opponentsMove in opponentsMoves:  # so this gives the white best move in response for a black move
                gs.makeMove(opponentsMove)  # for one of valid white move
                gs.getValidMoves()
                if gs.checkMate:
                    score = -turnMultiplier * CHECKMATE  # if it leads to checkmate score will be -(-1)*1000=1000
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)  # score = -(-1)*1(let pawn) = 1
                if score > opponentMaxScore:  # 1 > -1000 true
                    opponentMaxScore = score  # = 1
                gs.undoMove()  # undo that move and move to another one
        if opponentMaxScore < opponentMinMaxScore:  # 1<1000 (let say we find 1) if we find checkmate then didn't make a move
            opponentMinMaxScore = opponentMaxScore  # = 1
            bestPlayerMove = playerMove  # so we will have best black move in response of the best white move
        gs.undoMove()
    return bestPlayerMove


'''
Helper method to make first recursive call
'''
def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None  # if it doesn't find a move then it picks a random move
    random.shuffle(validMoves)
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    returnQueue.put(nextMove)

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:  # pruning happen
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):
    if gs.checkMate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE  # black wins
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(gs.board.shape[0]):  # 8
        for col in range(gs.board.shape[1]):  # 8
            square = gs.board[row][col]  # going through each sq on board
            if square != "--":  # if there is piece
                piece_type = square[1]
                piece_color = square[0]

                if piece_type in ["p", "K"]:  # For pawns and kings, differentiate between white and black
                    piecePositionScore = piecePositionScores[piece_color + piece_type][row][col]
                else:  # For other pieces like 'R', 'N', 'B', 'Q'
                    piecePositionScore = piecePositionScores[piece_type][row][col]

                # Calculate the piece score considering color
                if piece_color == 'w':
                    score += pieceScore[piece_type] + piecePositionScore * 0.1
                elif piece_color == 'b':
                    score -= pieceScore[piece_type] + piecePositionScore * 0.1
    return round(score, 1)



'''
Score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
