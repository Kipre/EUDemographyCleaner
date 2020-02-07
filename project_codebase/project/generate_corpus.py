import os
from os import path

import numpy
import pandas
corpus_path = "./data/corpus_splits/"
if not path.exists(corpus_path):
    os.mkdir(corpus_path)

#Loading dataset
df = pandas.read_csv("data/requests.csv", sep=";")
df = df[["motif", "demande"]]
df["motif"] = "__label__" + df["motif"].astype("str")
df["motif"] = df["motif"].str.replace(" ","_",regex=False)

# Number of splits
num_splits = 10


for split in range(num_splits):
    base_path = corpus_path + "split_" + str(split)
    if not path.exists(base_path):
        os.mkdir(base_path)

    train, test, dev = numpy.split(df.sample(frac=1), [int(.7 * len(df)), int(.9 * len(df))])  # type: # DataFrame

    train.to_csv(base_path + "/train.txt", index=False, sep="\t", header=False)
    test.to_csv(base_path + "/test.txt", index=False, sep="\t", header=False)
    dev.to_csv(base_path + "/dev.txt", index=False, sep="\t", header=False)
