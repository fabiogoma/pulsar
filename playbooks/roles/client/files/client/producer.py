import pulsar

client = pulsar.Client('pulsar://broker-1.europe.intranet:6650,broker-2.europe.intranet:6650,broker-3.europe.intranet:6650')

producer = client.create_producer('test')

for i in range(10):
    producer.send(('Hello-%d' % i).encode('utf-8'))

client.close()
