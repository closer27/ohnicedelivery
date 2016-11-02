from OrderParser.order import Order
from OrderParser.seller import Seller
import xlrd


class XlsReader:
    def __init__(self):
        pass

    def get_order_list(self, file, seller: Seller):
        workbook = xlrd.open_workbook(file_contents=file.stream.read())
        worksheet = workbook.sheet_by_index(0)  # 시트번호(인덱스)로 시트 가져오기

        order_list = []
        for row_val in range(worksheet.nrows):
            if row_val > 0:  # 헤더 제외
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
