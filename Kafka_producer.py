import json
from quixstreams import Application

class Kafka_producer():
    def __init__(self, topic_name, message_key):
        self.topic_name = topic_name
        self.message_key = message_key




    def kafka_producer_conf(self, broker_address):
        self.app = Application(
            broker_address = broker_address,
            loglevel = "DEBUG",
        )
    

    def kafka_produce(self, message_value):
        with self.app.get_producer() as producer:
            producer.produce(
                topic = self.topic_name,
                key = self.message_key,
                value = json.dumps(message_value),
            )

        