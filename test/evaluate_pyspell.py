from __future__ import print_function, division

import sys
import argparse

import pandas

from pyspell import BasicSpellCorrector


def evaluate(df, data_path, suggestions=0):
    pysp = BasicSpellCorrector(data_path)
    df["correction from pyspell"] = df["error"].apply(lambda x : pysp.correct(x, suggestions=suggestions))

    if suggestions > 0:
        df["true positive"] = df.apply(lambda x : x["correct form"] in x["correction from pyspell"] and x["error"] not in x["correction from pyspell"],
                                       axis=1)
        df["false negative"] = df.apply(lambda x : x["correct form"] not in x["correction from pyspell"] and x["error"] not in x["correction from pyspell"],
                                        axis=1)
        df["false positive"] = df.apply(lambda x : x["correct form"] not in x["correction from pyspell"] and x["error"] in x["correction from pyspell"],
                                        axis=1)

        # suggested corrections contain the expected correction and not the error
        true_positives = df[df["true positive"] == True]
        # suggested corrections don't contain the error or the expected correction, but are assumed to contain at least one correct suggestion
        false_negatives = df[df["false negative"] == True]
        # suggested corrections don't contain the expected correction but they do contain the error
        false_positives = df[df["false positive"] == True]
    else:
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


def assemble_test_data(path_to_Birkbeck_subset):
    import urllib2
    
    df = pandas.io.parsers.read_csv(path_to_Birkbeck_subset, index_col="index")
    tab0 = urllib2.urlopen("http://aspell.net/test/common-all/batch0.tab")
    for line in tab0:
        (error, correction) = line.strip().split("\t")
        df = df.append({"error" : error, "correct form" : correction, "edit distance" : None},
                       ignore_index=True)
    print(str(len(df)) + " test cases.")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--evaluate_dev_set", action="store_true")
    parser.add_argument("-t", "--evaluate_test_set", action="store_true")
    parser.add_argument("-s", "--number_of_suggestions", 
                        help="Look in the top N suggested corrections for the right one.",
                        default=0)
    args = parser.parse_args()

    if not(args.evaluate_dev_set or args.evaluate_test_set) or (args.evaluate_dev_set and args.evaluate_test_set):
        sys.stderr.write("Usage: '-t' for testing data, '-d' for development data.\n")
        sys.exit(1)
        
    if args.evaluate_dev_set:
        eval_data = pandas.io.parsers.read_csv("data/Birkbeck_subset_spelling_errors_development_set.csv", 
                                               index_col="index")
    elif args.evaluate_test_set:
        eval_data = assemble_test_data("data/Birkbeck_subset_spelling_errors_testing_set.csv")

    for data_file in ["en_ANC.txt.bz2", "big.txt"]:
        print(data_file)
        if args.number_of_suggestions > 0:
            evaluate(eval_data, "data/" + data_file, suggestions=args.number_of_suggestions)
        else:
            evaluate(eval_data, "data/" + data_file)
        print()
