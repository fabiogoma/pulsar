import pulsar

client = pulsar.Client('pulsar://broker-1.europe.intranet:6650,broker-2.europe.intranet:6650,broker-3.europe.intranet:6650')

consumer = client.subscribe('test', 'python-subscription')

while True:
    msg = consumer.receive()
    try:
        print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()