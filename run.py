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
        filepaths = []
        for argv in sys.argv[1:]:
            filepaths.append(argv)

        from OrderParser.reader import get_orderlist
        order_list = get_orderlist(filepaths)

        from OrderParser.writer import write_to_xls
        write_to_xls(order_list, get_newfile_path(sys.argv[1]))

    else:
        print('not correct file, please check again')
