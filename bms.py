import json
import logging
import random


class BMS():

    def __init__(self):
        self.batteries_status = {}
        self.load_batteries_info()
        

    def load_batteries_info(self):
        with open('home_configurations.json') as f:
            HOME_CONFIGURATIONS = json.load(f)

        i = 1
        for battery_capacity in HOME_CONFIGURATIONS['batteries_capacity_kwh']:
            battery_name = 'battery_' + str(i)
            if battery_name not in self.batteries_status:
                self.batteries_status[battery_name] = {"capacity_kwh": battery_capacity, 
                                                 "max_charge_speed_w": HOME_CONFIGURATIONS['batteries_charge_max_speed_w_second'][i-1],
                                                 "current_energy_wh":battery_capacity*1000,
                                                 "is_charging":0,
                                                 "status":'ideal',
                                                 "max_output_w": round(battery_capacity*1000/3600, 2)}
                i +=1

        self.batteries_status['battery_3']['current_energy_wh'] = 6000
        self.batteries_status['battery_2']['current_energy_wh'] = 7000
        self.batteries_status['battery_1']['current_energy_wh'] = 7500



    def charge_batteries(self, access_power_w, last_battery_charged = None):

        min_energy_battery = 'battery_1'
        min_energy = self.batteries_status[min_energy_battery]['current_energy_wh']
        full_charged_counter = 0
        loss = 1 - random.randint(850,1000)/1000


        for battery in self.batteries_status.keys():
            if int(self.batteries_status[battery]['current_energy_wh']) == self.batteries_status[battery]['capacity_kwh']*1000:
                self.batteries_status[battery]['status'] = 'ideal'
                full_charged_counter += 1

            if self.batteries_status[battery]['current_energy_wh'] < min_energy and battery != last_battery_charged:
                min_energy = self.batteries_status[battery]['current_energy_wh']
                min_energy_battery = battery

        if full_charged_counter == len(self.batteries_status.keys()):
            self.batteries_status[min_energy_battery]['status'] = 'ideal'

        if min_energy_battery == last_battery_charged or full_charged_counter == len(self.batteries_status.keys()):
            return access_power_w

        if access_power_w > self.batteries_status[min_energy_battery]['max_charge_speed_w']:
            access = access_power_w - self.batteries_status[min_energy_battery]['max_charge_speed_w']

            access_power_w = self.batteries_status[min_energy_battery]['max_charge_speed_w']
            self.batteries_status[min_energy_battery]['current_energy_wh'] += access_power_w - loss*access_power_w
            self.batteries_status[min_energy_battery]['current_energy_wh'] = round(self.batteries_status[min_energy_battery]['current_energy_wh'] , 2)
            self.batteries_status[min_energy_battery]['is_charging'] = 1

            if self.batteries_status[min_energy_battery]['current_energy_wh'] > self.batteries_status[min_energy_battery]['capacity_kwh']*1000:
                self.batteries_status[min_energy_battery]['current_energy_wh'] = self.batteries_status[min_energy_battery]['capacity_kwh']*1000
                self.batteries_status[min_energy_battery]['is_charging'] = 0
            
            self.charge_batteries(access_power_w = round(access,2), last_battery_charged = min_energy_battery)

        else:
            self.batteries_status[min_energy_battery]['current_energy_wh'] += access_power_w - loss*access_power_w
            self.batteries_status[min_energy_battery]['current_energy_wh'] = round(self.batteries_status[min_energy_battery]['current_energy_wh'] , 2)
            self.batteries_status[min_energy_battery]['is_charging'] = 1

            if self.batteries_status[min_energy_battery]['current_energy_wh'] > self.batteries_status[min_energy_battery]['capacity_kwh']*1000:
                self.batteries_status[min_energy_battery]['current_energy_wh'] = self.batteries_status[min_energy_battery]['capacity_kwh']*1000
                self.batteries_status[min_energy_battery]['is_charging'] = 0


        self.batteries_status[min_energy_battery]['status'] = 'charging'


    def consume_batteries(self, access_power_w):
        max_energy_battery = 'battery_1'
        max_energy = self.batteries_status[max_energy_battery]['current_energy_wh']
        full_discharged_counter = 0


        for battery in self.batteries_status.keys():
            if int(self.batteries_status[battery]['current_energy_wh']) == self.batteries_status[battery]['capacity_kwh']*1000:
                self.batteries_status[battery]['status'] = 'ideal'
                full_discharged_counter +=1

            if self.batteries_status[battery]['current_energy_wh'] > max_energy:
                max_energy = self.batteries_status[battery]['current_energy_wh']
                max_energy_battery = battery


        if full_discharged_counter == len(self.batteries_status.keys()):
            self.batteries_status[max_energy_battery]['status'] = 'ideal'
            return access_power_w


        if access_power_w > self.batteries_status[max_energy_battery]['max_output_w']:
            self.batteries_status[max_energy_battery]['current_energy_wh'] -= self.batteries_status[max_energy_battery]['max_output_w']
            self.batteries_status[max_energy_battery]['current_energy_wh'] = round(self.batteries_status[max_energy_battery]['current_energy_wh'] , 2)
            self.consume_batteries(access_power_w - self.batteries_status[max_energy_battery]['max_output_w'])
        else:
            self.batteries_status[max_energy_battery]['current_energy_wh'] -= access_power_w
            self.batteries_status[max_energy_battery]['current_energy_wh'] = round(self.batteries_status[max_energy_battery]['current_energy_wh'] , 2)


        self.batteries_status[max_energy_battery]['status'] = 'discharging'

