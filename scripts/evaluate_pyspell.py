from __future__ import print_function, division

import sys
import argparse
import pandas
from pyspell import BasicSpellCorrector


def evaluate(df, data_path, suggestions=0):
    pysp = BasicSpellCorrector(data_path)
    df["suggested"] = df["error"].apply(lambda x: pysp.correct(x, suggestions=suggestions))

    if suggestions > 0:
        df["true positive"] = df.apply(
            lambda x: x["correct form"] in x["suggested"] and x["error"] not in x["suggested"],
            axis=1)
        df["wrong suggestion"] = df.apply(
            lambda x: x["correct form"] not in x["suggested"] and x["error"] not in x["suggested"],
            axis=1)
        df["no suggestion"] = df.apply(
            lambda x: x["correct form"] not in x["suggested"] and x["error"] in x["suggested"],
            axis=1)

        # suggested corrections contain the expected correction and not the error
        corrected_correctly = df[df["true positive"] == True]
        # suggested corrections don't contain the error or the expected correction, but are assumed
        # to contain at least one correct suggestion
        wrong_suggestions = df[df["wrong suggestion"] == True]
        # suggested corrections don't contain the expected correction but they do contain the error
        no_suggestions = df[df["no suggestion"] == True]
    else:
        # error was corrected to the expected correction
        corrected_correctly = df[df["correct form"] == df["suggested"]]
        # error was corrected to something else
        wrong_suggestions = df[df["correct form"] != df["suggested"]]
        wrong_suggestions = wrong_suggestions[wrong_suggestions["suggested"] != wrong_suggestions["error"]]
        # error was corrected (or rather, not corrected at all) to itself
        no_suggestions = df[df["suggested"] == df["error"]]

    print("correct suggestions: {}".format(len(corrected_correctly)))
    print("wrong suggestions: {}".format(len(wrong_suggestions)))
    print("no suggestions: {}".format(len(no_suggestions)))

    # Note: false positive calculation here is not precisely correct because
    # we're not taking into account values that are ground-truth negative
    # (without a spelling error) but are only looking at the correctness of the
    # replacements (if correct, have true positive, if same as before have
    # false negative, if incorrect have "false positive")
    true_positives = len(corrected_correctly)
    false_positives = len(wrong_suggestions)
    false_negatives = len(no_suggestions)

    recall = true_positives / (true_positives + false_negatives)
    precision = true_positives / (true_positives + false_positives)

    print("recall: {0:.2%}".format(recall))
    print("precision: {0:.2%}".format(precision))


def assemble_test_data(path_to_Birkbeck_subset):
    import urllib2

    df = pandas.io.parsers.read_csv(path_to_Birkbeck_subset, index_col="index")
    tab0 = urllib2.urlopen("http://aspell.net/test/common-all/batch0.tab")
    for line in tab0:
        (error, correction) = line.strip().split("\t")
        df = df.append({"error": error,
                        "correct form": correction,
                        "edit distance": None},
                       ignore_index=True)
    print("{} test cases.\n".format(len(df)))
    return df


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--evaluate_dev_set", action="store_true")
    parser.add_argument("-t", "--evaluate_test_set", action="store_true")
    parser.add_argument("-s", "--number_of_suggestions", type=int,
                        help="Look in the top N suggested corrections for the right one.",
                        default=0)
    namespace = parser.parse_args(args)
    return namespace


def run(args):
    if not(args.evaluate_dev_set or args.evaluate_test_set) or (args.evaluate_dev_set and args.evaluate_test_set):
        sys.stderr.write("Usage: '-t' for testing data, '-d' for development data.\n")
        sys.exit(1)

    if args.evaluate_dev_set:
        eval_data = pandas.io.parsers.read_csv(
            "data/Birkbeck_subset_spelling_errors_development_set.csv",
            index_col="index")
    elif args.evaluate_test_set:
        eval_data = assemble_test_data(
            "data/Birkbeck_subset_spelling_errors_testing_set.csv")

    for data_file in ["en_ANC.txt.bz2", "big.txt"]:
        print(data_file)
        if args.number_of_suggestions > 0:
            evaluate(eval_data, "data/" + data_file, suggestions=args.number_of_suggestions)
        else:
            evaluate(eval_data, "data/" + data_file)
        print()


if __name__ == "__main__":
    run(parse_args())
