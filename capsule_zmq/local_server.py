import zmq
import tasks
import json
from ast import literal_eval

# import logging

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://0.0.0.0:5002')
print("Running server at //0.0.0.0:5002")




try:
    while True:
        task_data = socket.recv()
        task_data = literal_eval(task_data.decode('utf-8'))
        task = task_data.pop('task')
        task_kwargs = task_data.pop('task_kwargs')
        server_data = getattr(tasks, task)(**task_kwargs)
        if type(server_data) != bytes:
            socket.send_string(server_data)
        else:
            socket.send(server_data)
except Exception as e:
    print(e)



socket.close()
context.term()
