from syft.he.paillier.keys import KeyPair
from syft.he.keys import Paillier
import syft as sy
# from flask import Flask, request, Response
import redis, os, pickle


redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)
# app = Flask(__name__)

# @app.route('/keygen/<id>/<scheme>')
def create_keys(id,scheme):
    if(scheme == 'paillier'):
        pk,sk = Paillier()
        save_keys(conn,id,pk,sk)
        return pk.serialize()
    else:
        return "Unknown Scheme:" + str(scheme)

# @app.route('/bootstrap/<key_id>',methods=['POST'])
def bootstrap(key_id, data):
    cyphertext = sy.tensor.TensorBase.deserialize(data)
    pk,sk = get_keys(key_id)
    plaintext = cyphertext.decrypt(sk)
    clean_cyphertext = plaintext.encrypt(pk)
    return clean_cyphertext.serialize()

# @app.route('/decrypt/<key_id>',methods=['POST'])
def decrypt(key_id, data):
    cyphertext = sy.tensor.TensorBase.deserialize(data)
    pk,sk = get_keys(key_id)
    plaintext = cyphertext.decrypt(sk)
    try:
        b = plaintext.serialize()
    except:
        b = str(plaintext)
    return b

def save_keys(conn,id,pk,sk):
    conn.set(id+'_public',pk.serialize())
    conn.set(id+'_private',sk.serialize())

def get_keys(id):
    pk_bin = conn.get(id+'_public')
    sk_bin = conn.get(id+'_private')
    pk,sk = KeyPair().deserialize(pk_bin,sk_bin)
    return (pk,sk)
