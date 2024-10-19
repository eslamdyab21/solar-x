import json
import csv


base_dir = 'EGY_QH_Helwan.623780_TMYx.2009-2023/'
solar_intensity_file_path = base_dir + 'EGY_QH_Helwan.623780_TMYx.2009-2023.clm'
temp_file_path = base_dir + 'EGY_QH_Helwan.623780_TMYx.2009-2023.pvsyst'
year = 2013


def save_file(day_info_dict, date):
	base_dir = 'weather_history_splitted/'

	# with open(base_dir + date, 'w') as file:
	# 	json.dump(day_info_dict, file)
	
	keys = day_info_dict[0].keys()

	with open(base_dir + date + '.csv', 'w', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(day_info_dict)


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
					if len(day_info_dict) > 3:
						# print(date, prev_date, day_info_dict)
						solar_intensity_processing(day_info_dict, prev_date)
						# save this date data in a separate file
						save_file(day_info_dict[prev_date], prev_date)

					day_info_dict[date] = []
					day_info_dict[date].append({'hour': hour, 'solar_intensity': -1, 'temp': info[-3]})


	del day_info_dict[f'Day-Month-{year}']
	del day_info_dict[f'--{year}']

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