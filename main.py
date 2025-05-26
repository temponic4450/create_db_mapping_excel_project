import os
import sys
import time

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from main.ui.ui_main import Ui_MainWindow # 변환된 .ui 파일에서 생성된 클래스
from main.work.create import create_excel_file
# pyuic6.exe .\main\ui\main.ui -o .\main\ui_main.py



class MyApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    
    # UI 요소 초기화
    self.setWindowTitle("🔥 매핑 정의서 생성기")    
    self.setWindowIcon(QIcon(os.path.join(os.path.join(os.path.dirname(__file__), "ui"), "icon.png")))


    # button 클릭 시 동작 정의
    self.ui.Execute_Button.clicked.connect(self.wrap_create_excel_file)  # 엑셀 파일 생성
    self.ui.Exit_Button.clicked.connect(self.close)  
    
    self.ui.RDB_Select.addItems(["Oracle", "PostgreSQL","MSSQL","mariaDB","Tibero","DB2(LUW)"])  # RDBMS 선택 박스에 Oracle과 PostgreSQL 추가
    self.ui.RDB_Select.setCurrentText("Oracle")  # 기본값으로 Oracle 선택
    
    
  def wrap_create_excel_file(self):
    
    object_dict = {
          "RDBMS" : self.ui.RDB_Select.currentText(),
          "IP" : self.ui.IP_Text.text(),
          "PORT" : self.ui.PORT_Text.text(),
          "SID" : self.ui.SID_Text.text(),
          "SCHEMA" : self.ui.SCH_Text.text(),
          "USER" : self.ui.USER_Text.text(),
          "PASSWORD" : self.ui.PW_Text.text(),
          "SAVE_PATH" : self.ui.SP_Text.toPlainText()
    }  
    try:  
        # 입력값 검증
        if not object_dict["RDBMS"]:
            raise ValueError("RDBMS를 선택해주세요.")
        if not object_dict["IP"]:
            raise ValueError("IP 주소를 입력해주세요.")
        if not object_dict["PORT"]:
            raise ValueError("포트 번호를 입력해주세요.")
        if not object_dict["SID"]:
            raise ValueError("SID(OR database name)를 입력해주세요.")
        if not object_dict["SCHEMA"]:
            raise ValueError("스키마 이름을 입력해주세요.(USER 명)")
        if not object_dict["USER"]:
            raise ValueError("사용자 이름을 입력해주세요.")
        if not object_dict["PASSWORD"]:
            raise ValueError("비밀번호를 입력해주세요.")
        if not object_dict["SAVE_PATH"]:
            raise ValueError("저장 경로를 입력해주세요.")
      # 엑셀 파일 생성
        create_excel_file(object_dict)
    
  
      # 완료 메시지 출력
        self.ui.Log_Browsing.setPlainText("엑셀 파일 생성 완료! \n저장 경로: " + object_dict["SAVE_PATH"] + "\\매핑 정의서.xlsx")   
        self.ui.Log_Browsing.setStyleSheet("color: green; font-weight: bold;")  # 성공 메시지 스타일링
        time.sleep(1)  # 1초 대기
    except Exception as e:
        self.ui.Log_Browsing.appendPlainText(f"오류 발생: {str(e)}")
        self.ui.Log_Browsing.setStyleSheet("color: red; font-weight: bold;")  # 오류 메시지 스타일링 
        
        
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())