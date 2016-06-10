__author__ = 'wonny'

import csv


def parse(file_storage):
    f = str(file_storage.read(), encoding='utf-8')
    csv_f = csv.reader(f.split('\n'), delimiter=',')
    data = list(filter(lambda x: len(x) >= 17, [list(row) for row in csv_f]))[1:]
    for row in csv_f:
        print(row)

    print("Reading 'cracker' order success.")

    # book's order sheet
    idx_receiptor_name = 9
    idx_receiptor_phone = 14
    idx_zipcode = 10
    idx_address = 11
    idx_order_num = 0
    idx_product_name = 2
    idx_product_option = 4
    idx_caution = 15

    receiptor_names = []
    receiptor_phones = []
    zipcodes = []
    addresses = []
    order_nums = []
    product_names = []
    product_options = []
    cautions = []

    for row_val in range(len(data)):
        receiptor_names.append(data[row_val][idx_receiptor_name])
        receiptor_phones.append(data[row_val][idx_receiptor_phone])
        zipcodes.append(data[row_val][idx_zipcode])
        addresses.append(data[row_val][idx_address])
        order_nums.append(data[row_val][idx_order_num])
        product_names.append(data[row_val][idx_product_name])
        product_options.append(data[row_val][idx_product_option])
        cautions.append(data[row_val][idx_caution])

    print("Complete parsing.")

    order_list = []
    for row_val in range(len(receiptor_names)):
        order = {'receiptor_name': receiptor_names[row_val],
                 'receiptor_phone': receiptor_phones[row_val],
                 'zipcode': zipcodes[row_val],
                 'address': addresses[row_val],
                 'order_num': order_nums[row_val],
                 'product_name': product_names[row_val],
                 'product_option': product_options[row_val],
                 'caution': cautions[row_val]}
        order_list.append(order)

    for row_val in range(len(order_list)):
        print(order_list[row_val])

    return order_list

