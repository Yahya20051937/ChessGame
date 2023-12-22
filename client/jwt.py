import json


def decode_binary(encoded_string):
    decoded_string = ""
    i = 0
    while i < len(encoded_string):
        binary_representation = encoded_string[i: i + 8]
        decimal_representation = int(binary_representation, 2)
        char = chr(decimal_representation)
        decoded_string += char
        i += 8
    return decoded_string


def encode_binary(string):
    encoded_string = ""
    for char in string:
        ascii_value = ord(char)
        binary_representation = format(ascii_value, "08b")
        encoded_string += binary_representation
    return encoded_string


class JWT:
    def __init__(self, header, payload, signature):
        self.header = header
        self.payload = payload
        self.signature = signature

        self.username = self.payload["sub"]
        self.user_id = self.payload["id"]
        self.scope = self.payload["scope"]

    @staticmethod
    def Constructor(jwt_data):
        encoded_header = jwt_data.decode("utf-8").split("*")[0]
        encoded_payload = jwt_data.decode("utf-8").split("*")[1]
        signature = jwt_data.decode("utf-8").split("*")[2]

        header = json.loads(decode_binary(encoded_header))
        payload = json.loads(decode_binary(encoded_payload))

        return JWT(header, payload, signature)

    def generate(self):
        return encode_binary(json.dumps(self.header)) + "*" + encode_binary(json.dumps(self.payload)) + "*" + self.signature

