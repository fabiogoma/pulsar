import pulsar
import sys
import signal
import configparser
import os
import datetime
import requests

def terminateProcess(signalNumber, frame):
    print("")
    print("Exiting gracefully")
    sys.exit()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, terminateProcess)

    config = configparser.ConfigParser()
    config.read_file(open("{}/config.ini".format(os.path.dirname(__file__))))

    broker_address = config['default'].get('broker_address')
    topic_name  = config['default'].get('topic_name')
    messages_per_second = config['default'].getint('messages_per_second')
    counter_url = "{}/counter/out".format(config['default'].get('counter_url'))

    client = pulsar.Client(service_url=broker_address, operation_timeout_seconds=500)

    consumer = client.subscribe(topic=topic_name, subscription_name='python-subscription', consumer_type=pulsar._pulsar.ConsumerType.Shared)

    while True:
        msg = consumer.receive()
        try:
            print("Received message data='{}' publish_time='{}'".format(msg.data().decode('utf-8'), datetime.datetime.fromtimestamp(msg.publish_timestamp() / 1000.0)))
            # Acknowledge successful processing of the message
            consumer.acknowledge(msg)
            requests.put(counter_url)
        except:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)

    client.close()
