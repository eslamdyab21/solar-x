import json
import time
import logging
import datetime
from Kafka_consumer import Kafka_consumer
from database import Database

prev_hour = None
prev_minute = None


def update_db(db, value):
	global prev_minute, prev_hour

	time_stamp = str(datetime.datetime.now().replace(microsecond=0))
	current_hour = time_stamp.split()[1].split(':')[0]
	current_minute = time_stamp.split()[1].split(':')[1]


	if current_hour != prev_hour:

		for key in value['batteries'].keys():

			query = (
			    f"""
				INSERT INTO Battery_readings VALUES(NULL, {key.split('_')[-1]}, {value['batteries'][key]['current_energy_wh']}, {value['hourly_discharging'][current_hour]}, '{value['batteries'][key]['status']}', NOW(), NOW());
			    """
			)
			db.insert_query(query)

		prev_hour = current_hour
		logging.info('Database : insert_query done')
		logging.info("-------------------------------------------------")


	elif current_minute != prev_minute:

		for key in value['batteries'].keys():
			query = (
			    f"""
				UPDATE Battery_readings 
				SET current_energy_watt = {value['batteries'][key]['current_energy_wh']}, 
				current_hourly_consumption_watt = {value['hourly_discharging'][current_hour]}, 
				status = '{value['batteries'][key]['status']}',
				updated_at = NOW()

				WHERE battery = {key.split('_')[-1]}
				ORDER BY id DESC LIMIT 1
			    """
			)
			db.update_query(query)

		prev_minute = current_minute
		logging.info('Database : update_query done')
		logging.info("-------------------------------------------------")


	
def main():
	consumer = Kafka_consumer(topic_name = ["battery_data"])
	consumer.kafka_consumer_conf(broker_address = "localhost:9092", 
		                     consumer_group = "kafka_to_db",
		                     auto_offset_reset = "latest")
	
	db = Database()

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

			update_db(db, value)

			

if __name__ == "__main__":
	logging.basicConfig(level = "INFO")
	main()
