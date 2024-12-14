import json
import time
import logging
import datetime
from dotenv import load_dotenv
import os
from Kafka_consumer import Kafka_consumer
from Database import Database
from Kafka_db import Kafka_db



def main():
	load_dotenv()
	KAFKA_BROKER_ADDRESS = os.getenv('KAFKA_BROKER_ADDRESS')

	consumer = Kafka_consumer(topic_name = ["battery_data", "solar_energy_data", "home_energy_consumption"])
	consumer.kafka_consumer_conf(broker_address = KAFKA_BROKER_ADDRESS, 
		                     consumer_group = "kafka_to_db",
		                     auto_offset_reset = "latest")
	
	db = Database()
	kafka_db_battery = Kafka_db(db, logging)
	kafka_db_solar_pannel = Kafka_db(db, logging)
	kafka_db_home = Kafka_db(db, logging)


	while True:
		msg = consumer.consume(timeout = 1)

		if msg is None:
			pass    

		elif msg.error() is not None:
			raise Exception(msg.error())

		else:
			key = msg.key().decode("utf-8")
			value = dict(json.loads(msg.value()))
			offset = msg.offset()

			if key == 'bms':
				kafka_db_battery.update_battery_db(value)
			elif key == 'solar_w':
				kafka_db_solar_pannel.update_solar_pannels_db(value, 'Solar_pannel_readings')
			elif key == 'home_energy':
				kafka_db_home.update_home_db(value)

			

if __name__ == "__main__":
	logging.basicConfig(level = "INFO")
	main()
