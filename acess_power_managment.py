import json
import logging
import random
from Kafka_consumer import Kafka_consumer
from Kafka_producer import Kafka_producer
from bms import BMS

prev_home_consumption = None
def access_power_managment(key, value, bms):
    global prev_home_consumption

    if key == 'home_energy':
        prev_home_consumption = value

    elif prev_home_consumption != None:
        access_power_w = value['current_consumption_w'] - prev_home_consumption['current_consumption_w']

        if access_power_w > 0:
            access_power_from_batteries = bms.charge_batteries(round(access_power_w,2))

            if access_power_from_batteries:
                # charge the national grid
                pass

        else:
            negative_access_power_from_batteries = bms.consume_batteries(-1*access_power_w)

            if negative_access_power_from_batteries:
                # consume from the national grid
                pass


def main():

    consumer = Kafka_consumer(topic_name = ["solar_energy_data", "home_energy_consumption"])
    consumer.kafka_consumer_conf(broker_address = "localhost:9092", 
                                 consumer_group = "battery_proccessing",
                                 auto_offset_reset = "latest")

    producer = Kafka_producer(topic_name = "battery_data", message_key = "bms")
    producer.kafka_producer_conf(broker_address = "localhost:9092")

    bms = BMS()
    while True:
        msg = consumer.consume(timeout = 0.5)
        if msg is None:
            # print("Waiting....")
            pass    
        elif msg.error() is not None:
            raise Exception(msg.error())
        else:
            key = msg.key().decode("utf-8")
            value = json.loads(msg.value())
            offset = msg.offset()

            access_power_managment(key, dict(value), bms)

            msg = bms.batteries_status.copy()
            msg['time_stamp'] = value['time_stamp']

            producer.kafka_produce(message_value = msg)
            logging.debug(f"{msg}")

            # logging.debug(f"{offset} {key} {value}")
            logging.debug("-------------------------------------------------")



if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()
