import os
import argparse
import pandas as pd

# CSV file format: A,C,G,T,actual_nuc,chromosome,gene_name,genome_pos

chromosomes = ["X", "Y", "2L", "2R", "3L", "3R", "4", "dmel_mitochondrion_genome"]

def load_file(f):
    print "Loading: " + f
    data = pd.read_hdf(f, "genome", mode="r")
    print 'Retrieved ' + str(len(data)) + ' rows'
    # removes rows with chromosome values other than those listed in chromosomes list
    key = f[0:5]
    data = data.rename(columns={'A': key + '_A', 'G': key + '_B', 'C': key + '_C', 'T': key + '_T'})
    reduced = data[data.chromosome.isin(chromosomes)]
    print 'Relevant ' + str(len(reduced)) + ' rows'
    return reduced

def merge(data1, data2):
    # combine data1 and data2 and return the result
    print 'merging...'
    if (data1 is None):
        return data2
    data2 = pd.merge(right=data1, left=data2,
        how='outer', on=['chromosome', 'genome_pos', 'gene_name', 'actual_nuc'],
        left_index=False, right_index=False, sort=True, copy=False)
    return data2

def iterate(pathToCSVDir):
  file_list = os.listdir(pathToCSVDir)
  file_list = sorted([f for f in file_list if f.endswith(".h5")], key=lambda f: f.lower())
  previous = None
  for file in file_list:
      print(file)
      data = load_file(file)
      previous = merge(previous, data)
  return previous
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path-to-csv-dir", dest='path', type=str)
    args = parser.parse_args()
    r = iterate(args.path)
    print 'saving...'
    r.to_hdf("result.h5", key="genome", mode="w")


