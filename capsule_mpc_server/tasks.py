# from flask import Flask, request, Response
import os
import pickle
import redis
from syft.mpc.rss import MPCRepo

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)


def create_siblings(key_id, data):
    # id = key_id
    repo = pickle.loads(data)
    bob = MPCRepo()
    sam = MPCRepo()
    bob.set_siblings(repo, sam)
    repo.set_siblings(sam, bob)
    sam.set_siblings(bob, repo)
    # save_siblings(id, conn, bob, sam)
    return pickle.dumps(repo)


def save_ints(key_id, data):
    id = key_id
    repo = pickle.loads(data)
    bob = repo.siblings[0]
    sam = repo.siblings[1]
    save_siblings(id, conn, bob, sam)
    return ('True')


def save_siblings(id, conn, bob, sam):
    conn.set(id + '_bob', bob.ints)
    conn.set(id + '_sam', sam.ints)
