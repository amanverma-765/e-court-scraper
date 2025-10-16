import base64
import json
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ENCRYPTION_KEY = bytes.fromhex('4D6251655468576D5A7134743677397A')
DECRYPTION_KEY = bytes.fromhex('3273357638782F413F4428472B4B6250')

GLOBAL_IV_OPTIONS = [
    "556A586E32723575",
    "34743777217A2543",
    "413F4428472B4B62",
    "48404D635166546A",
    "614E645267556B58",
    "655368566D597133"
]


def generate_random_hex(size):
    return ''.join(random.choice('0123456789abcdef') for _ in range(size))


def encrypt_request(data):
    data_json = json.dumps(data, separators=(',', ':'))

    global_index = random.randint(0, len(GLOBAL_IV_OPTIONS) - 1)
    global_iv = GLOBAL_IV_OPTIONS[global_index]

    random_iv = generate_random_hex(16)

    full_iv_hex = global_iv + random_iv
    iv = bytes.fromhex(full_iv_hex)

    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)

    padded_data = pad(data_json.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')

    # Return: randomiv + globalIndex + encrypted_data
    return random_iv + str(global_index) + encrypted_base64


def decrypt_response(encrypted_response):
    try:
        encrypted_response = encrypted_response.strip()
        iv_hex = encrypted_response[:32]
        iv = bytes.fromhex(iv_hex)

        encrypted_data_base64 = encrypted_response[32:]
        encrypted_data = base64.b64decode(encrypted_data_base64)
        cipher = AES.new(DECRYPTION_KEY, AES.MODE_CBC, iv)

        decrypted_padded = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded, AES.block_size)

        plaintext = decrypted_data.decode('utf-8')
        return json.loads(plaintext)
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")


def decrypt_request(encrypted_request):
    try:
        encrypted_request = encrypted_request.strip()

        random_iv = encrypted_request[:16]
        global_index = int(encrypted_request[16])

        if global_index < 0 or global_index >= len(GLOBAL_IV_OPTIONS):
            raise ValueError(f"Invalid global IV index: {global_index}")

        encrypted_data_base64 = encrypted_request[17:]
        global_iv = GLOBAL_IV_OPTIONS[global_index]
        full_iv_hex = global_iv + random_iv
        iv = bytes.fromhex(full_iv_hex)

        encrypted_data = base64.b64decode(encrypted_data_base64)
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)

        decrypted_padded = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded, AES.block_size)

        plaintext = decrypted_data.decode('utf-8')
        return json.loads(plaintext)

    except Exception as e:
        raise ValueError(f"Request decryption failed: {str(e)}")
