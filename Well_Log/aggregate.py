import pandas as pd
import numpy as np
import os
import glob



# Code modified from https://thispointer.com/count-number-of-zeros-in-pandas-dataframe-column/
# Replace -999 with 0 and count how many times it appears per column
def count_and_replace(df, column):
    nan_count = 0
    if -999 in set(df[column]):
        nan_count = df[column].value_counts()[-999]
    df[column] = df[column].replace(-999, 0)
    return nan_count


def read_well_logs():
    # Code modified from https://www.geeksforgeeks.org/how-to-read-all-csv-files-in-a-folder-in-pandas/

    # use glob to get all the csv files 
    # in the folder
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))
  
    # loop over the list of csv files
    for f in csv_files:

    
        # read the csv file
        df = pd.read_csv(f)



        # print filename
        print('File Name:', f.split("\\")[-1])
    

        # Code copied from https://www.geeksforgeeks.org/iterating-over-rows-and-columns-in-pandas-dataframe/
        column_names = df.columns.values.tolist()
        nan_count = 0
        for column in column_names:
            nan_count = count_and_replace(df, column)
            print(column, nan_count)

        # print the content
        print('Content:')
        print(df)
        print()
        print()




def main():
    read_well_logs()


if __name__ == '__main__':
    main()