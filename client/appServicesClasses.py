class FriendRequest:
    def __init__(self, senderUserName, receiverUserName):
        self.senderUserName = senderUserName
        self.receiverUserName = receiverUserName

    def accept(self):
        pass

    def decline(self):
        pass


class Friend:
    @staticmethod
    def get(user, friendUserName):
        for friend in user.friends:
            if friend.userName == friendUserName:
                return friend
        return Friend(userName=friendUserName, status='online')


    def __init__(self, userName, status="offline", id_=0):
        self.userName = userName
        self.status = status
        self.id = id_
