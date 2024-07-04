from quixstreams import Application

class Kafka_consumer():
    def __init__(self, topic_name):
        self.topic_name = topic_name

        

    def kafka_consumer_conf(self, broker_address, consumer_group, auto_offset_reset):
        self.app = Application(
            broker_address = broker_address,
            loglevel = "DEBUG",
            consumer_group = consumer_group,
            auto_offset_reset = auto_offset_reset
        )

        self.consumer = self.app.get_consumer()
        self.consumer.subscribe(self.topic_name)

    
    def consume(self, timeout, store_offset = False):

        msg = self.consumer.poll(timeout)
        if msg and store_offset:
            self.consumer.store_offsets(msg)

        return msg