import pulsar
import sys
import signal
import configparser
import os
import datetime
import requests
import utils
import sys

logger = utils.generateLogger()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, utils.terminateProcess)

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
        except:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)

    client.close()
