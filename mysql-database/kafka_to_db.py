import json
import time
from Kafka_consumer import Kafka_consumer
from database import Database



def main():
	consumer = Kafka_consumer(topic_name = ["battery_data"])
	consumer.kafka_consumer_conf(broker_address = "localhost:9092", 
	                             consumer_group = "baterry_data_to_db",
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

	        for key in value['batteries'].keys():
		        query = (
		            f"""
		                INSERT INTO Battery_Readings VALUES(NULL, {key.split('_')[-1]}, {value['batteries'][key]['current_energy_wh']}, {value['batteries'][key]['current_energy_wh']}, '{value['batteries'][key]['status']}', NOW());
		            """
		        )

		        # result = db.select_query(query)
		        db.insert_db(query)

		        time.sleep(0.5)

	        print("-------------------------------------------------")

	    time.sleep(5)



if __name__ == "__main__":
    main()