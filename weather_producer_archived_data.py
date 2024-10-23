import logging
import datetime
import time
import random
import pandas as pd
from Kafka_producer import Kafka_producer



def read_file():
    base_dir = 'real_weather_data_etl/weather_history_splitted/'

    time_stamp = datetime.datetime.now().replace(microsecond=0)
    current_date = str(time_stamp.date()).split('-')
    current_date[0] = '2013'
    current_date = '-'.join(current_date)

    df = pd.read_csv(base_dir + current_date + '.csv')

    return df



def get_weather(df):
    msg = {'current':{'is_day':1, 'cloud_cover':random.randint(100,1000)/1000,
                  'wind_speed_10m':20, 'temperature_2m':35, 'time_stamp':0}, 
            'daily':{'sunrise':['2024-07-09T05:11:11'], 'sunset':['2024-07-09T18:11:11']}}
    
    time_stamp = datetime.datetime.now().replace(microsecond=0)
    current_hour = int(time_stamp.hour)
    current_minute = int(time_stamp.minute)
    
    sunrise_hour = df[df['solar_intensity'] > 0]['hour'].values[0]
    sunset_hour = df[df['solar_intensity'] > 0]['hour'].values[-1] + 1

    df = df[(df['hour'] == current_hour) & (df['minute'] == current_minute)]
    if df.size > 0:
        solar_intensity = df['solar_intensity'].values[0]
        temp = df['temp'].values[0]

        msg['current']['is_day'] = int(solar_intensity > 0)
        msg['current']['temperature_2m'] = float(temp)
        msg['current']['cloud_cover'] = float(1 - (solar_intensity/900))

    msg['daily']['sunrise'][0] = msg['daily']['sunrise'][0].replace('05', '0' + str(sunrise_hour))
    msg['daily']['sunset'][0] = msg['daily']['sunset'][0].replace('18', str(sunset_hour))

    return msg



def main():
    producer = Kafka_producer(topic_name = "weather_data", message_key = "Cairo") 
    producer.kafka_producer_conf(broker_address = "localhost:9092")
    
    prev_day = None
    df = read_file()

    while True:
        time_stamp = datetime.datetime.now().replace(microsecond=0)
        day = time_stamp.day

        if day != prev_day:
            df = read_file()

        weather = get_weather(df)

        logging.debug("Got Weather: %s", weather)

        producer.kafka_produce(message_value = weather)
        logging.debug("Produced a message in weather_data topic")
        
        prev_day = day
        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()