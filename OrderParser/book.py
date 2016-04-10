__author__ = 'wonny'

import os
import csv


def parse(file_path):
    if os.path.exists(file_path):
        print(file_path)
    else:
        print("not exist file")
        exit()

    f = open(file_path, encoding='cp949')
    csv_f = csv.reader(f, delimiter=',')
    data = list(filter(lambda x: len(x) >= 17, [list(row) for row in csv_f]))[1:]

    print("Reading 'book' order success.")
