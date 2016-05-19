__author__ = 'wonny'

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal

PROGRAM_TITLE = 'Delivery Swimmer'


from flask import Flask, request

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
        print(order_data)

        return "hello"

        # from OrderParser.writer import write_to_xls
        # write_to_xls(self.order_data, self.get_newfile_path(self.input_path_arr[0]))

        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name="file[]" multiple="multiple">
             <input type=submit value=Upload>
        </form>
        '''


class MyWidget(QWidget):
    dropped = pyqtSignal(str)
    input_path_arr = []
    output_path = ''
    order_data = []

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        self.progressBar = QProgressBar(self)

        self.label = QLabel("파일을 드래그해서 놓아주세요.", self)
        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)
        self.progressBar.setRange(0, 100)

        self.setAcceptDrops(True)
        self.dropped.connect(self.process)

        self.btn = QPushButton('변환하기', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 50)
        self.btn.clicked.connect(self.progress_spreadsheet)
        layout.addWidget(self.btn)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()

            input = event.mimeData().urls()[0].toLocalFile()
            self.dropped.emit(input)
        else:
            event.ignore()

    def process(self, input_path):
        self.input_path_arr.append(input_path)

        path_str = "현재 추가 된 발주리스트(중복해서 넣지마세요!)\n"
        for path in self.input_path_arr:
            path_str += path + "\n"
        self.label.setText(path_str)

    def progress_spreadsheet(self):
        if len(self.input_path_arr) <= 0:
            return

        from OrderParser.reader import get_orderlist
        self.order_data = get_orderlist(self.input_path_arr)

        from OrderParser.writer import write_to_xls
        write_to_xls(self.order_data, self.get_newfile_path(self.input_path_arr[0]))

        self.progressBar.setRange(0, 0)
        self.label.setText("변환 완료! 발주서와 같은 폴더에 생겼어요.")

    def get_newfile_path(self, current_file_path):
        import time
        today = "{}{}{}".format('플래티넘_',time.strftime("%Y%m%d"), '_라투투발주리스트')
        output_dir = os.path.dirname(current_file_path)
        self.label.setText(today)
        return os.path.join(output_dir, today + '.xls')


if __name__ == '__main__':
    app.debug = True
    app.run()