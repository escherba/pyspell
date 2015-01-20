import re
import logging
from itertools import chain
from collections import Counter
from pyspell.io import open_gz, read_text_resource


logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ASCII_EN_PATTERN = re.compile(u'\\b[a-z]+\\b', re.UNICODE | re.IGNORECASE)
REPLACE_MAP = {
    # replace fancy single apostrophes
    u"\u2018": u"'", u"\u2019": u"'", u"\u201a": u"'", u"\u201b": u"'", u"\u275b": u"'", u"\u275c": u"'",
    # replace fancy double apostrophes
    u"\u201c": u'"', u"\u201d": u'"', u"\u201e": u'"', u"\u201f": u'"', u"\u275d": u'"', u"\u275e": u'"',
    # replace underscores with spaces
    u"_": u" "
}
REPLACE_TRANSLATE = {ord(k): ord(v) for k, v in REPLACE_MAP.iteritems()}


class BasicSpellCorrector(object):
    '''
    http://norvig.com/spell-correct.html
    '''

    def __init__(self, words_data_file, alphabet=ALPHABET, pattern=ASCII_EN_PATTERN):
        self.word_pattern = pattern
        self.alphabet = alphabet
        with open_gz(words_data_file, 'r') as fh:
            lines = read_text_resource(fh)
            self.nwords = self.train(self.words(lines))
        self.word_value = self.create_key_lambda()

    def words(self, text):
        for line in text:
            line = line.translate(REPLACE_TRANSLATE)
            for match in self.word_pattern.finditer(line):
                yield match.group().lower()

    def train(self, features):
        LOG.info("Training...")
        model = Counter(features)
        LOG.info("Finished training with %d features", len(model))
        return model

    def edits1(self, word):
        splits = [(word[:i], word[i:]) for i in xrange(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts = [a + c + b for a, b in splits for c in self.alphabet]
        return set(chain(deletes, transposes, replaces, inserts))

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.nwords)

    def known(self, words):
        return set(w for w in words if w in self.nwords)

    def create_key_lambda(self, bias=None):
        """Allows to overlay bias for certain words w/o modifying the main dictionary"""
        if bias:
            bias_get = getattr(bias, 'get')
            nwords_get = self.nwords.get
            return lambda x: bias_get(x, 0) + nwords_get(x, 0)
        else:
            return self.nwords.get

    @property
    def bias(self):
        return self._bias

    @bias.setter
    def bias(self, value):
        self._bias = value
        self.word_value = self.create_key_lambda(value)

    def correct(self, word, suggestions=0):
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        return sorted(candidates, key=self.word_value, reverse=True)[0:suggestions] \
            if suggestions > 0 \
            else max(candidates, key=self.word_value)
