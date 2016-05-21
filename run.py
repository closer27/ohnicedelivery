__author__ = 'wonny'

import sys
from flask import Flask, request, send_file, make_response

PROGRAM_TITLE = 'Delivery Swimmer'

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_newfile_path():
    import time
    today = "{}{}{}".format('플래네틸', time.strftime("%Y%m%d"), '_라투투발주리스트.xls')
    print(today)
    return today


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        print(files)
        for file in files:
            print(file.filename)
            if not file or not allowed_file(file.filename):
                return '잘못된 파일이에요 : xls, xlsx, csv 파일만 올려주세요.'

        from OrderParser.reader import get_orderlist
        order_data = get_orderlist(files)

        from OrderParser.writer import write_to_xls
        f = write_to_xls(order_data)

        from urllib import parse
        response = make_response(send_file(f))
        response.headers["Content-Disposition"] = \
            "attachment; " \
            "filenane={ascii_filename};" \
            "filename*=UTF-8''{utf_filename}".format(
                ascii_filename="book.pdf",
                utf_filename=parse.quote(get_newfile_path())
            )

        return response

    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name="file[]" multiple="multiple">
             <input type=submit value=Upload>
        </form>
        '''

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=int(sys.argv[1]))