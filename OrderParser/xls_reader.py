from OrderParser.order import Order
from OrderParser.seller import Seller, Ably
import xlrd


class XlsReader:
    def __init__(self):
        pass

    def get_order_list(self, file, seller: Seller):
        workbook = xlrd.open_workbook(file_contents=file.stream.read())
        sheet_index = 1 if type(seller) is Ably else 0
        worksheet = workbook.sheet_by_index(sheet_index)  # 시트번호(인덱스)로 시트 가져오기

        order_list = []
        index_for_header = 1 if seller.description() == "Storefarm" else 0
        print(seller.description())
        for row_val in range(worksheet.nrows):
            if row_val > index_for_header:  # 헤더 제외
                row_data = worksheet.row_values(row_val)
                order_dict = {'recipient_name': row_data[seller.idx_recipient_name],
                              'recipient_phone': row_data[seller.idx_recipient_phone],
                              'zipcode': row_data[seller.idx_zipcode],
                              'address': row_data[seller.idx_address],
                              'order_num': row_data[seller.idx_order_num],
                              'product_name': row_data[seller.idx_product_name],
                              'product_option': row_data[seller.idx_product_option],
                              'caution': row_data[seller.idx_caution]}
                order_list.append(Order(order_dict))

        return order_list
