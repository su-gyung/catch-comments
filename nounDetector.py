from collections import defaultdict
from collections import Counter
import math
import reviewGetter as rg


class NounDetector:
    def __init__(self, num=10):
        self.noun_n = {}
        self.noun_p = {}
        self.top_num = num
        self.top_n = {}
        self.top_p = {}

    def __call__(self):
        pass

    def count_stems(self, pages):
        def is_positive_comment(_score):
            return bool(_score > 2)

        noun_n = defaultdict(int)
        noun_p = defaultdict(int)
        for comments in pages:
            for comment in comments:
                score = int(comment['score'])
                is_positive = is_positive_comment(score)
                if comment['like'].isdigit():
                    like = int(comment['like'])
                else:
                    like = 0

                inc = 1 + math.log(like+1)

                for sent in comment['morphology']:
                    for mph, pos in sent:
                        if pos == 'NNG':
                            if is_positive:
                                noun_p[mph] += inc
                            else:
                                noun_n[mph] += inc
        noun_n = {k: v for k, v in sorted(noun_n.items(), key=(lambda x: x[1]), reverse=True)}
        noun_p = {k: v for k, v in sorted(noun_p.items(), key=(lambda x: x[1]), reverse=True)}

        noun_n = {
            word: count for word, count in noun_n.items()
            if count > 1
        }
        noun_p = {
            word: count for word, count in noun_p.items()
            if count > 1
        }
        noun_p.pop('기', None)
        noun_p.pop('달', None)
        noun_p.pop('사용', None)
        noun_p.pop('재구', None)
        noun_p.pop('기재', None)
        noun_n.pop('기', None)
        noun_n.pop('달', None)
        noun_n.pop('사용', None)
        noun_n.pop('재구', None)
        noun_n.pop('기재', None)

        self.noun_n = noun_n
        self.noun_p = noun_p

        return noun_n, noun_p

    def get_top_noun(self):
        def get_unique_items(org, dup):
            result = {}
            for key, value in org.items():
                if key not in dup:
                    result[key] = value
            return result

        duplicate = []
        for key in self.noun_n:
            if key in self.noun_p:
                duplicate.append(key)

        noun_n_only = get_unique_items(self.noun_n, duplicate)
        noun_p_only = get_unique_items(self.noun_p, duplicate)
        top_n = dict(Counter(noun_n_only).most_common(self.top_num))
        for index, noun in enumerate(noun_n_only):
            if index == self.top_num - 1:
                value_last = noun_n_only[noun]
            if index == self.top_num:
                if value_last == noun_n_only[noun]:
                    keys = list(noun_n_only.keys())  # in python 3, you'll need `list(i.keys())`
                    values = list(noun_n_only.values())
                    for i in range(values.index(value_last), 10):
                        top_n.pop(keys[i])
                break

        top_p = dict(Counter(noun_p_only).most_common(self.top_num))
        for index, noun in enumerate(noun_p_only):
            if index == self.top_num - 1:
                value_last = noun_p_only[noun]
            if index == self.top_num:
                if value_last == noun_p_only[noun]:
                    keys = list(noun_p_only.keys())  # in python 3, you'll need `list(i.keys())`
                    values = list(noun_p_only.values())
                    for i in range(values.index(value_last), 10):
                        top_n.pop(keys[i])
                break
        self.top_n = top_n
        self.top_p = top_p
        return top_n, top_p

if __name__ == '__main__':
    pages = rg.pages

    nounDetector = NounDetector()
    nounDetector.count_stems(pages)

    top_n, top_p = nounDetector.get_top_noun()
    print(top_n)
    print(top_p)
