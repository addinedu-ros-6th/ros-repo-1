import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from dogniel import path_planner
import socket
import struct
import pickle
import threading
import cv2
import numpy as np

# 경로 계산 결과를 보관하는 리스트
path_list = []

# 이미지를 읽어와 맵을 처리
png_img = cv2.imread('/home/jun/ros-repo-1/image_source/dogniel_map_grid.png', cv2.COLOR_BGR2GRAY)

def transform(value, old_min, old_max, new_min, new_max):
    new_value = ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return new_value

# PathPublisher 클래스 정의
class PathPublisher(Node):
    def __init__(self):
        super().__init__('path_publisher')  # 노드 이름
        self.publisher = self.create_publisher(String, 'path_result', 10)  # 토픽 이름과 큐 크기

    def publish_path(self, result):
        if result:  # result가 비어 있지 않으면
            result_str = ' '.join(map(str, result))  # 리스트를 문자열로 변환
            msg = String()
            msg.data = result_str
            self.publisher.publish(msg)  # 메시지 발행
            self.get_logger().info(f"발행된 경로: {result_str}")
        else:
            self.get_logger().info("결과가 없으므로 경로를 발행하지 않습니다.")

# 클라이언트로부터 좌표를 처리하는 함수
def handle_coordinates(conn, path_publisher):
    old_min_x = 0
    old_max_x = 480
    old_min_y = 0
    old_max_y = 300
    new_min_x = 0
    new_max_x = 80
    new_min_y = 0
    new_max_y = 50
    while True:
        try:
            coord_data = conn.recv(4096)  # 좌표 데이터 수신
            if coord_data:
                coordinates = pickle.loads(coord_data)
                print(f"받은 좌표: {coordinates}")
                x = int(round((transform(coordinates[0], old_min_x, old_max_x, new_min_x, new_max_x)), 0))
                y = int(round((transform(coordinates[1], old_min_y, old_max_y, new_min_y, new_max_y)), 0))
                pos = (y, x)
                print(f"변환된 좌표{pos}")
                make_path(pos, path_publisher)  # 경로 계산 후 퍼블리시
        except Exception as e:
            print(f"좌표 수신 중 오류 발생: {e}")

# 경로 계산 및 퍼블리시하는 함수
def make_path(pos, path_publisher):
    path_list = []
    transmap = path_planner.map_change(png_img)
    temp_map = transmap
    make_route = path_planner.Astar()
    start = (24, 69)  # 시작 위치
    end = pos  # 도착 위치
    result, path = make_route.run(temp_map, start, end)

    if not path:  # 경로가 존재하지 않으면
        return []  # 빈 리스트 반환 (결과가 없으면)

    # 경로가 있으면 directions를 계산
    directions = []
    current_position = path[0]
    current_direction = None
    current_distance = 0

    for next_position in path[1:]:
        if next_position[0] == current_position[0]:
            if next_position[1] < current_position[1]:
                direction = 'S'
                distance = current_position[1] - next_position[1]
            else:
                direction = 'N'
                distance = next_position[1] - current_position[1]
        elif next_position[1] == current_position[1]:
            if next_position[0] > current_position[0]:
                direction = 'E'
                distance = next_position[0] - current_position[0]
            else:
                direction = 'W'
                distance = current_position[0] - next_position[0]

        if current_direction != direction:
            if current_direction is not None:
                directions.append((current_direction, current_distance))
            current_direction = direction
            current_distance = distance
        else:
            current_distance += distance

        current_position = next_position

    directions.append((current_direction, current_distance))  # 마지막 방향과 거리 추가

    result = []
    for direction, distance in directions:
        result.append(direction)
        result.append(distance)

    # result가 비어 있지 않으면 퍼블리시
    if result:
        path_publisher.publish_path(result)
        print(result)
    else:
        print("경로가 없어서 퍼블리시하지 않습니다.")
    
    return result

# 서버 시작 함수
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 7000))  # 포트 7000에서 수신
    server_socket.listen(1)
    print("클라이언트 연결 대기 중...")

    rclpy.init()  # ROS 2 초기화
    path_publisher = PathPublisher()  # PathPublisher 객체 생성

    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"클라이언트 {addr} 연결됨.")

            # 좌표 수신을 위한 쓰레드 시작
            coord_thread = threading.Thread(target=handle_coordinates, args=(conn, path_publisher))
            coord_thread.start()

        except Exception as e:
            print(f"서버 오류 발생: {e}")

# ROS 2 노드 실행
if __name__ == "__main__":
    main()
