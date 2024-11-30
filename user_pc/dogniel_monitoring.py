import sys
import socket
import cv2
import pickle
import struct
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QStackedWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPolygon, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPoint, QTimer

class VideoStreamThread_cctv(QThread):
    update_frame_cctv = pyqtSignal(np.ndarray)

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

                frame = cv2.resize(frame, dsize=(480, 300))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR에서 RGB로 변환
                # 시그널로 numpy 배열을 전송
                self.update_frame_cctv.emit(frame)

            except Exception as e:
                print(f"오류 발생: {e}")
                break
        self.client_socket.close()

class VideoStreamThread(QThread):
    # 시그널 데이터 타입을 numpy.ndarray로 변경
    update_frame = pyqtSignal(np.ndarray)

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
                frame = cv2.resize(frame, dsize=(700, 500))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 시그널로 numpy 배열을 전송
                self.update_frame.emit(frame)

            except Exception as e:
                print(f"오류 발생: {e}")
                break
        self.client_socket.close()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./user_pc/dogniel_monitoring.ui', self)  # UI 파일 경로
        
        self.zoom_factor = 1.0
        self.width, self.height = self.dogniel_minibot_cam_Label.width(), self.dogniel_minibot_cam_Label.height()
        self.wr, self.hr = 3, 2  # 너비 : 높이
        
        #self.dogniel_turn_left_Button.setIcon(QIcon('./img_source/left_button.png'))
        #self.dogniel_turn_right_Button.setIcon(QIcon('./img_source/right_button.png'))
        
        self.dogniel_map_Label.setPixmap(QPixmap('/home/addinedu/ros-repo-demo/image_source/dogniel_map.png'))

        # 슬라이더의 값 변경 시 호출될 함수 연결
        self.dogniel_verticalSlider.valueChanged.connect(self.update_zoom)
        
        # 각방 버튼
        self.dogniel_room_1_Button.clicked.connect(self.room_1)
        self.dogniel_room_2_Button.clicked.connect(self.room_2)
        self.dogniel_room_3_Button.clicked.connect(self.room_3)
        self.dogniel_room_4_Button.clicked.connect(self.room_4)
        self.dogniel_room_5_Button.clicked.connect(self.room_5)
        
        self.dogniel_red_zone_1.setStyleSheet("background: transparent; border: none;")
        self.dogniel_red_zone_2.setStyleSheet("background: transparent; border: none;")
        self.dogniel_red_zone_3.setStyleSheet("background: transparent; border: none;")
        self.dogniel_red_zone_4.setStyleSheet("background: transparent; border: none;")
        
        ## 로봇 캠 스트리밍 스레드 시작
        #self.server_robot_ip = "192.168.0.4"  # CCTV의 IP주소
        #self.video_thread = VideoStreamThread(self.server_robot_ip)
        #self.video_thread.update_frame.connect(self.update_video_frame)
        #self.video_thread.start()
##
        ## CCTV 비디오 스트리밍 스레드 시작
        #self.server_cctv_ip = "192.168.0.6"  # CCTV의 IP주소
        #self.video_thread_cctv = VideoStreamThread_cctv(self.server_cctv_ip)
        #self.video_thread_cctv.update_frame_cctv.connect(self.update_video_frame_cctv)
        #self.video_thread_cctv.start()
    #
        ## 다른 서버와의 소켓 연결
        #self.target_server_ip = "localhost"  # 다른 서버의 IP 주소
        #self.target_server_port = 7000  # 다른 서버의 포트 번호
#
        #self.target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.target_socket.connect((self.target_server_ip, self.target_server_port))
        
        self.clicked_point = None
        #self.points = []  # 클릭한 점들을 저장하는 리스트

        self.dogniel_turn_left_Button.pressed.connect(self.turn_left)
        self.dogniel_turn_left_Button.released.connect(self.stop_turn_signal)
        self.dogniel_turn_right_Button.pressed.connect(self.turn_right)
        self.dogniel_turn_right_Button.released.connect(self.stop_turn_signal)
        
        self.dogniel_room_1_Button.clicked.connect(self.room_1)
        self.dogniel_room_2_Button.clicked.connect(self.room_2)
        self.dogniel_room_3_Button.clicked.connect(self.room_3)
        self.dogniel_room_4_Button.clicked.connect(self.room_4)
        self.dogniel_room_5_Button.clicked.connect(self.room_5)
        
        self.turn_timer = QTimer(self)
        self.turn_timer.timeout.connect(self.send_direction)  # 회전 신호 보내는 함수 연결
        
    def turn_left(self):
        self.turn_direction = "L"  # 왼쪽 방향
        self.turn_timer.start(100)  # 100ms 간격으로 신호 전송
        
        
    def turn_right(self):
        self.turn_direction = "R"  # 왼쪽 방향
        self.turn_timer.start(100)  # 100ms 간격으로 신호 전송
        
    def stop_turn_signal(self):
        self.turn_timer.stop()  # 타이머 정지
        
    def room_1(self):
        self.room_num = 1
        self.send_room_num()

    def room_2(self):
        self.room_num = 2
        self.send_room_num()

    def room_3(self):
        self.room_num = 3
        self.send_room_num()

    def room_4(self):
        self.room_num = 4
        self.send_room_num()

    def room_5(self):
        self.room_num = 5
        self.send_room_num()

    def mouseEnterEvent(self, event):
        # 마우스가 버튼 위에 올 때 GIF 시작
        self.dogniel_piramid_Button.show()

    def update_video_frame(self, frame):
        """QLabel에 비디오 프레임을 업데이트하는 함수."""
        # 원본 영상의 변환할 사각형 정의
        src_points = np.array([[0 + self.zoom_factor*self.wr, 0 + self.zoom_factor*self.hr],
                               [self.width - self.zoom_factor*self.wr, 0 + self.zoom_factor*self.hr],
                               [self.width - self.zoom_factor*self.wr, self.height - self.zoom_factor*self.hr],
                               [0 + self.zoom_factor*self.wr, self.height - self.zoom_factor*self.hr]], dtype='float32')
        # 출력 영상의 사각형 정의
        dst_points = np.array([[0, 0], [self.width, 0], [self.width, self.height], [0, self.height]], dtype='float32')
        # 원근 변환 행렬 계산
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        transformed_frame = cv2.warpPerspective(frame, matrix, (self.width, self.height))
        # QLabel 크기에 맞추기
        if transformed_frame.size != 0:
            h, w, ch = transformed_frame.shape
            bytes_per_line = ch * w
            image = QImage(transformed_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            scaled_frame = image.scaled(self.dogniel_minibot_cam_Label.size(), Qt.IgnoreAspectRatio)
            self.dogniel_minibot_cam_Label.setPixmap(QPixmap.fromImage(scaled_frame))

    def update_zoom(self, value):
        self.zoom_factor = value / 2
        
    def update_video_frame_cctv(self, frame):
        """QLabel에 CCTV 비디오 프레임을 업데이트하는 함수."""
        pos = [[338, 65], [479, 247], [3, 261], [155, 73]]
        cctv_width = self.dogniel_cctv_Label.width()
        cctv_height = self.dogniel_cctv_Label.height()
        # 원본 영상의 변환할 사각형 정의
        src_points = np.array(pos, dtype='float32')
        # 출력 영상의 사각형 정의
        dst_points = np.array([[0, 0], [cctv_width, 0], [cctv_width, cctv_height], [0, cctv_height]], dtype='float32')
        # 원근 변환 행렬 계산
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        transformed_frame = cv2.warpPerspective(frame, matrix, (cctv_width, cctv_height))
        # QLabel 크기에 맞추기
        if transformed_frame.size != 0:
            image = QImage(transformed_frame, transformed_frame.shape[1], transformed_frame.shape[0], QImage.Format_RGB888)
            scaled_frame = image.scaled(self.dogniel_cctv_Label.size(), Qt.IgnoreAspectRatio)
            self.dogniel_cctv_Label.setPixmap(QPixmap.fromImage(scaled_frame))

    def mousePressEvent(self, event): #dogniel_map_Label
        """마우스 왼쪽 클릭 시 좌표 저장"""
        if event.button() == Qt.LeftButton:
            if self.dogniel_map_Label.geometry().contains(event.pos()):
                self.clicked_point = event.pos() - self.dogniel_map_Label.pos()
                self.dogniel_map_Label.update()  # QLabel 업데이트
                print(f"Clicked Coordinates: {self.clicked_point.x()}, {self.clicked_point.y()}")
                
                # 클릭된 좌표를 서버로 전송
                self.send_coordinates(self.clicked_point)

    def paintEvent(self, event):
        self.dogniel_map_Label.setPixmap(QPixmap('/home/addinedu/ros-repo-demo/image_source/dogniel_map.png'))
        """QLabel에 마지막 클릭한 좌표를 표시"""
        if self.clicked_point:
            pixmap = self.dogniel_map_Label.pixmap()
            if pixmap:
                painter = QPainter(pixmap)
                
                # 빨간 점을 그리기
                painter.setPen(QColor(255, 0, 0))  # 빨간색
                painter.setBrush(QColor(255, 0, 0))  # 빨간색
                painter.drawEllipse(self.clicked_point, 5, 5)  # 반경 5로 점 그리기
                
                painter.end()

                # QLabel에 변경된 pixmap을 설정
                self.dogniel_map_Label.setPixmap(pixmap)
                
            self.dogniel_map_Label.update()  # QLabel 업데이트


    def send_coordinates(self, coords):
        """서버에 좌표 전송"""
        data = pickle.dumps((coords.x(), coords.y()))
        self.target_socket.sendall(data)
        
    def send_direction(self):
        """서버에 회전 신호 전송"""
        data = pickle.dumps(self.turn_direction)
        self.target_socket.sendall(data)

    def send_room_num(self):
        """서버에 회전 신호 전송"""
        data = pickle.dumps(self.room_num)
        self.target_socket.sendall(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    sys.exit(app.exec_())
