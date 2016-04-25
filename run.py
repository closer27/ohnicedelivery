__author__ = 'wonny'

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal

PROGRAM_TITLE = 'Delivery Swimmer'


from flask import Flask, request, jsonify, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


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
    app.run()
    # app = QApplication(sys.argv)
    # w = MyWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle("Delivery Swimmer")
    # w.show()
    #
    # sys.exit(app.exec_())