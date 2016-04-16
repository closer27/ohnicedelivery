__author__ = 'wonny'

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal

PROGRAM_TITLE = 'Delivery Swimmer'


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

        self.label.setText(input_path + "가 추가되었습니다.")

    def progress_spreadsheet(self):
        from OrderParser.reader import get_orderlist
        self.order_data = get_orderlist(self.input_path_arr)

        from OrderParser.writer import write_to_xls
        write_to_xls(self.order_data, self.get_newfile_path(sys.argv[1]))

        self.progressBar.setRange(0, 0)

    def get_newfile_path(self, current_file_path):
        import time
        today = time.strftime("플래네틸_%Y%m%d_라투투발주리스트")
        output_dir = os.path.dirname(current_file_path)
        return os.path.join(output_dir, today + '.xls')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepaths = []
        for argv in sys.argv[1:]:
            filepaths.append(argv)

        # order_list = get_orderlist(filepaths)
        #
        # write_to_xls(order_list, get_newfile_path(sys.argv[1]))

        app = QApplication(sys.argv)

        w = MyWidget()
        w.resize(250, 150)
        w.move(300, 300)
        w.setWindowTitle("Delivery Swimmer")
        w.show()

        sys.exit(app.exec_())

else:
    print('not correct file, please check again')
