import datetime


class Kafka_db():

    def __init__(self, db, logging):
        self.db = db
        self.logging = logging

        self.prev_hour = None
        self.current_hour = None

        self.prev_minute = None
        self.current_minute = None


        

    def update_battery_db(self, value):

        time_stamp = str(datetime.datetime.now().replace(microsecond=0))
        self.current_hour = time_stamp.split()[1].split(':')[0]
        self.current_minute = time_stamp.split()[1].split(':')[1]


        if self.current_hour != self.prev_hour:

            for key in value['batteries'].keys():

                query = (
                    f"""
                    INSERT INTO Battery_readings VALUES(NULL, {key.split('_')[-1]}, {value['batteries'][key]['current_energy_wh']}, {value['hourly_discharging'][self.current_hour]}, '{value['batteries'][key]['status']}', NOW(), NOW());
                    """
                )
                self.db.insert_query(query)

            self.prev_hour = self.current_hour
            self.logging.info('Database : insert_query battery done')
            self.logging.info("-------------------------------------------------")


        elif self.current_minute != self.prev_minute:

            for key in value['batteries'].keys():
                query = (
                    f"""
                    UPDATE Battery_readings 
                    SET current_energy_watt = {value['batteries'][key]['current_energy_wh']}, 
                    current_hourly_consumption_watt = {value['hourly_discharging'][self.current_hour]}, 
                    status = '{value['batteries'][key]['status']}',
                    updated_at = NOW()

                    WHERE battery = {key.split('_')[-1]}
                    ORDER BY id DESC LIMIT 1
                    """
                )
                self.db.update_query(query)

            self.prev_minute = self.current_minute
            self.logging.info('Database : update_query battery done')
            self.logging.info("-------------------------------------------------")




    def update_solar_pannels_db(self, value, table_name):

        time_stamp = str(datetime.datetime.now().replace(microsecond=0))
        self.current_hour = time_stamp.split()[1].split(':')[0]
        self.current_minute = time_stamp.split()[1].split(':')[1]


        if self.current_hour != self.prev_hour:
            query = (
                f"""
                INSERT INTO Solar_pannel_readings VALUES (NULL, 1, {value['consumption_accumulated_w']}, {value['current_consumption_w_accumulated_hourly'][self.current_hour]}, NOW(), NOW());
                """
            )
            self.db.insert_query(query)

            self.prev_hour = self.current_hour
            self.logging.info('Database : insert_query solar pannels done')
            self.logging.info("-------------------------------------------------")


        elif self.current_minute != self.prev_minute:
            query = (
                f"""
                UPDATE Solar_pannel_readings 
                SET generation_watt = {value['consumption_accumulated_w']}, 
                generation_hourly_watt = {value['current_consumption_w_accumulated_hourly'][self.current_hour]}, 
                updated_at = NOW()

                ORDER BY id DESC LIMIT 1
                """
            )
            self.db.update_query(query)

            self.prev_minute = self.current_minute
            self.logging.info('Database : update_query solar pannels done')
            self.logging.info("-------------------------------------------------")


    def update_home_db(self, value):

        time_stamp = str(datetime.datetime.now().replace(microsecond=0))
        self.current_hour = time_stamp.split()[1].split(':')[0]
        self.current_minute = time_stamp.split()[1].split(':')[1]


        if self.current_hour != self.prev_hour:
            query = (
                f"""
                INSERT INTO Home_readings VALUES (NULL, 1, {value['consumption_accumulated_w']}, {value['current_consumption_w_accumulated_hourly'][self.current_hour]}, NOW(), NOW());
                """
            )
            self.db.insert_query(query)

            self.prev_hour = self.current_hour
            self.logging.info('Database : insert_query home done')
            self.logging.info("-------------------------------------------------")


        elif self.current_minute != self.prev_minute:
            query = (
                f"""
                UPDATE Home_readings 
                SET consumption_watt = {value['consumption_accumulated_w']}, 
                consumption_hourly_watt = {value['current_consumption_w_accumulated_hourly'][self.current_hour]}, 
                updated_at = NOW()

                ORDER BY id DESC LIMIT 1
                """
            )
            self.db.update_query(query)

            self.prev_minute = self.current_minute
            self.logging.info('Database : update_query home done')
            self.logging.info("-------------------------------------------------")