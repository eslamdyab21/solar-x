import json
import logging
import random
import datetime
from mysql_database.Database import Database


class BMS():

    def __init__(self):
        self.batteries_status = {'time_stamp':None, 'batteries':{}, 
                                 'hourly_discharging': {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,
                                 "6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,
                                 "15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0}}

        self.reset_hourly_discharging_flag = True
        self.db = Database()


        self.load_batteries_info()
        self.load_batteries_day_data_from_db()
        

    def load_batteries_info(self):
        with open('home_configurations.json') as f:
            HOME_CONFIGURATIONS = json.load(f)

        i = 1
        for battery_capacity in HOME_CONFIGURATIONS['batteries_capacity_kwh']:
            battery_name = 'battery_' + str(i)
            if battery_name not in self.batteries_status['batteries']:
                self.batteries_status['batteries'][battery_name] = {"capacity_kwh": battery_capacity, 
                                                "max_charge_speed_w": HOME_CONFIGURATIONS['batteries_charge_max_speed_w_second'][i-1],
                                                 "current_energy_wh":battery_capacity*1000,
                                                 "is_charging":0,
                                                 "status":'ideal',
                                                 "max_output_w": round(battery_capacity*1000/3600, 2)}
                i +=1

        self.batteries_status['batteries']['battery_3']['current_energy_wh'] = 10000
        self.batteries_status['batteries']['battery_2']['current_energy_wh'] = 8600
        self.batteries_status['batteries']['battery_1']['current_energy_wh'] = 9860


    def load_batteries_day_data_from_db(self):
        result = self.db.load_batteries_day_data()
        if result:
            for record in result:
                battery_name = 'battery_' + str(record[0])
                self.batteries_status['batteries'][battery_name]['current_energy_wh'] = float(record[1])
                self.batteries_status['hourly_discharging'][str(record[-1].hour)] = float(record[2])


    def reset_hourly_discharging(self):
        time_stamp = str(datetime.datetime.now().replace(microsecond=0))
        current_hour = time_stamp.split()[1].split(':')[0]

        if int(current_hour) == 0 and self.reset_hourly_discharging_flag:
            self.batteries_status['hourly_discharging'] = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,
                                                            "7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,
                                                            "14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,
                                                            "21":0,"22":0,"23":0}
            self.reset_hourly_discharging_flag = False

        elif int(current_hour) != 0:
            self.reset_hourly_discharging_flag = True


    def charge_batteries(self, access_power_w, last_battery_charged = None):

        min_energy_battery = 'battery_1'
        min_energy = self.batteries_status['batteries'][min_energy_battery]['current_energy_wh']
        full_charged_counter = 0
        loss = 1 - random.randint(850,1000)/1000


        for battery in self.batteries_status['batteries'].keys():

            if int(self.batteries_status['batteries'][battery]['current_energy_wh']) == self.batteries_status['batteries'][battery]['capacity_kwh']*1000:
                full_charged_counter += 1

            if self.batteries_status['batteries'][battery]['current_energy_wh'] < min_energy and battery != last_battery_charged:
                min_energy = self.batteries_status['batteries'][battery]['current_energy_wh']
                min_energy_battery = battery


            self.batteries_status['batteries'][battery]['status'] = 'ideal'


        if full_charged_counter == len(self.batteries_status['batteries'].keys()):
            self.batteries_status['batteries'][min_energy_battery]['status'] = 'ideal'

        if min_energy_battery == last_battery_charged or full_charged_counter == len(self.batteries_status['batteries'].keys()):
            return access_power_w


        if access_power_w > self.batteries_status['batteries'][min_energy_battery]['max_charge_speed_w']:
            access = access_power_w - self.batteries_status['batteries'][min_energy_battery]['max_charge_speed_w']

            access_power_w = self.batteries_status['batteries'][min_energy_battery]['max_charge_speed_w']
            self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] += access_power_w - loss*access_power_w
            self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] = round(self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] , 2)
            self.batteries_status['batteries'][min_energy_battery]['is_charging'] = 1

            if self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] > self.batteries_status['batteries'][min_energy_battery]['capacity_kwh']*1000:
                self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] = self.batteries_status['batteries'][min_energy_battery]['capacity_kwh']*1000
                self.batteries_status['batteries'][min_energy_battery]['is_charging'] = 0
            
            self.charge_batteries(access_power_w = round(access,2), last_battery_charged = min_energy_battery)

        else:
            self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] += access_power_w - loss*access_power_w
            self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] = round(self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] , 2)
            self.batteries_status['batteries'][min_energy_battery]['is_charging'] = 1

            if self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] > self.batteries_status['batteries'][min_energy_battery]['capacity_kwh']*1000:
                self.batteries_status['batteries'][min_energy_battery]['current_energy_wh'] = self.batteries_status['batteries'][min_energy_battery]['capacity_kwh']*1000
                self.batteries_status['batteries'][min_energy_battery]['is_charging'] = 0


        self.batteries_status['batteries'][min_energy_battery]['status'] = 'charging'
        self.reset_hourly_discharging()


    def discharge_batteries(self, access_power_w, last_battery_discharged = None):
        max_energy_battery = 'battery_1'
        max_energy = 0
        full_discharged_counter = 0

        time_stamp = datetime.datetime.now().replace(microsecond=0)
        current_hour = str(time_stamp.hour)

        for battery in self.batteries_status['batteries'].keys():
            if int(self.batteries_status['batteries'][battery]['current_energy_wh']) == 0:
                self.batteries_status['batteries'][battery]['status'] = 'ideal'
                full_discharged_counter +=1

            if self.batteries_status['batteries'][battery]['current_energy_wh'] > max_energy and battery != last_battery_discharged:
                max_energy = self.batteries_status['batteries'][battery]['current_energy_wh']
                max_energy_battery = battery

        
        if max_energy_battery == last_battery_discharged or full_discharged_counter == len(self.batteries_status['batteries'].keys()):
            self.batteries_status['batteries'][max_energy_battery]['status'] = 'ideal'
            
            return access_power_w


        if access_power_w > self.batteries_status['batteries'][max_energy_battery]['max_output_w']:
            self.batteries_status['batteries'][max_energy_battery]['current_energy_wh'] -= self.batteries_status['batteries'][max_energy_battery]['max_output_w']
            self.batteries_status['batteries'][max_energy_battery]['current_energy_wh'] = round(self.batteries_status['batteries'][max_energy_battery]['current_energy_wh'] , 2)
            self.batteries_status['hourly_discharging'][current_hour] += self.batteries_status['batteries'][max_energy_battery]['max_output_w']
            self.batteries_status['hourly_discharging'][current_hour] = round(self.batteries_status['hourly_discharging'][current_hour],2)
            
            self.discharge_batteries(access_power_w - self.batteries_status['batteries'][max_energy_battery]['max_output_w'], last_battery_discharged = max_energy_battery)

        elif self.batteries_status['batteries'][max_energy_battery]['current_energy_wh'] - access_power_w < 0:
            return access_power_w

        else:
            self.batteries_status['batteries'][max_energy_battery]['current_energy_wh'] -= access_power_w
            self.batteries_status['batteries'][max_energy_battery]['current_energy_wh'] = round(self.batteries_status['batteries'][max_energy_battery]['current_energy_wh'] , 2)
            self.batteries_status['hourly_discharging'][current_hour] += access_power_w
            self.batteries_status['hourly_discharging'][current_hour] = round(self.batteries_status['hourly_discharging'][current_hour],2)
                

        self.batteries_status['batteries'][max_energy_battery]['status'] = 'discharging'
        self.reset_hourly_discharging()