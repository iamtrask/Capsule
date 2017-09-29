from syft.he.paillier.keys import KeyPair, PublicKey
import syft
import redis, os, requests, random
import zmq, json

class LocalCapsuleClient():

    def __init__(self,host='127.0.0.1',port='5000'):
        self.host = host
        self.port = port
        ctx = zmq.Context()
        self.task_socket = ctx.socket(zmq.REQ)
        self.task_socket.connect('tcp://127.0.0.1:5001')


    def keygen(self,scheme='paillier'):
        id = str(random.randint(0,2**32))
        task_kwargs = {
            "id": id,
            "scheme": scheme,
        }
        self.task_socket.send_string(str({"task":"create_keys", "task_kwargs":task_kwargs}))
        r = self.task_socket.recv()
        pk = PublicKey.deserialize(r)
        pk.id = id
        return pk

    def bootstrap(self,x,id=None):
        if(id is None):
            id = x.public_key.id
        data = x.serialize()
        task_kwargs = {
            "key_id": id,
            "data": data,
        }
        self.task_socket.send_string(str({"task":"bootstrap", "task_kwargs":task_kwargs }))
        r = self.task_socket.recv()
        return syft.tensor.TensorBase.deserialize(r)

    def decrypt(self,x,id=None):
        if(id is None):
            id = x.public_key.id
        data = x.serialize()
        task_kwargs = {
            "key_id": id,
            "data": data,
        }
        self.task_socket.send_string(str({"task":"decrypt", "task_kwargs":task_kwargs }))
        r = self.task_socket.recv()
        try:
            out = syft.tensor.TensorBase.deserialize(r)
        except:
            out = float(r.content)
        return out
