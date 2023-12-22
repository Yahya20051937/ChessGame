class Player:
    blackPiecesPositions = {'king': (5, 1), 'queen': (4, 1), 'bishop1': (3, 1), 'bishop2': (6, 1),
                            'knight1': (2, 1), 'knight2': (7, 1), 'rook1': (1, 1), 'rook2': (8, 1), 'pawn': (1, 2)}

    whitePiecesPositions = {'king': (5, 8), 'queen': (4, 8), 'bishop1': (3, 8), 'bishop2': (6, 8), 'knight1': (2, 8),
                            'knight2': (7, 8), 'rook1': (1, 8), 'rook2': (8, 8), 'pawn': (1, 7)}

    blackPiecesDeadPositions = {'king': (9, 1), 'queen': (9, 2), 'bishop1': (9, 3), 'bishop2': (9, 4),
                                'knight1': (9, 5), 'knight2': (9, 6), 'rook1': (9, 7), 'rook2': (9, 8), 'pawn': (10, 1)}

    whitePiecesDeadPositions = {'king': (-1, 1), 'queen': (-1, 2), 'bishop1': (-1, 3), 'bishop2': (-1, 4),
                                'knight1': (-1, 5),
                                'knight2': (-1, 6), 'rook1': (-1, -7), 'rook2': (-1, 8), 'pawn': (0, 1)}

    @staticmethod
    def get_pieces(color, board, screen):
        from .pieces import King, Queen, Rook, Bishop, Pawn, Knight
        from .movements_positions import Position
        if color == 'black':
            PiecesPositions = Player.blackPiecesPositions
            DeadPiecesPositions = Player.blackPiecesDeadPositions
        else:
            PiecesPositions = Player.whitePiecesPositions
            DeadPiecesPositions = Player.blackPiecesDeadPositions

        king = King(name='king',
                    startingPosition=Position(chessX=PiecesPositions['king'][0], chessY=PiecesPositions['king'][1],
                                              board=board, screen=screen), board=board,
                    color=color,
                    deadPosition=Position(chessX=DeadPiecesPositions['king'][0], chessY=DeadPiecesPositions['king'][1],
                                          screen=screen, board=board))
        queen = Queen(name='queen',
                      startingPosition=Position(chessX=PiecesPositions['queen'][0], chessY=PiecesPositions['queen'][1],
                                                board=board, screen=screen), board=board,
                      color=color, deadPosition=Position(chessX=DeadPiecesPositions['queen'][0],
                                                         chessY=DeadPiecesPositions['queen'][1], screen=screen,
                                                         board=board))
        bishop1 = Bishop(name='bishop1', startingPosition=Position(chessX=PiecesPositions['bishop1'][0],
                                                                   chessY=PiecesPositions['bishop1'][1], board=board,
                                                                   screen=screen),
                         board=board,
                         color=color, deadPosition=Position(chessX=DeadPiecesPositions['bishop1'][0],
                                                            chessY=DeadPiecesPositions['bishop1'][1], screen=screen,
                                                            board=board))
        bishop2 = Bishop(name='bishop2', startingPosition=Position(chessX=PiecesPositions['bishop2'][0],
                                                                   chessY=PiecesPositions['bishop2'][1], board=board,
                                                                   screen=screen),
                         board=board,
                         color=color, deadPosition=Position(chessX=DeadPiecesPositions['bishop2'][0],
                                                            chessY=DeadPiecesPositions['bishop2'][1], screen=screen,
                                                            board=board))
        knight1 = Knight(name='knight1', startingPosition=Position(chessX=PiecesPositions['knight1'][0],
                                                                   chessY=PiecesPositions['knight1'][1], board=board,
                                                                   screen=screen),
                         board=board,
                         color=color, deadPosition=Position(chessX=DeadPiecesPositions['knight1'][0],
                                                            chessY=DeadPiecesPositions['knight1'][1], screen=screen,
                                                            board=board))
        knight2 = Knight(name='knight2', startingPosition=Position(chessX=PiecesPositions['knight2'][0],
                                                                   chessY=PiecesPositions['knight2'][1], board=board,
                                                                   screen=screen),
                         board=board,
                         color=color, deadPosition=Position(chessX=DeadPiecesPositions['knight2'][0],
                                                            chessY=DeadPiecesPositions['knight2'][1], screen=screen,
                                                            board=board))
        rook1 = Rook(name='rook1',
                     startingPosition=Position(chessX=PiecesPositions['rook1'][0], chessY=PiecesPositions['rook1'][1],
                                               board=board, screen=screen), board=board,
                     color=color,
                     deadPosition=Position(chessX=DeadPiecesPositions['rook1'][0],
                                           chessY=DeadPiecesPositions['rook1'][1],
                                           screen=screen, board=board))
        rook2 = Rook(name='rook2',
                     startingPosition=Position(chessX=PiecesPositions['rook2'][0], chessY=PiecesPositions['rook2'][1],
                                               board=board, screen=screen), board=board,
                     color=color,
                     deadPosition=Position(chessX=DeadPiecesPositions['rook2'][0],
                                           chessY=DeadPiecesPositions['rook2'][1],
                                           screen=screen, board=board))
        pieces = [king, queen, bishop1, bishop2, knight1, knight2, rook1, rook2]

        for i in range(8):
            pawn = Pawn(name=f'pawn{i + 1}',
                        startingPosition=Position(chessX=i + 1, chessY=PiecesPositions['pawn'][1], board=board,
                                                  screen=screen),
                        board=board,
                        color=color,
                        deadPosition=Position(chessX=DeadPiecesPositions['pawn'][0], chessY=i + 1, board=board,
                                              screen=screen))
            pieces.append(pawn)
        return pieces

    def __init__(self, color, board, screen):
        self.color = color
        self.pieces = self.get_pieces(self.color, board, screen)
        for piece in self.pieces:
            piece.player = self


class OnlinePlayer(Player):
    def __init__(self, color, board, screen, user):
        super().__init__(color, board, screen)
        self.user = user