import json


def solar_intensity_processing(file_path):
	day_info_dict = {}
	year = 2013
	with open(file_path, 'rb') as file:
		for line in file:
			line = line.decode("utf-8").strip()

			# new day
			if line[0] == '*':
				day_month = line.split()
				if len(day_month) > 1:
					month = day_month[-1]
					day = day_month[2]
					hour = 1
					date = str(day) + '-' + str(month) + '-' + str(year)
					day_info_dict[date] = []

			# add day solar intensity info	
			else:
				day_info = line.split(',')
				if len(day_info) == 6:
					# col 3: Direct normal solar intensity   (W/m**2)
					# which is in index 2
					day_info_dict[date].append({'hour': hour, 'solar_intensity': day_info[2], 'temp': 0})
					hour += 1


	print(json.dumps(day_info_dict, indent=2))


def main():
	base_dir = 'EGY_QH_Helwan.623780_TMYx.2009-2023/'
	solar_intensity_file_path = 'EGY_QH_Helwan.623780_TMYx.2009-2023.clm'
	temp_file_path = 'EGY_QH_Helwan.623780_TMYx.2009-2023.pvsyst'

	solar_intensity_processing(base_dir + solar_intensity_file_path)


main()