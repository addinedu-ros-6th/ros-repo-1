import socket
import cv2
import pickle
import struct
import numpy as np
import math
import threading
from utils import ARUCO_DICT, aruco_display
from cv2 import aruco
import time
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from dogniel_msgs.msg import ArucoData
from rclpy.executors import MultiThreadedExecutor
import utils

class ArucoDataPublisher(Node):
    def __init__(self):
        super().__init__('aruco_data_publisher')
        self.publisher_ = self.create_publisher(ArucoData, '/aruco_data', 10)

    def publish_message(self, id, theta, z):
        msg = ArucoData()
        msg.id = id
        msg.theta = theta
        msg.z = z
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: id={msg.id}, theta={msg.theta}, z={msg.z}')

def receive_video(server_ip, aruco_pub):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 4000))  # 서버 IP와 포트

    marker_types = ["DICT_5X5_100", "DICT_7X7_100"]
    matrix_coefficients_path = '/home/addinedu/ros2_ws/src/dogniel/dogniel/calibration_matrix.npy'
    distortion_coefficients_path = '/home/addinedu/ros2_ws/src/dogniel/dogniel/distortion_coefficients.npy'
    
    matrix_coefficients = np.load(matrix_coefficients_path)
    distortion_coefficients = np.load(distortion_coefficients_path)
    
    time.sleep(0.5)

    while rclpy.ok():
        try:
            data_size_bytes = client_socket.recv(struct.calcsize('L'))
            if not data_size_bytes:
                print("클라이언트와의 연결이 끊어졌습니다.")
                break
            data_size = struct.unpack('L', data_size_bytes)[0]
            data = b''
            while len(data) < data_size:
                packet = client_socket.recv(data_size - len(data))
                if not packet:
                    print("클라이언트와의 연결이 끊어졌습니다.")
                    break
                data += packet
            frame = pickle.loads(data)
            frame = cv2.UMat(frame)

            for marker_type in marker_types:
                arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[marker_type])
                arucoParams = cv2.aruco.DetectorParameters()
                aruco_detector = cv2.aruco.ArucoDetector(dictionary=arucoDict, detectorParams=arucoParams)
                corners, ids, rejected = aruco_detector.detectMarkers(frame)

                for corner in corners:
                    ndarray_image = corner.get()
                    if len(corners) > 0:
                        for i in range(0, len(ids.get())):
                            if marker_type == 'DICT_5X5_100':
                                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i].get(), 0.052, matrix_coefficients, distortion_coefficients)
                            elif marker_type == 'DICT_7X7_100':
                                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i].get(), 0.062, matrix_coefficients, distortion_coefficients)
                            
                            if rvec is not None and tvec is not None:
                                if rvec[0][0][0] > 0:
                                    rvec[0][0][2] = rvec[0][0][2] * -1
                                
                                # ArUco 마커의 회전 및 위치 정보
                                id = int(ids.get()[0][0])
                                theta = rvec[0][0][2]  # 회전각 (단위: 라디안)
                                z = tvec[0][0][2] - 0.04  # Z축 위치
                                
                                x = tvec[0][0][0]
                                
                                if abs(x) < 0.02:
                                    aruco_pub.publish_message(id, theta, z)
                                    print(f"Published: id={id}, theta={theta}, z={z}")

                                np.set_printoptions(precision=2)
                                cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec[0][0], tvec[0][0], 0.01)

                frame_fin = cv2.aruco.drawDetectedMarkers(frame, corners, ids) 
                cv2.imshow('Received Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"오류 발생: {e}")
            break

    client_socket.close()
    cv2.destroyAllWindows()

def main():
    rclpy.init()

    aruco_pub = ArucoDataPublisher()

    # 서버 IP 설정 (Raspberry Pi 또는 다른 서버의 IP)
    server_ip = '192.168.0.4'  # Raspberry Pi의 IP 주소 입력

    # 비디오 수신을 별도의 스레드에서 실행
    video_thread = threading.Thread(target=receive_video, args=(server_ip, aruco_pub))
    video_thread.start()

    # ROS2 spin (토픽 구독을 계속 처리)
    rclpy.spin(aruco_pub)

    # 비디오 스레드 종료 후 ROS2 종료
    video_thread.join()
    aruco_pub.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
