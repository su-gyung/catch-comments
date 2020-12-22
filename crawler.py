# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import re
from config import maxPage, browser_url


def remove_invalid_ch(text):
    invalid = re.compile('�', flags=re.UNICODE)
    emoji = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    valid = invalid.sub(r'', text)
    removed = emoji.sub(r'', valid)
    return removed


def make_structured(comments, has_option):
    structured = []
    end_flag = False
    cmt = comments.split("\n")
    length = len(cmt)
    index = 0
    print(index, length)
    while index < length - 1:
        elem = {}
        while cmt[index] != "평점":
            index += 1
        index += 1
        elem['score'] = cmt[index]      # 평점
        # print(index, 'score', cmt[index])

        index += 1
        elem['userid'] = cmt[index]     # 아이디
        # print(index, 'userid', cmt[index])

        index += 1
        elem['date'] = cmt[index]       # 날짜
        # print(index, 'date', cmt[index])

        # if cmt[index] == two_weeks_ago:  # 2주 전 케이스까지.
        #     end_flag = True
        #     print("!!!!!!!!!!!! end !!!!!!!!!!!!")
        #     break
        __date = cmt[index]

        if has_option:
            index += 1
            if "선택" not in cmt[index]:
                index -= 1
                break
            elem['option'] = cmt[index]     # 옵션
            # print(index, 'option', cmt[index])

        index += 2
        text = []

        no_img_no_reply = False
        while cmt[index] not in ["더보기", "동영상컨텐츠", "이미지 펼쳐보기", "사진/비디오 수"]:
            # print(index, "text append", cmt[index])
            line = cmt[index]
            index += 1
            if line == '':
                continue
            text.append(line)
            if cmt[index].isdigit():
                no_img_no_reply = True
                break
        elem['text'] = text              # 댓글
        # print(index, 'text', text)

        if no_img_no_reply:
            elem['like'] = cmt[index]
        else:
            while cmt[index] not in ["이미지 펼쳐보기", "판매자", "평점"]:
                index += 1
            index += 1
            elem['like'] = cmt[index]       # 좋아요
        # print("좋아요", index, cmt[index])

        while cmt[index] not in ["리뷰 더보기/접기", "평점"]:
            # print(index, cmt[index])
            if index == length-1:
                # print("break")
                break
            index += 1
        structured.append(elem)
    return structured, end_flag


def get_review(url, has_option):
    # selenium setting
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")

    # Config.CONFIG['CHROMEPATH']
    # url = 'https://shopping.naver.com/fresh/localfood/stores/100900237/products/5109995394?NaPm=ct%3Dkfyvr7om%7Cci%3Dshoppingwindow%7Ctr%3Dswl%7Chk%3Db178b29b4b7fe54f63fd2579d278e5d1f9ca6cb6%7Ctrx%3D'

    driver = webdriver.Chrome(executable_path=browser_url, chrome_options=options)  # 크롬 창 열기
    driver.get(url)

    comments_all = []

    # review page count
    for i in range(maxPage):
        print(i, "*********** page ***************")
        # 페이지 읽기
        # tests = driver.find_elements_by_css_selector('.review_list > ._1QyrsagqZm._2w8VqYht7m > a')
        # for test in tests:
        #     print("page", test.text)
        #     print("page tag", test.tag_name)
        #     print("current", test.get_attribute("aria-current"))
        #
        # 특정 원소 불러올 때까지 기다리기
        try:
            element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, ".review_list"))
            )
            # lowest = driver.find_elements_by_css_selector(
            #     ".review_list > ._1TvkeQbpJb > ._JEL2FoNN4 > ._1tea9tCBDM > ._1Bf0nJ9MZy")[3]
            # ActionChains(driver).click(lowest).perform()

            newest = driver.find_elements_by_css_selector(
                ".review_list > ._1TvkeQbpJb > ._JEL2FoNN4 > ._1tea9tCBDM > ._1Bf0nJ9MZy")[1]
            ActionChains(driver).click(newest).perform()
        finally:
            for element in driver.find_elements_by_class_name('review_list'):
                comments_page = element.text[element.text.find("리뷰 더보기/접기")+10:]

                valid_comments_page = remove_invalid_ch(comments_page)
                structured, end_flag = make_structured(valid_comments_page, has_option)
                comments_all.append(structured)
                if end_flag:
                    break
        if end_flag:
            break
        next_button = driver.find_element_by_css_selector(".review_list > ._1QyrsagqZm._2w8VqYht7m > ._3togxG55ie._2_kozYIF0B")
        next_hidden = next_button.get_attribute("aria-hidden")
        print("hidden", next_hidden)
        if next_hidden == "true":
            break
        ActionChains(driver).click(next_button).perform()
    driver.quit()
    return comments_all
