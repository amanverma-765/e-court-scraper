import base64
import json
import random
import urllib.parse
from urllib import response

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Encryption key for requests (hex-encoded)
ENCRYPTION_KEY = bytes.fromhex('4D6251655468576D5A7134743677397A')

# Decryption key for responses (hex-encoded)
DECRYPTION_KEY = bytes.fromhex('3273357638782F413F4428472B4B6250')

# Array of predefined IV prefixes (hex-encoded)
GLOBAL_IV_OPTIONS = [
    "556A586E32723575",
    "34743777217A2543",
    "413F4428472B4B62",
    "48404D635166546A",
    "614E645267556B58",
    "655368566D597133"
]


def generate_random_hex(size):
    """
    Generate a random hexadecimal string of specified size.
    """
    return ''.join(random.choice('0123456789abcdef') for _ in range(size))


def encrypt_request(data: dict):
    """
    Encrypt data for API request.

    The encryption process:
    1. Convert data to JSON string
    2. Randomly select a global IV prefix from predefined options
    3. Generate a random 16-character hex string
    4. Combine them to create 32-character IV
    5. Encrypt using AES-128-CBC
    6. Encode ciphertext as Base64
    7. Prepend random IV + global IV index to the encrypted data

    Args:
        data (dict): Dictionary containing request data

    Returns:
        str: Encrypted data string with format: randomiv + globalIndex + base64_encrypted_data
    """
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
    """
    Decrypt API response.

    The decryption process:
    1. Extract IV from first 32 characters
    2. Extract encrypted data from remaining characters
    3. Decode from Base64
    4. Decrypt using AES-128-CBC
    5. Remove padding
    6. Parse JSON response

    Args:
        encrypted_response (str): Encrypted response string

    Returns:
        dict: Decrypted JSON data as dictionary
    """
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
    """
    Decrypt an encrypted request parameter.
    """
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


if __name__ == '__main__':
    txt = """

01b057a05a5442091gjiPN2SCUNb7%2BUiX4ePhhwJZt2Jcc%2BaoJykV6P5BV35jYSCZ4OwYs4x4xer7t2B%2B

"""
    req = urllib.parse.unquote(txt)
    data = decrypt_request(req)

    # data = decrypt_response(txt)

    print(data)
