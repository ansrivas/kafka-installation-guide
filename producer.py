from pykafka import KafkaClient


bootstrap_servers = '192.168.178.22:9092,192.168.178.20:9092'


def generate_data(msg, use_rdkafka=False):
    topic_name = b'test-topic'
    client = KafkaClient(hosts=bootstrap_servers)
    topic = client.topics[topic_name]
    producer = topic.get_producer(use_rdkafka=use_rdkafka)

    print "Publishing async messages !"
    # produce the message

    for x in xrange(0, 10):
        producer.produce(msg)

    # flush background queue
    producer.stop()
    print "Published Successfuly to: {0} \n".format(topic_name)

if __name__ == "__main__":

    # What else could it be ?
    msg = 'Hello World '

    # This calls the librdkafka .so which is very high performant !
    # After installing librdkafka, turn `use_rdkafka= True`
    # http://docs.confluent.io/3.0.0/installation.html#installation-apt

    rdkafka = False
    generate_data(msg, use_rdkafka=rdkafka)
