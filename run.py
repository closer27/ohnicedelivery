__author__ = 'wonny'

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('file name : ' + sys.argv[1])
        from OrderParser.book import parse
        parse(sys.argv[1])

    else:
        print('not correct file, please check again')
