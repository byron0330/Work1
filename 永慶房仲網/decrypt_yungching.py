import json
import base64
import hashlib
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

# 固定參數
SALT = bytes([2, 7, 0, 5, 1, 3, 8, 0])
ITERATIONS = 1000
KEY_SIZE = 32
IV_SIZE = 16

from Crypto.Hash import SHA1


def derive_key_iv(password: str):
    # SHA256(password)
    password_hash = hashlib.sha256(password.encode('utf-8')).digest()
    # PBKDF2-SHA1，產生 48 bytes（key + iv）
    derived = PBKDF2(password_hash, SALT, dkLen=KEY_SIZE + IV_SIZE, count=ITERATIONS, hmac_hash_module=SHA1)

    key = derived[:KEY_SIZE]
    iv = derived[KEY_SIZE:]
    return key, iv

def decrypt_base64(ciphertext_b64: str, key_name: str):
    ciphertext_bytes = base64.b64decode(ciphertext_b64)
    key, iv = derive_key_iv(key_name)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext_bytes)
    # 移除 PKCS#7 padding
    pad_len = plaintext_padded[-1]
    plaintext = plaintext_padded[:-pad_len]
    return plaintext.decode('utf-8')


def decrypt_yungching_data(ciphertext_b64: str, key_name: str = "金鑰名稱") -> str:
    """
    解密永慶房仲前端 AES-CBC + Base64 加密資料
    :param ciphertext_b64: 加密過的 base64 字串（從 data 欄位取得）
    :param key_name: 解密用的金鑰名稱
    :return: 解密後的明文 JSON 字串
    """
    try:
        plaintext = decrypt_base64(ciphertext_b64, key_name)
        return json.loads(plaintext)
    except Exception as e:
        raise RuntimeError(f"解密失敗：{e}")
