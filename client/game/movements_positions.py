class Position:
    def __init__(self, chessX, chessY, board, screen):
        self.chessX = chessX
        self.chessY = chessY
        self.board = board
        self.screen = screen

    def get_x(self):
        x = (self.chessX / 8) * self.board.get_width() - (self.board.get_width() / 8) + 300

        return x

    def get_y(self):
        y = (self.chessY / 8) * self.board.get_height() - (self.board.get_height() / 8)

        return y


class Move:
    @staticmethod
    def getDiagonalMoves(piece, opponent, screen):  # bishop, queen
        from .chessObjects import Square

        rightTopMove = 1
        blockingPiece = None
        while piece.Position.chessX + rightTopMove <= 8 and piece.Position.chessY - rightTopMove >= 1:
            movement = (piece.moveDiagonally, (+rightTopMove, -rightTopMove))
            destinationSquare = Square.getSquare(piece.Position.chessX + rightTopMove,
                                                 piece.Position.chessY - rightTopMove)
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='topRight', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    rightTopMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='topRight')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)
            rightTopMove += 1

        rightBottomMove = 1
        blockingPiece = None
        while piece.Position.chessX + rightBottomMove <= 8 and piece.Position.chessY + rightBottomMove <= 8:
            destinationSquare = Square.getSquare(
                piece.Position.chessX + rightBottomMove, piece.Position.chessY + rightBottomMove)
            movement = (piece.moveDiagonally, (+rightBottomMove, +rightBottomMove))
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='bottomRight', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    rightBottomMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement,
                            destinationSquare=destinationSquare, name='bottomRight')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)
            rightBottomMove += 1

        # Loop 3: Left-Top Move
        leftTopMove = 1
        blockingPiece = None
        while piece.Position.chessX - leftTopMove >= 1 and piece.Position.chessY - leftTopMove >= 1:
            destinationSquare = Square.getSquare(piece.Position.chessX - leftTopMove,
                                                 piece.Position.chessY - leftTopMove)
            movement = (piece.moveDiagonally, (-leftTopMove, -leftTopMove))
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='topLeft', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    leftTopMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='topLeft')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)

            leftTopMove += 1

        # Loop 4: Left-Bottom Move
        leftBottomMove = 1
        blockingPiece = None
        while piece.Position.chessX - leftBottomMove >= 1 and piece.Position.chessY + leftBottomMove <= 8:
            destinationSquare = Square.getSquare(piece.Position.chessX - leftBottomMove,
                                                 piece.Position.chessY + leftBottomMove)
            movement = (piece.moveDiagonally, (-leftBottomMove, leftBottomMove))
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='bottomLeft', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    leftBottomMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='bottomLeft')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)
            leftBottomMove += 1

    @staticmethod
    def getHorizontalMoves(piece, opponent, screen):
        from .chessObjects import Square

        rightMove = 1
        blockingPiece = None
        while piece.Position.chessX + rightMove <= 8:
            movement = (piece.moveHorizontally, (+rightMove,))
            destinationSquare = Square.getSquare(piece.Position.chessX + rightMove,
                                                 piece.Position.chessY)
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='right', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    rightMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement,
                            destinationSquare=destinationSquare, name='right')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)
            rightMove += 1

        leftMove = 1
        blockingPiece = None
        while piece.Position.chessX - leftMove >= 1:
            movement = (piece.moveHorizontally, (-leftMove,))
            destinationSquare = Square.getSquare(piece.Position.chessX - leftMove, piece.Position.chessY)
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='left', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    leftMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='left')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)
            leftMove += 1

    @staticmethod
    def getVerticalMoves(piece, opponent, screen):
        from .chessObjects import Square
        topMove = 1
        blockingPiece = None
        while piece.Position.chessY - topMove >= 1:
            movement = (piece.moveVertically, (-topMove,))
            destinationSquare = Square.getSquare(piece.Position.chessX, piece.Position.chessY - topMove)
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='top', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    topMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement,
                            destinationSquare=destinationSquare, name='top')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)
            topMove += 1

        bottomMove = 1
        blockingPiece = None
        while piece.Position.chessY + bottomMove <= 8:
            movement = (piece.moveVertically, (+bottomMove,))
            destinationSquare = Square.getSquare(piece.Position.chessX, piece.Position.chessY + bottomMove)
            if destinationSquare.currentPiece is not None:
                destinationSquare.handleBlockingPiece(movingPiece=piece, movement=movement, opponent=opponent,
                                                      screen=screen, name='bottom', blockingPiece=blockingPiece)
                if destinationSquare.currentPiece.color != piece.color:
                    blockingPiece = destinationSquare.currentPiece
                    bottomMove += 1
                    continue
                else:
                    break
            if blockingPiece is None:
                move = Move(movement=movement,
                            destinationSquare=destinationSquare, name='bottom')
                if move.checkIfNotDangerous(movingPiece=piece, opponent=opponent):
                    piece.normalMoves.append(move)
            bottomMove += 1

    def __init__(self, movement, destinationSquare, name):
        self.func, self.args = movement[0], movement[1]
        self.destinationSquare = destinationSquare
        self.name = name

    def __repr__(self):
        return f'{self.name}, {self.destinationSquare}'

    def make_move(self):

        self.func(*self.args)

    def checkIfNotDangerous(self, movingPiece, opponent):
        from .functions import comparePieces, getPlayerKing
        forbiddenMoves = {'right,left': 'top,bottom,topLeft,topRight,bottomLeft,bottomRight,L',
                          'top,bottom': 'right,left,topRight,topLeft,bottomLeft,bottomRight,L',
                          'topLeft,bottomRight,L': 'topRight,bottomLeft,top,bottom,left,right,L',
                          'topRight,bottomLeft,L': 'topLeft,bottomRight,top,bottom,left,right,L'
                          }
        isDangerous = False
        for piece in opponent.pieces:
            for blockedMove in piece.blockedCaptureMoves:
                if comparePieces(blockedMove.blockingPiece, movingPiece):
                    if comparePieces(getPlayerKing(movingPiece.player), blockedMove.pieceToCapture):
                        for key in forbiddenMoves.keys():
                            if blockedMove.name in key.split(','):
                                if self.name in forbiddenMoves[key].split(','):
                                    isDangerous = True

                                    break
        if isDangerous:
            return False
        return True


class CaptureMove(Move):

    def __init__(self, movement, destinationSquare, pieceToCapture, name):
        super().__init__(movement, destinationSquare, name)
        self.pieceToCapture = pieceToCapture

    def make_capture(self):
        self.func(*self.args)
        self.pieceToCapture.alive = False


class BlockedCaptureMove(CaptureMove):
    def __init__(self, movement, destinationSquare, pieceToCapture, name, blockingPiece):
        super().__init__(movement, destinationSquare, pieceToCapture, name)
        self.blockingPiece = blockingPiece
