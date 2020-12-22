# -*- coding: utf-8 -*-
import pickle
from config import filepath


def write_comment_to_file(comments_list, filename):
    try:
        # with open(filepath+filename+'.txt', 'w', encoding="utf-8") as f:
        #     f.write(comments)
        with open(filepath+filename+'.txt', 'wb') as f:
            pickle.dump(comments_list, f)
    except IOError as e:
        print("Couldn't open or write to file (%s)." % e)


def read_comment_file(filename):
    with open(filepath+filename+'.txt', 'rb') as f:
        data_list = []
        while True:
            try:
                data = pickle.load(f)
            except EOFError:
                break
            data_list.append(data)
    return data_list[0]


def write_comment_to_string_file(comments, filename):
    try:
        with open(filepath+filename+'.txt', 'w', encoding="utf-8") as f:
            f.write(comments)
    except IOError as e:
        print("Couldn't open or write to file (%s)." % e)


if __name__ == "__main__":
    data = read_comment_file("1000025002_1003352049_long")
    # write_comment_to_string_file(str(data), "1000025002_1003352049_text")
    print(data)