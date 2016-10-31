from OrderParser.order import Order
from OrderParser.seller import Seller
import csv
import io


class CsvReader:
    def __init__(self):
        pass

    def get_order_list(self, file, seller: Seller, encoding='cp949'):
        if seller.description() == "Babosarang":
            buf = io.StringIO(file.read().decode('cp949'))
            buf.seek(0)
            csv_f = csv.reader(buf, delimiter='\t', dialect=csv.excel_tab)
        else:
            f = str(file.read(), encoding=encoding)
            csv_f = csv.reader(f.split('\r\n'), delimiter=',')

        data = list(filter(lambda x: len(x) >= 17, [list(row) for row in csv_f]))[1:]
        if seller.description() == "Babosarang":
            data2 = list(map(lambda x: list(map(lambda elem: elem[1:] if elem.startswith('\'') else elem, x)), data))
            data = data2

        recipient_names = []
        recipient_phones = []
        zipcodes = []
        addresses = []
        order_nums = []
        product_names = []
        product_options = []
        cautions = []

        for row_val in range(len(data)):
            recipient_names.append(data[row_val][seller.idx_recipient_name])
            recipient_phones.append(data[row_val][seller.idx_recipient_phone])
            zipcodes.append(data[row_val][seller.idx_zipcode])
            addresses.append(data[row_val][seller.idx_address])
            order_nums.append(data[row_val][seller.idx_order_num])
            product_names.append(data[row_val][seller.idx_product_name])
            product_options.append(data[row_val][seller.idx_product_option])
            cautions.append(data[row_val][seller.idx_caution])

        order_list = []
        for row_val in range(len(recipient_names)):
            order_dict = {'recipient_name': recipient_names[row_val],
                          'recipient_phone': recipient_phones[row_val],
                          'zipcode': zipcodes[row_val],
                          'address': addresses[row_val],
                          'order_num': order_nums[row_val],
                          'product_name': product_names[row_val],
                          'product_option': product_options[row_val],
                          'caution': cautions[row_val]}
            order_list.append(Order(order_dict))

        # for row_val in range(len(order_list)):
        #     print(order_list[row_val])

        return order_list
