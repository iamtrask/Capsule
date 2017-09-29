from syft.he.paillier.keys import KeyPair, PublicKey
import syft
import redis, os, requests, random

class LocalCapsuleClient():

    def __init__(self,host='127.0.0.1',port='5000'):
        self.host = host
        self.port = port

    def keygen(self,scheme='paillier'):
        id = str(random.randint(0,2**32))
        r = requests.get('http://'+self.host+':'+self.port+'/keygen/'+id+'/'+scheme)
        print(r.content)
        pk = PublicKey.deserialize(r.content)
        pk.id = id
        return pk

    def bootstrap(self,x,id=None):
        if(id is None):
            id = x.public_key.id
        r = requests.post('http://'+self.host+':'+self.port+"/bootstrap/"+str(id), data=x.serialize())
        return syft.tensor.TensorBase.deserialize(r.content)

    def decrypt(self,x,id=None):

        if(id is None):
            id = x.public_key.id
        r = requests.post('http://'+self.host+':'+self.port+"/decrypt/"+str(id), data=x.serialize())
        try:
            out = syft.tensor.TensorBase.deserialize(r.content)
        except:
            out = float(r.content)
        return out
