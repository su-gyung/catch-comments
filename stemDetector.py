from collections import defaultdict
import math
import reviewGetter as rg


class StemExtractor:

    def __init__(self):
        self.alpha = 1
        self.beta = 0.01
        self.gamma = 0.001

        self.cnt = 0  # 리뷰에 나온 단어 전체 개수
        self.vocab_all = {}

        self.vocab = {}  # 긍정문에 나온 단어: 개수
        self.vocab_not = {}  # 부정문에 나온 단어: 개수

        self.cnt_vocab = 0  # 긍정문에 나온 단어 개수 (중복 제외)
        self.cnt_vocab_not = 0  # 부정문에 나온 단어 개수 (중복 제외)

        self.cnt_vocab_all = 0  # 리뷰 전체 긍정문에 나온 전체 단어 개수
        self.cnt_vocab_not_all = 0  # 리뷰 전체 부정문에 나온 전체 단어 개수

        self.vocab_p = {}  # 긍정리뷰(score > 2)에 나온 단어: 개수
        self.vocab_n = {}  # 부정리뷰(score <= 2)에 나온 단어: 개수

        self.cnt_comment_positive = 0  # 긍정리뷰 개수
        self.cnt_comment_negative = 0  # 부정리뷰 개수

    def __call__(self, sent):
        pass

    def is_positive_comment(self, score):
        return bool(score > 2)

    def count_stems(self, pages):
        stop_v = ["하", "이"]

        cnt = 0                 # 리뷰에 나온 단어 전체 개수
        vocab_all = {}

        vocab = defaultdict(int)              # 긍정문에 나온 단어: 개수
        vocab_not = defaultdict(int)          # 부정문에 나온 단어: 개수

        cnt_vocab = 0           # 긍정문에 나온 단어 개수 (중복 제외)
        cnt_vocab_not = 0       # 부정문에 나온 단어 개수 (중복 제외)

        cnt_vocab_all = 0       # 리뷰 전체 긍정문에 나온 전체 단어 개수
        cnt_vocab_not_all = 0   # 리뷰 전체 부정문에 나온 전체 단어 개수

        vocab_p = defaultdict(int)            # 긍정리뷰(score > 2)에 나온 단어: 개수
        vocab_n = defaultdict(int)            # 부정리뷰(score <= 2)에 나온 단어: 개수

        cnt_comment_positive = 0    # 긍정리뷰 개수
        cnt_comment_negative = 0    # 부정리뷰 개수

        temp = []
        is_not = False

        for comments in pages:
            for comment in comments:
                score = int(comment['score'])
                is_positive = self.is_positive_comment(score)
                if is_positive:
                    cnt_comment_positive += 1
                else:
                    cnt_comment_negative += 1
                if comment['like'].isdigit():
                    like = int(comment['like'])
                else:
                    like = 0
                for sent in comment['morphology']:
                    for mph in sent:
                        word = mph[0]
                        pos = mph[1]

                        # stop word
                        if pos[0] == "V" and word in stop_v:
                            continue

                        # 부정
                        if word == "안":
                            is_not = True
                            continue

                        # NNG
                        if pos == "NNG":
                            inc = 1 + math.log(like+1)
                            if is_positive:
                                vocab_p[word] += inc
                            else:
                                vocab_n[word] += inc

                        # 부정어
                        if word == "않":
                            is_not = True
                            continue

                        if pos in ["XR", "VA", "VV"]:
                            temp.append(mph)
                            if mph in vocab_all:
                                vocab_all[mph] = vocab_all.get(mph) + 1
                            else:
                                vocab_all[mph] = 1

                        # split 단위
                        if pos[0] in ["S", "U"] or pos.startswith("EF") or pos == "ECE":
                            inc = 1 + math.log(like+1)
                            if is_not:
                                is_not = False
                                cnt_vocab_not_all += 1
                                for t in temp:
                                    cnt += 1
                                    vocab_not[t] += inc
                            else:
                                cnt_vocab_all += 1
                                for t in temp:
                                    cnt += 1
                                    vocab[t] += inc
                            temp = []

        self.cnt = cnt
        self.vocab_all = vocab_all

        self.vocab = vocab
        self.vocab_not = vocab_not
        self.cnt_vocab = cnt_vocab
        self.cnt_vocab_not = cnt_vocab_not
        self.cnt_vocab_all = cnt_vocab_all
        self.cnt_vocab_not_all = cnt_vocab_not_all

        self.vocab_p = vocab_p
        self.vocab_n = vocab_n
        self.cnt_comment_positive = cnt_comment_positive
        self.cnt_comment_negative = cnt_comment_negative

        result = {
            'cnt': cnt,         # 리뷰에 나온 단어 전체 개수
            'vocab': vocab,          # 긍정문에 나온 단어: 개수
            'vocab_not': vocab_not,  # 부정문에 나온 단어: 개수
            'cnt_vocab': cnt_vocab,          # 긍정문에 나온 단어 개수 (중복 제외)
            'cnt_vocab_not': cnt_vocab_not,  # 부정문에 나온 단어 개수 (중복 제외)
            'cnt_vocab_all': cnt_vocab_all,             # 리뷰 전체 긍정문에 나온 전체 단어 개수
            'cnt_vocab_not_all': cnt_vocab_not_all,     # 리뷰 전체 부정문에 나온 전체 단어 개수
            'vocab_p': vocab_p,     # 긍정리뷰(score > 2)에 나온 단어: 개수
            'vocab_n': vocab_n,     # 부정리뷰(score <= 2)에 나온 단어: 개수
            'cnt_comment_positive': cnt_comment_positive,   # 긍정리뷰 개수
            'cnt_comment_negative': cnt_comment_negative    # 부정리뷰 개수
        }
        return result
    # return sorted_vocab, sorted_not_vocab, cnt_vocab_all, cnt_vocab_not_all, sorted_vocab_p, sorted_vocab_n, cnt_vocab, cnt_vocab_not, cnt_comment_positive, cnt_comment_negative

    def select_stems(self):
        duplicate = []
        for key in self.vocab:
            if key in self.vocab_not:
                duplicate.append(key)

        stem_n = {}
        stem_p = {}

        for dup in duplicate:
            neg_per_comment = self.vocab_not[dup] / self.cnt_vocab_not_all
            pos_per_comment = self.vocab[dup] / self.cnt_vocab_all

            p = math.log(neg_per_comment / pos_per_comment)
            # print(dup, neg_per_comment, pos_per_comment, "//", self.vocab_not[dup], self.vocab[dup], p)

            if neg_per_comment > pos_per_comment:
                if p > self.alpha:
                    if neg_per_comment > self.beta:
                        stem_n[dup] = p * neg_per_comment * 100
                    elif pos_per_comment > self.gamma:
                        stem_n[dup] = p * neg_per_comment * 100
            else:
                p = -1*p
                if p > self.alpha:
                    if pos_per_comment > self.beta:
                        stem_p[dup] = p * pos_per_comment * 100
                    elif neg_per_comment > self.gamma:
                        stem_p[dup] = p * pos_per_comment * 100
        return stem_n, stem_p

    def make_word(self, vocab_n, vocab_p):
        word_value_n = {}
        word_value_p = {}
        for word, pos in vocab_p:
            word_value_p[word + "다"] = vocab_p[(word, pos)]
        for word, pos in vocab_n:
            word_value_n[word + "지 않다"] = vocab_n[(word, pos)]
        return word_value_n, word_value_p


if __name__ == '__main__':
    pages = rg.pages

    keywords = {}
    extractor = StemExtractor()
    extractor.count_stems(pages)
    stem_n, stem_p = extractor.select_stems()
    word_n, word_p = extractor.make_word(stem_n, stem_p)

    print(word_n)
    print(word_p)
