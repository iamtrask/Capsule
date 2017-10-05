import zmq
import tasks
import json
from ast import literal_eval
# import logging

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://127.0.0.1:5001')

while True:
    try:
        task_data = socket.recv()
        task_data = literal_eval(task_data.decode('utf-8'))
        task = task_data.pop('task')
        task_kwargs = task_data.pop('task_kwargs')
        server_data = getattr(tasks, task)(**task_kwargs)
        socket.send(server_data)
    except Exception as e:
        print(e)

socket.close()
context.term()
