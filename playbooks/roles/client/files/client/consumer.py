import pulsar
import sys
import signal
import configparser
import os
import datetime

counter = 0

def terminateProcess(signalNumber, frame):
    print("\nExiting gracefully. {} messages were succesfully consumed".format(str(counter)))
    sys.exit()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, terminateProcess)

    config = configparser.ConfigParser()
    config.read_file(open("{}/config.ini".format(os.path.dirname(__file__))))

    broker_address = config['default'].get('broker_address')
    topic_name  = config['default'].get('topic_name')
    messages_per_second = config['default'].getint('messages_per_second')

    client = pulsar.Client(broker_address)

    consumer = client.subscribe(topic_name, 'python-subscription')

    while True:
        msg = consumer.receive()
        try:
            print("Received message data='{}' publish_time='{}'".format(msg.data().decode('utf-8'), datetime.datetime.fromtimestamp(msg.publish_timestamp() / 1000.0)))
            # Acknowledge successful processing of the message
            consumer.acknowledge(msg)
            counter += 1
        except:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)

    client.close()
