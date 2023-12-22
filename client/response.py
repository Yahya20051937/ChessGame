from types import coroutine
import requests


@coroutine
def authenticationResponse(page, responseLabel, requestType):
    from user import User
    from jwt import JWT
    from pages import Page
    ERRORS = {301: "Invalid Password", 302: "Invalid userName", 303: "Username already Used", 304: "Email already used", 500:"ERROR 500"}
    BASE_URL = f'http://127.0.0.1:5000/authenticate/{requestType}'

    while page.running:

        data = yield

        response = requests.post(BASE_URL, headers=data)

        if response.status_code == 200:
            page.running = False
            # data = response.json()
            # user = User(username=data['userName'], id_=data['id'])
            jwt = JWT.Constructor(jwt_data=response.content)
            user = User(username=jwt.username, id_=jwt.user_id, jwt=jwt)
            user.online = True
            Page.get('home', page, user)
        else:
            page.responding = True
            responseLabel.text = ERRORS[response.status_code]


async def sendRequest(g):
    await g


