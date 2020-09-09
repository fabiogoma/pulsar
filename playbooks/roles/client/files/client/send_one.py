import pulsar
import uuid
import configparser
import os

config = configparser.ConfigParser()
config.read_file(open("{}/config.ini".format(os.path.dirname(__file__))))

broker_address = config['default'].get('broker_address')
topic_name  = config['default'].get('topic_name')
messages_per_second = config['default'].getint('messages_per_second')
counter_url = "{}/counter/in".format(config['default'].get('counter_url'))

client = pulsar.Client(service_url=broker_address, operation_timeout_seconds=500)
producer = client.create_producer(topic=topic_name, send_timeout_millis=500000, max_pending_messages=10000)

producer.send(str(uuid.uuid4()).encode('utf-8'))
requests.put(counter_url)

client.close()