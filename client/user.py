import json
import random
import threading
from types import coroutine
import requests
from threading import Thread
import socket
from response import sendRequest

PORT = 5050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)

ERRORS = {306: "UserName not found", 200: "Request sent", 307: "Request already exists",
          308: "The receiver is already a friend", 401: "Unauthorized Page", 500: "Server Error"}


class User:

    def __init__(self, username, id_, jwt):
        self.username = username
        self.id = id_
        self.jwt = jwt
        self.friendRequests = []
        self.friends = []
        self.getFriends()
        self.getFriendRequests()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(ADDR)
        self.connection.settimeout(1)
        self.currentPage = None
        self.currentGameId = None
        self.opponentMoveMessage = None
        self.receivedInvitations = []
        self.online = False
        self.startGameMessageContent = None

        self.connection.sendall(
            json.dumps(
                {"from": f"{self.username},{self.id}", "to": "SERVER", "type": "info", "content": "online",
                 "jwt": self.jwt.generate()}).encode())
        thread = Thread(target=self.getMessages, name='Message Thread')
        thread.start()

    @coroutine
    def friendRequestResponse(self, page, responseLabel, requestType):

        BASE_URL = f'http://127.0.0.1:5000/friendRequest/{requestType}'
        while page.running:
            friendUserName = yield
            response = requests.get(BASE_URL + f'/{friendUserName}', headers={"jwt": self.jwt.generate()
                                                                              })
            page.responding = True
            responseLabel.text = ERRORS[response.status_code]

    def getFriendRequests(self):
        from appServicesClasses import FriendRequest
        self.friendRequests = []
        BASE_URL = f'http://127.0.0.1:5000/friendRequest/get'
        response = requests.get(BASE_URL, headers={"jwt": self.jwt.generate()})
        if response.status_code != 401:
            friendRequestsSendersUserNames = response.json()['receivedRequests']
            for senderUsername in friendRequestsSendersUserNames.split('/')[:-1]:
                friendRequest = FriendRequest(senderUserName=senderUsername, receiverUserName=self.username)
                self.friendRequests.append(friendRequest)
        else:
            print("401")

    def getFriends(self):
        from appServicesClasses import Friend

        BASE_URL = f'http://127.0.0.1:5000/friends/get'
        response = requests.get(BASE_URL, headers={"jwt": self.jwt.generate()})
        if response.status_code != 401:
            friendsUserNames = response.json()['friends'].split('/')[:-1]
            friendsStatus = response.json()['status'].split('/')[:-1]
            for _ in range(len(friendsUserNames)):
                friend = Friend(userName=friendsUserNames[_], status=friendsStatus[_])
                self.friends.append(friend)
        else:
            print("401")

    @coroutine
    def acceptOrDeclineFriendRequest(self, page):
        """
        The generator receives the friend request sender username, and with accept or reject request type,
        then after sending the request to the server, then if the request was a success, we delete the friend request,
        and then we update the request widgets attribute in the page object
        :param page:
        :return:
        """
        BASE_URL = f'http://127.0.0.1:5000/friendRequest'
        while page.running:
            senderUserName, requestType = yield
            receiverUserName = self.username
            response = requests.get(BASE_URL + f'/{requestType}/{receiverUserName}',
                                    headers={"jwt": self.jwt.generate()})
            if response.status_code != 401:
                self.getFriends()
                self.getFriendRequests()
            else:
                print("401")

    def getMessages(self):
        from communication import Message, GameMessage, ChatMessage
        while self.online:
            try:
                socketMessage = self.connection.recv(5000).decode()

                message = Message(user=self, socketMessage=socketMessage)
                print(f"Message received : {message.socketMessage}")
                if message.type == 'gameMove':
                    gameMessage = GameMessage(user=self, socketMessage=socketMessage)
                    if int(gameMessage.gameId) == int(
                            self.currentGameId):  # we only add the game message if it has the same id of the game that user is playing
                        self.opponentMoveMessage = gameMessage
                elif message.type == 'chatMessage':
                    # if the message type is a chat message, and if the user current game id and the chat message game id are equal, then the user current page is an online game page so, we can append this message to the chatMessages attribute to be displayed
                    chatMessage = ChatMessage(user=self, socketMessage=socketMessage)
                    if int(self.currentGameId) == int(chatMessage.gameId):
                        self.currentPage.chatMessages.append(chatMessage)

                else:
                    message.parse()
            except socket.timeout:
                continue

    def logOut(self):
        from communication import Message
        """
        The user here sends a request to the server to log him out in the database, and also sends a message to every friend in the game server to inform him that is changed his status
        :return: 
        """
        BASE_URL = f'http://127.0.0.1:5000/authenticate/logOut/{self.username}'

        response = requests.get(BASE_URL, headers={"jwt": self.jwt.generate()})
        if response.status_code != 401:
            self.online = False
            message = Message(
                socketMessage=json.dumps(
                    {"from": f"{self.username},{self.id}", "to": "SERVER", "type": "info", "content": "offline",
                     "jwt": self.jwt.generate()}),
                user=self)
            message.send()

    def inviteFriend(self, friend):
        from communication import Message
        message = Message.Constructor(senderUserName=self.username, senderId=self.id, type_="gameInvitation",
                                      receiverUserName=friend.userName, content="", user=self)
        message.send()

    def sendMoveMessage(self, movingPiece, move, opponent, gameId, capturedPiece=None):
        from communication import GameMessage
        if capturedPiece is None:
            capturedPieceName = "None"
        else:
            capturedPieceName = capturedPiece.name
        gameMessage = GameMessage.GConstructor(senderUserName=self.username, senderId=self.id,
                                               movingPieceName=movingPiece.name,
                                               destinationSquareX=move.destinationSquare.topLeftPosition.chessX,
                                               destinationSquareY=move.destinationSquare.topLeftPosition.chessY,
                                               receiverUserName=opponent.userName, type_="gameMove", user=self,
                                               gameId=gameId, capturedPieceName=capturedPieceName)

        gameMessage.send()

    def sendChatMessage(self, receiverUserName, content, gameId):
        """
        Here, we construct a chatMessage, we send it to the server, and we also append it to the user current pages chat messages attribute, to be displayed on the screen
        :param receiverUserName:
        :param content:
        :param gameId:
        :return:
        """
        from communication import ChatMessage
        chatMessage = ChatMessage.ChatConstructor(senderUserName=self.username, senderId=self.id,
                                                  gameId=gameId,
                                                  content=content,
                                                  receiverUserName=receiverUserName,
                                                  type_='chatMessage', user=self)
        self.currentPage.chatMessages.append(chatMessage)
        self.currentPage.chatMessageEntry.text = ''
        chatMessage.send()

    def sendInvitation(self, friendUserName):
        """
        The content key will have the invitation id as a value
        :param friendUserName:
        :return:
        """
        from communication import Message

        message = Message.Constructor(senderUserName=self.username, senderId=self.id, type_="invitation",
                                      content=random.randint(1, 494641949),
                                      user=self, receiverUserName=friendUserName)
        message.send()
