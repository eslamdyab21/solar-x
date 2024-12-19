import json
import logging
from Kafka_consumer import Kafka_consumer


def main():
    consumer = Kafka_consumer(topic_name = ["weather_processed"])
    consumer.kafka_consumer_conf(broker_address = "localhost:9092", 
                                 consumer_group = "weather_reader",
                                 auto_offset_reset = "earliest")

    while True:
        msg = consumer.consume(timeout = 1)
        if msg is None:
            # print("Waiting.....")
            pass    
        elif msg.error() is not None:
            raise Exception(msg.error())
        else:
            key = msg.key().decode("utf-8")
            value = json.loads(msg.value())
            offset = msg.offset()

            logging.debug(f"{offset} {key} {value}")


if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()
