#!/bin/bash

exec python3 weather_producer_archived_data.py &
exec python3 solar_producer.py &
exec python3 home_energy_usage.py &
exec python3 acess_power_managment.py &
exec python3 mysql_database/kafka_to_db.py