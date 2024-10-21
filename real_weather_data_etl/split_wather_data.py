import json
import csv
import random
import os

base_dir = 'EGY_QH_Helwan.623780_TMYx.2009-2023/'
solar_intensity_file_path = base_dir + 'EGY_QH_Helwan.623780_TMYx.2009-2023.clm'
temp_file_path = base_dir + 'EGY_QH_Helwan.623780_TMYx.2009-2023.pvsyst'
year = 2013
next_day_line_index = None


def add_minutes_freq(day_info, date):
	day_info_by_minute = []

	for index in range(len(day_info) - 1):
		for m in range(1, 60):
			hour = day_info[index]['hour']

			current_hour_solar_intensity = float(day_info[index]['solar_intensity'])
			next_hour_solar_intensity = float(day_info[index+1]['solar_intensity'])
			solar_intensity = round(random.uniform(current_hour_solar_intensity, next_hour_solar_intensity), 2) 

			current_hour_temp = float(day_info[index]['temp']) - 1
			next_hour_temp = float(day_info[index+1]['temp']) + 1
			temp = round(random.uniform(current_hour_temp, next_hour_temp), 2)

			day_info_by_minute.append({'hour': hour, 'minute':m, 'solar_intensity': solar_intensity, 'temp': temp})

	
	return day_info_by_minute



def save_file(day_info, date):
	base_dir = 'weather_history_splitted/'
	
	if not os.path.exists(base_dir):
		os.makedirs(base_dir)

	keys = day_info[0].keys()

	with open(base_dir + date + '.csv', 'w', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(day_info)


def temp_processing():
	day_info_dict = {}
	prev_date = None

	with open(temp_file_path, 'rb') as file:
		for line in file:
			info = line.decode("utf-8", errors='ignore').strip().split(',')

			if len(info) == 11:
				month = info[1]
				day = info[2]
				hour = info[3]
				date = str(day) + '-' + str(month) + '-' + str(year)


				if date in day_info_dict.keys():
					day_info_dict[date].append({'hour': hour, 'solar_intensity': -1, 'temp': info[-3]})
					prev_date = date

				else:					
					if day_info_dict and prev_date:
						solar_intensity_processing(day_info_dict, prev_date)
						# increase the frequency to minutes
						day_info_by_minute = add_minutes_freq(day_info_dict[prev_date], prev_date)
						# save_file(day_info_dict[prev_date], prev_date)
						save_file(day_info_by_minute, prev_date)


					day_info_dict = {}
					day_info_dict[date] = []
					day_info_dict[date].append({'hour': hour, 'solar_intensity': -1, 'temp': info[-3]})




 
def solar_intensity_processing(day_info_dict, date):
	global next_day_line_index
	hour = 1

	with open(solar_intensity_file_path, 'rb') as file:
		for line_index, line in enumerate(file):

			if next_day_line_index is None:
				line = line.decode("utf-8").strip()
				if line == '* day  1 month  1':
					next_day_line_index = line_index + 1

				
			elif line_index >= next_day_line_index:
				line = line.decode("utf-8").strip()
				info = line.split(',')
				day_info_dict[date][hour-1]['solar_intensity'] = info[2]

				hour += 1

				if hour == 25:
					next_day_line_index = line_index + 2
					break



def main():
	temp_processing()


main()
