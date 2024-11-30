import sys
from datetime import datetime
import socket
import cv2
import pickle
import struct
import threading
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QLabel, QStackedWidget, QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import mysql.connector

class VideoStreamThread(QThread):
    update_frame = pyqtSignal(QImage)

    def __init__(self, server_ip):
        super().__init__()
        self.server_ip = server_ip
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.client_socket.connect((self.server_ip, 4000))  # 서버 IP와 포트
        while True:
            try:
                data_size_bytes = self.client_socket.recv(struct.calcsize('L'))
                if not data_size_bytes:
                    print("클라이언트와의 연결이 끊어졌습니다.")
                    break
                data_size = struct.unpack('L', data_size_bytes)[0]
                data = b''
                while len(data) < data_size:
                    packet = self.client_socket.recv(data_size - len(data))
                    if not packet:
                        print("클라이언트와의 연결이 끊어졌습니다.")
                        break
                    data += packet
                frame = pickle.loads(data)

                # OpenCV로 이미지를 QLabel에 표시할 수 있는 형식으로 변환
                frame = cv2.resize(frame, dsize=(640, 640))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR에서 RGB로 변환
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.update_frame.emit(q_img)

            except Exception as e:
                print(f"오류 발생: {e}")
                break
        self.client_socket.close()

class VideoStreamThread_cctv(QThread):
    update_frame_cctv = pyqtSignal(QImage)

    def __init__(self, server_cctv_ip):
        super().__init__()
        self.server_cctv_ip = server_cctv_ip
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.client_socket.connect((self.server_cctv_ip, 5000))  # 서버 IP와 포트
        while True:
            try:
                data_size_bytes = self.client_socket.recv(struct.calcsize('L'))
                if not data_size_bytes:
                    print("클라이언트와의 연결이 끊어졌습니다.")
                    break
                data_size = struct.unpack('L', data_size_bytes)[0]
                data = b''
                while len(data) < data_size:
                    packet = self.client_socket.recv(data_size - len(data))
                    if not packet:
                        print("클라이언트와의 연결이 끊어졌습니다.")
                        break
                    data += packet
                frame = pickle.loads(data)

                # OpenCV로 이미지를 QLabel에 표시할 수 있는 형식으로 변환
                #frame = cv2.resize(frame, dsize=(640, 640))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR에서 RGB로 변환
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.update_frame_cctv.emit(q_img)

            except Exception as e:
                print(f"오류 발생: {e}")
                break
        self.client_socket.close()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./manager_pc/dogniel_manager/dogniel_manager.ui', self)

        self.stacked_widget = self.findChild(QStackedWidget, 'stackedWidget')
        self.stacked_widget.hide()

        self.c_Button.clicked.connect(self.toggle_options1)
        self.r_Button.clicked.connect(self.toggle_options2)

        self.hide_sub_buttons(self.verticalLayoutWidget)
        self.hide_sub_buttons(self.verticalLayoutWidget_2)

        self.c1_Button.clicked.connect(lambda: self.go_to_page(0))
        self.p2_register_Button.clicked.connect(self.register)
        self.c2_Button.clicked.connect(lambda: self.go_to_page(1))
        self.c3_Button.clicked.connect(lambda: self.go_to_page(2))

        self.r1_Button.clicked.connect(lambda: self.go_to_page(3))
        self.r2_Button.clicked.connect(lambda: self.go_to_page(4))

        self.p1_check_Button.clicked.connect(self.customer_check)

        self.p1_listWidget.itemClicked.connect(self.on_list_item_click)
        self.p3_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.c3_Button.clicked.connect(self.fetch_data)
        
        
        self.fetch_data()

        # 비디오 스트리밍 스레드 시작
        #self.server_ip = '192.168.0.4'  # Raspberry Pi의 IP 주소
        #self.video_thread = VideoStreamThread(self.server_ip)
        #self.video_thread.update_frame.connect(self.update_video_frame)
        #self.video_thread.start()

        # 비디오 스트리밍 스레드 시작
        self.server_cctv_ip = '192.168.0.6'  # cctv의 IP주소
        self.video_thread_cctv = VideoStreamThread_cctv(self.server_cctv_ip)
        self.video_thread_cctv.update_frame_cctv.connect(self.update_video_frame_cctv)
        self.video_thread_cctv.start()
        
    def update_video_frame_cctv(self, frame):
        """QLabel에 비디오 프레임을 업데이트하는 함수."""
        scaled_frame = frame.scaled(self.p4_cctv_Label.size(), Qt.IgnoreAspectRatio)
        self.p4_cctv_Label.setPixmap(QPixmap.fromImage(scaled_frame))

    def update_video_frame(self, frame):
        """QLabel에 비디오 프레임을 업데이트하는 함수."""
        self.p5_minibot_cam_2_Label.setPixmap(QPixmap.fromImage(frame))

    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='0',
                database='dogniel_database'
            )
            return connection
        except mysql.connector.Error as e:
            print(f"DB 연결 실패: {e}")
            return None

    def hide_sub_buttons(self, widget):
        if widget is not None:
            widget.hide()
            for button in widget.findChildren(QPushButton):
                button.hide()

    def toggle_options1(self):
        if self.verticalLayoutWidget.isVisible():
            self.hide_sub_buttons(self.verticalLayoutWidget)
        else:
            self.verticalLayoutWidget.show()
            for button in self.verticalLayoutWidget.findChildren(QPushButton):
                button.show()
            self.stacked_widget.show()

    def toggle_options2(self):
        if self.verticalLayoutWidget_2.isVisible():
            self.hide_sub_buttons(self.verticalLayoutWidget_2)
        else:
            self.verticalLayoutWidget_2.show()
            for button in self.verticalLayoutWidget_2.findChildren(QPushButton):
                button.show()
            self.stacked_widget.show()

    def go_to_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def customer_check(self):
        name_text = self.p1_name.text()
        phone_num = str(self.p1_phone_num.text())
        self.p1_name.clear()
        self.p1_phone_num.clear()

        if name_text and phone_num:
            connection = self.connect_to_db()
            if connection:
                cursor = connection.cursor()
                query = "SELECT name FROM customer_information WHERE name = %s AND phone_number LIKE %s"
                cursor.execute(query, (name_text, f'%{phone_num}'))

                results = cursor.fetchall()
                cursor.close()
                connection.close()

                self.p1_listWidget.clear()  # 이전 검색 결과 지우기
                if results:
                    for row in results:
                        self.p1_listWidget.addItem(row[0])  # 이름을 리스트에 추가
                else:
                    QMessageBox.information(self, '결과', '고객을 찾을 수 없습니다.')
        else:
            QMessageBox.warning(self, '경고', '이름과 전화번호 뒷자리를 모두 입력해주세요.')

    def on_list_item_click(self, item):
        name = item.text()
        response = QMessageBox.question(self, '체크인', f'{name}을 체크인 하시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No)

        if response == QMessageBox.Yes:
            # 현재 날짜만 가져오기 (시간 제외)
            current_date = datetime.now().strftime('%Y-%m-%d')  # 'YYYY-MM-DD' 형식으로 날짜만

            # 데이터베이스 연결
            connection = self.connect_to_db()
            if connection:
                cursor = connection.cursor()

                # customer_information 테이블에서 id, name을 가져오는 쿼리
                query_customer = "SELECT id FROM customer_information WHERE name = %s"
                cursor.execute(query_customer, (name,))
                customer_data = cursor.fetchone()

                if customer_data:
                    # customer_id를 가져옴
                    customer_id = customer_data[0]

                    # 해당 id로 dog_information 테이블에서 dog_name과 dog_remarks를 가져오는 쿼리
                    query_dog = "SELECT dog_name, dog_remarks FROM dog_information WHERE id = %s"
                    cursor.execute(query_dog, (customer_id,))
                    dog_data = cursor.fetchone()

                    if dog_data:
                        # dog_name과 dog_remarks 가져오기
                        dog_name = dog_data[0]
                        dog_remarks = dog_data[1]

                        # check_in_status 테이블에 새 레코드 삽입
                        insert_query = """INSERT INTO check_in_status (id, name, dog_name, check_in, check_out, remarks)
                                          VALUES (%s, %s, %s, %s, NULL, %s)"""
                        cursor.execute(insert_query, (customer_id, name, dog_name, current_date, dog_remarks))

                        # DB 커밋
                        connection.commit()

                        cursor.close()
                        connection.close()

                        # 체크인 완료 메시지
                        QMessageBox.information(self, '체크인 완료', f'{name}님이 체크인되었습니다.')

                        # 테이블 갱신
                        self.fetch_data()  # fetch_data 메서드 호출하여 테이블 업데이트
                    else:
                        QMessageBox.warning(self, '오류', '해당 고객의 반려견 정보가 존재하지 않습니다.')
                else:
                    QMessageBox.warning(self, '오류', '고객 정보가 존재하지 않습니다.')
            else:
                QMessageBox.critical(self, '오류', '체크인 데이터베이스 연결에 실패했습니다.')
        else:
            print(f'{name} 체크인 취소.')





    def register(self):
        # 입력값 가져오기
        name = self.p2_name.text()
        gender = self.p2_gender.text()
        birth_date = self.p2_birth_date.text()
        phone_number = self.p2_phone_num.text()
        dog_name = self.p2_dog_name.text()
        dog_breed = self.p2_dog_breed.text()
        dog_gender = self.p2_dog_gender.text()
        dog_birth_year = self.p2_dog_birth_year.text()
        dog_neutered = self.p2_dog_neutered.text()
        dog_health_issue = self.p2_dog_health_issue.text()
        dog_vaccination_status = self.p2_dog_vaccination_status.text()
        dog_remarks = self.p2_dog_remarks.text()

        # DB 연결
        connection = self.connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()

                # 고객 정보 삽입
                insert_customer_query = """
                INSERT INTO customer_information (name, gender, birth_date, phone_number)
                VALUES (%s, %s, %s, %s)
                """
                customer_data = (name, gender, birth_date, phone_number)
                cursor.execute(insert_customer_query, customer_data)
                customer_id = cursor.lastrowid  # 마지막 삽입된 고객 ID 가져오기

                # 반려견 정보 삽입
                insert_dog_query = """
                INSERT INTO dog_information (id, dog_name, dog_breed, dog_gender, dog_birth_year,
                                             dog_neutered, dog_health_issue, dog_vaccination_status, dog_remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                dog_data = (customer_id, dog_name, dog_breed, dog_gender, dog_birth_year,
                            dog_neutered, dog_health_issue, dog_vaccination_status, dog_remarks)
                cursor.execute(insert_dog_query, dog_data)

                # 커밋
                connection.commit()
                QMessageBox.information(self, "Success", "등록 완료!")
                self.clear_fields()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"등록 실패: {e}")
                connection.rollback()  # 오류 발생 시 롤백

            finally:
                cursor.close()
                connection.close()  # 커넥션 종료
        else:
            QMessageBox.critical(self, "Error", "DB 연결 실패.")

    def clear_fields(self):
        # 입력 필드 초기화
        self.p2_name.clear()
        self.p2_birth_date.clear()
        self.p2_phone_num.clear()
        self.p2_dog_name.clear()
        self.p2_dog_breed.clear()
        self.p2_dog_gender.clear()
        self.p2_dog_birth_year.clear()
        self.p2_dog_neutered.clear()
        self.p2_dog_health_issue.clear()
        self.p2_dog_vaccination_status.clear()
        self.p2_dog_remarks.clear()
        self.p2_gender.clear()

    def fetch_data(self):
        try:
            connection = self.connect_to_db()
    
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, dog_name, check_in, check_out, remarks FROM check_in_status")  # 모든 컬럼을 선택
    
            # 결과 가져오기
            rows = cursor.fetchall()
            print(f"Fetched {len(rows)} rows")  # 디버깅 출력
            print(rows)  # rows의 내용을 출력하여 데이터가 정상적으로 가져와지는지 확인
    
            # 테이블 위젯 초기화
            self.p3_tableWidget.setRowCount(0)  # 테이블을 비웁니다.
    
            # 열 제목 설정 (여기서 컬럼 수도 정의합니다)
            self.p3_tableWidget.setColumnCount(6)
            self.p3_tableWidget.setHorizontalHeaderLabels(["ID", "Name", "Dog Name", "Check In", "Check Out", "Remarks"])
    
            # 데이터 추가
            for row in rows:
                row_position = self.p3_tableWidget.rowCount()  # 현재 테이블의 행 수
                self.p3_tableWidget.insertRow(row_position)  # 새로운 행 추가
    
                # 각 열에 데이터를 추가
                self.p3_tableWidget.setItem(row_position, 0, QTableWidgetItem(str(row[0])))  # ID
                self.p3_tableWidget.setItem(row_position, 1, QTableWidgetItem(row[1]))        # Name
                self.p3_tableWidget.setItem(row_position, 2, QTableWidgetItem(row[2]))        # Dog Name
                self.p3_tableWidget.setItem(row_position, 3, QTableWidgetItem(str(row[3])))  # Check In
                self.p3_tableWidget.setItem(row_position, 4, QTableWidgetItem(str(row[4])))  # Check Out
                self.p3_tableWidget.setItem(row_position, 5, QTableWidgetItem(row[5]))        # Remarks
            print(row[5],"asdasd")
    
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    

        
def transform(value, old_min, old_max, new_min, new_max):
    """값을 다른 범위로 변환"""
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

def handle_coordinates(conn): #min : 원점
    old_min_x = 0
    old_max_x = 480
    old_min_y = 0
    old_max_y = 300
    new_min_x = 1
    new_max_x = 79
    new_min_y = 1
    new_max_y = 49
    
    while True:
        try:
            request_data = conn.recv(4096)  # 데이터 수신
            if request_data:
                data = pickle.loads(request_data)
                
                if isinstance(data, tuple):
                    x_point = data[0]
                    y_point = data[1]
                    print(data)
                    print(f"x 좌표: {x_point}")
                    print(f"y 좌표: {y_point}")

                    x = x_point
                    y = y_point

                    # 좌표 변환 및 목표 위치 설정
                    transformed_x = int(transform(x, old_min_x, old_max_x, new_min_x, new_max_x))
                    transformed_y = int(transform(y, old_min_y, old_max_y, new_min_y, new_max_y))
                    print(transformed_x, transformed_y)

                elif isinstance(data, str):
                    direction = data
                    w = 0.4
                    if direction == "L":
                        v = w
                    elif direction == "R":
                        v = -w

                elif isinstance(data, int):
                    if data == 1:
                        coordinates = (0.3, 0.14)
                        x = coordinates[0]
                        y = coordinates[1]
                        print(x, y)
                    elif data == 2:
                        coordinates = (-0.15, 0.41)
                        x = coordinates[0]
                        y = coordinates[1]
                    elif data == 3:
                        coordinates = (-0.15, 0.72)
                        x = coordinates[0]
                        y = coordinates[1]
                    elif data == 4:
                        coordinates = (-0.15, 1.02)
                        x = coordinates[0]
                        y = coordinates[1]
                    elif data == 5:
                        coordinates = (-0.15, 1.34)
                        x = coordinates[0]
                        y = coordinates[1]
        except Exception as e:
            print(f"좌표 수신 중 오류 발생: {e}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 7000))  # 포트 7000에서 수신
    server_socket.listen(2)
    print("클라이언트 연결 대기 중...")

    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"클라이언트 {addr} 연결됨.")

            # 좌표 수신을 위한 쓰레드 시작
            coord_thread = threading.Thread(target=handle_coordinates, args=(conn,))
            coord_thread.start()

        except Exception as e:
            print(f"서버 오류 발생: {e}")

if __name__ == '__main__':
    # 서버 시작
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    sys.exit(app.exec_())
