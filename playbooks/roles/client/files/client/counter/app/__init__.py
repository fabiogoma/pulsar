from flask import Flask, jsonify
from multiprocessing import Value

published = Value('i', 0)
consumed = Value('i', 0)
app = Flask(__name__)

@app.route('/counter/in', methods=['PUT'])
def published_message():
    with published.get_lock():
        published.value += 1
        out = published.value
    return jsonify(total_published=out)

@app.route('/counter/out', methods=['PUT'])
def consumed_message():
    with consumed.get_lock():
        consumed.value += 1
        out = consumed.value
    return jsonify(total_consumed=out)

@app.route('/counter/total', methods=['GET'])
def total_message():
    total_published = 0
    total_consumed = 0

    with published.get_lock():
        total_published = published.value

    with consumed.get_lock():
        total_consumed = consumed.value

    total_message_dict = { "total_published": total_published, "total_consumed": total_consumed }

    return jsonify(total_messages=total_message_dict)

@app.route('/counter/reset', methods=['POST'])
def reset_message():
    total_published = 0
    total_consumed = 0

    with published.get_lock():
        published.value = total_published

    with consumed.get_lock():
        consumed.value = total_consumed

    total_message_dict = { "total_published": total_published, "total_consumed": total_consumed }

    return jsonify(total_messages=total_message_dict)
