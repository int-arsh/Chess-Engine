import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}


knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rockScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

whiteKingScores = [[3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [2, 3, 3, 4, 4, 3, 3, 2],
                   [1, 2, 2, 2, 2, 2, 2, 1],
                   [2, 2, 0, 0, 0, 0, 2, 2],
                   [2, 3, 1, 0, 0, 1, 3, 2]]

blackKingScores = [[2, 3, 1, 0, 0, 1, 3, 2],
                   [2, 2, 0, 0, 0, 0, 2, 2],
                   [1, 2, 2, 2, 2, 2, 2, 1],
                   [2, 3, 3, 4, 4, 3, 3, 2],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3],
                   [3, 4, 4, 5, 5, 4, 4, 3]]



piecePositionScores = {"N": knightScores, "Q": queenScores, "B": bishopScores, "R": rockScores, "wp": whitePawnScores,
                       "bp": blackPawnScores, "wK": whiteKingScores, "bK": blackKingScores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

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
def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None  # if it doesn't find a move then it picks a random move
    random.shuffle(validMoves)
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

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
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):  # 8
        for col in range(len(gs.board[row])):  # 8
            square = gs.board[row][col]  # going through each sq on board
            if square != "--":  # if there is piece
                # score it positionally
                piecePositionScore = 0
                if square[1] == "p" or square[1] == "K":  # for pawns
                    piecePositionScore = piecePositionScores[square][row][col]
                else:  # for other pieces
                    piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * .1
    return score



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
