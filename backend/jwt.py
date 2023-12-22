import functools
import json
import random
import time
from hashlib import blake2b
from functions import encode_binary, decode_binary
from flask import request, make_response


class JWT:
    private_key = encode_binary("Wydad3719")

    def __init__(self, username=None, user_id=None, header=None, payload=None, signature=None):

        self.header = self.generate_header(header)
        self.payload = self.generate_payload(username, user_id, payload)
        self.encoded_header = encode_binary(self.header)
        self.encoded_payload = encode_binary(self.payload)
        self.signature = self.generate_signature(signature)

    @staticmethod
    def generate_header(header=None):
        if header is None:
            algorithm = random.choice(["RS256", "RSA"])
            return json.dumps({"alg": algorithm})
        return header

    @staticmethod
    def generate_payload(username, user_id, payload=None):
        if payload is None:
            payload_ = dict()
            issued_at = time.time()
            expires_at = time.time() + 60

            payload_["sub"] = username
            payload_["id"] = user_id
            payload_["scope"] = ""
            payload_["iat"] = issued_at
            payload_["exp"] = expires_at
            return json.dumps(payload_)
        return payload

    def fill_user_details(self, user_details_instance):
        payload_dict = json.loads(self.payload)
        username = payload_dict["sub"]
        user_id = payload_dict["id"]
        scope = payload_dict["scope"]
        user_details_instance.id = user_id
        user_details_instance.username = username
        user_details_instance.scope = scope

    def generate_signature(self, signature=None):
        if signature is None:
            signature_ = blake2b(f"{self.encoded_header}*{self.encoded_payload}*{self.private_key}".encode("utf-8"),
                                 digest_size=32).hexdigest()
            return signature_
        return signature

    def generate(self):
        return f"{self.encoded_header}*{self.encoded_payload}*{self.signature}"

    def is_authorized(self):
        if self.signature == self.generate_signature():
            return True
        return False

    @staticmethod
    def Constructor(jwt):
        if jwt is not None:
            json_header = decode_binary(jwt.split("*")[0])
            json_payload = decode_binary(jwt.split("*")[1])
            json_signature = jwt.split("*")[2]
            return JWT(header=json_header, payload=json_payload, signature=json_signature)
        return None


def verify_authorization(end_point):
    from user_details import UserDetails

    @functools.wraps(end_point)
    def wrapper(*args, user_details=UserDetails.build()):
        jwt = JWT.Constructor(request.headers.get("jwt"))
        if jwt is not None and jwt.is_authorized():
            jwt.fill_user_details(user_details)
            return end_point(user_details, *args)
        else:
            response = make_response()
            response.status_code = 401
        return response

    return wrapper
