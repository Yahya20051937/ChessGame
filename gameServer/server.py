import json
import socket
import threading
from sqlalchemy import create_engine, text


class Message:

    @staticmethod
    def Constructor(senderUserName, senderId, receiverUserName, type_, content, server, senderConnection):

        return Message(
            socketMessage=json.dumps(
                {"from": f'{senderUserName},{senderId}', "to": receiverUserName, "type": type_, "content": content}),
            server=server, senderConnection=senderConnection)

    def __init__(self, socketMessage, server, senderConnection):
        from jwt import JWT
        print(socketMessage)
        try:
            self.socketMessage = json.loads(socketMessage)
            self.senderUserName = self.socketMessage.get('from').split(',')[0]
            self.senderId = self.socketMessage.get('from').split(',')[1]
            self.receiverUserName = self.socketMessage.get('to')
            self.type = self.socketMessage.get('type')
            self.content = self.socketMessage.get('content')
            self.jwt = JWT.Constructor(self.socketMessage.get("jwt"))
            self.server = server
            self.senderConnection = senderConnection
        except json.decoder.JSONDecodeError:
            print("json.decoder.JSONDecodeError")

    def send(self):
        if self.receiverUserName == 'SERVER':
            self.server.parseServerMessage(message=self)
            return

        for client in self.server.clients:

            if client.username == self.receiverUserName:
                socketMessage = json.dumps(self.socketMessage)
                client.connection.sendall(socketMessage.encode(Server.FORMAT))
                print(f"Message sent, {socketMessage}")


class Client:
    @staticmethod
    def get(userName):
        for client in Client.clients:
            if client.username == userName:
                return client
        return None

    clients = []

    def __init__(self, connection, username, id_):
        self.connection = connection
        self.username = username
        self.id = id_
        Client.clients.append(self)


def handleConnection(conn, server):
    while True:

        try:
            socketMessage = conn.recv(2000).decode(Server.FORMAT)

            message = Message(socketMessage=socketMessage, server=server, senderConnection=conn)
            if message.jwt is not None and message.jwt.is_authorized():  #
                try:
                    if message.type == 'invitation':
                        server.addInvitation(message)

                    print("Message Received ....")
                    message.send()

                    if message.content == "offline":

                        break

                except AttributeError:
                    print("ERROR")
            else:
                print("401 : Unauthorized")

        except ConnectionResetError or json.decoder.JSONDecodeError:
            break


class GameInvitation:
    invitations = []

    @staticmethod
    def get(id_):
        for inv in GameInvitation.invitations:
            if int(inv.id) == int(id_):
                return inv

    def __init__(self, sender, receiver, id_):
        self.sender = sender
        self.receiver = receiver
        self.id = id_
        GameInvitation.invitations.append(self)

    def startOnlineGame(self, server):
        """
        Here we send two messages to both users, to inform them that the invitation has been accepted and that the game has started, and the game id and also the color
        """

        message1 = Message.Constructor(senderUserName='SERVER', senderId='999', receiverUserName=self.sender.username,
                                       server=server, senderConnection=server, type_="info",
                                       content=f"startGame:{self.id}:{self.receiver.username}:black")
        message2 = Message.Constructor(senderUserName='SERVER', senderId='999', receiverUserName=self.receiver.username,
                                       server=server, senderConnection=server, type_="info",
                                       content=f"startGame:{self.id}:{self.sender.username}:white")

        message1.send()
        message2.send()


class Server:
    PORT = 5050
    HEADER = 64
    SERVER = socket.gethostbyname(socket.gethostname())
    FORMAT = 'utf-8'
    ADDR = (SERVER, PORT)

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind(Server.ADDR)
        self.clients = []
        self.gameInvitations = []  # (sender, receiver, id)
        db_uri = 'sqlite:///C:/Users/HP/PycharmProjects/pythonProject/ChessGame/backend/database.db'
        engine = create_engine(db_uri)
        self.dbConnection = engine.connect()

    def addInvitation(self, message):
        sender = Client.get(message.senderUserName)
        receiver = Client.get(message.receiverUserName)
        invitationId = message.content
        gameInvitation = GameInvitation(sender=sender, receiver=receiver, id_=invitationId)
        self.gameInvitations.append(gameInvitation)

    def parseServerMessage(self, message):
        """
        If the server receives an info message that informs that he changed his status,
         we first edit his row in the database, then we send a message to each one of his friends,
         to inform them that he changed his status
        :param message:
        :return:
        """
        if message.content == 'online' or message.content == 'offline':
            client = Client(connection=message.senderConnection, username=message.senderUserName, id_=message.senderId)
            if message.content == "online":
                self.clients.append(client)

            else:
                indexCounter = -1
                for client in self.clients:
                    indexCounter += 1
                    if client.username == message.senderUserName:
                        self.clients.pop(indexCounter)
                        break

            query = text("SELECT * FROM friendship")
            result = self.dbConnection.execute(query)
            friendships = result.fetchall()

            for friendship in friendships:

                if int(friendship[1]) == int(message.senderId):
                    query = text('SELECT userName FROM user_model WHERE id = :user_id')
                    result = self.dbConnection.execute(query, {'user_id': friendship[2]})
                    friendUserName = result.fetchone()[0]
                    message = Message.Constructor(senderUserName=message.senderUserName, senderId=message.senderId,
                                                  receiverUserName=friendUserName, type_="info",
                                                  content=message.content, server=self, senderConnection=self)
                    message.send()

                elif int(friendship[2]) == int(message.senderId):
                    query = text('SELECT userName FROM user_model WHERE id = :user_id')
                    result = self.dbConnection.execute(query, {'user_id': friendship[1]})
                    friendUserName = result.fetchone()[0]
                    message = Message.Constructor(senderUserName=message.senderUserName, senderId=message.senderId,
                                                  receiverUserName=friendUserName, type_="info",
                                                  content=message.content, server=self, senderConnection=self)
                    message.send()
        elif message.content.split(':')[0] == "invitationAccept":
            invitationId = message.content.split(":")[1]
            gameInvitation = GameInvitation.get(invitationId)

            gameInvitation.startOnlineGame(server=self)

    def start(self):
        self.server.listen()
        print("Running")

        while True:
            conn, addr = self.server.accept()
            print("New connection")
            thread = threading.Thread(target=handleConnection, args=(conn, self))
            thread.start()


if __name__ == '__main__':
    server_ = Server()
    server_.start()
