__author__ = 'wonny'

import OrderParser.book as book
import OrderParser.storefield as storefield
import OrderParser.raremoment as raremoment
import OrderParser.tentoten as tentoten
import OrderParser.cracker as cracker
import OrderParser.fool as fool
import OrderParser.aworld as aworld


def get_orderlist(filepaths):
    orderlist_integrated = []
    for file in filepaths:
        print("get_orderlist : " + file.filename)
        orderlist_integrated.extend(get_data_from_file(file))

    return orderlist_integrated


def get_data_from_file(file):
    print("get_data_from_file: " + file.filename)
    if "uniq" in file.filename:
        return raremoment.parse(file)
    elif "스토어" in file.filename:
        return storefield.parse(file)
    elif "TEN" in file.filename:
        return tentoten.parse(file)
    elif "배송리스트" in file.filename:
        return book.parse(file)
    elif "orders" in file.filename:
        return cracker.parse(file)
    elif "보사랑" in file.filename:
        return fool.parse(file)
    elif "GDorder" in file.filename:
        return aworld.parse(file)
    else:
        print("잘못된 파일이 들어가있어요 ㅜㅜ 파일을 올바르게 다시 넣어주세요")
        return None
