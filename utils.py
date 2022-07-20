import pandas as pd
import os
import glob


def print_dataframe(df):
    pd.options.display.width = None
    pd.options.display.max_columns = None
    pd.set_option('display.max_rows', 3000)
    pd.set_option('display.max_columns', 3000)
    print(df)


def reset_data():
    files = glob.glob('data/*.csv')
    files += glob.glob('*.yaml')
    files += glob.glob('test/*.csv')
    files += glob.glob('*.json')
    #print("FILES:", files)
    for f in files:
        os.remove(f)
# python -c "from utils import *;reset_data()"


def csv_to_dict(file_path):

    dict_from_csv = pd.read_csv(file_path, encoding='latin-1', delimiter=';', decimal=',', index_col=0, ).to_dict()

    return dict_from_csv
