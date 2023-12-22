import json

import pygame.event


class Message:
    @staticmethod
    def Constructor(senderUserName, senderId, receiverUserName, type_, content, user):
        return Message(
            socketMessage=json.dumps(
                {"from": f'{senderUserName},{senderId}', "to": receiverUserName, "type": type_, "content": content,
                 "jwt": user.jwt.generate()}),
            user=user)

    def __init__(self, socketMessage, user):
        self.socketMessageJson = socketMessage
        # print(socketMessage)
        self.socketMessage = json.loads(socketMessage)
        self.senderUserName = self.socketMessage.get('from').split(',')[0]
        self.senderId = self.socketMessage.get('from').split(',')[1]
        self.receiverUserName = self.socketMessage.get('to')
        self.type = self.socketMessage.get('type')
        self.content = self.socketMessage.get('content')
        self.user = user

    def send(self):
        self.user.connection.sendall(self.socketMessageJson.encode())

    def parse(self):
        if self.type == 'info':
            print("Message Type :: INFO")
            self.parse_info()

        elif self.type == 'invitation':
            self.parse_invitation()

    def parse_info(self):
        """
        If the message is a start game message, we send the startGameMessageContent attribute to the  message content, and we add the start game event to the pygame events queue.
        :return:
        """
        from pages import StartOnlineGameEvent

        if self.content == "online" or self.content == "offline":

            for friend in self.user.friends:
                if friend.userName == self.senderUserName:
                    friend.status = self.content

        elif self.content.split(':')[0] == 'startGame':
            self.user.startGameMessageContent = self.content
            self.user.currentGameId = self.content.split(':')[1]
            startGameEvent = pygame.event.Event(StartOnlineGameEvent)
            pygame.event.post(startGameEvent)

    def parse_invitation(self):
        """
        The content key has the invitation id as a value, we tell the server that we accepted the invitation with that particular id.
        :return:
        """
        senderFriend = [f for f in self.user.friends if f.userName == self.senderUserName][0]
        id_ = self.content
        invitation = Invitation(user=self.user, senderFriend=senderFriend, id_=id_)
        self.user.receivedInvitations.append(invitation)


class Invitation:
    def __init__(self, user, senderFriend, id_):
        self.user = user
        self.id = id_
        self.senderFriend = senderFriend

    def accept(self):
        message = Message.Constructor(senderUserName=self.user.username, senderId=self.user.id,
                                      receiverUserName='SERVER',
                                      type_='info', content=f'invitationAccept:{self.id}', user=self.user)
        message.send()

    def reject(self):
        message = Message.Constructor(senderUserName=self.user.username, senderId=self.user.id,
                                      receiverUserName='SERVER', type_='info',
                                      content=f'invitationReject:{self.id}', user=self.user)
        message.send()


class GameMessage(Message):
    @staticmethod
    def GConstructor(senderUserName, senderId, receiverUserName, type_, movingPieceName, destinationSquareX, gameId,
                     destinationSquareY, user, capturedPieceName="None"):
        return GameMessage(
            socketMessage=json.dumps({"from": f"{senderUserName},{senderId}", "to": receiverUserName, "type": type_,
                                      "destinationSquareX": destinationSquareX,
                                      "destinationSquareY": destinationSquareY,
                                      "movingPieceName": movingPieceName, "gameId": gameId,
                                      "capturedPieceName": capturedPieceName, "jwt": user.jwt.generate()}), user=user)

    def __init__(self, socketMessage, user):
        super().__init__(socketMessage, user)
        self.gameId = self.socketMessage.get('gameId')
        self.movingPieceName = self.socketMessage.get('movingPieceName')
        self.capturedPieceName = self.socketMessage.get('capturedPieceName')
        self.destinationSquareX = self.socketMessage.get('destinationSquareX')
        self.destinationSquareY = self.socketMessage.get('destinationSquareY')

    def execute(self, userPlayer, opponentPlayer):
        print("Executing")
        for piece in opponentPlayer.pieces:
            if piece.name == self.movingPieceName:
                piece.Position.chessX = self.destinationSquareX
                piece.Position.chessY = self.destinationSquareY
        for piece in userPlayer.pieces:
            if piece.name == self.capturedPieceName:
                piece.Position.chessX = piece.deadPosition.chessX
                piece.Position.chessY = piece.deadPosition.chessY
                piece.alive = False


class ChatMessage(Message):
    @staticmethod
    def ChatConstructor(senderUserName, senderId, receiverUserName, type_, content, user, gameId):
        return Message(
            socketMessage=json.dumps(
                {"from": f'{senderUserName},{senderId}', "to": receiverUserName, "type": type_, "content": content,
                 "gameId": gameId, "jwt" : user.jwt.generate()
                 }),
            user=user)

    def __init__(self, socketMessage, user):
        super().__init__(socketMessage, user)
        self.gameId = self.socketMessage.get('gameId')
