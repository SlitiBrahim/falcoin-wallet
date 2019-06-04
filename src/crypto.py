import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii

def generate_private_key():
    random_generator = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_generator)

    return private_key

def generate_key_pair():
    private_key = generate_private_key()
    public_key = private_key.publickey()

    return key_to_hex(private_key), key_to_hex(public_key)

def key_to_hex(key):
    return binascii.hexlify(key.exportKey(format='DER')).decode('ascii')

def sign_message(message, private_key_str):
    private_key = RSA.importKey(binascii.unhexlify(private_key_str))
    h = SHA.new(message.encode('utf8'))
    signer = PKCS1_v1_5.new(private_key)

    return binascii.hexlify(signer.sign(h)).decode('ascii')

def verify_signature(sig, msg, public_key_str):
    public_key = RSA.importKey(binascii.unhexlify(public_key_str))
    verifier = PKCS1_v1_5.new(public_key)
    str_hash = SHA.new(msg.encode('utf8'))

    return verifier.verify(str_hash, binascii.unhexlify(sig))
