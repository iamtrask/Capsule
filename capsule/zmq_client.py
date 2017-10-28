from syft.he.paillier.keys import PublicKey
import syft
import random
import zmq
import pickle


class LocalCapsuleClient():

    def __init__(self, host='127.0.0.1', port='5000'):
        self.host = host
        self.port = port
        ctx = zmq.Context()
        self.task_socket = ctx.socket(zmq.REQ)
        self.task_socket.connect('tcp://127.0.0.1:5002')

    def keygen(self, scheme='paillier'):
        id = str(random.randint(0, 2**32))
        task_kwargs = {
            "id": id,
            "scheme": scheme,
        }
        self.task_socket.send_string(str({
            "task": "create_keys",
            "task_kwargs": task_kwargs
        }))
        r = self.task_socket.recv()
        pk = PublicKey.deserialize(r)
        pk.id = id
        return pk

    def bootstrap(self, x, id=None):
        if(id is None):
            id = x.public_key.id
        data = x.serialize()
        task_kwargs = {
            "key_id": id,
            "data": data,
        }
        self.task_socket.send_string(str({
            "task": "bootstrap",
            "task_kwargs": task_kwargs
        }))
        r = self.task_socket.recv()
        return syft.tensor.TensorBase.deserialize(r)

    def decrypt(self, x, id=None):
        if(id is None):
            id = x.public_key.id
        data = x.serialize()
        task_kwargs = {
            "key_id": id,
            "data": data,
        }
        self.task_socket.send_string(str({
            "task": "decrypt",
            "task_kwargs": task_kwargs
        }))
        r = self.task_socket.recv()
        try:
            # print("Hello.........................")
            out = syft.tensor.TensorBase.deserialize(r)
        except Exception as e:
            # print("Hello.........................")
            print(e)
            out = float(r)
        return out


class MPCCapsuleClient():
    def __init__(self, repo):
        self.id = str(random.randint(0, 2**32))
        self.repo = repo
        ctx = zmq.Context()
        self.task_socket = ctx.socket(zmq.REQ)
        self.task_socket.connect('tcp://127.0.0.1:5003')

    def create_siblings(self):
        data = pickle.dumps(self.repo)
        task_kwargs = {
            "key_id": self.id,
            "data": data,
        }
        self.task_socket.send_string(str({
            "task": "create_siblings",
            "task_kwargs": task_kwargs
        }))
        r = self.task_socket.recv()
        self.repo1 = pickle.loads(r)
        return self.repo1

    def save(self, repo1):
        data = pickle.dumps(repo1)
        task_kwargs = {
            "key_id": self.id,
            "data": data,
        }
        self.task_socket.send_string(str({
            "task": "save_ints",
            "task_kwargs": task_kwargs
        }))
        # r = self.task_socket.recv()
        self.task_socket.recv()
        return True

class SPDZCapsuleClient():
    def __init__(self, repo):
        self.id = str(random.randint(0, 2**32))
        self.repo = repo
        ctx = zmq.Context()
        self.task_socket = ctx.socket(zmq.REQ)
        self.task_socket.connect('tcp://127.0.0.1:5005')

    def create_parties(self):
        data = pickle.dumps(self.repo)
        task_kwargs = {
            "key_id": self.id,
            "data": data,
        }
        self.task_socket.send_string(str({
            "task": "create_parties",
            "task_kwargs": task_kwargs
        }))
        r = self.task_socket.recv()
        self.repo1 = pickle.loads(r)
        return self.repo1

    def save(self, repo1):
        data = pickle.dumps(repo1)
        task_kwargs = {
            "key_id": self.id,
            "data": data,
        }
        self.task_socket.send_string(str({
            "task": "save_parties_ints",
            "task_kwargs": task_kwargs
        }))
        # r = self.task_socket.recv()
        self.task_socket.recv()
        return True
