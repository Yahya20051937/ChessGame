def get_squares(board, screen):
    from .chessObjects import Square
    from .movements_positions import Position
    squares = []
    for x in range(1, 9):
        for y in range(1, 9):
            square = Square(topLeftPosition=Position(chessX=x, chessY=y, board=board, screen=screen),
                            width=board.get_width() / 8,
                            height=board.get_height() / 8)
            squares.append(square)
    return squares


def comparePieces(piece1, piece2):
    if piece1.Position.chessX == piece2.Position.chessX and piece1.Position.chessY == piece2.Position.chessY:
        return True
    return False


def comparePieceSquare(piece, square):
    if piece.Position.chessX == square.topLeftPosition.chessX and piece.Position.chessY == square.topLeftPosition.chessY:
        return True
    return False


def compareSquares(square1, square2):
    if square1.topLeftPosition.chessX == square2.topLeftPosition.chessX and square1.topLeftPosition.chessY == square2.topLeftPosition.chessY:
        return True
    return False


def changeActivePlayer(player1, player2, activePlayer):
    if player1.color != activePlayer.color:
        return player1
    else:
        return player2


def getPlayerKing(player):
    king = None
    for piece in player.pieces:
        if piece.name == 'king':
            king = piece
            return king


def getOpponent(page):
    if page.activePlayer.color == "black":
        return page.whitePlayer
    else:
        return page.blackPlayer


def getImageName(piece):

    if piece.name[:-1] == 'pawn':
        return 'pawn'
    if piece.name[:-1] == 'rook':
        return 'rook'
    if piece.name[:-1] == 'bishop':
        return 'bishop'
    if piece.name[:-1] == 'knight':
        return 'knight'
    else:
        return piece.name
