from OrderParser.seller import TenByTen, Babosarang, Biskit, Book, StoreFarm, Uniqmoment, Aland
from OrderParser.xls_reader import XlsReader
from OrderParser.html_reader import HTMLReader
from OrderParser.csv_reader import CsvReader


class Reader:
    files = []
    xls_reader = XlsReader()
    html_reader = HTMLReader()
    csv_reader = CsvReader()

    def __init__(self):
        pass

    def set_order_list(self, files):
        self.files = files

    def get_order_list(self):
        order_list = []
        for file in self.files:
            print("get_order_list : " + file.filename)
            order_list.extend(self.transform_sheet(file))
        return order_list

    def transform_sheet(self, file):
        if "TEN" in file.filename:
            return self.html_reader.get_order_list(file=file, seller=TenByTen())
        elif "uniq" in file.filename:
            return self.html_reader.get_order_list(file=file, seller=Uniqmoment())
        elif "GDorder" in file.filename:
            return self.html_reader.get_order_list(file=file, seller=Aland())
        elif "스토어" in file.filename:
            return self.xls_reader.get_order_list(file=file, seller=StoreFarm())
        elif "배송리스트" in file.filename:
            return self.csv_reader.get_order_list(file=file, seller=Book())
        elif "orders" in file.filename:
            return self.csv_reader.get_order_list(file=file, seller=Biskit(), encoding="utf-8")
        elif "보사랑" in file.filename:
            return self.csv_reader.get_order_list(file=file, seller=Babosarang(), encoding='euc-kr')
        else:
            print("잘못된 파일이 들어가있어요 ㅜㅜ 파일을 올바르게 다시 넣어주세요")
            return None
