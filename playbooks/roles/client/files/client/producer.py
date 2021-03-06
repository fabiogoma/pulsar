import pulsar
import uuid
import sys
import signal
import time
import configparser
import os
import requests
import utils
import sys

logger = utils.generateLogger()
counter_url = ''

def Callback(res, msg_id):
    if res == pulsar._pulsar.Result.Ok:
        try:
            requests.put(counter_url)
        except OSError as osError:
            logger.info("OS Error: {0}".format(osError))
        except requests.exceptions.HTTPError as httpError:
            logger.info("Http Error: {0}".format(httpError))
        except requests.exceptions.Timeout as timeout:
            logger.info("Timeout Error: {0}".format(timeout))
        except requests.exceptions.ConnectionError as connectionError:
            logger.info("Connection Error: {0}".format(connectionError))
        except requests.exceptions.RequestException as requestException:
            logger.info("Request Exception: {0}".format(requestException))

if __name__ == '__main__':

    signal.signal(signal.SIGINT, utils.terminateProcess)

    config = configparser.ConfigParser()
    config.read_file(open("{}/config.ini".format(os.path.dirname(__file__))))

    broker_address = config['default'].get('broker_address')
    topic_name  = config['default'].get('topic_name')
    messages_per_second = config['default'].getint('messages_per_second')
    counter_url = "{}/counter/in".format(config['default'].get('counter_url'))

    client = pulsar.Client(service_url=broker_address, operation_timeout_seconds=500)
    producer = client.create_producer(topic=topic_name, send_timeout_millis=0, producer_name="python-producer", max_pending_messages=10000)

    while True:
        for i in range(messages_per_second):
            producer.send_async(str(uuid.uuid4()).encode('utf-8'), Callback)
        time.sleep(1)

    client.close()
