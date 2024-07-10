import datetime
import logging
import random
import json
import time


consumption_acumm = 0
current_consumption = 0


def load_home_load():
    with open('home_appliances_consumption.json') as f:
        HOME_USAGE_POWER = json.load(f)

    return HOME_USAGE_POWER


def get_time_in_seconds(t):
    hours = int(t.split(':')[0])*3600
    minutes = int(t.split(':')[1])*60

    return hours + minutes 


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


    energy_consumption = {'time_stamp':time_stamp, 'current_total_consumption':current_total_consumption, 'consumption_acumm':consumption_acumm}

    return energy_consumption



def main():

    HOME_USAGE_POWER = load_home_load()
    while True:
        energy_consumption = home_energy_usage_per_second(HOME_USAGE_POWER)
        
        logging.debug("Got energy consumption: %s", energy_consumption)



        time.sleep(1)



if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()