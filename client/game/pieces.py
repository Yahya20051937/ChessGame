import time

import pygame


class Piece:

    def __init__(self, name, startingPosition, deadPosition, color, board):
        from .functions import getImageName
        self.name = name
        self.Position = startingPosition
        self.deadPosition = deadPosition

        self.player = None
        self.color = color
        try:
            self.width = board.get_width() / 8
            self.height = board.get_height() / 8
        except AttributeError:
            self.width = 0
            self.height = 0
        self.movesTypes = []
        self.normalMoves = []
        self.captureMoves = []
        self.blockedCaptureMoves = []
        self.blockAttackMoves = []
        self.alive = True
        self.mockDead = False
        self.image = pygame.transform.scale(pygame.image.load(f'game/assets/{getImageName(self)}--{self.color}.png'),
                                            (self.width, self.height))
        self.rect = pygame.Rect(self.Position.get_x(), self.Position.get_y(), self.width, self.height)

    def __repr__(self):
        return f'{self.name} {self.color} {self.Position.chessX} {self.Position.chessY}'

    def update(self, screen, opponent):
        # print(self, len(self.normalMoves) + len(self.captureMoves))
        from .functions import getPlayerKing
        if self.alive:
            self.rect = pygame.Rect(self.Position.get_x(), self.Position.get_y(), self.width, self.height)
            self.normalMoves = []
            self.captureMoves = []
            self.blockAttackMoves = []
            self.blockedCaptureMoves = []
            if not self.mockDead:
                for moveType in self.movesTypes:
                    moveType(self, opponent, screen)

                if getPlayerKing(self.player).inDanger:
                    self.getBlockAttackMoves(opponent=opponent, screen=screen)

        else:

            self.normalMoves = []
            self.captureMoves = []
            self.blockAttackMoves = []
            self.blockedCaptureMoves = []

            self.rect = pygame.Rect(self.deadPosition.get_x(), self.deadPosition.get_y(), self.width, self.height)

        screen.blit(self.image, self.rect)

    def moveVertically(self, value):
        self.Position.chessY += value

    def moveHorizontally(self, value):
        self.Position.chessX += value

    def moveDiagonally(self, valueX, valueY):
        self.Position.chessX += valueX
        self.Position.chessY += valueY

    def displayPossibleMoves(self, squares, reverse=False):
        """
        If the king is in danger, we display only the block attack moves, otherwise, we display all the possible moves
        :param squares:
        :param reverse:
        :return:
        """
        from .functions import compareSquares, getPlayerKing
        king = getPlayerKing(self.player)
        if king.inDanger:

            for move in self.blockAttackMoves:

                for square in squares:
                    if compareSquares(square1=square, square2=move.destinationSquare):

                        if not reverse:
                            square.showBlockEffect = True
                        else:
                            square.showBlockEffect = False

                        break
            return
        for move in self.normalMoves:
            for square in squares:
                if compareSquares(square, move.destinationSquare):
                    if not reverse:
                        square.showMoveEffect = True
                    else:
                        square.showMoveEffect = False
                    break
        for move in self.captureMoves:
            for square in squares:
                if compareSquares(square, move.destinationSquare):
                    if not reverse:
                        square.showCaptureEffect = True
                    else:
                        square.showCaptureEffect = False

    def getBlockAttackMoves(self, opponent, screen):
        from .functions import getPlayerKing, comparePieces

        king = getPlayerKing(self.player)

        for move in self.normalMoves + self.captureMoves:

            mockPiece = Piece(name=self.name, startingPosition=move.destinationSquare.topLeftPosition,
                              deadPosition=self.deadPosition,
                              color=self.color, board=None)
            destinationSquareCurrentPiece = move.destinationSquare.currentPiece

            if destinationSquareCurrentPiece is not None:
                destinationSquareCurrentPiece.mockDead = True  # we mock kill this piece, so that its capture moves won't be relevant

            move.destinationSquare.currentPiece = mockPiece

            kingInDanger = False
            for piece in opponent.pieces:

                piece.update(screen=screen, opponent=self.player)
                for captureMove in piece.captureMoves:

                    if comparePieces(captureMove.pieceToCapture, king):
                        kingInDanger = True

                        break

            if kingInDanger is False:
                self.blockAttackMoves.append(move)

            move.destinationSquare.currentPiece = destinationSquareCurrentPiece
            if move.destinationSquare.currentPiece is not None:
                move.destinationSquare.currentPiece.mockDead = False

            for piece in opponent.pieces:
                piece.update(screen=screen, opponent=self.player)

            # after mocking the kill and place, we need to make everything back as it was


class Pawn(Piece):
    def __init__(self, name, startingPosition, deadPosition, color, board):
        super().__init__(name, startingPosition, deadPosition, color, board)
        self.movesTypes = [self.getPawnMoves, self.getPawnCaptureMoves]
        self.is_initial = True

    def getPawnMoves(self, opponent, screen):
        from .chessObjects import Square
        from .movements_positions import Move, Position

        if self.color == 'white':
            if self.Position.chessY - 1 >= 1 and Square.getSquare(self.Position.chessX,
                                                                  self.Position.chessY - 1).currentPiece is None:
                move = Move(movement=(self.moveVertically, (-1,)),
                            destinationSquare=Square.getSquare(X=self.Position.chessX, Y=self.Position.chessY - 1,
                                                               ), name='top')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            if self.is_initial:  # since the pawn is initial, we don't have to check for the board limits
                if Square.getSquare(self.Position.chessX, self.Position.chessY - 2).currentPiece is None:
                    move = Move(movement=(self.moveVertically, (-2,)),
                                destinationSquare=Square.getSquare(X=self.Position.chessX, Y=self.Position.chessY - 2,
                                                                   ), name='top')
                    if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                        self.normalMoves.append(move)
        elif self.color == 'black':
            if self.Position.chessY + 1 <= 8 and Square.getSquare(self.Position.chessX,
                                                                  self.Position.chessY + 1).currentPiece is None:
                move = Move(movement=(self.moveVertically, (+1,)),
                            destinationSquare=Square.getSquare(X=self.Position.chessX, Y=self.Position.chessY + 1,
                                                               ), name='bottom')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)

            if self.is_initial:  # since the pawn is initial, we don't have to check for the board limits
                if Square.getSquare(self.Position.chessX, self.Position.chessY + 2).currentPiece is None:
                    move = Move(movement=(self.moveVertically, (+2,)),
                                destinationSquare=Square.getSquare(X=self.Position.chessX, Y=self.Position.chessY + 2,
                                                                   ), name='bottom')
                    if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                        self.normalMoves.append(move)

    def getPawnCaptureMoves(self, opponent, screen):
        from .chessObjects import Square
        from .movements_positions import CaptureMove
        if self.color == 'white':
            # right top move
            if self.Position.chessY - 1 >= 1 and self.Position.chessX + 1 <= 8:
                destinationSquare = Square.getSquare(self.Position.chessX + 1, self.Position.chessY - 1)

                if destinationSquare.currentPiece is not None:
                    if destinationSquare.currentPiece.color == 'black':
                        captureMove = CaptureMove(movement=(self.moveDiagonally, (1, -1)),
                                                  destinationSquare=destinationSquare,
                                                  pieceToCapture=destinationSquare.currentPiece, name='rightTop')
                        if captureMove.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                            self.captureMoves.append(captureMove)
            # left top move
            if self.Position.chessY - 1 >= 1 and self.Position.chessX - 1 >= 1:
                destinationSquare = Square.getSquare(self.Position.chessX - 1, self.Position.chessY - 1)
                if destinationSquare.currentPiece is not None:
                    if destinationSquare.currentPiece.color == 'black':
                        captureMove = CaptureMove(movement=(self.moveDiagonally, (-1, -1)),
                                                  destinationSquare=destinationSquare,
                                                  pieceToCapture=destinationSquare.currentPiece, name='leftTop')
                        if captureMove.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                            self.captureMoves.append(captureMove)
        elif self.color == 'black':
            # right bottom move
            if self.Position.chessY + 1 <= 8 and self.Position.chessX + 1 <= 8:
                destinationSquare = Square.getSquare(self.Position.chessX + 1, self.Position.chessY + 1)
                if destinationSquare.currentPiece is not None:
                    if destinationSquare.currentPiece.color == 'white':
                        captureMove = CaptureMove(movement=(self.moveDiagonally, (1, 1)),
                                                  destinationSquare=destinationSquare,
                                                  pieceToCapture=destinationSquare.currentPiece, name='rightBottom')
                        if captureMove.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                            self.captureMoves.append(captureMove)
            # left bottom move
            if self.Position.chessY + 1 <= 8 and self.Position.chessX - 1 >= 1:
                destinationSquare = Square.getSquare(self.Position.chessX - 1, self.Position.chessY + 1)
                if destinationSquare.currentPiece is not None:
                    if destinationSquare.currentPiece.color == 'white':
                        captureMove = CaptureMove(movement=(self.moveDiagonally, (-1, 1)),
                                                  destinationSquare=destinationSquare,
                                                  pieceToCapture=destinationSquare.currentPiece, name='leftBottom')

                        if captureMove.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                            self.captureMoves.append(captureMove)

    def update(self, screen, opponent):
        from .functions import getPlayerKing
        # print(self, len(self.normalMoves) + len(self.captureMoves))
        if self.alive:
            self.normalMoves = []
            self.captureMoves = []
            self.blockAttackMoves = []
            self.blockedCaptureMoves = []

            if not self.mockDead:
                self.rect = pygame.Rect(self.Position.get_x(), self.Position.get_y(), self.width, self.height)
                self.getPawnMoves(opponent=opponent, screen=screen)
                self.getPawnCaptureMoves(opponent=opponent, screen=screen)

                if getPlayerKing(self.player).inDanger:
                    self.getBlockAttackMoves(opponent, screen)

        else:
            self.normalMoves = []
            self.captureMoves = []
            self.blockAttackMoves = []
            self.blockedCaptureMoves = []
            self.rect = pygame.Rect(self.deadPosition.get_x(), self.deadPosition.get_y(), self.width, self.height)

        screen.blit(self.image, self.rect)


class King(Piece):
    def __init__(self, name, startingPosition, deadPosition, color, board):
        super().__init__(name, startingPosition, deadPosition, color, board)

        self.movesTypes = [self.getKingMoves]
        self.inDanger = False
        self.board = board
        self.escapeMoves = []

    @staticmethod
    def checkIfSafeMove(move, opponent):
        from .chessObjects import Square
        from .functions import compareSquares
        for piece in opponent.pieces:
            if piece.name[:-1] != 'pawn':
                for normalMove in piece.normalMoves:
                    if compareSquares(normalMove.destinationSquare, move.destinationSquare):
                        return False
            else:

                if piece.color == 'white':
                    pawnCaptureMoveDestinationSquare1 = Square.getSquare(piece.Position.chessX + 1,
                                                                         piece.Position.chessY - 1)
                    pawnCaptureMoveDestinationSquare2 = Square.getSquare(piece.Position.chessX - 1,
                                                                         piece.Position.chessY - 1)
                    try:
                        if compareSquares(move.destinationSquare,
                                          pawnCaptureMoveDestinationSquare1) or compareSquares(
                            move.destinationSquare, pawnCaptureMoveDestinationSquare2):
                            return False
                    except AttributeError:  # to handle the case where the destination square was not found, if the pawn is on the board limits
                        pass
                else:
                    pawnCaptureMoveDestinationSquare1 = Square.getSquare(piece.Position.chessX + 1,
                                                                         piece.Position.chessY + 1)
                    pawnCaptureMoveDestinationSquare2 = Square.getSquare(piece.Position.chessX - 1,
                                                                         piece.Position.chessY + 1)
                    try:
                        if compareSquares(move.destinationSquare,
                                          pawnCaptureMoveDestinationSquare1) or compareSquares(
                            move.destinationSquare, pawnCaptureMoveDestinationSquare2):
                            return False
                    except AttributeError:
                        pass

        return True

    def handleOneUnitDiagonalMove(self, directionX, directionY, opponent, screen, getCapture=True):
        from .chessObjects import Square
        from .movements_positions import Move
        directions = {'right': 1, 'left': -1, 'top': -1, 'bottom': 1}
        movement = (self.moveDiagonally, (directions[directionX], directions[directionY]))
        if 1 <= self.Position.chessX + directions[directionX] <= 8 and 1 <= self.Position.chessY + directions[
            directionY] <= 8:

            destinationSquare = Square.getSquare(self.Position.chessX + directions[directionX],
                                                 self.Position.chessY + directions[directionY])
            if destinationSquare.currentPiece is not None:
                if getCapture:
                    destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                          screen=screen, name=f'{directionX},{directionY}')
            else:
                move = Move(destinationSquare=destinationSquare, movement=movement, name=f'{directionX},{directionY}')
                if King.checkIfSafeMove(move=move, opponent=opponent):
                    self.normalMoves.append(move)

    def handleOneUnitVerticalMove(self, directionY, opponent, screen, getCapture=True):
        from .chessObjects import Square
        from .movements_positions import Move
        directions = {'top': -1, 'bottom': 1}
        movement = (self.moveVertically, (directions[directionY],))
        if 1 <= self.Position.chessY + directions[directionY] <= 8:
            destinationSquare = Square.getSquare(self.Position.chessX, self.Position.chessY + directions[directionY])
            if destinationSquare.currentPiece is not None:
                if getCapture:
                    destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                          screen=screen, name=f'f{directionY},')
            else:
                move = Move(destinationSquare=destinationSquare, movement=movement, name=f'f{directionY},')
                if King.checkIfSafeMove(move=move, opponent=opponent):
                    self.normalMoves.append(move)

    def handleOneUnitHorizontalMove(self, directionX, opponent, screen, getCapture=True):
        from .chessObjects import Square
        from .movements_positions import Move
        directions = {'right': 1, 'left': -1}
        movement = (self.moveHorizontally, (directions[directionX],))
        if 1 <= self.Position.chessX + directions[directionX] <= 8:
            destinationSquare = Square.getSquare(self.Position.chessX + directions[directionX], self.Position.chessY)
            if destinationSquare.currentPiece is not None:
                if getCapture:
                    destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                          screen=screen, name=f'{directionX},')
            else:
                move = Move(destinationSquare=destinationSquare, movement=movement, name=f'{directionX},')
                if King.checkIfSafeMove(move=move, opponent=opponent):
                    self.normalMoves.append(move)

    def getKingMoves(self, opponent, screen):

        # diagonal moves
        self.handleOneUnitDiagonalMove('right', 'top', opponent, screen)
        self.handleOneUnitDiagonalMove('left', 'top', opponent, screen)
        self.handleOneUnitDiagonalMove('right', 'bottom', opponent, screen)
        self.handleOneUnitDiagonalMove('left', 'bottom', opponent, screen)

        # vertical moves
        self.handleOneUnitVerticalMove('top', opponent, screen)
        self.handleOneUnitVerticalMove('bottom', opponent, screen)

        # horizontal moves
        self.handleOneUnitHorizontalMove('right', opponent, screen)
        self.handleOneUnitHorizontalMove('left', opponent, screen)

    def getKingEscapeMoves(self, opponent, screen):

        from .functions import comparePieces
        for move in self.normalMoves + self.captureMoves:
            mockKing = King(name='king', startingPosition=move.destinationSquare.topLeftPosition,
                            deadPosition=self.deadPosition, color=self.color, board=self.board)
            destinationSquareCurrentPiece = move.destinationSquare.currentPiece
            move.destinationSquare.currentPiece = mockKing
            # we need to find all the capture moves of the opponent pieces if the king is in this square (if the king makes this move)
            if destinationSquareCurrentPiece is not None:
                destinationSquareCurrentPiece.mockDead = True
            moveIsSecure = True
            for piece in opponent.pieces:
                piece.update(screen=screen, opponent=self.player,
                             )  # to get the new capture and normal moves
                for captureMove in piece.captureMoves:

                    if comparePieces(piece1=captureMove.pieceToCapture, piece2=mockKing):
                        moveIsSecure = False
                        break
            if moveIsSecure:
                self.escapeMoves.append(move)

            move.destinationSquare.currentPiece = destinationSquareCurrentPiece
            if move.destinationSquare.currentPiece is not None:
                move.destinationSquare.currentPiece.mockDead = False
            for piece in opponent.pieces:
                piece.update(screen=screen, opponent=self.player)

    def displayPossibleMoves(self, squares, reverse=False):
        from .functions import compareSquares
        if self.inDanger:
            for move in self.escapeMoves:
                for square in squares:
                    if compareSquares(square, move.destinationSquare):
                        if not reverse:
                            square.showEscapeEffect = True
                        else:
                            square.showEscapeEffect = False
        else:
            for move in self.normalMoves:
                for square in squares:
                    if compareSquares(square, move.destinationSquare):
                        if not reverse:
                            square.showMoveEffect = True
                        else:
                            square.showMoveEffect = False
                        break
            for move in self.captureMoves:
                for square in squares:
                    if compareSquares(square, move.destinationSquare):
                        if not reverse:
                            square.showCaptureEffect = True
                        else:
                            square.showCaptureEffect = False

    def checkIfInDanger(self, opponent):
        from .functions import comparePieces
        for piece in opponent.pieces:
            for captureMove in piece.captureMoves:
                if comparePieces(piece1=captureMove.pieceToCapture, piece2=self):
                    self.inDanger = True

    def update(self, screen, opponent):

        # print(self, len(self.normalMoves) + len(self.captureMoves))
        if self.alive:
            self.normalMoves = []
            self.captureMoves = []
            self.escapeMoves = []
            self.blockedCaptureMoves = []
            self.inDanger = False
            self.rect = pygame.Rect(self.Position.get_x(), self.Position.get_y(), self.width, self.height)
            self.getKingMoves(opponent=opponent, screen=screen)

            self.checkIfInDanger(opponent=opponent)

            if self.inDanger:
                imageFileName = f'game/assets/{self.name}--{self.color}--red.png'
                self.getKingEscapeMoves(opponent=opponent, screen=screen)
            else:
                imageFileName = f'game/assets/{self.name}--{self.color}.png'
            self.image = pygame.transform.scale(pygame.image.load(imageFileName), (self.width, self.height))

        else:
            self.rect = pygame.Rect(self.deadPosition.get_x(), self.deadPosition.get_y(), self.width, self.height)

        screen.blit(self.image, self.rect)


class Queen(Piece):
    def __init__(self, name, startingPosition, deadPosition, color, board):
        super().__init__(name, startingPosition, deadPosition, color, board)
        from .movements_positions import Move
        self.movesTypes = [Move.getVerticalMoves, Move.getDiagonalMoves, Move.getHorizontalMoves]


class Rook(Piece):
    def __init__(self, name, startingPosition, deadPosition, color, board):
        super().__init__(name, startingPosition, deadPosition, color, board)
        from .movements_positions import Move
        self.movesTypes = [Move.getVerticalMoves, Move.getHorizontalMoves]


class Knight(Piece):
    def __init__(self, name, startingPosition, deadPosition, color, board):
        super().__init__(name, startingPosition, deadPosition, color, board)
        self.movesTypes = [self.getKnightMove]

    def getKnightMove(self, opponent, screen):
        from .chessObjects import Square
        from .movements_positions import Move

        # Case 1: Y - 2, X + 1
        movement = (self.LMove, (1, -2))
        if self.Position.chessX + 1 <= 8 and self.Position.chessY - 2 >= 1:
            destinationSquare = Square.getSquare(self.Position.chessX + 1, self.Position.chessY - 2)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

        # Case 2: Y - 2, X - 1
        movement = (self.LMove, (-1, -2))
        if self.Position.chessX - 1 >= 1 and self.Position.chessY - 2 >= 1:
            destinationSquare = Square.getSquare(self.Position.chessX - 1, self.Position.chessY - 2)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

        # Case 3: Y - 1, X - 2
        movement = (self.LMove, (-2, -1))
        if self.Position.chessX - 2 >= 1 and self.Position.chessY - 1 >= 1:
            destinationSquare = Square.getSquare(self.Position.chessX - 2, self.Position.chessY - 1)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

        # Case 4: Y + 1, X - 2
        movement = (self.LMove, (-2, 1))
        if self.Position.chessX - 2 >= 1 and self.Position.chessY + 1 <= 8:
            destinationSquare = Square.getSquare(self.Position.chessX - 2, self.Position.chessY + 1)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

        # Case 5: Y + 2, X - 1
        movement = (self.LMove, (-1, 2))
        if self.Position.chessX - 1 >= 1 and self.Position.chessY + 2 <= 8:
            destinationSquare = Square.getSquare(self.Position.chessX - 1, self.Position.chessY + 2)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

        # Case 6: Y + 2, X + 1
        movement = (self.LMove, (1, 2))
        if self.Position.chessX + 1 <= 8 and self.Position.chessY + 2 <= 8:
            destinationSquare = Square.getSquare(self.Position.chessX + 1, self.Position.chessY + 2)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

        # Case 7: Y + 1, X + 2
        movement = (self.LMove, (2, 1))
        if self.Position.chessX + 2 <= 8 and self.Position.chessY + 1 <= 8:
            destinationSquare = Square.getSquare(self.Position.chessX + 2, self.Position.chessY + 1)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

        # Case 8: Y - 1, X + 2
        movement = (self.LMove, (2, -1))
        if self.Position.chessX + 2 <= 8 and self.Position.chessY - 1 >= 1:
            destinationSquare = Square.getSquare(self.Position.chessX + 2, self.Position.chessY - 1)
            if destinationSquare.currentPiece is None:
                move = Move(movement=movement, destinationSquare=destinationSquare, name='L')
                if move.checkIfNotDangerous(movingPiece=self, opponent=opponent):
                    self.normalMoves.append(move)
            else:
                destinationSquare.handleBlockingPiece(movingPiece=self, movement=movement, opponent=opponent,
                                                      screen=screen, name='L')

    def update(self, screen, opponent):
        # print(self, len(self.normalMoves) + len(self.captureMoves))
        from .functions import getPlayerKing
        if self.alive:
            self.normalMoves = []
            self.captureMoves = []
            self.blockAttackMoves = []
            if not self.mockDead:
                self.rect = pygame.Rect(self.Position.get_x(), self.Position.get_y(), self.width, self.height)
                self.getKnightMove(opponent=opponent, screen=screen)
                if getPlayerKing(self.player).inDanger:
                    self.getBlockAttackMoves(opponent, screen)

        else:
            self.normalMoves = []
            self.captureMoves = []
            self.blockAttackMoves = []
            self.rect = pygame.Rect(self.deadPosition.get_x(), self.deadPosition.get_y(), self.width, self.height)

        screen.blit(self.image, self.rect)

    def LMove(self, valueX, valueY):
        self.Position.chessX += valueX
        self.Position.chessY += valueY


class Bishop(Piece):
    def __init__(self, name, startingPosition, deadPosition, color, board):
        super().__init__(name, startingPosition, deadPosition, color, board)
        from .movements_positions import Move
        self.movesTypes = [Move.getDiagonalMoves]
