
from pykafka import KafkaClient

# ip of your brokers, check the ports as well
bootstrap_servers = '192.168.178.22:9092,192.168.178.20:9092'
zookeeper_connect = '192.168.178.22:2181,192.168.178.20:2181'


def consume_data(use_rdkafka=False):
    topic_name = b'test-topic'
    # Setup client
    client = KafkaClient(hosts=bootstrap_servers)
    print "Printing available topics: {0}".format(client.topics)
    topic = client.topics[topic_name]
    print "Printing offset info: {0}".format(topic.latest_available_offsets())

    try:

        # This is an example of very simple consumer

        consumer = topic.get_simple_consumer(use_rdkafka=use_rdkafka)
        for msg in consumer:
            if msg is not None:
                print "offset is: {0}".format(msg.offset)
                print "Msg received: {0}".format(msg.value)

        # The following is a more preferred balanced_consumer example

        # consumer = topic.get_balanced_consumer(consumer_group='Testing',
        #                                        auto_commit_enable=True,
        #                                        zookeeper_connect=zookeeper_connect)
        # while True:
        #     msg = consumer.consume()
        #     if msg is not None:
        #         print "offset is: {0}".format(msg.offset)
        #         print "Msg received: {0}".format(msg.value)

    except (KeyboardInterrupt, SystemExit):
        consumer.stop()
        print 'Successfuly terminated the consumer..\n'

if __name__ == "__main__":

    # if you have librdkafka installed, set it to True, will give a huge
    # performance boost
    rdkafka = False
    consume_data(use_rdkafka=rdkafka)
