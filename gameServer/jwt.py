from hashlib import blake2b
from functions import encode_binary, decode_binary


class JWT:
    private_key = encode_binary("Wydad3719")

    def __init__(self, header, payload, signature):
        self.header = header
        self.payload = payload
        self.signature = signature

    def generate_signature(self):
        signature_ = blake2b(
            f"{encode_binary(self.header)}*{encode_binary(self.payload)}*{self.private_key}".encode("utf-8"),
            digest_size=32).hexdigest()
        return signature_

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
