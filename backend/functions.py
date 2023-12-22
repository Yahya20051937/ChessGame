import base64


def is_prime(n):
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            print("divider found" , i)
            return False
    return True


def get_random_prime_number(other_than=0):
    for i in range(10, 1000000000000000000000000000000000000000000000000):

        if is_prime(i) and i != other_than:
            return i


def has_common_factor(n1, n2):
    for i in range(2, max(n1, n2) + 1):
        if n1 % i == 0 and n2 % i == 0:
            return True
    return False


def phi(p, q):
    return (p - 1) * (q - 1)


def get_encoding_key(T):
    for e in range(1, T + 1):
        if is_prime(e) and T % e != 0:
            return e


def get_decoding_key(N, e, T):
    for d in range(2, N):
        if (d * e) % T == 1:
            return d


def reverse_dict(dict_):
    reversed_dict = dict()
    for key in dict_.keys():
        reversed_dict[dict_[key]] = key
    return reversed_dict


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


def encode(decoded_jwt):
    binary_jwt = int(encode_binary(decoded_jwt))
    print(binary_jwt)
    p = 7
    q = 19

    N = p * q
    T = phi(p, q)

    e = get_encoding_key(T)
    d = get_decoding_key(N, e, T)
    # print(p, q, N, T, e, d)
    encoded_jwt_binary = (binary_jwt ** e) % N
    print(encoded_jwt_binary)

    decoded_jwt_binary = (encoded_jwt_binary ** d) % N
    print(decoded_jwt_binary)
    # decoded_jwt_b = decode_binary(str(decoded_jwt_binary))

    # print(decoded_jwt_b)



# encode("yahya")

def test_encode(n):
    p = 7193
    q = 9319

    N = p * q
    print(N)
    T = phi(p, q)
    print("Looking for e")
    e = get_encoding_key(T)
    print("e found", e)
    print("Looking for d")
    d = get_decoding_key(N, e, T)
    print("d found", d)
    cipher = (n ** e) % N
    text = (cipher ** d) % N
    print(cipher, text)






