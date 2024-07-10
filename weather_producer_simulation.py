import requests
import logging
import datetime
import time
import random
from Kafka_producer import Kafka_producer

msg = {'current':{'is_day':1, 'cloud_cover':random.randint(650,1000)/1000,
                  'wind_speed_10m':20, 'temperature_2m':35, 'time_stamp':0}, 
       'daily':{'sunrise':['2024-07-09T05:58:58'], 'sunset':['2024-07-09T20:58:58']}}

def get_weather():
    time_stamp = str(datetime.datetime.now().replace(microsecond=0))
    msg['time_stamp'] = time_stamp

    return msg


def main():
    producer = Kafka_producer(topic_name = "weather_data", message_key = "Cairo") 
    producer.kafka_producer_conf(broker_address = "localhost:9092")

    while True:
        weather = get_weather()

        logging.debug("Got Weather: %s", weather)

        producer.kafka_produce(message_value = weather)
        logging.debug("Produced a message in weather_data topic")
        
        time.sleep(10)


if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()