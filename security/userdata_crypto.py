# coding=utf-8

import protector

# ENGINE_PUBLIC_KEY = os.environ['ENGINE_PUBLIC_KEY']
# ENGINE_PUBLIC_KEY = './keys/engine_public_key.pem'

# 讀取 Engine 的 public key
# return value: public_key
def load_public_key():
    return protector.open_public_key(protector.ENGINE_PUBLIC_KEY)

# 辨識身分：確認此指令 token 是否為正確的身分名稱發出的 
# plaintext_token: string (注意 plaintext_token 不可含機密資訊 )
# signed_token: bytes
# public_key: *.pem
# return value: bool
def is_correct_requester(plaintext_token, signed_token, public_key):
    return protector.is_correct_requester(plaintext_token, signed_token, public_key)

# 加密資料：加密要傳送出去的 user data 內容 (JSON 格式)
# raw_json: json
# public_key: *.pem
# return value: string list
def encrypt_userdata(raw_json, public_key):
    return protector.encrypt_plaintext(protector.convert_json_to_string(raw_json), public_key)


