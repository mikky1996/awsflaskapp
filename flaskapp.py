from flask import Flask, jsonify
from flask import request
from flask import abort
from threading import Lock
app = Flask(__name__)

lock = Lock()
queue = []

import sqlite3

@app.route('/')
def hello_world():
  return 'Flask server running on AWS!'

@app.route('/put/<msg>', methods=['GET'])
def put_in_queue(msg):
    with lock:
        queue.append(msg)
    return jsonify({'resp': "Message was put"}), 200

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

@app.route('/clear', methods=['GET'])
def clear_queue():
    with lock:
        del queue[:]
    return jsonify({'resp': "Queue was cleared"})

@app.route('/getEvents', methods=['GET'])
def getEvents():
    conn = sqlite3.connect('/home/ubuntu/flaskapp/compToIphone.db')
    c = conn.cursor()
    resp_list = []
    for (num, name, reason, icon, time) in c.execute('SELECT * FROM msgToIphone;'):
        resp_list.append({'name':name, 'reason':reason, 'icon':icon, 'time':time})
    return jsonify({'resp':resp_list}), 200

@app.route('/clearDB', methods=['GET'])
def clearDB():
    conn = sqlite3.connect('/home/ubuntu/flaskapp/compToIphone.db')
    c = conn.cursor()
    c.execute("DELETE FROM msgToIphone;")
    conn.commit()
    return jsonify({'resp':"table deleted"}), 200

@app.route('/postEvent', methods=['POST'])
def eventIncoming():
    conn = sqlite3.connect('/home/ubuntu/flaskapp/compToIphone.db')
    c = conn.cursor()
    d = request.json
    try:
        name = d['name']
        reason = d['reason']
        icon = d['icon']
        time = d['time']
    except:
        raise ValueError(str(d))
    c.execute('INSERT INTO msgToIphone (name, reason, icon, time) Values("{}", "{}", "{}", "{}");'.format(name, reason, icon, time))
    conn.commit()
    dbc = list(c.execute('SELECT * FROM msgToIphone;'))
    return jsonify({'resp': dbc}), 200


if __name__ == '__main__':
  app.run()
