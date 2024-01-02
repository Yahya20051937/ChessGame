from flask import Flask
import secrets
from user_details import UserDetails
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


from authentication.views import signUp, logIn, logOut
from appServices.views import sendFriendRequest, getReceivedFriendRequests, acceptFriendRequest, declineFriendRequest, \
    getFriends
from jwt import verify_authorization

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = secrets.token_hex(16)

db = SQLAlchemy(app)
secret_key = "Wydad3719"

user_friend = db.Table('user_friend', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('friend_id'))


@app.route('/authenticate/signUp', methods=['POST'])
def handleSignUp():
    return signUp()


@app.route('/authenticate/logIn', methods=['POST'])
def handleLogIn():
    return logIn()


@app.route('/authenticate/logOut', methods=['GET'])
def handleLogOut():
    return logOut()


@app.route('/friendRequest/send/<receiverUserName>', methods=['GET'])
def handleSendFriendRequest(receiverUserName):
    return sendFriendRequest(receiverUserName)


@app.route('/friendRequest/get', methods=['GET'])
def handleGetFriendRequests():
    return getReceivedFriendRequests()


@app.route('/friendRequest/<requestType>/<senderUserName>', methods=['GET'])
def handleAcceptOrDeclineFriendRequest(requestType, senderUserName):
    if requestType == 'accept':
        return acceptFriendRequest(senderUserName)
    elif requestType == 'decline':
        return declineFriendRequest(senderUserName)


@app.route('/friends/get', methods=['GET'])
def handleGetFriends():
    return getFriends()


"""def delete():
    from authentication.models import UserModel
    from appServices.models import FriendRequest, Friendship
    session = db.session
    try:

        # session.query(FriendRequest).delete()
        session.query(UserModel).delete()
        session.commit()
        print("<Deleted>")
    except Exception as e:
        session.rollback()
        print(Exception)
    finally:
        session.close()
    session.query(FriendRequest).delete()
    session.query(Friendship).delete()
    session.query(UserModel).delete()
    session.commit()
    session.close()"""


def create():
    from authentication.models import UserModel
    from appServices.models import FriendRequest, Friendship
    # print(FriendRequest.__tablename__)
    # FriendRequest.__table__.create(db.engine)
    UserModel.__table__.create(db.engine)
    # Friendship.__table__.create(db.engine)
    # print(UserModel.query)
    # print(FriendRequest.query)
    # print('<Created>')


if __name__ == '__main__':
    # delete()
    # create()

    app.run(debug=True)
