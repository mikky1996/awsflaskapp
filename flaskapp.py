from flask import Flask, jsonify
from threading import Lock
app = Flask(__name__)

lock = Lock()
queue = []

@app.route('/')
def hello_world():
  return 'Flask server running on AWS!'

@app.route('/put/<msg>', methods=['GET'])
def put_in_queue(msg):
    with lock:
        queue.append(msg)
    return jsonify({'resp': "Message was put"})

@app.route('/queue', methods=['GET'])
def get_the_queue():
    with lock:
        q = queue
    return jsonify({'queue': q})

@app.route('/pop', methods=['GET'])
def pop_the_queue():
    with lock:
        if len(queue) != 0:
            queue.pop(0)
    return jsonify({'resp': "Message was popped"})

if __name__ == '__main__':
  app.run()
