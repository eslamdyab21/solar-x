import json
import logging
import random
from dotenv import load_dotenv
import os
from Kafka_consumer import Kafka_consumer
from Kafka_producer import Kafka_producer
from bms import BMS


def access_power_management(solar_msg, home_msg, bms):

    access_power_w = solar_msg['current_consumption_w'] - home_msg['current_consumption_w']

    if access_power_w > 0:
        access_power_from_batteries = bms.charge_batteries(round(access_power_w,2))

        if access_power_from_batteries:
            # charge the national grid
            pass

    else:
        negative_access_power_from_batteries = bms.discharge_batteries(-1*access_power_w)

        if negative_access_power_from_batteries:
            # consume from the national grid
            pass


solar_energy_stack = []
home_energy_stack  = []
def data_of_same_second(key, msg, bms):

    if key == "solar_w":
        current_solar_msg = msg

        if len(home_energy_stack) == 0:
            solar_energy_stack.append(current_solar_msg)
            return False
        
        last_home_energy_msg = home_energy_stack[-1]

        if current_solar_msg["time_stamp"] == last_home_energy_msg["time_stamp"]:
            del home_energy_stack[-1]

            access_power_management(current_solar_msg, last_home_energy_msg, bms) 
            return True

        else:
            solar_energy_stack.append(current_solar_msg)
            return False


    elif key == "home_energy":
        current_home_msg = msg

        if len(solar_energy_stack) == 0:
            home_energy_stack.append(current_home_msg)
            return False
        
        last_solar_msg = solar_energy_stack[-1]

        if current_home_msg["time_stamp"] == last_solar_msg["time_stamp"]:
            del solar_energy_stack[-1]

            access_power_management(last_solar_msg, current_home_msg, bms)
            return True
        
        else:
            home_energy_stack.append(current_home_msg)
            return False




def main():
    load_dotenv()
    KAFKA_BROKER_ADDRESS = os.getenv('KAFKA_BROKER_ADDRESS')

    consumer = Kafka_consumer(topic_name = ["solar_energy_data", "home_energy_consumption"])
    consumer.kafka_consumer_conf(broker_address = KAFKA_BROKER_ADDRESS, 
                                 consumer_group = "battery_proccessing",
                                 auto_offset_reset = "latest")

    producer = Kafka_producer(topic_name = "battery_data", message_key = "bms")
    producer.kafka_producer_conf(broker_address = KAFKA_BROKER_ADDRESS)

    bms = BMS()
    while True:
        msg = consumer.consume(timeout = 1.0)

        if msg is None:
            print("Waiting....")
            pass    

        elif msg.error() is not None:
            raise Exception(msg.error())
        
        else:
            key = msg.key().decode("utf-8")
            value = json.loads(msg.value())
            offset = msg.offset()

            logging.debug(f"{offset} {key} {value}")

            if data_of_same_second(key, dict(value), bms):
                # access_power_managment(key, dict(value), bms)

                msg = bms.batteries_status.copy()
                msg['time_stamp'] = value['time_stamp']

                producer.kafka_produce(message_value = msg)
                logging.debug(f"{msg}")

                # logging.debug(f"{offset} {key} {value}")
                logging.debug("-------------------------------------------------")



if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()
