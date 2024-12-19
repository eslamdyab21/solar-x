import json
from quixstreams import Application

class Kafka_producer():
    def __init__(self, topic_name, message_key):
        self.topic_name = topic_name
        self.message_key = message_key
        self.make_producer_on_starting = True




    def kafka_producer_conf(self, broker_address):
        self.app = Application(
            broker_address = broker_address,
            loglevel = "DEBUG",
        )
    

    def kafka_produce(self, message_value):
        if self.make_producer_on_starting:
            self.producer = self.app.get_producer()
            self.make_producer_on_starting = False
        
        self.producer.produce(
            topic = self.topic_name,
            key = self.message_key,
            value = json.dumps(message_value),
        )

        