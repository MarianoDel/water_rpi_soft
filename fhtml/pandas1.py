import pandas as pd

# pulses file location
file_location = '../../20241216'
file_name = 'master_meas.csv'

# read csv pulses file
file_loc_name = file_location + '/' + file_name
pulse_data = pd.read_csv (file_loc_name, header=None, usecols=[0, 1])


# show 5 rows
print("first five rows")
print(pulse_data.head())

print("last five rows")
print(pulse_data.tail())

print("columns attr")
print(pulse_data.columns)

