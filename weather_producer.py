import requests
import logging
import time
from Kafka_producer import Kafka_producer



def get_weather():
    api_url = "https://api.open-meteo.com/v1/forecast?latitude=30.0626&longitude=31.2497&current=temperature_2m,is_day,cloud_cover,wind_speed_10m&timezone=Africa%2FCairo"

    response = requests.get(api_url)

    return response.json()


def main():
    producer = Kafka_producer(topic_name = "weather_data_demo", message_key = "Cairo") 
    producer.kafka_producer_conf(broker_address = "localhost:9092")

    while True:
        weather = get_weather()
        logging.debug("Got Weather: %s", weather)

        producer.kafka_produce(message_value = weather)
        logging.debug(f"Produced a message in weather_data_demo topic")
        time.sleep(60)


if __name__ == "__main__":
    logging.basicConfig(level = "DEBUG")
    main()