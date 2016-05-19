__author__ = 'wonny'

from bs4 import BeautifulSoup


def parse(file_storage):

    # 10x10's order sheet
    idx_receiptor_name = 6
    idx_receiptor_phone = 8
    idx_zipcode = 9
    idx_address = 10
    idx_order_num = 0
    idx_product_name = 14
    idx_product_option = 15
    idx_caution = 11

    data = file_storage.read()
    file_storage.seek(0)

    print("Reading 'ten to ten' order success.")

    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find("table")

    order_list = []
    for row in table.find_all("tr")[1:]:
        row_data = row.find_all("td")
        order = {'receiptor_name': row_data[idx_receiptor_name].get_text(),
                 'receiptor_phone': row_data[idx_receiptor_phone].get_text(),
                 'zipcode': row_data[idx_zipcode].get_text(),
                 'address': row_data[idx_address].get_text(),
                 'order_num': row_data[idx_order_num].get_text(),
                 'product_name': row_data[idx_product_name].get_text(),
                 'product_option': row_data[idx_product_option].get_text(),
                 'caution': row_data[idx_caution].get_text()}
        order_list.append(order)

    print("Complete parsing.")

    return order_list
