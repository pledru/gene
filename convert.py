import os
import argparse
import pandas as pd

def convert(file):
    print(file)
    new_file = file.replace(".csv", ".h5")
    print(new_file)
    cvs = pd.read_csv(file, sep=",", index_col=False, header=0,
                      dtype={"genome_pos": int, "A": int, "C": int, "G": int, "T": int,
                      "actual_nuc": str, "chromosome": str, "gene_name": str})
    cvs.to_hdf(new_file, key="genome", mode="w")

def convertAll(dir):
    file_list = os.listdir(dir)
    file_list = sorted([f for f in file_list if f.endswith(".csv")], key=lambda f: f.lower())
    for file in file_list:
        convert(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path-to-csv-dir", dest='path', type=str)
    args = parser.parse_args()
    convertAll(args.path)
