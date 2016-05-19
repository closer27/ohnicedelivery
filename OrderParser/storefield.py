# -*- coding: cp949 -*-
__author__ = 'wonny'

import xlrd


def parse(file_storage):
    workbook = xlrd.open_workbook(file_contents=file_storage.stream.read())
    worksheet = workbook.sheet_by_index(0)    # 시트번호(인덱스)로 시트 가져오기

    print("Reading 'storefield' order success.")

    # storefield's order sheet
    idx_receiptor_name = 4
    idx_receiptor_phone = 37
    idx_zipcode = 41
    idx_address = 39
    idx_order_num = 3
    idx_product_name = 15
    idx_product_option = 17
    idx_caution = 42

    order_list = []
    for row_val in range(worksheet.nrows):
        if row_val > 0:    # 헤더 제외
            row_data = worksheet.row_values(row_val)
            order = {'receiptor_name': row_data[idx_receiptor_name],
                     'receiptor_phone': row_data[idx_receiptor_phone],
                     'zipcode': row_data[idx_zipcode],
                     'address': row_data[idx_address],
                     'order_num': row_data[idx_order_num],
                     'product_name': row_data[idx_product_name],
                     'product_option': row_data[idx_product_option],
                     'caution': row_data[idx_caution]}
            order_list.append(order)

    print("Complete parsing.")

    for row_val in range(len(order_list)):
        print(order_list[row_val])

    return order_list
