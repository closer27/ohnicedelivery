import sys
from flask import Flask, request, send_file, make_response, render_template
from OrderParser.order_manager import OrderManager

PROGRAM_TITLE = 'Delivery Swimmer'

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}

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

        order_manager = OrderManager(files=files)
        f = order_manager.get_unified_sheet()

        from urllib import parse
        response = make_response(send_file(f))
        response.headers["Content-Disposition"] = \
            "attachment; " \
            "filename={ascii_filename};" \
            "filename*=UTF-8''{utf_filename}".format(
                ascii_filename="book.pdf",
                utf_filename=parse.quote(get_newfile_path())
            )

        return response

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
