import pulsar
import uuid
import sys
import signal
import time
import configparser
import os

counter = 1
messages_per_second = 0

def terminateProcess(signalNumber, frame):
    print()
    print("Exiting gracefully. {} messages sent".format(str(counter * messages_per_second)))
    sys.exit()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, terminateProcess)

    config = configparser.ConfigParser()
    config.read_file(open("{}/config.ini".format(os.path.dirname(__file__))))

    broker_address = config['default'].get('broker_address')
    topic_name  = config['default'].get('topic_name')
    messages_per_second = config['default'].getint('messages_per_second')

    client = pulsar.Client(service_url=broker_address, operation_timeout_seconds=500)
    producer = client.create_producer(topic=topic_name, send_timeout_millis=500000, max_pending_messages=10000)

    while True:
        for i in range(messages_per_second):
            try:
                producer.send(str(uuid.uuid4()).encode('utf-8'))
            except KeyboardInterrupt:
                print("Exiting gracefully. {} messages sent".format(str(counter * messages_per_second)))
                sys.exit()
            except:
                print('Message send failure')
        time.sleep(1)
        counter += 1

    client.close()
