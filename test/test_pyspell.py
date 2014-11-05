import sys

import pandas

from pyspell import BasicSpellCorrector


def evaluate(df, data_path):
    true_positives = 0 # error was corrected to the expected correction
    false_negatives = 0 # error was corrected to something else
    false_positives = 0 # error was corrected to itself

    pysp = BasicSpellCorrector(data_path)
    df["correction from pyspell"] = df["error"].apply(lambda x : pysp.correct(x))
    print df


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
