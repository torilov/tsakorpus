from flask import Flask
from elasticsearch.exceptions import ConnectionError
import os
import re
import random

SETTINGS_DIR = '../conf'
MAX_PAGE_SIZE = 100     # maximum number of sentences per page
MIN_TOTAL_FREQ_WORD_QUERY = 2000  # minimal number of processed tokens after which
                                  # the word/lemma search involving multiple words
                                  # may be stopped due to timeout
sessionData = {}        # session key -> dictionary with the data for current session
random.seed()

rxIndexAtEnd = re.compile('_[0-9]+$')

# Read settings before we import anything else. Many modules
# imported after this point reference the settings object,
# therefore it has to exist at import time.
from .corpus_settings import CorpusSettings
settings = CorpusSettings()
settings.load_settings(os.path.join(SETTINGS_DIR, 'corpus.json'),
                       os.path.join(SETTINGS_DIR, 'categories.json'))

# Continue with module imports. Beware that there are other
# circular import issues, so the order of imported modules
# should not change.
from search_engine.client import SearchClient
from .response_processors import SentenceViewer
localizations = {}
sc = SearchClient(SETTINGS_DIR, settings)
sentView = SentenceViewer(settings, sc)
sc.qp.rp = sentView
sc.qp.wr.rp = sentView

try:
    settings.corpus_size = sc.get_n_words()  # size of the corpus in words
    for lang in settings.languages:
        # number of word types for each frequency rank
        settings.word_freq_by_rank.append(sentView.extract_cumulative_freq_by_rank(sc.get_word_freq_by_rank(lang)))
        # number of lemmata for each frequency rank
        settings.lemma_freq_by_rank.append(sentView.extract_cumulative_freq_by_rank(sc.get_lemma_freq_by_rank(lang)))
    settings.ready_for_work = True
except ConnectionError:
    # Elasticsearch is down
    settings.corpus_size = 0
    for lang in settings.languages:
        settings.word_freq_by_rank.append({})
        settings.lemma_freq_by_rank.append({})
sc.qp.maxFreqRank = max(max(len(settings.word_freq_by_rank[i]), len(settings.lemma_freq_by_rank[i]))
                        for i in range(len(settings.languages))) + 1


app = Flask(__name__)
app.secret_key = 'kkj6hd)^js7#dFQ'

app.config.update(dict(
    LANGUAGES=settings.interface_languages,
    BABEL_DEFAULT_LOCALE=settings.default_locale
))

from .views import *
