import datetime
import logging
import random
import json
import time
from Kafka_producer import Kafka_producer


consumption_acumm = 0
current_consumption = 0
power_w_accumulated_hourly = 0
prev_hour = 0
power_w_accumulated_hourly_set = {"00":0,"01":0,"02":0,"03":0,"04":0,"05":0,"06":0,"07":0,
    "08":0,"09":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,
    "21":0,"22":0,"23":0}


def load_home_load():
    with open('home_appliances_consumption.json') as f:
        HOME_USAGE_POWER = json.load(f)

    return HOME_USAGE_POWER


def get_time_in_seconds(t):
    hours = int(t.split(':')[0])*3600
    minutes = int(t.split(':')[1])*60

    return hours + minutes 


def get_power_w_accumulated_hourly(current_hour, current_total_consumption):
    global prev_hour, power_w_accumulated_hourly

    if current_hour == prev_hour:
        power_w_accumulated_hourly += current_total_consumption
    else:
        power_w_accumulated_hourly = 0

    power_w_accumulated_hourly_set[current_hour] = round(power_w_accumulated_hourly,2)

    prev_hour = current_hour


def home_energy_usage_per_second(HOME_USAGE_POWER):
    global consumption_acumm, current_consumption
    current_total_consumption = 0

    time_stamp = str(datetime.datetime.now().replace(microsecond=0))
    current_time = get_time_in_seconds(time_stamp.split()[1])
    

    for appliance in HOME_USAGE_POWER.keys():
        for time_interval in HOME_USAGE_POWER[appliance]['time'].split(','):
            start_time = get_time_in_seconds(time_interval.split('-')[0])
            end_time = get_time_in_seconds(time_interval.split('-')[1])
            
            if current_time > start_time and current_time < end_time:
                consumption_low = HOME_USAGE_POWER[appliance]['consumption'][0] / 3600
                consumption_high = HOME_USAGE_POWER[appliance]['consumption'][1] / 3600
                current_consumption = (random.randint(800,1000)/1000) * (consumption_low + consumption_high) / 2
                current_total_consumption += current_consumption
                consumption_acumm += current_consumption
                break

    current_total_consumption = round(current_total_consumption,2)
    consumption_acumm = round(consumption_acumm,2)

    current_hour = time_stamp.split()[1].split(':')[0]
    get_power_w_accumulated_hourly(current_hour, current_total_consumption)

    energy_consumption = {'time_stamp':time_stamp, 'current_consumption_w':current_total_consumption, 
                          'consumption_accumulated_w':consumption_acumm, 'current_consumption_w_accumulated_hourly':power_w_accumulated_hourly_set}

    return energy_consumption



def main():
    producer = Kafka_producer(topic_name = "home_energy_consumption", message_key = "home_energy") 
    producer.kafka_producer_conf(broker_address = "localhost:9092")

    HOME_USAGE_POWER = load_home_load()
    while True:
        energy_consumption = home_energy_usage_per_second(HOME_USAGE_POWER)
        
        logging.debug("Got energy consumption: %s", energy_consumption)

        producer.kafka_produce(message_value = energy_consumption)
        logging.debug("Produced a message in home_energy_consumption topic")


        time.sleep(1)



if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()