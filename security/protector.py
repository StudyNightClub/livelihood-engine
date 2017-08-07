# coding=utf-8

import os
import rsa
import json
import traceback

ENGINE_PUBLIC_KEY = os.environ['ENGINE_PUBLIC_KEY']
ENGINE_PRIVATE_KEY = os.environ['ENGINE_PRIVATE_KEY']
LINEBOT_PUBLIC_KEY = os.environ['LINEBOT_PUBLIC_KEY']
LINEBOT_PRIVATE_KEY = os.environ['LINEBOT_PRIVATE_KEY']

""" For any two services """
# 表明身分：對要傳送出去的指令 (身分名稱) token 簽名
# plaintext_token: string (注意 plaintext_token 不可含機密資訊 )
# private_key: *.pem
# return value: bytes
def sign_request_token(plaintext_token, private_key):
    return sign_plaintext(plaintext_token, private_key)

# 辨識身分：確認此指令 token 是否為正確的身分名稱發出的
# plaintext_token: string (注意 plaintext_token 不可含機密資訊 )
# signed_token: bytes
# public_key: *.pem
# return value: bool
def is_correct_requester(plaintext_token, signed_token, public_key):
    return verify_signature(plaintext_token, signed_token, public_key)

# 加密資料：加密要傳送出去的 service data 內容 (string 格式)
# raw_str: string
# public_key: *.pem
# return value: string list
def encrypt_service_data(raw_str, public_key):
    return encrypt_plaintext(raw_str, public_key, 4)

# 解密資料：解密收到的 service data 內容 (string 格式)
# encrypted_str_list: string list
# private_key: *.pem
# return value: string
def decrypt_service_data(encrypted_str_list, private_key):
    return decrypt_ciphertext(encrypted_str_list, private_key)


""" Unit functions """
def generate_and_save_keys(public_key_source, private_key_source):
    (public_key, private_key) = rsa.newkeys(1024)

    with open(public_key_source, 'w+') as file:
        file.write(public_key.save_pkcs1('PEM').decode())

    with open(private_key_source, 'w+') as file:
        file.write(private_key.save_pkcs1('PEM').decode())

def open_public_key(key_source):
    with open(key_source,'r') as file:
        public_key = rsa.PublicKey.load_pkcs1(file.read().encode())
    return public_key

def open_private_key(key_source):
    with open(key_source,'r') as file:
        private_key = rsa.PrivateKey.load_pkcs1(file.read().encode())
    return private_key

def convert_json_to_string(raw_json):
    encoded_json = json.dumps(raw_json, sort_keys=True, skipkeys=True)
    return encoded_json

def convert_string_to_json(str):
    decoded_json = json.loads(str)
    return decoded_json

def encrypt_plaintext(str, public_key):    
    utf8_string_size = 4
    encrypted_string_size = ((1024 // 8) - 11) // utf8_string_size
    ciphertext_list = []        
    try:
        i = 0
        while(i <= len(str)):
            sub_str = str[i:(i+encrypted_string_size)]
            content = sub_str.encode()            
            ciphertext = rsa.encrypt(content, public_key)
            ciphertext_list.append(ciphertext)          
            i += encrypted_string_size
        print('Encrypted.')
        return ciphertext_list
    except:
        print('------ Encryption is failed. ------')
        traceback.print_exc()
        return None

def decrypt_ciphertext(ciphertext_list, private_key):
    plaintext_list = []        
    try:
        for ciphertext in ciphertext_list:
            content = rsa.decrypt(ciphertext, private_key)
            sub_str = content.decode()
            plaintext_list.append(sub_str)
        plaintext = ''.join(plaintext_list)
        print('Decrypted.')
        return plaintext
    except:
        print('------ Decryption is failed. ------')
        traceback.print_exc()
        return 'null'

def sign_plaintext(str, private_key):
    try:
        ciphertext = rsa.sign(str.encode(), private_key, 'SHA-256')
        print('Signed.')
        return ciphertext
    except:
        print('------ Signature is failed. ------')
        traceback.print_exc()
        return b'0'

def verify_signature(str, ciphertext, public_key):
    try:
        verified_result = rsa.verify(str.encode(), ciphertext, public_key)
        print('Verified.')
        return verified_result
    except:
        print('------ Verification is failed. ------')
        traceback.print_exc()
        return False


