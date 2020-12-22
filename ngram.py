from collections import defaultdict
import random
import reviewGetter as rg

pages = rg.pages


class Ngram:
    def __init__(self, _n_range=(2, 3)):
        self.n_begin, self.n_end = _n_range
        self.ngram_counter = defaultdict(int)

    def __call__(self):
        pass

    def set_ngram_counter(self, min_count=0):
        if min_count <= 0:
            _ngram_counter = self.ngram_counter
        else:
            _ngram_counter = {
                ngram: count for ngram, count in self.ngram_counter.items()
                if count >= min_count
            }
        _ngram_counter = {k: v for k, v in sorted(_ngram_counter.items(), key=(lambda x: x[1]), reverse=True)}
        return _ngram_counter

    def set_ngram(self, pages):
        def append_ngram(sent, n_range=(3, 3)):
            def ngram_to_key(_ngram):
                key = ""
                for item in _ngram:
                    word, pos = item
                    key += "/" + word + "-" + pos
                return key

            def to_ngrams(_sent, _n):
                ngrams = []
                for b in range(0, len(_sent) - _n + 1):
                    ngrams.append(ngram_to_key(_sent[b:b + _n]))
                return ngrams

            n_begin, n_end = n_range
            for n in range(n_begin, n_end + 1):
                for ngram in to_ngrams(sent, n):
                    self.ngram_counter[str(ngram)] += 1
                    # print(str(ngram))

        temp = []

        for comments in pages:
            for comment in comments:
                for sent in comment['morphology']:
                    for mph in sent:
                        word = mph[0]
                        pos = mph[1]
                        if pos in ["XR", "VA", "VV", "NNG", "MAG"] or word in ['안', '않']:
                            temp.append(mph)
                        if pos[0] in ["S", "U"] or pos.startswith("EF") or pos == "ECE":
                            append_ngram(temp)
                            temp = []
                    append_ngram(temp)
                    temp = []

    def select_ngram_noun(self, stems):
        _list = {key: value for key, value in self.ngram_counter.items() if any([s in key for s in stems])}

        ngrams_selected = {}
        for stem in stems:
            ngrams_has_stem = {ngram: value for ngram, value in _list.items() if "/" + stem + "-NNG" in ngram}
            if len(ngrams_has_stem) == 0:
                continue
            max_index = max(ngrams_has_stem, key=ngrams_has_stem.get)
            ngrams_max = [k for k, v in ngrams_has_stem.items() if v == ngrams_has_stem[max_index]]
            ran_index = random.randint(0, len(ngrams_max) - 1)

            ngram = ngrams_max[ran_index]
            ngrams_selected[ngram] = stems[stem]
        return ngrams_selected

    def get_only_stem(self, ngrams):
        only_stem = {}
        for ngram in ngrams:
            pos = ["XR", "VA", "VV", "NNG", "MAG", "VXV"]
            stems = ngram.replace('/', '')
            stems = stems.replace('-', ' ')
            for p in pos:
                stems = stems.replace(p, '')
            only_stem[stems] = ngrams[ngram]
        return only_stem


if __name__ == '__main__':
    ngram = Ngram()
    ngram.set_ngram(pages)
    ngram_counter = ngram.set_ngram_counter()
    print(ngram_counter)
