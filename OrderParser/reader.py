__author__ = 'wonny'

import OrderParser.book as book
import OrderParser.storefield as storefield
import OrderParser.raremoment as raremoment
import OrderParser.tentoten as tentoten


def get_orderlist(filepaths):
    orderlist_integrated = []
    for filepath in filepaths:
        orderlist_integrated.extend(get_data_from_file(filepath))

    return orderlist_integrated


def get_data_from_file(filepath):
    if "uniq" in filepath:
        return raremoment.parse(filepath)
    elif "스토어" in filepath:
        return storefield.parse(filepath)
    elif "TEN" in filepath:
        return tentoten.parse(filepath)
    elif "배송리스트" in filepath:
        return book.parse(filepath)
    else:
        print("잘못된 파일이 들어가있어요 ㅜㅜ 파일을 올바르게 다시 넣어주세요")
        return None
