import zmq
from ast import literal_eval
import pickle
import argparse
import importlib


def create_payload(data, success=True):
    output = {
        'success': success,
        'payload': data
    }
    return pickle.dumps(output)


def main(args):
    tasks = importlib.import_module(args.type + '_' + 'tasks')

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:' + args.port)
    print(args.type.upper() + " Server is listening on 127.0.0.1:" + args.port)

    while True:
        try:
            task_data = socket.recv()
            task_data = literal_eval(task_data.decode('utf-8'))
            task = task_data.pop('task')
            task_kwargs = task_data.pop('task_kwargs')
            server_data = getattr(tasks, task)(**task_kwargs)

            socket.send(create_payload(server_data))

        except Exception as e:
            print("Encountered exception: ", e)
            socket.send(create_payload(e, False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Local Capsule Server")
    parser.add_argument(
        '--type',
        required=True,
        type=str,
        help="Type of tasks to be processed.",
        choices=['mpc', 'zmq']
    )
    parser.add_argument(
        '--port',
        help="Port for the listening socket.",
        default='5002'
    )

    args = parser.parse_args()

    main(args)
