import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves):  # called for AI move
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
