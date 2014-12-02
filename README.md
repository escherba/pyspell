pyspell
=======

A pure Python spelling module, based on Peter Norvig's spelling corrector (but with alternate word sets).

## Why?

TL;DR: Ease of installation, and improvements on Norvig's work.

[pyenchant](http://pythonhosted.org/pyenchant/) is great, no doubt, but it requires external C libraries.  If you're not on a *nix platform, get ready to be thoroughly annoyed and frustrated by trying to get them working in a purely 64-bit environment.  And what if you're not a developer, or don't have admin rights to your machine?  Same thing applies to [aspell](http://aspell.net/), only `aspell` hasn't been updated in...how long? :confused:

Obviously [Norvig's script](http://norvig.com/spell-correct.html), which we're going to start with, was only meant as a proof-of-concept.  Problem is, it's actually pretty great, save for the supplied data, `big.txt`.  Norvig just copied and pasted in random works from [Project Gutenberg](https://www.gutenberg.org/), boiler-place licensing text and all, and augmented that with words from the [British National Corpus](http://www.natcorp.ox.ac.uk/).  As a result, we see weird (to an American) things happen, such as "mom" be corrected to "mon". :confused:

## What's Here

* A re-implementation (ok, copy, LOL) of Norvig's proof-of-concept, in `pyspell.norvig.BasicSpellCorrector` (a.k.a. `BasicSpellCorrector`), with the abilty to return either the single best correction or the top _N_ suggestions (_N_ is user-specified).
    - The training data sets are explained in the `data/README.md`, and evaluation results are provided, below.

## Future Work

* Include additional development/testing data that contains pairs of errors and corrections that are the same, to verify that, when a correctly-spelled word is passed to `correct()` that same correctly-spelled word is returned.
* Expand `BasicSpellCorrector` with the work described in [Norvig's chapter in _Beautiful Data_](http://norvig.com/ngrams/).
* Incorporate in the `aspell` dictionaries as a fallback, creating a purely Python port of `aspell`.
* Ensure that this works with >= 2.7 and 3.x.

## Evaluation

The script `test/test_pyspell.py` will give you insight into how precision and recall are being computed.

<!--Currently, on the development set:

|                                                                     | Precision | Recall |
|---------------------------------------------------------------------|:---------:|:------:|
| Baseline (GNU aspell 0.60.6.1, `en` dict) [1]                       |    88.82% | 87.26% |
| `BasicSpellCorrector` with `big.txt`                                |    76.14% | 61.52% |
| `BasicSpellCorrector` with `en_ANC.txt.bz2`                         |    77.37% | 63.38% |
| `BasicSpellCorrector` with `big.txt`, top 10 suggestions [2]        |    79.66% | 75.49% |
| `BasicSpellCorrector` with `en_ANC.txt.bz2`, top 10 suggestions [2] |    80.42% | 76.10% |-->

Currently, on the testing set:

|                                                                     | Precision | Recall |
|---------------------------------------------------------------------|:---------:|:------:|
| Baseline (GNU aspell 0.60.6.1, `en` dict) [1]                       |    94.82% | 90.89% |
| `BasicSpellCorrector` with `big.txt`                                |    80.21% | 68.05% |
| `BasicSpellCorrector` with `en_ANC.txt.bz2`                         |    85.62% | 72.50% |
| `BasicSpellCorrector` with `big.txt`, top 10 suggestions [2]        |    82.68% | 80.18% |
| `BasicSpellCorrector` with `en_ANC.txt.bz2`, top 10 suggestions [2] |    87.33% | 83.93% |

[1] `en` includes American, British, and Canadian English.  Also, since `aspell` returns multiple suggestions per error, if the desired correction is on the list of corrections, we count this as a true positive.

[2] Evaluation was done by asking `BasicSpellCorrector` to return the top 10 suggestions per error, or all of the suggestions, whichever was less.
