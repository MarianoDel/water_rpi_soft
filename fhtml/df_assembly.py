import pandas as pd
from datetime import datetime, date, timedelta
import sys

# pulses file location
files_dir = '../../'
file_name = 'master_meas.csv'


def DataFrameAssembly (init_date_str, end_date_str, ten_min=True):
    # if data comes like this YYYY-MM-DD convert to this YYYYMMDD
    
    # convert to date and check days qtty
    init_date = date.fromisoformat(init_date_str)
    end_date = date.fromisoformat(end_date_str)

    date_delta = end_date - init_date
    print('days between dates: ' + str(date_delta.days))

    if date_delta.days < 0:
        df_err = 'end date must be equal or greater then init date'
        print(df_err)
        return df_err, None

    if date_delta.days > 100:
        df_err = 'no more than hundred days can be readed by this script'
        print(df_err)
        return df_err, None

    # create dummys directories
    df_list = []
    
    for d in range(date_delta.days + 1):
        days_delta = timedelta(days=d)
        date_to_log = init_date + days_delta
        date_to_log_str = date_to_log.strftime("%Y%m%d")
        date_to_log_fullpath_str = files_dir + date_to_log_str + '/' + file_name
        try:
            pulse_df = pd.read_csv (date_to_log_fullpath_str, header=None, usecols=[0, 1])
            df_list.append(pulse_df)
            (rows, cols) = pulse_df.shape
            print('date getted: ' + date_to_log_str + \
                  ' entries: ' + str(rows))
        except:
            print('date not found: ' + date_to_log_str)
            continue
        
    # concatenate df trials
    # df = pd.concat(df_list, ignore_index=True)
    # if ten_min == False:
    #     # convert df index 0 to datetime
    #     # print("  Before conversion:")
    #     # print(df.info())
    #     df[0] = pd.to_datetime(df[0], format="%Y-%m-%d -- %H:%M")
    #     # print("  After conversion:")
    #     # print(df.info())
    #     # then group by hours
    #     df_group = df.groupby(pd.Grouper(key=0,freq='h'))
    #     df = df_group[1].sum().reset_index()
    #     print("  After grouped:")
    #     print(df.info())

    # concatenate df production    
    try:
        df = pd.concat(df_list, ignore_index=True)
        if ten_min == False:
            # convert df index 0 to datetime
            # print("  Before conversion:")
            # print(df.info())
            df[0] = pd.to_datetime(df[0], format="%Y-%m-%d -- %H:%M")
            # print("  After conversion:")
            # print(df.info())
            # then group by hours
            df_group = df.groupby(pd.Grouper(key=0,freq='h'))
            df = df_group[1].sum().reset_index()
            # print("  After grouped:")
            # print(df.info())
    except:
        df_err = 'dataframe errors on selected dates!'
        print(df_err)
        return df_err, None
    
    return None, df


if __name__ == "__main__":
    # check args for operation
    if len(sys.argv) != 3:
        print('use this script with format YYYYMMDD or YYYY-MM-DD: init_date end_date')
        sys.exit()

    # get the dates
    init_date_str = sys.argv[1]
    end_date_str = sys.argv[2]
    # test with ten minutes data
    # my_df = DataFrameAssembly(init_date_str, end_date_str)
    # test with hours data
    my_df_err, my_df = DataFrameAssembly(init_date_str, end_date_str, False)

    if isinstance (my_df, pd.DataFrame):
        print("\ndf first five rows")
        print(my_df.head())

        print("\ndf last five rows")
        print(my_df.tail())

        print("\ndf columns attr")
        print(my_df.columns)

        (rows, cols) = my_df.shape
        print('\ndf total entries: ' + str(rows))
    else:
        print('\nan error df getted for dates!!!')

