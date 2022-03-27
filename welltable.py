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
        
def fill_data(df, well_log, well_log_data):
    # Get mean values for each well feature
    feature_means = df.mean(numeric_only=True).T

    # Append feature_means[index] into data_list[well][index]
    for feature in range(len(feature_means)):
        if feature != 12: # Don't have a mean for 'Zone' value
            well_log_data[well_log][feature] = feature_means[feature]

def main():
    # Code modified from https://www.geeksforgeeks.org/how-to-read-all-csv-files-in-a-folder-in-pandas/
    # Get CSV files from Well_Log folder
    path = str(os.getcwd()) + '/Well_Log'
    all_logs = glob.glob(os.path.join(path, "WP*.csv"))

    # Store all well log info
    well_log_data = [ [0]*12 for _ in range(50) ]
    well_log_data_upper = [ [0]*12 for _ in range(50) ]
    well_log_data_lower = [ [0]*12 for _ in range(50) ]

    # Loop through each log individually
    for well_log in range(len(all_logs)):
        df = pd.read_csv(all_logs[well_log])
        # well_name = all_logs[well_log].split('\\')[-1].split('.')[0]
        column_headers = df.columns
        column_headers = column_headers[:-1]

        # Convert -999 to NaN
        make_nan(df)
        
        # Get upper and lower here
        upper_df = df.loc[df['Zone'] == 'Upper']
        lower_df = df.loc[df['Zone'] == 'Lower']

        fill_data(df, well_log, well_log_data)
        fill_data(upper_df, well_log, well_log_data_upper)
        fill_data(lower_df, well_log, well_log_data_lower)


    # Create a dataframe with the mean values
    mean_df = pd.DataFrame(well_log_data, columns = column_headers)
    mean_df_upper = pd.DataFrame(well_log_data_upper, columns = column_headers)
    mean_df_lower = pd.DataFrame(well_log_data_lower, columns = column_headers)


    # Get path to csv file with production info
    production_csv_path = str(os.getcwd()) + '\Well_Head_and_Completion_Aggprod.csv'  
    production_df = pd.read_csv(production_csv_path)

    # Combine the dataframes
    combined_df = pd.concat([production_df, mean_df.set_index(production_df.index)], axis=1)
    del combined_df['Completion']    
    print(combined_df)    
    print(combined_df.describe().T)

    combined_df_upper = pd.concat([production_df, mean_df_upper.set_index(production_df.index)], axis=1)
    del combined_df_upper['Completion']
    print(combined_df_upper)    
    print(combined_df_upper.describe().T)

    combined_df_lower = pd.concat([production_df, mean_df_lower.set_index(production_df.index)], axis=1)
    del combined_df_lower['Completion']
    print(combined_df_lower)    
    print(combined_df_lower.describe().T)

    sns.pairplot(combined_df_upper, vars = combined_df_upper.columns, markers = 'o')
    sns.pairplot(combined_df_lower, vars = combined_df_upper.columns, markers = 'o')



if __name__ == '__main__':
    main()