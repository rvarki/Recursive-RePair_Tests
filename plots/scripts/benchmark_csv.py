#!/usr/bin/env python3
import argparse
import os
import pandas as pd
from pathlib import Path

Description = """
Generate CSV file needed to generate time and memory usage plots
   by Rahul Varki
"""

def main():
    parser = argparse.ArgumentParser(description=Description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', help='Path to benchmarks.txt', type=str, dest="input", required=True)
    parser.add_argument('-c', '--current_dir', help='Path to current directory', type=str, dest="current_dir", required=True)
    parser.add_argument('-o', '--output', help='Path to output csv file', type=str, dest="output", required=True)
    args = parser.parse_args()

    in_file = args.input
    curr_dir = args.current_dir
    out_file = args.output
    out_dir = os.path.dirname(args.output)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(args.input):
        print("Error: file {} does not exists!".format(args.input))
        return

    sample = []
    tool = []
    ref = []
    rule = []
    s = []
    cpu_time = []
    max_rss = []
    
    def lines_that_contain(string, fp):
        return [line for line in fp if string in line]

    with open(out_file, "w") as outfile:
        with open(in_file, "r") as infile:
            for file in infile:
                abs_filepath = os.path.abspath(os.path.join(curr_dir,file.strip()))
                if (os.path.exists(abs_filepath)):
                    filename_parts = os.path.basename(abs_filepath.strip()).split(".")
                    df = pd.read_csv(abs_filepath.strip(), sep='\t')
                    sample.append(filename_parts[0])
                    tool.append(filename_parts[2])
                    ref.append(filename_parts[1])
                    rule.append(filename_parts[3])
                    s.append(df.iat[0,0])
                    cpu_time.append(df.iat[0,9])
                    max_rss.append(df.iat[0,2])

        d = {'sample': sample, 'tool': tool, 'ref': ref, 'rule': rule, 'sec': s, 'cpu_time': cpu_time, 'max_rss': max_rss}
        df = pd.DataFrame(data = d)
        df.to_csv(outfile)

if __name__ == '__main__':
    main()

