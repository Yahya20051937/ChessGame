from jwt import verify_authorization
from flask import jsonify, make_response


@verify_authorization
def sendFriendRequest(user_details, receiverUserName):
    from .models import FriendRequest
    code = FriendRequest.sendRequest(user_details.username, receiverUserName)
    response = make_response('')
    response.status_code = code
    return response

@verify_authorization
def getReceivedFriendRequests(user_details):
    from authentication.models import UserModel
    user = UserModel.query.filter_by(userName=user_details.username).first()
    receivedRequests = user.getReceivedFriendRequests()
    receivedRequestsStr = ""
    for receivedRequest in receivedRequests:
        receivedRequestsStr += f"{receivedRequest.senderUserName}/"

    response = make_response(jsonify({"receivedRequests": receivedRequestsStr}))
    return response

@verify_authorization
def acceptFriendRequest(user_details, senderUserName):
    from .models import FriendRequest, Friendship
    Friendship.create(userName1=senderUserName, userName2=user_details.username)
    FriendRequest.deleteRequest(senderUserName=senderUserName, receiverUserName=user_details.username)
    response = make_response()
    return response

@verify_authorization
def declineFriendRequest(user_details, senderUserName):
    from .models import FriendRequest
    FriendRequest.deleteRequest(senderUserName=senderUserName, receiverUserName=user_details.username)
    return make_response()

@verify_authorization
def getFriends(user_details):
    """
    The friends username and current status will be sent as json, so that every friend username and friend status has the same index on the string splitting by a slash

    :return:
    """
    from .models import Friendship
    friends = Friendship.getFriends(user_details.username)
    friendsUserNames = ""
    friendsStatus = ""
    for friend in friends:
        friendsUserNames += f"{friend.userName}/"
        friendsStatus += f"{friend.status}/"
    response = make_response(jsonify({"friends": friendsUserNames, "status": friendsStatus}))
    return response
