import socket
import cv2
import pickle
import struct
import numpy as np
from utils import ARUCO_DICT, aruco_display
from cv2 import aruco
import time

def receive_video(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 4000))  # 서버 IP와 포트
    marker_types = ["DICT_5X5_100", "DICT_7X7_100"]
    matrix_coefficients_path = './calibration_matrix.npy'
    distortion_coefficients_path = './distortion_coefficients.npy'
    
    matrix_coefficients = np.load(matrix_coefficients_path)
    distortion_coefficients = np.load(distortion_coefficients_path)
    time.sleep(0.5)
    while True:
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
            # frame = cv2.resize(frame, dsize=(640,480))
            # frame_marker=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame_marker=cv2.UMat(frame_marker)
            frame = cv2.UMat(frame)
            for marker_type in marker_types:
            # ArUCo 사전 로드
                arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[marker_type])
                arucoParams = cv2.aruco.DetectorParameters()
                # 마커 감지
                aruco_detector = cv2.aruco.ArucoDetector(dictionary=arucoDict, detectorParams=arucoParams)
                corners, ids, rejected = aruco_detector.detectMarkers(frame)
                
                for corner in corners:
                    ndarray_image = corner.get()
                    
                    x_1 = ndarray_image[0][0][0]
                    y_1 = ndarray_image[0][0][1]
                    p_1 = (int(x_1),int(y_1))
                    
                    x_2 = ndarray_image[0][1][0]
                    y_2 = ndarray_image[0][1][1]
                    p_2 = (int(x_2),int(y_2))
                    
                    x_3 = ndarray_image[0][2][0]
                    y_3 = ndarray_image[0][2][1]
                    p_3 = (int(x_3),int(y_3))
                    
                    x_4 = ndarray_image[0][3][0]
                    y_4 = ndarray_image[0][3][1]
                    p_4 = (int(x_4),int(y_4))

                    cv2.putText(frame, '1', p_1, 2, 0.8, (254, 1, 15), 1, cv2.LINE_AA)
                    cv2.putText(frame, '2', p_2, 2, 0.8, (254, 1, 15), 1, cv2.LINE_AA)
                    cv2.putText(frame, '3', p_3, 2, 0.8, (254, 1, 15), 1, cv2.LINE_AA)
                    cv2.putText(frame, '4', p_4, 2, 0.8, (254, 1, 15), 1, cv2.LINE_AA)
                    
                    if len(corners) > 0:
                        for i in range(0, len(ids.get())):
                            if marker_type == 'DICT_5X5_100':
                            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
                                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i].get(), 0.052, matrix_coefficients, distortion_coefficients)
                            elif marker_type == 'DICT_7X7_100':
                            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
                                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i].get(), 0.062, matrix_coefficients, distortion_coefficients)                                            
                # aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.05)
                        if rvec is not None and tvec is not None:
                            print(f"rotation vector : {rvec}")
                            print(f"translation vector : {tvec}\n")
                            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec[0][0], tvec[0][0], 0.01)
                        # 감지된 마커 시각화
                frame_fin=cv2.aruco.drawDetectedMarkers(frame, corners, ids) 
                cv2.imshow('Received Video', frame_fin)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # elif cv2.waitKey(1) & 0xFF == ord('w'):
            #     filename = f'image_{int(cv2.getTickCount())}.png'
            #     cv2.imwrite(filename, frame)
            #     print(f"save image {filename}")
                
        except Exception as e:
                print(f"오류 발생: {e}")
                break
        # 영상 표시
    client_socket.close()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    server_ip = '192.168.0.4'  # Raspberry Pi의 IP 주소 입력
    receive_video(server_ip)