import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob



# Code modified from https://thispointer.com/count-number-of-zeros-in-pandas-dataframe-column/
# Replace -999 with 0 and count how many times it appears per column
def count_and_replace(df, column):
    nan_count = 0
    if column != 'Zone':
        df.loc[df[column] < -990, column] = -999
    if -999 in set(df[column]):
        nan_count = df[column].value_counts()[-999]
    df[column] = df[column].replace(-999, 0)
    return nan_count


def read_well_logs():
    # Code modified from https://www.geeksforgeeks.org/how-to-read-all-csv-files-in-a-folder-in-pandas/

    # use glob to get all the csv files 
    # in the folder
    path = os.getcwd()
    joined_csv = glob.glob(os.path.join(path, "*.csv"))

    df = pd.concat(map(pd.read_csv, joined_csv), ignore_index=True)

    # Code copied from https://www.geeksforgeeks.org/iterating-over-rows-and-columns-in-pandas-dataframe/
    column_names = df.columns.values.tolist()
    nan_count_list = []
    for column in column_names:
        nan_count = count_and_replace(df, column)
        nan_count_list.append(nan_count)


    
    # print the content
    print('Content:')
    print(df)

    for idx in range(len(column_names)):
        if nan_count_list[idx] != 0:
            print(column_names[idx], '--- nan count:', nan_count_list[idx])
        
    print()
    print()
    print(df.describe().T)
    print(path)
    #df.to_csv(r'C:\Users\benja\Documents\2022 PGE Hackathon\Longhorn_Energy_Club\Well_Log/df.csv')

    (sum(nan_count_list)/len(df)).plot(kind = 'bar')
    plt.subplots_adjust(left=0.0, bottom=0.0, right=3.2, top=1.2, wspace=0.2, hspace=0.2) # plot formatting
    plt.xlabel('Feature'); plt.ylabel('Percentage of Missing Records'); plt.title('Data Completeness')
    plt.ylim([0,1.0])
    plt.show()


def main():
    read_well_logs()


if __name__ == '__main__':
    main()