import json
import csv
import random


base_dir = 'EGY_QH_Helwan.623780_TMYx.2009-2023/'
solar_intensity_file_path = base_dir + 'EGY_QH_Helwan.623780_TMYx.2009-2023.clm'
temp_file_path = base_dir + 'EGY_QH_Helwan.623780_TMYx.2009-2023.pvsyst'
year = 2013



def add_minutes_freq(day_info, date):
	day_info_by_minute = []

	for index in range(len(day_info) - 1):
		for m in range(1, 60):
			hour = day_info[index]['hour']

			current_hour_solar_intensity = float(day_info[index]['solar_intensity'])
			next_hour_solar_intensity = float(day_info[index+1]['solar_intensity'])
			solar_intensity = random.uniform(current_hour_solar_intensity, next_hour_solar_intensity) 

			current_hour_temp = float(day_info[index]['temp'])
			next_hour_temp = float(day_info[index+1]['temp'])
			temp = random.uniform(current_hour_temp, next_hour_temp)

			day_info_by_minute.append({'hour': hour, 'minute':m, 'solar_intensity': solar_intensity, 'temp': temp})

	
	return day_info_by_minute



def save_file(day_info, date):
	base_dir = 'weather_history_splitted/'

	# with open(base_dir + date, 'w') as file:
	# 	json.dump(day_info_dict, file)
	
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
					# print(date, prev_date, day_info_dict)
					solar_intensity_processing(day_info_dict, prev_date)

					# save this date data in a separate file
					if day_info_dict and prev_date:
						# increase the frequency to minutes
						day_info_by_minute = add_minutes_freq(day_info_dict[prev_date], prev_date)
						# save_file(day_info_dict[prev_date], prev_date)
						save_file(day_info_by_minute, prev_date)


					day_info_dict = {}
					day_info_dict[date] = []
					day_info_dict[date].append({'hour': hour, 'solar_intensity': -1, 'temp': info[-3]})


	# del day_info_dict[f'Day-Month-{year}']
	# del day_info_dict[f'--{year}']

	# print(day_info_dict)
	# print(json.dumps(day_info_dict, indent=2))



 
def solar_intensity_processing(day_info_dict, date):
	with open(solar_intensity_file_path, 'rb') as file:
		for line in file:
			line = line.decode("utf-8").strip()

			# new day
			if line[0] == '*':
				day_month = line.split()
				if len(day_month) > 1:
					month = day_month[-1]
					day = day_month[2]
					hour = 1
					current_date = str(day) + '-' + str(month) + '-' + str(year)

			else:
				info = line.split(',')
				if len(info) == 6:
					# col 3: Direct normal solar intensity   (W/m**2)
					# which is in index 2
					if current_date == date:
						day_info_dict[date][hour-1]['solar_intensity'] = info[2]
					
					hour += 1




def main():
	
	temp_processing()


main()