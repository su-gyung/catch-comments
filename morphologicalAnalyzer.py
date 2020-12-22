# -*- coding: utf-8 -*-
import crawler as cm
import fileReadWrite as frw
from konlpy.tag import Kkma
import datetime


class MorphologicalAnalyzer:
    def __init__(self, url):
        self.kkma = Kkma()
        self.url = url

    def get_comments_with_mp(self, has_option):
        def get_today():
            date = datetime.datetime.now()
            return date.strftime('%y%m%d')

        def get_file_name(url):
            store_id = url[url.find("stores/") + 7:url.find("/products/")]
            product_id = url[url.find("/products/") + 10:]

            today = get_today()
            return store_id + "_" + product_id

        def get_comments_file():
            filename = get_file_name(self.url)
            today = get_today()



        comments = cm.get_review(url, has_option)

        for page in comments:
            for comment in page:
                morphology = []
                for text in comment['text']:
                    mp = self.kkma.pos(text)
                    morphology.append(mp)
                comment['morphology'] = morphology

        frw.write_comment_to_file(comments, filename+"_long")
        frw.write_comment_to_string_file(str(comments), filename+"_text")

        return comments


if __name__ == "__main__":
    # 게장
    url = 'https://shopping.naver.com/fresh/localfood/stores/1000025002/products/1003352049'
    save_review(url, True)
