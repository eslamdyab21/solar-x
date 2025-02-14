FROM python:3.9


WORKDIR /usr/app/src

COPY Kafka_consumer.py ./
COPY Kafka_producer.py ./
COPY weather_producer_archived_data.py ./
COPY solar_producer.py ./
COPY home_energy_usage.py ./
COPY acess_power_managment.py ./
COPY bms.py ./
COPY home_appliances_consumption.json ./
COPY home_configurations.json ./
COPY .env ./
COPY real_weather_data_etl ./real_weather_data_etl
COPY mysql_database ./mysql_database
COPY run.sh ./

RUN pip install quixstreams
RUN pip install pandas
RUN pip install mysql-connector-python
RUN pip install python-dotenv

# RUN chmod +x run.sh
# RUN ./run.sh