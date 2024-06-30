import json
import logging
import datetime 
from Kafka_consumer import Kafka_consumer
from Kafka_producer import Kafka_producer




def main():
    consumer = Kafka_consumer(topic_name = ["weather_data_demo"])
    consumer.kafka_producer_conf(broker_address = "localhost:9092", 
                                 consumer_group = "weather_reader4solar",
                                 auto_offset_reset = "latest")


    producer = Kafka_producer(topic_name = "solar_energy_data", message_key = "solar_w")
    producer.kafka_producer_conf(broker_address = "localhost:9092")

    value = None
    while True:
        msg = consumer.consume(timeout = 1)

        if msg is None:
            print("Waiting....")   
        elif msg.error() is not None:
            raise Exception(msg.error())
        else:
            key = msg.key().decode("utf-8")
            value = json.loads(msg.value())
            offset = msg.offset()
            # logging.debug(f"{offset} {key} {value}")

            value = dict(value)
            solar_energy = get_solar_energy(value)
            producer.kafka_produce(message_value = solar_energy)
            logging.debug(f"{solar_energy}")
            
        
        if value:
            solar_energy = get_solar_energy(value)
            producer.kafka_produce(message_value = solar_energy)
            logging.debug(f"{solar_energy}")


if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()
