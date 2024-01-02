from manage import db
from appServices.models import FriendRequest


class UserModel(db.Model):
    __tablename__ = 'user_model'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    status = db.Column(db.String(100))

    received_requests = db.relationship('FriendRequest', backref='receiver')

    @staticmethod
    def authenticate(userName, password):
        users = UserModel.query.all()
        for user in users:
            if user.userName == userName:
                if user.password == password:
                    user.status = "online"
                    db.session.commit()
                    return user, 300
                else:
                    return None, 301
        return None, 302

    @staticmethod
    def register(userName, email, password):
        users = UserModel.query.all()
        usernames = [user.userName for user in users]
        emails = [user.email for user in users]

        if userName in usernames:
            return None, 303
        else:
            if email in emails:
                return None, 304
            else:
                newUser = UserModel(userName=userName, email=email, password=password, status="online")
                db.session.add(newUser)
                db.session.commit()
                return newUser, 305



    def getReceivedFriendRequests(self):
        return self.received_requests

    def getFriends(self):
        """
        First we get all the friendships where our a user is taking part, then we get all the ids of the user friends, to get the actual friends objects
        :return:
        """
        from appServices.models import Friendship
        userFriendships = Friendship.query.filter_by(friend1_id=self.id).all() + Friendship.query.filter_by(
            friend2_id=self.id).all()
        friends = []
        for friendship in userFriendships:
            friend_id = [id_ for id_ in [friendship.friend1_id, friendship.friend2_id] if id_ != self.id][0]
            friend = UserModel.query.filter_by(id=friend_id).first()
            friends.append(friend)
        return friends
