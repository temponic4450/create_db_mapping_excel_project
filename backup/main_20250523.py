import os
import sys
import time

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from main_ui import Ui_MainWindow # 변환된 .ui 파일에서 생성된 클래스
# 

# 
UI_PATH = os.path.join(os.path.dirname(__file__), "ui")

# UI 파일 로드
form_class = uic.loadUiType(os.path.join(UI_PATH, "main.ui"))[0]  # main.ui 파일 경로


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # UI 요소 초기화
        self.setWindowTitle("🔥 매핑 정의서 생성기 - Oracle Version")    
        self.setWindowIcon(QIcon(os.path.join(UI_PATH, "icon.png")))
        
        self.ui.Execute_Button.clicked.connect()
        self.ui.Exit_Buttion.clicked.connect(self.close)
        
        
   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())