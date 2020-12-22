from codes import fileReadWrite
from config import path

pages = fileReadWrite.read_comment_file(path)


def get_review(url):
    filename = path
    pages = fileReadWrite.read_comment_file(filename)
    return pages