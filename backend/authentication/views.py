
from flask import Flask, request, session, jsonify, make_response
from jwt import verify_authorization


def logIn():
    from .models import UserModel
    from jwt import JWT
    userName = request.headers.get('userName')
    password = request.headers.get('password')
    user, code = UserModel.authenticate(userName, password)
    if user is not None:
        jwt = JWT(username=userName, user_id=user.id)
        response = make_response(jwt.generate())
        response.status_code = 200
    else:
        response = make_response('')
        response.status_code = code
    return response


def signUp():
    from .models import UserModel
    from jwt import JWT
    userName = request.headers.get('userName')
    password = request.headers.get('password')
    email = request.headers.get('email')

    user, code = UserModel.register(userName, email, password)
    if user is not None:
        jwt = JWT(userName, user_id=user.id)
        response = make_response(jwt.generate())
        response.status_code = 200
    else:
        response = make_response('')
        response.status_code = code

    return response


@verify_authorization
def logOut(user_details):
    from .models import UserModel
    from manage import db
    user = UserModel.query.filter_by(userName=user_details.username).first()
    user.status = "offline"
    db.session.commit()
    return make_response('')
