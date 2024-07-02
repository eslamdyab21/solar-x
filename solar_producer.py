import json
import logging
import datetime 
from Kafka_consumer import Kafka_consumer
from Kafka_producer import Kafka_producer



solar_power_w_accumulated = 0
def get_solar_energy(msg):
    global solar_power_w_accumulated
    # time_stamp = msg["current"]["time"]
    time_stamp = str(datetime.datetime.now().replace(microsecond=0))
    is_day = msg["current"]["is_day"]
    wind_speed = msg["current"]["wind_speed_10m"]
    cloud_cover_percentage = msg["current"]["cloud_cover"]
    celcius = msg["current"]["temperature_2m"]
    solar_panel_size = 100
    solar_power_w = solar_panel_size * is_day * (wind_speed / (celcius * (1 - cloud_cover_percentage/100)))
    
    
    if solar_power_w_accumulated is None:
        solar_power_w_accumulated = solar_power_w
    else:
        solar_power_w_accumulated  += solar_power_w

    if time_stamp.split()[1].split(':')[0] == "24":
        solar_power_w_accumulated = 0

    new_msg = {
        "solar_power_w" : round(solar_power_w, 2),
        "solar_power_w_accum" : round(solar_power_w_accumulated, 2)
    }

    return new_msg


def main():
    consumer = Kafka_consumer(topic_name = ["weather_data"])
    consumer.kafka_consumer_conf(broker_address = "localhost:9092", 
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
