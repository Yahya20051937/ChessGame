def encode_binary(string):
    encoded_string = ""
    for char in string:
        ascii_value = ord(char)
        binary_representation = format(ascii_value, "08b")
        encoded_string += binary_representation
    return encoded_string


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
