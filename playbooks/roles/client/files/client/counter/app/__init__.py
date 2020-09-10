from flask import Flask, jsonify
from pymemcache.client import base

client = base.Client(('counter.europe.intranet', 11211))

app = Flask(__name__)

@app.route('/counter/in', methods=['PUT'])
def published_message():
    client.incr('published', 1)
    out = int(client.get('published').decode('utf-8'))
    return jsonify(total_published=out)

@app.route('/counter/out', methods=['PUT'])
def consumed_message():
    client.incr('consumed', 1)
    out = int(client.get('consumed').decode('utf-8'))
    return jsonify(total_consumed=out)

@app.route('/counter/total', methods=['GET'])
def total_message():
    total_published = 0
    total_consumed = 0

    total_published = int(client.get('published').decode('utf-8'))
    total_consumed = int(client.get('consumed').decode('utf-8'))

    total_message_dict = { "total_published": total_published, "total_consumed": total_consumed }

    return jsonify(total_messages=total_message_dict)

@app.route('/counter/reset', methods=['POST'])
def reset_message():
    client.set('published', '0')
    client.set('consumed', '0')

    total_published = int(client.get('published').decode('utf-8'))
    total_consumed = int(client.get('consumed').decode('utf-8'))

    total_message_dict = { "total_published": total_published, "total_consumed": total_consumed }

    return jsonify(total_messages=total_message_dict)
