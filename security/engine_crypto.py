# coding=utf-8

import protector

# ENGINE_PRIVATE_KEY = os.environ['ENGINE_PRIVATE_KEY']
# ENGINE_PRIVATE_KEY = './keys/engine_private_key.pem'

# 讀取 Engine 的 private key
# return value: private_key
def load_private_key():
    return protector.open_private_key(protector.ENGINE_PRIVATE_KEY)

# 表明身分：對要傳送出去的指令 (身分名稱) token 簽名
# plaintext_token: string (注意 plaintext_token 不可含機密資訊 )
# private_key: *.pem
# return value: bytes
def sign_request_token(plaintext_token, private_key):
    return protector.sign_request_token(plaintext_token, private_key)

# 解密資料：解密收到的 user data 內容 (JSON 格式)
# encrypted_json: string list
# private_key: *.pem
# return value: json
def decrypt_userdata(encrypted_json, private_key):
    return protector.convert_string_to_json(protector.decrypt_ciphertext(encrypted_json, private_key))


