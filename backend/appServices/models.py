from manage import db


class FriendRequest(db.Model):
    __tablename__ = 'friend_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    senderUserName = db.Column(db.String(100))

    @staticmethod
    def sendRequest(senderUserName, receiverUserName):

        """
        The receiver may exist and may not, so if the receiver variable is None, we return the status code 306 that says "The username is not found" ,
        and then we check if a request already exists between the two user, if not we create a request
        We also need to check if the sender and receiver are already friends
        :param senderUserName:
        :param receiverUserName:
        :return:
        """
        from authentication.models import UserModel

        sender = UserModel.query.filter_by(userName=senderUserName).first()
        receiver = UserModel.query.filter_by(userName=receiverUserName).first()
        if receiver is None or receiver.userName == sender.userName:
            return 306
        for friendRequest in FriendRequest.query.all():
            if (
                    friendRequest.senderUserName == senderUserName and friendRequest.receiver_id == receiver.id) or (
                    friendRequest.senderUserName == receiverUserName and friendRequest.receiver.id == sender.id):
                return 307
        for friendship in Friendship.query.all():
            if (friendship.friend1_id == sender.id and friendship.friend2_id == receiver.id) or (
                    friendship.friend1_id == receiver.id and friendship.friend2_id == sender.id):
                return 308

        friendRequest = FriendRequest(senderUserName=senderUserName, receiver_id=receiver.id)
        db.session.add(friendRequest)
        db.session.commit()
        return 200

    @staticmethod
    def deleteRequest(senderUserName, receiverUserName):
        from authentication.models import UserModel
        allRequest = FriendRequest.query.all()
        receiver = UserModel.query.filter_by(userName=receiverUserName).first()
        for friendRequest in allRequest:
            if friendRequest.senderUserName == senderUserName and friendRequest.receiver_id == receiver.id:
                db.session.delete(friendRequest)
                db.session.commit()
                return 200


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    friend1_id = db.Column(db.Integer)
    friend2_id = db.Column(db.Integer)

    @staticmethod
    def create(userName1, userName2):
        from authentication.models import UserModel
        user1 = UserModel.query.filter_by(userName=userName1).first()
        user2 = UserModel.query.filter_by(userName=userName2).first()
        friendship = Friendship(friend1_id=user1.id, friend2_id=user2.id)
        db.session.add(friendship)
        db.session.commit()
        return 200

    @staticmethod
    def getFriends(userName):
        from authentication.models import UserModel

        friends = []
        user = UserModel.query.filter_by(userName=userName).first()
        for friendship in Friendship.query.all():
            if friendship.friend1_id == user.id:
                friend = UserModel.query.filter_by(id=friendship.friend2_id).first()
                friends.append(friend)
            elif friendship.friend2_id == user.id:
                friend = UserModel.query.filter_by(id=friendship.friend1_id).first()
                friends.append(friend)
        return friends
