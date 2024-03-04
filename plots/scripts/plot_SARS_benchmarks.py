#!/usr/bin/python3

# Import the necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import json, os
from matplotlib import gridspec
import matplotlib.text as mtext
import argparse


# library &amp; dataset
import seaborn as sns


Description = """
Plot the experimental results

    by Rahul Varki
"""

def save_plot(df_rbr,df_br,outdir,plot,sample,rule):

    px = 1/plt.rcParams['figure.dpi']

    #fig = plt.figure(figsize=(6.3, 4.7))
    plt.plot(df_br["ref"], df_br[plot], marker = 's', color = "royalblue", label='BigRePair', linewidth=2.0, markersize=8.0)
    plt.plot(df_rbr["ref"], df_rbr[plot], marker = 'D', color = "darkorange", label='Re$^2$Pair', linewidth=2.0, markersize=8.0)
    plt.xticks(df_rbr["ref"])
    plt.xticks(fontsize='x-large')
    plt.yticks(fontsize='x-large')
    plt.grid()
    plt.legend()
    plt.legend(loc='upper left', fontsize='x-large')
    
    if plot == "sec":
        plt.ylabel('Wall-clock time (s)', fontsize='x-large')
        plt.xlabel('Haplotypes (x1000)', fontsize='x-large')
    if plot == "cpu_time":
        plt.ylabel('CPU time (s)', fontsize='x-large')
        plt.xlabel('Haplotypes (x1000)', fontsize='x-large')
    if plot == "max_rss":
        plt.ylabel('Maximum Resident Set Size (MiB)', fontsize='x-large')
        plt.xlabel('Haplotypes (x1000)', fontsize='x-large')

    # if sample == "chr1":
    #     plt.title('Chr1')
    # if sample == "SARS-CoV2":
    #     plt.title('SARS-CoV2')
    # if sample == "T2T":
    #     plt.title('T2T')


    plt.tight_layout()

    # Save the figure
    outfile_name = os.path.join(outdir,sample + "." + rule + "." + plot)
    print("Saving {}".format(outfile_name + ".png"))
    plt.savefig(outfile_name + ".png", dpi=300, bbox_inches='tight')#,  additional_artists=art, bbox_inches="tight")#bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.savefig(outfile_name + ".pdf", bbox_inches='tight')#,  additional_artists=art, bbox_inches="tight")#bbox_extra_artists=(lgd,), bbox_inches='tight')

    plt.close()



def main():
    parser = argparse.ArgumentParser(description=Description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-r', '--rbr', help='Path to the rbr benchmark csv file', type=str, dest="rbr", required=True)
    parser.add_argument('-b', '--br', help='Path to the br benchmark csv file', type=str, dest="br", required=True)
    parser.add_argument('-o', '--outdir', help='Path to the output directory', type=str, dest="outdir", required=True)
    args = parser.parse_args()

    rbr_csv = args.rbr
    br_csv = args.br
    outdir = args.outdir

    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    print("Loading {}".format(args.rbr))
    df_rbr = pd.read_csv(rbr_csv)
    print("Loading {}".format(args.br))
    df_br = pd.read_csv(br_csv)

    # Take the filename parts of the rbr file for the output file
    filename_parts = os.path.basename(rbr_csv).split(".")
    sample = filename_parts[0]
    rule = filename_parts[2]

    print(df_rbr)

    for plot in ["sec","cpu_time","max_rss"]:  
        save_plot(df_rbr,df_br,outdir,plot,sample,rule)




if __name__ == '__main__':
	main()
