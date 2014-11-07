pyspell
=======

A pure Python spelling module, based on Peter Norvig's spelling corrector (but with alternate word sets).

## Why?

TL;DR: Ease of installation, and improvements on Norvig's work.

[pyenchant](http://pythonhosted.org/pyenchant/) is great, no doubt, but it requires external C libraries.  If you're not on a *nix platform, get ready to be thoroughly annoyed and frustrated by trying to get them working in a purely 64-bit environment.  And what if you're not a developer, or don't have admin rights to your machine?  Same thing applies to [aspell](http://aspell.net/), only `aspell` hasn't been updated in...how long? :confused:

Obviously [Norvig's script](http://norvig.com/spell-correct.html), which we're going to start with, was only meant as a proof-of-concept.  Problem is, it's actually pretty great, save for the supplied data, `big.txt`.  Norvig just copied and pasted in random works from [Project Gutenberg](https://www.gutenberg.org/), boiler-place licensing text and all, and augmented that with words from the [British National Corpus](http://www.natcorp.ox.ac.uk/).  As a result, we see weird (to an American) things happen, such as "mom" be corrected to "mon". :confused:

## What's Here

* A re-implementation (ok, copy, LOL) of Norvig's proof-of-concept, in `pyspell.norvig.BasicSpellCorrector` (a.k.a. `BasicSpellCorrector`).
    - The training data sets are explained in the `data/README.md`, and evaluation results are provided, below.

## Future Work

* Expand `BasicSpellCorrector` with the work described in [Norvig's chapter in _Beautiful Data_](http://norvig.com/ngrams/).
* Incorporate in the `aspell` dictionaries as a fallback, creating a purely Python port of `aspell`.
* Ensure that this works with >= 2.7 and 3.x.

## Evaluation

The script `test/test_pyspell.py` will give you insight into how precision and recall are being computed.

Currently, on the development set:

|                                             | Precision | Recall |
|---------------------------------------------|:---------:|:------:|
| Baseline (GNU aspell 0.60.6.1)              |           |        |
| `BasicSpellCorrector` with `big.txt`        |    76.14% | 61.52% |
| `BasicSpellCorrector` with `en_ANC.txt.bz2` |    77.37% | 63.38% |
