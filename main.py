import stemDetector as sd
import nounDetector as nd
import ngram as ng
import wordCloud as wc
import reviewGetter as rg
import sys


if __name__ == '__main__':
    url = sys.argv[1]
    print("........ 리뷰 가져오는 중 ........")
    pages = rg.get_review(url)

    print("........ 부정어를 이용한 어간 탐색 중 ........")
    extractor = sd.StemExtractor()
    extractor.count_stems(pages)
    stem_n, stem_p = extractor.select_stems()
    word_n, word_p = extractor.make_word(stem_n, stem_p)
    words = {}
    words.update(word_n)
    words.update(word_p)
    # print(words)

    print("........ 평점을 이용한 명사 탐색 중 ........")
    nounDetector = nd.NounDetector()
    nounDetector.count_stems(pages)

    top_n, top_p = nounDetector.get_top_noun()
    # print("top_n", top_n)
    # print("top_p", top_p)

    print("........ 3-grams 생성 중 ........")
    ngram = ng.Ngram()
    ngram.set_ngram(pages)
    ngram.set_ngram_counter()
    print("........ 의미 확장 중 ........")
    ngram_noun_n = ngram.select_ngram_noun(top_n)
    ngram_stems_n = ngram.get_only_stem(ngram_noun_n)
    ngram_noun_p = ngram.select_ngram_noun(top_p)
    ngram_stems_p = ngram.get_only_stem(ngram_noun_p)

    # print(ngram_noun_n)
    # print(ngram_noun_p)

    print("........ 워드클라우드 생성 중 ........")
    wordCloud = wc.MyWordCloud(ngram_stems_n, ngram_stems_p, words)
    wordCloud.set_color()
    # wordCloud.show()
    wordCloud.save()

    print("........ ........ ........ ")
    print("........ 완료 ........")
