import pandas as pd
from datetime import datetime, date, timedelta
import sys

# pulses file location
files_dir = '../../'
file_name = 'master_meas.csv'


def DataFrameAssembly (init_date_str, end_date_str):
    # if data comes like this YYYY-MM-DD convert to this YYYYMMDD
    
    # convert to date and check days qtty
    init_date = date.fromisoformat(init_date_str)
    end_date = date.fromisoformat(end_date_str)

    date_delta = end_date - init_date
    print('days between dates: ' + str(date_delta.days))

    if date_delta.days < 0:
        print('end date must be equal or greater then init date')
        return

    if date_delta.days > 100:
        print('no more than hundred days can be readed by this script')
        return

    # create dummys directories
    df_list = []
    
    for d in range(date_delta.days + 1):
        days_delta = timedelta(days=d)
        date_to_log = init_date + days_delta
        date_to_log_str = date_to_log.strftime("%Y%m%d")
        date_to_log_fullpath_str = files_dir + date_to_log_str + '/' + file_name
        # try:
            # pulse_df = pd.read_csv (date_to_log_fullpath_str, header=None, usecols=[0, 1])
            # df_list.append(pulse_df)
            # print('date getted: ' + date_to_log_str + ' entries: ' + pulse_df.rows)
        # except:
        #     print('date not found: ' + date_to_log_str)
        #     continue

        pulse_df = pd.read_csv (date_to_log_fullpath_str, header=None, usecols=[0, 1])
        df_list.append(pulse_df)
        (rows, cols) = pulse_df.shape
        print('date getted: ' + date_to_log_str + \
              ' entries: ' + str(rows))
        
    # concatenate df
    try:
        df = pd.concat(df_list, axis=1)        
    except:
        print("dataframe errors on selected dates!")


if __name__ == "__main__":
    # check args for operation
    if len(sys.argv) != 3:
        print('use this script with format YYYYMMDD or YYYY-MM-DD: init_date end_date')
        sys.exit()

    # get the dates
    init_date_str = sys.argv[1]
    end_date_str = sys.argv[2]
    my_df = DataFrameAssembly(init_date_str, end_date_str)

    if isinstance (my_df, pd.DataFrame):
        print("df first five rows")
        print(my_df.head())

        print("df last five rows")
        print(my_df.tail())

        print("df columns attr")
        print(my_df.columns)

        (rows, cols) = my_df.shape
        print('df total entries: ' + str(rows))
    else:
        print('an error df getted for dates!!!')

