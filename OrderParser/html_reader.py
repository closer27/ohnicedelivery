from OrderParser.order import Order
from OrderParser.seller import Seller
from bs4 import BeautifulSoup


class HTMLReader:
    def __init__(self):
        pass

    def get_order_list(self, file, seller: Seller):
        data = file.read()
        file.seek(0)

        soup = BeautifulSoup(data, 'html.parser', from_encoding='cp949')

        if soup.find('tbody'):
            table = soup.find('tbody')
            start_index = 0
        else:
            table = soup.find("table")
            start_index = 1

        order_list = []
        for row in table.find_all("tr")[start_index:]:
            row_data = row.find_all("td")
            order_dict = {'recipient_name': row_data[seller.idx_recipient_name].get_text(),
                          'recipient_phone': row_data[seller.idx_recipient_phone].get_text(),
                          'zipcode': row_data[seller.idx_zipcode].get_text(),
                          'address': row_data[seller.idx_address].get_text(),
                          'order_num': row_data[seller.idx_order_num].get_text(),
                          'product_name': row_data[seller.idx_product_name].get_text(),
                          'product_option': row_data[seller.idx_product_option].get_text(),
                          'caution': row_data[seller.idx_caution].get_text()}
            order_list.append(Order(order_dict))

        return order_list
