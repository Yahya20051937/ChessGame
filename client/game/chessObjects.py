import pygame


class Square:
    MoveEffect = (150, 255, 150)
    CaptureEffect = (210, 10, 10)
    EscapeEffect = (100, 120, 100)
    ShowBlockEffect = (150, 200, 100)
    objects = []

    @staticmethod
    def getSquare(X, Y):
        for square in Square.objects:
            if square.topLeftPosition.chessX == X and square.topLeftPosition.chessY == Y:
                return square

    def __init__(self, topLeftPosition, width, height):
        self.topLeftPosition = topLeftPosition
        self.rect = pygame.Rect(self.topLeftPosition.get_x(), self.topLeftPosition.get_y(), width, height)

        self.currentPiece = None
        self.showMoveEffect = False
        self.showCaptureEffect = False
        self.showEscapeEffect = False
        self.showBlockEffect = False
        Square.objects.append(self)
        # self.removeMoveEffect = False

    def update(self, pieces, screen):
        from .functions import comparePieceSquare
        if self.showMoveEffect:
            pygame.draw.rect(screen, Square.MoveEffect, self.rect)
        elif self.showCaptureEffect:
            pygame.draw.rect(screen, Square.CaptureEffect, self.rect)
        elif self.showEscapeEffect:
            pygame.draw.rect(screen, Square.EscapeEffect, self.rect)
        elif self.showBlockEffect:
            pygame.draw.rect(screen, Square.ShowBlockEffect, self.rect)
        for piece in pieces:
            if piece.alive:
                if comparePieceSquare(piece=piece, square=self):
                    self.currentPiece = piece
                    return
        self.currentPiece = None

    def handleBlockingPiece(self, movingPiece, movement, opponent, screen, name, blockingPiece=None):
        from .movements_positions import CaptureMove, BlockedCaptureMove
        if self.currentPiece.color != movingPiece.color:
            if blockingPiece is None:
                captureMove = CaptureMove(movement=movement, destinationSquare=self,
                                          pieceToCapture=self.currentPiece, name=name)
                if captureMove.checkIfNotDangerous(movingPiece=movingPiece, opponent=opponent):
                    movingPiece.captureMoves.append(captureMove)
            else:
                if name not in [m.name for m in movingPiece.blockedCaptureMoves]:
                    blockedCaptureMove = BlockedCaptureMove(movement=movement, destinationSquare=self,
                                                            pieceToCapture=self.currentPiece, name=name,
                                                            blockingPiece=blockingPiece)
                    movingPiece.blockedCaptureMoves.append(blockedCaptureMove)

    def __repr__(self):
        return f'Square : {self.topLeftPosition.chessX, self.topLeftPosition.chessY, self.currentPiece}'
