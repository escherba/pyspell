pyspell
=======

A pure Python spelling module, based on Peter Norvig's spelling corrector (but with alternate word sets).

## Why?

TL;DR: Ease of installation, and improvements on Norvig's work.

[pyenchant](http://pythonhosted.org/pyenchant/) is great, no doubt, but it requires external libraries.  If you're not on a *nix platform, get ready to be thoroughly annoyed and frustrated by trying to get them working in a purely 64-bit environment.  And what if you're not a developer, or don't have admin rights to your machine?  Same thing applies to [aspell](http://aspell.net/), only `aspell` hasn't been updated in...how long? :confused:

Obviously [Norvig's script](http://norvig.com/spell-correct.html), which we're going to start with, was only meant as a proof-of-concept.  Problem is, it's actually pretty great, save for the supplied data, `big.txt`.  Norvig just copied and pasted in random works from [Project Gutenberg](https://www.gutenberg.org/), boiler-place licensing text and all, and augmented that with words from the [British National Corpus](http://www.natcorp.ox.ac.uk/).  As a result, we see weird (to an American) things happen, such as "mom" be corrected to "mon". :confused:

## Goals

* Start with Norvig's script, but provide additional word sets; specifically an American English one based on the (open) [American National Corpus](http://www.americannationalcorpus.org/) and the [Brown Corpus](http://www.hit.uib.no/icame/brown/bcm.html).
* Incorporate in the `aspell` dictionaries as a fallback, creating a purely Python port of `aspell`.
* Will work with >= 2.7 and 3.x.
