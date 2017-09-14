from django.shortcuts import render
from django.http import HttpResponse
from syft.he.paillier.keys import KeyPair
from syft.he.keys import Paillier
import syft as sy
import redis, os, pickle
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)


def save_keys(conn, id, pk, sk):
    conn.set(id + '_public', pk.serialize())
    conn.set(id + '_private', sk.serialize())


def get_keys(id):
    pk_bin = conn.get(id + '_public')
    sk_bin = conn.get(id + '_private')
    pk, sk = KeyPair().deserialize(pk_bin, sk_bin)
    return (pk, sk)

@csrf_exempt
def keygen(request, id, scheme):
    # id: url
    # scheme: url

    if (scheme == 'paillier'):
        pk, sk = Paillier()
        save_keys(conn, id, pk, sk)
        serialized = pk.serialize()
        print('Type is ', type(serialized))
        return HttpResponse(serialized)
    else:
        return HttpResponse("Unknown Scheme:" + str(scheme))

@csrf_exempt
def bootstrap(request, key_id=None):
    # id: url
    # data: post
    if key_id:
        cyphertext = sy.tensor.TensorBase.deserialize(request.body)
        pk, sk = get_keys(key_id)
        plaintext = cyphertext.decrypt(sk)
        try:
            b = plaintext.serialize()
        except:
            b = str(plaintext)
        return HttpResponse(b)
    else:
        return HttpResponse('No Key ID')

@csrf_exempt
def decrypt(request, key_id=None):
    # id: url
    # data: post
    if key_id:
        print(request.body)
        cyphertext = sy.tensor.TensorBase.deserialize(request.body)
        pk, sk = get_keys(key_id)
        plaintext = cyphertext.decrypt(sk)
        try:
            b = plaintext.serialize()
        except:
            b = str(plaintext)

        return HttpResponse(b)
    else:
        return HttpResponse('No Key Id')
