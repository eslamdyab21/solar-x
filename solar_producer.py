import json
import logging
import datetime 
import random
from dotenv import load_dotenv
import os
from Kafka_consumer import Kafka_consumer
from Kafka_producer import Kafka_producer
from mysql_database.Database import Database


solar_power_w_accumulated = 0
solar_power_w_accumulated_hourly = 0
prev_hour = 0
solar_power_w_accumulated_hourly_set = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,
    "8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,
    "21":0,"22":0,"23":0}

db = Database()


def load_solar_day_data_from_db():
    global solar_power_w_accumulated, solar_power_w_accumulated_hourly_set, solar_power_w_accumulated_hourly

    time_stamp = datetime.datetime.now().replace(microsecond=0)
    current_hour = time_stamp.hour

    result = db.load_solar_day_data()
    if result:
        for record in result:

            solar_power_w_accumulated = float(record[0])
            solar_power_w_accumulated_hourly_set[str(record[-1].hour)] = float(record[1])

            if current_hour == record[-1].hour:
                solar_power_w_accumulated_hourly = float(record[1])


def get_time_in_seconds(t):
    hours = int(t.split(':')[0])*3600
    minutes = int(t.split(':')[1])*60
    seconds = int(t.split(':')[2])

    return hours + minutes + seconds


def get_power_w_accumulated(time_stamp, celcius, solar_intensity, 
                            solar_panel_rating_w_sec, solar_intensity_power_rating,
                            temp_power_rating):
    
    global solar_power_w_accumulated, solar_power_w, solar_power_w_accumulated_hourly_set

        
    random_per = random.randint(650,1000)/1000

    solar_power_w = solar_panel_rating_w_sec * random_per * (1 /(1 - (temp_power_rating - celcius)/(temp_power_rating))) \
                                         * (1 - (solar_intensity_power_rating - solar_intensity)/solar_intensity_power_rating)
                                            
                                                                                     
    # solar_power_w = solar_panel_rating_w_sec * is_day * t_presentage * (1 - cloud_cover_percentage/100) * random_per

    if solar_power_w_accumulated is None:
        solar_power_w_accumulated = solar_power_w
    else:
        solar_power_w_accumulated  += solar_power_w

    current_hour = time_stamp.split()[1].split(':')[0]

    if int(current_hour) == 1:
        solar_power_w_accumulated = 0
        solar_power_w_accumulated_hourly_set = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,
                                                "8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,
                                                "21":0,"22":0,"23":0}
    


def get_power_w_accumulated_hourly(current_hour):
    global prev_hour, solar_power_w, solar_power_w_accumulated_hourly

    if current_hour == prev_hour:
        solar_power_w_accumulated_hourly += solar_power_w
    else:
        solar_power_w_accumulated_hourly = 0
    
    solar_power_w_accumulated_hourly_set[current_hour] = round(solar_power_w_accumulated_hourly,2)

    prev_hour = current_hour



def get_solar_energy(msg):
    global solar_power_w, solar_power_w_accumulated, solar_power_w_accumulated_hourly_set
    
    # time_stamp = str(datetime.datetime.now().replace(microsecond=0))
    time_stamp = str(msg["current"]["time_stamp"])
    celcius = msg["current"]["temperature_2m"]
    solar_intensity = msg["current"]["solar_intensity"]
    solar_panel_rating_kwh = 10
    solar_panel_rating_w_sec = solar_panel_rating_kwh*1000/3600
    solar_intensity_power_rating = 1000
    temp_power_rating = 25


    get_power_w_accumulated(time_stamp, celcius, solar_intensity, 
                            solar_panel_rating_w_sec, solar_intensity_power_rating,
                            temp_power_rating)


    current_hour = time_stamp.split()[1].split(':')[0]
    get_power_w_accumulated_hourly(current_hour)
    

    new_msg = {
        "time_stamp":time_stamp,
        "current_consumption_w" : round(solar_power_w, 2),
        "consumption_accumulated_w" : round(solar_power_w_accumulated, 2),
        "current_consumption_w_accumulated_hourly" : solar_power_w_accumulated_hourly_set
    }

    return new_msg


def main():
    load_dotenv()
    KAFKA_BROKER_ADDRESS = os.getenv('KAFKA_BROKER_ADDRESS')

    consumer = Kafka_consumer(topic_name = ["weather_data"])
    consumer.kafka_consumer_conf(broker_address = KAFKA_BROKER_ADDRESS, 
                                 consumer_group = "weather_reader4solarX",
                                 auto_offset_reset = "latest")


    producer = Kafka_producer(topic_name = "solar_energy_data", message_key = "solar_w")
    producer.kafka_producer_conf(broker_address = KAFKA_BROKER_ADDRESS)

    load_solar_day_data_from_db()
    
    value = None
    while True:
        msg = consumer.consume(timeout = 1.0, store_offset = True)

        if msg is None:
            print("Waiting....")   

        elif msg.error() is not None:
            raise Exception(msg.error())
        
        else:
            key = msg.key().decode("utf-8")
            value = json.loads(msg.value())
            offset = msg.offset()
            logging.debug(f"{offset} {key} {value}")

            value = dict(value)
            solar_energy = get_solar_energy(value)
            producer.kafka_produce(message_value = solar_energy)
            logging.debug(f"{solar_energy}")
            
        
        # if value and msg is not None:
        #     solar_energy = get_solar_energy(value)
        #     producer.kafka_produce(message_value = solar_energy)
        #     logging.debug(f"{solar_energy}")


if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()
