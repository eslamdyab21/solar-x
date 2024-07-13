import json
import logging
import random
from Kafka_consumer import Kafka_consumer
from Kafka_producer import Kafka_producer


prev_home_consumption = None
batteries_status = {}


def load_batteries_info():
    global batteries_status

    with open('home_configurations.json') as f:
        HOME_CONFIGURATIONS = json.load(f)

    i = 1
    for battery_capacity in HOME_CONFIGURATIONS['batteries_capacity_kwh']:
        battery_name = 'battery_' + str(i)
        if battery_name not in batteries_status:
            batteries_status[battery_name] = {"capacity_kwh": battery_capacity, 
                                             "max_charge_speed_w": HOME_CONFIGURATIONS['batteries_charge_max_speed_w_second'][i-1],
                                             "current_energy_wh":battery_capacity*1000,
                                             "is_charging":0}
            i +=1


def charge_batteries(access_power_w, last_battery_charged = None):
    global batteries_status

    min_energy_battery = 'battery_1'
    min_energy = batteries_status[min_energy_battery]['current_energy_wh']
    full_charged_counter = 0
    loss = 1 - random.randint(850,1000)/1000


    for battery in batteries_status.keys():
        if int(batteries_status[battery]['current_energy_wh']) == batteries_status[battery]['capacity_kwh']*1000:
            full_charged_counter += 1

        if batteries_status[battery]['current_energy_wh'] < min_energy and battery != last_battery_charged:
            min_energy = batteries_status[battery]['current_energy_wh']
            min_energy_battery = battery

    if min_energy_battery == last_battery_charged or full_charged_counter == len(batteries_status.keys()):
        return

    if access_power_w > batteries_status[min_energy_battery]['max_charge_speed_w']:
        access = access_power_w - batteries_status[min_energy_battery]['max_charge_speed_w']

        access_power_w = batteries_status[min_energy_battery]['max_charge_speed_w']
        batteries_status[min_energy_battery]['current_energy_wh'] += access_power_w - loss*access_power_w
        batteries_status[min_energy_battery]['current_energy_wh'] = round( batteries_status[min_energy_battery]['current_energy_wh'] , 2)
        batteries_status[min_energy_battery]['is_charging'] = 1

        if batteries_status[min_energy_battery]['current_energy_wh'] > batteries_status[min_energy_battery]['capacity_kwh']*1000:
            batteries_status[min_energy_battery]['current_energy_wh'] = batteries_status[min_energy_battery]['capacity_kwh']*1000
            batteries_status[min_energy_battery]['is_charging'] = 0
        
        charge_batteries(access_power_w = round(access,2), last_battery_charged = min_energy_battery)

    else:
        batteries_status[min_energy_battery]['current_energy_wh'] += access_power_w - loss*access_power_w
        batteries_status[min_energy_battery]['current_energy_wh'] = round(batteries_status[min_energy_battery]['current_energy_wh'] , 2)
        batteries_status[min_energy_battery]['is_charging'] = 1

        if batteries_status[min_energy_battery]['current_energy_wh'] > batteries_status[min_energy_battery]['capacity_kwh']*1000:
            batteries_status[min_energy_battery]['current_energy_wh'] = batteries_status[min_energy_battery]['capacity_kwh']*1000
            batteries_status[min_energy_battery]['is_charging'] = 0



def consume_batteries(access_power_w):
    pass


def bms(key, value):
    global prev_home_consumption, batteries_status

    if key == 'home_energy':
        prev_home_consumption = value
    elif prev_home_consumption != None:
        access_power_w = value['current_consumption_w'] - prev_home_consumption['current_consumption_w']
        if access_power_w > 0:
            charge_batteries(round(access_power_w,2))
        else:
            consume_batteries(-1*access_power_w)


def main():
    global batteries_status

    consumer = Kafka_consumer(topic_name = ["solar_energy_data", "home_energy_consumption"])
    consumer.kafka_consumer_conf(broker_address = "localhost:9092", 
                                 consumer_group = "battery_proccessing",
                                 auto_offset_reset = "latest")

    producer = Kafka_producer(topic_name = "battery_data", message_key = "bms")
    producer.kafka_producer_conf(broker_address = "localhost:9092")

    load_batteries_info()

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

            bms(key, dict(value))
            msg = batteries_status.copy()
            msg['time_stamp'] = value['time_stamp']

            producer.kafka_produce(message_value = msg)
            logging.debug(f"{msg}")

            # logging.debug(f"{offset} {key} {value}")
            logging.debug("-------------------------------------------------")


if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()
