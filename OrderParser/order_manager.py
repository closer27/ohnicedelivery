from OrderParser.reader import Reader
from OrderParser.writer import write_to_xls


class OrderManager:
    def __init__(self, files):
        self.reader = Reader()
        self.reader.set_order_list(files)

    def get_order_list(self):
        order_list = self.reader.get_order_list()
        print(order_list)
        return order_list

    def get_unified_sheet(self):
        return write_to_xls(self.get_order_list())
