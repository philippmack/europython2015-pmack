import matplotlib.pyplot as plt
import glob
import pandas as pd
import argparse
from matplotlib import cm

def plot_working(df):

    #SURPLUS;OOS;QUANTILE;VERSION_ID
    df = df.sort('OOS')
    df.set_index('OOS',inplace=True)
    ax = df.groupby('VERSION_ID')['SURPLUS'].plot(labels='VERSION_ID', style='o-')

    plt.ylabel('EXCESS RATE')
    plt.xlabel('OOS RATE')
    plt.legend()
    plt.savefig('Working_Curve.png')

def plot_get_all_files(files):
    file_list = glob.glob(files)
    df_all = []
    for I in file_list:
        df_all.append(pd.read_csv(I,sep=';'))
    df_plot = pd.concat(df_all)
    plot_working(df_plot)

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument("-f","--files", help="files to plot", type=str)
   args = parser.parse_args()

   plot_get_all_files(args.files)

