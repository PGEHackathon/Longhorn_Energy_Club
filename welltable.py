import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# Replaces -999 values with NaN
def make_nan(df):
    column_names = df.columns.values.tolist() # List of column names
    for column in column_names:
        if column != 'Zone': # Filled with strings so it can cause error
            df.loc[df[column] < -997, column] = np.nan # Replace -999 with NaN
        

def main():

    # Code modified from https://www.geeksforgeeks.org/how-to-read-all-csv-files-in-a-folder-in-pandas/
    # Get CSV files from Well_Log folder
    path = str(os.getcwd()) + '/Well_Log'
    all_logs = glob.glob(os.path.join(path, "WP*.csv"))

    # Store all well log info
    well_log_data = [ [0]*12 for _ in range(50) ]
    column_headers = [0] * 12

    # Loop through each log individually
    for well_log in range(len(all_logs)):
        df = pd.read_csv(all_logs[well_log])
        # well_name = all_logs[well_log].split('\\')[-1].split('.')[0]
        column_headers = df.columns
        column_headers = column_headers[:-1]

        # Convert -999 to NaN
        make_nan(df)

        # Get mean values for each well feature
        feature_means = df.mean(numeric_only=True).T

        # Append feature_means[index] into data_list[well][index]
        for feature in range(len(feature_means)):
            if feature != 12: # Don't have a mean for 'Zone' value
                well_log_data[well_log][feature] = feature_means[feature]
    
    # Create a dataframe with the mean values
    mean_df = pd.DataFrame(well_log_data, columns = column_headers)

    # Get path to csv file with production info
    production_csv_path = str(os.getcwd()) + '\Well_Head_and_Completion_Aggprod.csv'  
    production_df = pd.read_csv(production_csv_path)

    # Combine the dataframes
    combined_df = pd.concat([production_df, mean_df.set_index(production_df.index)], axis=1)
    print(combined_df)    

    print(combined_df.describe().T)


if __name__ == '__main__':
    main()