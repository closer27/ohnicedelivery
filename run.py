__author__ = 'wonny'

import sys
import os


def get_newfile_path(current_file_path):
    import time
    today = time.strftime("플래네틸_%Y%m%d_라투투발주리스트")
    output_dir = os.path.dirname(current_file_path)
    return os.path.join(output_dir, today + '.xls')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print('file name : ' + filepath)
        from OrderParser.book import parse
        order_list = parse(filepath)

        from OrderParser.writer import write_to_xls
        write_to_xls(order_list, get_newfile_path(filepath))

    else:
        print('not correct file, please check again')
