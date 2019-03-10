import rsa
import os
from server.commonFunctions import readFile, printToFile

def key_to_str(key: rsa.PrivateKey) -> str:
    return ' '.join(map(str, [key.n, key.e, key.d, key.p, key.q]))

def pub_key_to_str(pub_key: rsa.PublicKey) -> str:
    return ' '.join(map(str, [pub_key.n, pub_key.e]))

def keygen() -> None:
    pub_key, key = rsa.newkeys(512)
    printToFile(key_to_str(key), os.path.join("server", "key"))
    printToFile(pub_key_to_str(pub_key), os.path.join("server", "key.pub"))

def encrypt(message: str) -> str:
    pub_key = rsa.PublicKey(*map(int, readFile(os.path.join("server", "key.pub")).split()))
    hashed = str(rsa.encrypt(bytes(message, "utf-8"), pub_key).hex())
    return hashed

def decrypt(hashed: str) -> str:
    key = rsa.PrivateKey(*map(int, readFile(os.path.join("server", "key")).split()))
    message = str(rsa.decrypt(bytes.fromhex(hashed), key))[2:-1]
    return message

