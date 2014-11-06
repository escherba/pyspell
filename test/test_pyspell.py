from __future__ import print_function, division

import sys

import pandas

from pyspell import BasicSpellCorrector


def evaluate(df, data_path):
    pysp = BasicSpellCorrector(data_path)
    df["correction from pyspell"] = df["error"].apply(lambda x : pysp.correct(x))

    # error was corrected to the expected correction
    true_positives = df[df["correct form"] == df["correction from pyspell"]]
    # error was corrected to something else
    false_negatives = df[df["correct form"] != df["correction from pyspell"]]
    false_negatives = false_negatives[false_negatives["correction from pyspell"] != false_negatives["error"]]
    # error was corrected (or rather, not corrected at all) to itself
    false_positives = df[df["correction from pyspell"] == df["error"]]

    print("true positives = " + str(len(true_positives)))
    print("false negatives = " + str(len(false_negatives)))
    print("false positives = " + str(len(false_positives)))

    precision = len(true_positives) / (len(true_positives) + len(false_positives))
    recall = len(true_positives) / (len(true_positives) + len(false_negatives))

    print("precision = " + str(precision * 100))
    print("recall = " + str(recall * 100))


if __name__ == "__main__":
    if sys.argv[1] == "-d":
        eval_data = pandas.io.parsers.read_csv("data/Birkbeck_subset_spelling_errors_development_set.csv", 
                                               index_col="index")
    elif sys.argv[1] == "-t":
        eval_data = pandas.io.parsers.read_csv("data/Birkbeck_subset_spelling_errors_testing_set.csv",
                                               index_col="index")
    else:
        sys.stderr.write("Usage: '-t' for testing data, '-d' for development data.\n")
        sys.exit(1)

    for data_file in ["en_ANC.txt.bz2"]:
        evaluate(eval_data, "data/" + data_file)
