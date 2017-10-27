# from flask import Flask, request, Response
import os
import pickle
import redis
from syft.mpc.rss import MPCRepo as RSSMPCRepo
from syft.mpc.spdz import MPCRepo as SPDZMPCRepo

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)


def create_siblings(key_id, data):
    repo = pickle.loads(data)
    bob = RSSMPCRepo()
    sam = RSSMPCRepo()
    bob.set_siblings(repo, sam)
    repo.set_siblings(sam, bob)
    sam.set_siblings(bob, repo)
    return pickle.dumps(repo)


def create_parties(key_id, data):
    repo = pickle.loads(data)
    bob = SPDZMPCRepo()
    bob.set_parties(repo)
    repo.set_parties(bob)

    return pickle.dumps(repo)


def save_ints(key_id, data):
    id = key_id
    repo = pickle.loads(data)
    bob = repo.siblings[0]
    sam = repo.siblings[1]
    save_siblings(id, conn, bob, sam)
    return ('True')


def save_ints_spdz(key_id, data):
    id = key_id
    repo = pickle.loads(data)
    bob = repo.another_party[0]
    conn.set(id + '_bob', bob.ints)
    return ('True')


def save_siblings(id, conn, bob, sam):
    conn.set(id + '_bob', bob.ints)
    conn.set(id + '_sam', sam.ints)
