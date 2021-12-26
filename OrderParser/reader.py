from OrderParser.seller import TenByTen, Biskit, Book, StoreFarm, Uniqmoment, Aland, Hottracks
from OrderParser.xls_reader import XlsReader
from OrderParser.html_reader import HTMLReader
from OrderParser.csv_reader import CsvReader
import unicodedata

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
        filename = unicodedata.normalize('NFKC', file.filename)
        print(unicodedata.normalize('NFKC', "스마트스토어") in filename)
        if "TEN" in filename:
            return self.html_reader.get_order_list(file=file, seller=TenByTen())
        elif "uniq" in filename:
            return self.html_reader.get_order_list(file=file, seller=Uniqmoment())
        elif unicodedata.normalize('NFKC', "정보") in filename:
            return self.xls_reader.get_order_list(file=file, seller=Aland())
        elif unicodedata.normalize('NFKC', "스마트스토어") in filename:
            return self.xls_reader.get_order_list(file=file, seller=StoreFarm())
        elif unicodedata.normalize('NFKC', "배송리스트") in filename:
            return self.csv_reader.get_order_list(file=file, seller=Book())
        elif "orders" in filename:
            return self.csv_reader.get_order_list(file=file, seller=Biskit(), encoding="utf-8")
        elif "vendor" in filename:
            return self.html_reader.get_order_list(file=file, seller=Hottracks())
        else:
            print("잘못된 파일이 들어가있어요 ㅜㅜ 파일을 올바르게 다시 넣어주세요")
            return None
