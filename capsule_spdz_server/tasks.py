import os
import pickle
import redis
from syft.mpc.spdz.repo import MPCRepo

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)


def create_parties(key_id, data):
    # id = key_id
    repo = pickle.loads(data)
    server2 = MPCRepo()
    repo.set_parties(server2)
    server2.set_parties(repo)
    # save_siblings(id, conn, bob, sam)
    return pickle.dumps(repo)


def save_parties_ints(key_id, data):
    id = key_id
    repo = pickle.loads(data)
    server2 = repo.another_party[0]
    save_parties(id, conn, server2)
    return ('True')


def save_parties(id, conn, server2):
    conn.set(id + '_server2', server2.ints)
