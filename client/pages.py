import threading
import time

import pygame
import requests

pygame.init()

StartOnlineGameEvent = pygame.USEREVENT + 1


class Page:
    """
    This is the parent class, from which all the app pages will inherit, some pages that require authentication will need a user attribute,
     like game page and home, other won't require this argument,
      because they are pre authentication pages
    """
    pages = []
    FPS = 60

    @staticmethod
    def get(name, currentPage, *args):
        PagesNames = {'auth': AuthPage, 'logIn': LogInPage, 'signUp': SignUpPage, 'home': HomePage, 'game': GamePage,
                      'addFriend': AddFriendPage, 'friendRequests': FriendRequestsPage, 'friends': FriendsPage,
                      'invitations': InvitationsPage, "onlineGame": OnlineGamePage}

        currentPage.running = False
        page = PagesNames[name](currentPage.screen, *args)
        current_thread = threading.current_thread()
        print(f"My function is running in thread: {current_thread.name}")
        page.run()

    def __init__(self, screen):
        self.screen = screen
        self.running = False
        self.activeEntry = None
        self.responding = False
        Page.pages.append(self)

    def update(self, *args):
        self.screen.fill((250, 250, 250))
        for element in args:
            element.draw(self.screen)

        pygame.display.flip()

    def run(self):
        pass


class AuthPage(Page):

    def run(self):
        from widgets import Button
        clock = pygame.time.Clock()

        logInButton = Button(x=self.screen.get_width() / 2 - 100, y=300, width=200, height=70, text='Log in',
                             color=(250, 250, 250), backGroundColor=(0, 0, 0), func=Page.get)
        singUpButton = Button(x=self.screen.get_width() / 2 - 100, y=375, width=200, height=70, text='Sign Up',
                              color=(250, 250, 250), backGroundColor=(0, 0, 0), func=Page.get)
        self.running = True
        while self.running:
            clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    logInButton.handle_event(event, 'logIn', self)
                    singUpButton.handle_event(event, 'signUp', self)
            self.update(logInButton, singUpButton)


class LogInPage(Page):
    def __init__(self, screen):
        from widgets import Label, Entry, Button
        from response import sendRequest, authenticationResponse
        super().__init__(screen)

        self.responseLabel = Label(text='', x=(self.screen.get_width() / 8) * 2, y=(self.screen.get_height() / 4) * 3,
                                   width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))

        self.running = True
        self.func = sendRequest(authenticationResponse(self, self.responseLabel, 'logIn'))
        self.func.send(None)

        self.userNameLabel = Label(text='userName:', x=(self.screen.get_width() / 8) * 2,
                                   y=(self.screen.get_height() / 4),
                                   width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        self.userNameEntry = Entry(x=self.userNameLabel.rect.x + self.userNameLabel.rect.width + 10,
                                   y=self.userNameLabel.rect.y,
                                   width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        self.passwordLabel = Label(text='password:', x=(self.screen.get_width() / 8) * 2,
                                   y=(self.screen.get_height() / 4) + 60,
                                   width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        self.passwordEntry = Entry(x=self.userNameLabel.rect.x + self.userNameLabel.rect.width + 10,
                                   y=self.passwordLabel.rect.y,
                                   width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        self.submitButton = Button(x=self.screen.get_width() - 100, y=(self.screen.get_height() / 8) * 7, width=80,
                                   height=50, text='submit', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                   func=self.func.send)

        self.backButton = Button(x=0, y=50, width=100,
                                 height=50, text='Back', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                 func=Page.get)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.running = False
                    break
                else:
                    try:
                        self.userNameEntry.handle_event(event, self)
                        self.passwordEntry.handle_event(event, self)
                        self.submitButton.handle_event(event,
                                                       {'userName': self.userNameEntry.text,
                                                        'password': self.passwordEntry.text}
                                                       )  # solved???
                        self.backButton.handle_event(event, 'auth', self)
                    except StopIteration:
                        pass
            if not self.responding:
                self.update(self.userNameLabel, self.passwordLabel, self.userNameEntry, self.passwordEntry,
                            self.submitButton, self.backButton)
            else:
                self.update(self.userNameLabel, self.passwordLabel, self.userNameEntry, self.passwordEntry,
                            self.submitButton, self.backButton, self.responseLabel)


class SignUpPage(Page):
    def run(self):
        from response import authenticationResponse, sendRequest
        from widgets import Label, Entry, Button
        clock = pygame.time.Clock()
        responseLabel = Label(text='', x=(self.screen.get_width() / 8) * 2, y=(self.screen.get_height() / 4) * 3,
                              width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))

        self.running = True
        func = sendRequest(authenticationResponse(self, responseLabel, 'signUp'))
        func.send(None)

        userNameLabel = Label(text='userName:', x=(self.screen.get_width() / 8) * 2, y=(self.screen.get_height() / 4),
                              width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        userNameEntry = Entry(x=userNameLabel.rect.x + userNameLabel.rect.width + 10, y=userNameLabel.rect.y,
                              width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))

        emailLabel = Label(text='Email:', x=(self.screen.get_width() / 8) * 2, y=(self.screen.get_height() / 4) + 60,
                           width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        emailEntry = Entry(x=userNameLabel.rect.x + userNameLabel.rect.width + 10, y=emailLabel.rect.y,
                           width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))

        passwordLabel = Label(text='password:', x=(self.screen.get_width() / 8) * 2,
                              y=(self.screen.get_height() / 4) + 130,
                              width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        passwordEntry = Entry(x=userNameLabel.rect.x + userNameLabel.rect.width + 10, y=passwordLabel.rect.y,
                              width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))

        submitButton = Button(x=self.screen.get_width() - 100, y=(self.screen.get_height() / 8) * 7, width=80,
                              height=50,
                              text='submit', color=(250, 250, 250), backGroundColor=(0, 0, 0), func=func.send)
        backButton = Button(x=0, y=50, width=100,
                            height=50, text='Back', color=(250, 250, 250), backGroundColor=(0, 0, 0), func=Page.get)

        while self.running:
            clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.running = False

                else:
                    userNameEntry.handle_event(event, self)
                    passwordEntry.handle_event(event, self)
                    emailEntry.handle_event(event, self)
                    submitButton.handle_event(event,
                                              {'userName': userNameEntry.text, 'password': passwordEntry.text,
                                               'email': emailEntry.text})
                    backButton.handle_event(event, 'auth', self)
            if not self.responding:
                self.update(userNameLabel, passwordLabel, userNameEntry, passwordEntry, submitButton, emailLabel,
                            emailEntry, backButton)
            else:
                self.update(userNameLabel, passwordLabel, userNameEntry, passwordEntry, submitButton, emailLabel,
                            emailEntry, backButton, responseLabel)


class HomePage(Page):
    def __init__(self, screen, user):
        super().__init__(screen)
        self.user = user
        self.user.currentPage = self

    def run(self):
        from appServicesClasses import Friend
        from widgets import Button

        offlineGameButton = Button(x=self.screen.get_width() / 2 - 150, y=self.screen.get_height() / 2, width=300,
                                   height=70, text='Offline Game', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                   func=Page.get)
        onlineRandomGameButton = Button(x=self.screen.get_width() / 2 - 150, y=self.screen.get_height() / 2 + 80,
                                        width=300, height=70, text='Online Random Game', color=(250, 250, 250),
                                        backGroundColor=(0, 0, 0), func=print)
        addFriendButton = Button(x=self.screen.get_width() - 310, y=80, width=300,
                                 height=70, text='Add friend', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                 func=Page.get)
        friendRequestsButton = Button(x=self.screen.get_width() - 310, y=160, width=300,
                                      height=70, text='Friend Requests', color=(250, 250, 250),
                                      backGroundColor=(0, 0, 0),
                                      func=Page.get)
        friendsButton = Button(x=10, y=10, width=300, height=70, text='Friends', color=(250, 250, 250),
                               backGroundColor=(0, 0, 0), func=Page.get)
        invitationsButton = Button(x=10, y=90, width=300, height=70, text='Invitations', color=(250, 250, 250),
                                   backGroundColor=(0, 0, 0), func=Page.get)
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.user.logOut()
                elif event.type == StartOnlineGameEvent:
                    gameId = self.user.startGameMessageContent.split(':')[1]
                    opponent = Friend.get(user=self.user,
                                          friendUserName=self.user.startGameMessageContent.split(':')[2])
                    playerColor = self.user.startGameMessageContent.split(':')[3]

                    Page.get('onlineGame', self, self.user, opponent, playerColor, gameId)
                else:
                    offlineGameButton.handle_event(event, 'game', self, self.user)
                    addFriendButton.handle_event(event, 'addFriend', self, self.user)
                    friendRequestsButton.handle_event(event, 'friendRequests', self, self.user)
                    friendsButton.handle_event(event, 'friends', self, self.user)
                    invitationsButton.handle_event(event, 'invitations', self, self.user)

            self.update(offlineGameButton, onlineRandomGameButton, addFriendButton, friendsButton, friendRequestsButton,
                        invitationsButton)


class GamePage(Page):
    def __init__(self, screen, user):
        from game.players import Player
        from game.functions import get_squares
        super().__init__(screen)
        self.BOARD = pygame.transform.scale(pygame.image.load('game/assets/chessBoard2.png'),
                                            (self.screen.get_width() * ((
                                                                                self.screen.get_width() * 0.58333333333333333333333333333333) / 1200),
                                             self.screen.get_height()))
        self.user = user
        self.user.currentPage = self
        self.selectedPiece = None
        self.whitePlayer = Player(color='white', board=self.BOARD, screen=screen)
        self.blackPlayer = Player(color='black', board=self.BOARD, screen=screen)
        self.gameId = None
        self.squares = get_squares(board=self.BOARD, screen=screen)
        self.activePlayer = self.whitePlayer

    def update(self, *elements):
        self.screen.fill((250, 250, 250))
        self.screen.blit(self.BOARD, (300, 0))

        for square in self.squares:
            square.update(pieces=self.whitePlayer.pieces + self.blackPlayer.pieces, screen=self.screen)

        for piece in self.whitePlayer.pieces:
            piece.update(screen=self.screen, opponent=self.blackPlayer)

        for piece in self.blackPlayer.pieces:
            piece.update(screen=self.screen, opponent=self.whitePlayer)

        for square in self.squares:
            square.update(pieces=self.whitePlayer.pieces + self.blackPlayer.pieces, screen=self.screen)

        for element in elements:
            element.draw(self.screen)

        pygame.display.flip()

    def changeActivePlayer(self):

        if "white" == self.activePlayer.color:
            self.activePlayer = self.blackPlayer
            return
        self.activePlayer = self.whitePlayer

    def handleGameEvent(self, event, online=False):
        from game.functions import comparePieces, compareSquares, getOpponent
        from game.pieces import Pawn
        from game.movements_positions import CaptureMove

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # this code is for selecting a piece and displaying its moves
                for piece in self.activePlayer.pieces:
                    if piece.rect.collidepoint(event.pos):
                        if self.selectedPiece is None:
                            self.selectedPiece = piece

                            self.selectedPiece.displayPossibleMoves(squares=self.squares)

                        else:
                            if comparePieces(self.selectedPiece,
                                             piece):  # if the selected piece is the same piece that we are selecting , we need to deselect it
                                piece.displayPossibleMoves(squares=self.squares, reverse=True)
                                self.selectedPiece = None

                            else:
                                # if we are selected another pieces, we need to deselect the selected piece and select the new one
                                self.selectedPiece.displayPossibleMoves(squares=self.squares, reverse=True)
                                piece.displayPossibleMoves(squares=self.squares)

                                self.selectedPiece = piece
                # this code is for making a move
                if self.selectedPiece is not None:

                    for square in self.squares:
                        if square.showMoveEffect or square.showCaptureEffect or square.showEscapeEffect or square.showBlockEffect:
                            if square.rect.collidepoint(event.pos):
                                for move in self.selectedPiece.normalMoves + self.selectedPiece.captureMoves:
                                    if compareSquares(square1=square, square2=move.destinationSquare):
                                        if self.selectedPiece.name[:-1] == "pawn":
                                            self.selectedPiece.is_initial = False  # we moved the pawn, so it's not initial anymore
                                        if move.__class__ == CaptureMove:
                                            move.make_capture()
                                            if online:  # if the game is online, we after making the move by the active player, he sends a message to the other player to inform him of his move
                                                opponent = getOpponent(self)
                                                self.activePlayer.user.sendMoveMessage(movingPiece=self.selectedPiece,
                                                                                       move=move,
                                                                                       opponent=opponent.user,
                                                                                       gameId=self.gameId,
                                                                                       capturedPiece=move.pieceToCapture)

                                        else:
                                            move.make_move()
                                            if online:
                                                opponent = getOpponent(self)
                                                self.activePlayer.user.sendMoveMessage(movingPiece=self.selectedPiece,
                                                                                       move=move,
                                                                                       opponent=opponent.user,
                                                                                       gameId=self.gameId)
                                        self.selectedPiece.displayPossibleMoves(squares=self.squares, reverse=True)
                                        self.selectedPiece = None
                                        self.changeActivePlayer()
                                        break

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.user.logOut()
                else:
                    self.handleGameEvent(event=event)

            self.update()


class OnlineGamePage(GamePage):
    def __init__(self, screen, user, opponent, userColor, gameId):
        super().__init__(screen, user)
        from widgets import Entry, Button
        from game.players import OnlinePlayer

        if userColor == 'white':
            whiteUser = self.user
            blackUser = opponent

        else:
            whiteUser = opponent
            blackUser = self.user

        self.gameId = gameId
        self.whitePlayer = OnlinePlayer(color='white', board=self.BOARD, screen=self.screen, user=whiteUser)
        self.blackPlayer = OnlinePlayer(color='black', board=self.BOARD, screen=self.screen, user=blackUser)
        self.activePlayer = self.whitePlayer

        if userColor == "white":
            self.onsitePlayer = self.whitePlayer
            self.offsitePlayer = self.blackPlayer

        else:
            self.onsitePlayer = self.blackPlayer
            self.offsitePlayer = self.whitePlayer

        self.chatMessages = []
        self.chatMessagesLabels = []
        self.chatBlock = pygame.Rect(0, 0, 200, self.screen.get_height())
        self.chatMessageEntry = Entry(x=120, y=0, width=80, height=20, backGroundColor=(0, 0, 0), color=(250, 250, 250))
        self.sendMessageButton = Button(x=120, y=25, text='Send', func=self.user.sendChatMessage, width=50, height=25,
                                        backGroundColor=(0, 0, 0), color=(250, 250, 250))

    def getChatMessagesLabels(self):
        """
        Since 800 is the height of the screen, and each message has a height of 25, so 800/25 = 32. by removing two essential elements, the button and the entry, we are left
        with 30 space, so the logical thing is to display the last thirty messages.
        :return:
        """
        from widgets import Label
        self.chatMessagesLabels = []
        y = 0
        if len(self.chatMessages) < 30:
            lim = 0
        else:
            lim = len(self.chatMessages) - 30
        for message in self.chatMessages[lim:]:
            if message.senderUserName == self.onsitePlayer.user.username:
                x = 120
            else:
                x = 0
            messageLabel = Label(text=message.content, x=x, y=y, width=80, height=20, backGroundColor=(0, 0, 0),
                                 color=(250, 250, 250))
            y += 25
            self.chatMessagesLabels.append(messageLabel)
        self.chatMessageEntry.rect.y = y
        self.sendMessageButton.rect.y = y + 25

    def run(self):

        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.getChatMessagesLabels()
            page_elements = self.chatMessagesLabels + [self.chatMessageEntry, self.sendMessageButton]

            clock.tick(Page.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.user.logOut()
                else:
                    if self.activePlayer.color == self.onsitePlayer.color:
                        self.handleGameEvent(event, online=True)
                self.chatMessageEntry.handle_event(event, self)
                self.sendMessageButton.handle_event(event, self.offsitePlayer.user.userName, self.chatMessageEntry.text, self.gameId)
            if self.activePlayer.color != self.onsitePlayer.color:

                if self.onsitePlayer.user.opponentMoveMessage is not None:
                    self.onsitePlayer.user.opponentMoveMessage.execute(userPlayer=self.onsitePlayer,
                                                                       opponentPlayer=self.activePlayer)
                    self.changeActivePlayer()
                    self.onsitePlayer.user.opponentMoveMessage = None
            self.update(*page_elements)
            # pygame.draw.rect(self.screen, (250, 250, 250), self.chatBlock)


class AddFriendPage(Page):
    def __init__(self, screen, user):
        from widgets import Label, Button, Entry
        from response import sendRequest
        super().__init__(screen)
        self.user = user
        self.user.currentPage = self
        self.responseLabel = Label(text='', x=(self.screen.get_width() / 2) - 125, y=(self.screen.get_height() / 4) * 3,
                                   width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        self.running = True
        self.func = sendRequest(
            self.user.friendRequestResponse(page=self, responseLabel=self.responseLabel, requestType='send'))
        self.func.send(None)

        self.friendNameLabel = Label(text='userName:', x=(self.screen.get_width() / 8) * 2,
                                     y=(self.screen.get_height() / 2) - 25,
                                     width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))
        self.friendNameEntry = Entry(x=self.friendNameLabel.rect.x + self.friendNameLabel.rect.width + 10,
                                     y=self.friendNameLabel.rect.y,
                                     width=250, height=50, color=(250, 250, 250), backGroundColor=(0, 0, 0))

        self.submitButton = Button(x=self.screen.get_width() - 100, y=(self.screen.get_height() / 8) * 7, width=80,
                                   height=50,
                                   text='submit', color=(250, 250, 250), backGroundColor=(0, 0, 0), func=self.func.send)
        self.backButton = Button(x=0, y=50, width=100,
                                 height=50, text='Back', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                 func=Page.get)

    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.user.logOut()
                elif event.type == StartOnlineGameEvent:
                    pass
                else:
                    self.friendNameEntry.handle_event(event, self)
                    self.submitButton.handle_event(event, self.friendNameEntry.text)
                    self.backButton.handle_event(event, 'home', self, self.user)
            if self.responding:
                self.update(self.responseLabel, self.friendNameEntry, self.friendNameLabel, self.submitButton,
                            self.backButton)
            else:
                self.update(self.friendNameEntry, self.friendNameLabel, self.submitButton, self.backButton)


class FriendRequestsPage(Page):
    def __init__(self, screen, user):
        from response import sendRequest
        from widgets import Button
        super().__init__(screen)
        self.user = user
        self.user.currentPage = self
        self.running = True
        self.func = sendRequest(self.user.acceptOrDeclineFriendRequest(self))
        self.func.send(None)
        self.requestsWidgets = []
        self.backButton = Button(x=0, y=50, width=100,
                                 height=50, text='Back', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                 func=Page.get)

    def getRequestsWidgets(self):
        from widgets import Label, Button
        self.requestsWidgets = []
        for i in range(1, len(self.user.friendRequests) + 1):
            y = (self.screen.get_height() / 8) * i
            x = (self.screen.get_width() / 3)
            # print(self.user.friendRequests[i - 1].senderUserName, self.user.friendRequests[i - 1].receiverUserName)
            requestLabel = Label(text=self.user.friendRequests[i - 1].senderUserName, x=x, y=y, width=300, height=70,
                                 color=(250, 250, 250), backGroundColor=(0, 0, 0))
            acceptButton = Button(text='Accept', x=requestLabel.rect.x + 310, y=y, width=100, height=70,
                                  color=(250, 250, 250), backGroundColor=(0, 0, 0), func=self.func.send)
            declineButton = Button(text='Decline', x=requestLabel.rect.x + 420, y=y, width=100, height=70,
                                   color=(250, 250, 250), backGroundColor=(0, 0, 0), func=self.func.send)
            self.requestsWidgets.append((requestLabel, acceptButton, declineButton))

    def run(self):
        from appServicesClasses import Friend
        clock = pygame.time.Clock()
        self.running = True
        self.user.currentPage = self
        while self.running:
            self.getRequestsWidgets()
            clock.tick(Page.FPS)
            pageElements = [element for widgets in self.requestsWidgets for element in widgets]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.user.logOut()
                elif event.type == StartOnlineGameEvent:
                    gameId = self.user.startGameMessageContent.split(':')[1]
                    opponent = Friend.get(user=self.user,
                                          friendUserName=self.user.startGameMessageContent.split(':')[2])
                    playerColor = self.user.startGameMessageContent.split(':')[3]

                    Page.get('onlineGame', self, self.user, opponent, playerColor, gameId)
                else:
                    self.backButton.handle_event(event, 'home', self, self.user)
                    for widgets in self.requestsWidgets:
                        label = widgets[0]
                        acceptButton = widgets[1]
                        declineButton = widgets[2]
                        acceptButton.handle_event(event, (label.text, 'accept'))
                        declineButton.handle_event(event, (label.text, 'decline'))

            self.update(self.backButton, *pageElements)


class FriendsPage(Page):
    def __init__(self, screen, user):
        from widgets import Button
        super().__init__(screen)
        self.user = user
        self.user.currentPage = self
        self.friendsWidgets = []
        self.backButton = Button(x=0, y=50, width=100,
                                 height=50, text='Back', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                 func=Page.get)

    def getFriendsWidgets(self):
        from widgets import Label, Button
        self.friendsWidgets = []
        x = 100
        y = 100
        for i in range(len(self.user.friends)):
            y += 75
            friendLabel = Label(text=self.user.friends[i].userName, x=x, y=y, width=300, height=70,
                                color=(250, 250, 250), backGroundColor=(0, 0, 0))
            onlineLabel = Label(text=self.user.friends[i].status, x=x + 310, y=y, width=300, height=70,
                                color=(250, 250, 250), backGroundColor=(0, 0, 0))
            inviteButton = Button(text="Invite", x=x + 310 + 310, y=y, width=100, height=70, backGroundColor=(0, 0, 0),
                                  color=(250, 250, 250), func=self.user.sendInvitation)
            self.friendsWidgets.append((friendLabel, onlineLabel, inviteButton))

    def run(self):
        from appServicesClasses import Friend
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(Page.FPS)
            self.getFriendsWidgets()
            page_elements = [element for widgets in self.friendsWidgets for element in widgets]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.user.logOut()
                elif event.type == StartOnlineGameEvent:
                    gameId = self.user.startGameMessageContent.split(':')[1]
                    opponent = Friend.get(user=self.user,
                                          friendUserName=self.user.startGameMessageContent.split(':')[2])
                    playerColor = self.user.startGameMessageContent.split(':')[3]

                    Page.get('onlineGame', self, self.user, opponent, playerColor, gameId)
                else:
                    for widgets in self.friendsWidgets:
                        inviteButton = widgets[2]
                        inviteButton.handle_event(event, widgets[0].text)

                    self.backButton.handle_event(event, 'home', self, self.user)
            self.update(self.backButton, *page_elements)


class InvitationsPage(Page):
    def __init__(self, screen, user):
        from widgets import Button
        super().__init__(screen)
        self.user = user
        self.user.currentPage = self
        self.invitationsWidgets = []
        self.backButton = Button(x=0, y=50, width=100,
                                 height=50, text='Back', color=(250, 250, 250), backGroundColor=(0, 0, 0),
                                 func=Page.get)

    def getInvitationsWidgets(self):
        from widgets import Label, Button
        self.invitationsWidgets = []
        x = self.screen.get_width() / 3
        y = 0
        for i in range(len(self.user.receivedInvitations)):
            y += 75
            invitationLabel = Label(text=self.user.receivedInvitations[i].senderFriend.userName, x=x, y=y, width=300,
                                    height=70,
                                    color=(250, 250, 250), backGroundColor=(0, 0, 0))
            acceptButton = Button(text="Accept", x=x + 310, y=y, width=100, height=70, backGroundColor=(0, 0, 0),
                                  color=(250, 250, 250), func=self.user.receivedInvitations[i].accept)
            rejectButton = Button(text="Reject", x=x + 310 + 110, y=y, width=100, height=70, backGroundColor=(0, 0, 0),
                                  color=(250, 250, 250), func=self.user.receivedInvitations[i].reject)
            self.invitationsWidgets.append((invitationLabel, acceptButton, rejectButton))

    def run(self):
        from appServicesClasses import Friend
        self.running = True
        clock = pygame.time.Clock()
        start = time.time()

        while self.running:
            clock.tick(Page.FPS)

            self.getInvitationsWidgets()

            page_elements = [element for widgets in self.invitationsWidgets for element in widgets]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.user.logOut()
                elif event.type == StartOnlineGameEvent:
                    gameId = self.user.startGameMessageContent.split(':')[1]
                    opponent = Friend.get(user=self.user,
                                          friendUserName=self.user.startGameMessageContent.split(':')[2])
                    playerColor = self.user.startGameMessageContent.split(':')[3]

                    Page.get('onlineGame', self, self.user, opponent, playerColor, gameId)
                else:
                    for widgets in self.invitationsWidgets:
                        acceptButton = widgets[1]
                        rejectButton = widgets[2]
                        acceptButton.handle_event(event)
                        rejectButton.handle_event(event)
                    self.backButton.handle_event(event, 'home', self, self.user)
            self.update(self.backButton, *page_elements)


if __name__ == "__main__":
    screen_ = pygame.display.set_mode((1200, 800))
    p = LogInPage(screen=screen_)

    p.passwordEntry.text = '123'
    p.run()
