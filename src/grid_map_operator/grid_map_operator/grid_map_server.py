# 이것이 가장 최근코드다

import os
import rclpy as rp
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msg.action import PathPlanner
from ament_index_python.packages import get_package_share_directory
from queue import Queue
from multiprocessing import Process
import numpy as np
from geometry_msgs.msg import Twist
from math import atan2, pi
import cv2

def inflation_generator(x, y, map):
    rows = x
    cols = y

    # 상하좌우 방향 (위, 아래, 왼쪽, 오른쪽)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 변경 상태를 추적하는 배열
    changed = True  # 변경이 있을 때까지 반복

    while changed:
        changed = False
        # 새로운 행렬을 저장할 numpy 배열 (한 번 변경할 때마다 갱신)
        new_matrix = map.copy()  # map의 복사본을 생성 (numpy의 copy 사용)

        # 행렬을 순회
        for i in range(rows):
            for j in range(cols):
                if map[i][j] == 1:  # 1은 벽을 의미
                    # '1'에 인접한 '0'을 찾음
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and map[ni][nj] == 0:
                            # 인접한 '0'을 '3'으로 변경
                            if new_matrix[ni][nj] == 0:  # 변경되지 않은 '0'에 대해서만
                                new_matrix[ni][nj] = 3
                                changed = True  # 변경이 있으면 플래그 True로 설정

        # map을 new_matrix로 갱신
        map = new_matrix.copy()  # 변경된 행렬로 갱신
        
    return map  # 최종 결과 반환

def map_change(map):
    origin_map = np.array(map)  # 이미지를 가져와 맵을 만들 데이터로 분리
    print("origin_map_shape : ", origin_map.shape)
    height = origin_map.shape[0]  # 높이
    width = origin_map.shape[1]  # 넓이
    
    for i in range(height):  # 행
        for j in range(width):  # 열
            point = origin_map[i][j]
            if point == 0:  # 각 행열칸에 들어있는 값이 0인 경우 벽
                origin_map[i][j] = 1  # 벽은 1
            elif point == 205:  # 길은 205로 표시되어 있다면
                origin_map[i][j] = 0  # 길은 0
    
    inflation_map = inflation_generator(height, width, origin_map)
    return inflation_map

def distance_walker(self,path,msg):
    i=1
    msg.linear.x = 0.0
    count = 1
    
    
            
    msg.linear.x = float(count)
    print(f"distance : {count*3}cm " )
    self.cmd_vel_pub.publish(msg)
    
        

def driving_bot(self,path,msg):
    self.msg = msg
    # current_direction = None
    # path_direction = None
    # if 0.9 < start_direction <= 1:
    #     current_direction = "west"
    # elif -0.8 <= start_direction <= -0.75:
    #     current_direction = 'north'
    # elif 0.7 <= start_direction <= 0.85:
    #     current_direction = 'south'
    # elif start_direction < 0.15:
    #     current_direction = 'east'
    
    distance_walker(self,path,self.msg)

    # # 연속된 x 값과 y 값의 카운트를 저장할 변수
    # x_count = 1  # 첫 번째 값부터 시작하므로 1로 초기화
    # y_count = 1
    # repeated_x = {}  # 연속된 x 값의 카운트를 저장할 딕셔너리
    # repeated_y = {}  # 연속된 y 값의 카운트를 저장할 딕셔너리

    # # 경로의 각 (x, y) 값을 순회
    # for i in range(1, len(item)):
    #     # x 값이 연속되면 x_count 증가, 아니면 카운트하고 리셋
    #     if path[i][0] == path[i-1][0]:
    #         x_count += 1
    #     else:
    #         repeated_x[item[i-1][0]] = x_count
    #         x_count = 1  # 연속이 끊어졌으므로 카운트를 1로 초기화

    #     # y 값이 연속되면 y_count 증가, 아니면 카운트하고 리셋
    #     if item[i][1] == item[i-1][1]:
    #         y_count += 1
    #     else:
    #         repeated_y[item[i-1][1]] = y_count
    #         y_count = 1  # 연속이 끊어졌으므로 카운트를 1로 초기화

    # # 마지막 값 처리 (마지막 값의 연속 개수를 딕셔너리에 저장)
    # repeated_x[item[-1][0]] = x_count
    # repeated_y[item[-1][1]] = y_count








 





# A* 알고리즘을 위한 클래스
class Astar:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def heuristic(self, node, goal, D=1):
        dx = abs(node.position[0] - goal.position[0])
        dy = abs(node.position[1] - goal.position[1])
        return D * (dx + dy)

    def is_safe_from_obstacles(self, maze, position):
        """이동할 위치가 2칸 내에 1이나 3이 있는지 체크"""
        x, y = position
        # 주변 2칸 범위 확인 (상하좌우, 대각선 포함)
        for i in range(max(0, x - 3), min(len(maze), x + 3)):
            for j in range(max(0, y - 3), min(len(maze[0]), y + 3)):
                if maze[i][j] == 1 or maze[i][j] == 3:
                    return False  # 1 또는 3을 만났으므로 안전하지 않음
        return True  # 안전한 위치

    def aStar(self, maze, start, end):
        startNode = Astar(None, start)
        endNode = Astar(None, end)
        openList = [startNode]
        closedList = []
        
        while openList:
            currentNode = openList[0]
            currentIdx = 0
            for index, item in enumerate(openList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIdx = index
            openList.pop(currentIdx)
            closedList.append(currentNode)
            if currentNode == endNode:
                path = []
                current = currentNode
                while current is not None:
                    x, y = current.position
                    maze[x][y] = 2
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            children = []
            for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
                if (0 <= nodePosition[0] < len(maze)) and (0 <= nodePosition[1] < len(maze[0])) and maze[nodePosition[0]][nodePosition[1]] == 0:
                    if not self.is_safe_from_obstacles(maze, nodePosition):  # 장애물 근처는 피하도록 추가
                        continue
                    new_node = Astar(currentNode, nodePosition)
                    children.append(new_node)

            for child in children:
                if child in closedList:
                    continue
                child.g = currentNode.g + 1
                child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
                child.f = child.g + child.h
                if len([openNode for openNode in openList if child == openNode and child.g > openNode.g]) > 0:
                    continue
                openList.append(child)

    def run(self, maze, start, end):
        path = self.aStar(maze, start, end)
        return maze, path


# AMCL Listener 클래스
class amcl_listener(Node):
    def __init__(self, domain_id, state_queue):
        super().__init__('amcl_listener_' + str(domain_id))
        self.domain_id = domain_id
        self.state_queue = state_queue
        
        # AMCL 위치 정보 초기화
        self.current_pos_x = None
        self.current_pos_y = None
        self.current_pos_orientation_z = None

        # 구독 설정
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            'amcl_pose',  # 동일한 주제 이름
            self.listener_callback,
            10
        )
        self.get_logger().info(f"AMCL Listener node initialized for domain_id={domain_id}")

    def listener_callback(self, msg):
        # amcl_pose 정보를 받아옴
        self.current_pos_x = msg.pose.pose.position.x
        self.current_pos_y = msg.pose.pose.position.y
        self.current_pos_orientation_z = msg.pose.pose.orientation.z
        
        self.get_logger().info(f"Received amcl_pose: pos_x={self.current_pos_x}, pos_y={self.current_pos_y}, orientation_z={self.current_pos_orientation_z}")

    def get_current_position(self):
        """현재 위치를 반환하는 메서드"""
        return self.current_pos_x, self.current_pos_y, self.current_pos_orientation_z


# Botplanner 클래스, 경로 계획을 수행하는 부분
class Botplanner(Node):
    def __init__(self, domain_id, state_queue, amcl_listener):
        super().__init__('Bot_planner_' + str(domain_id))
        self._action_server = ActionServer(self, PathPlanner, 'pathplanner', self.execute_callback)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.state_queue = state_queue
        self.amcl_listener = amcl_listener  # amcl_listener 인스턴스를 받음
        self.msg = Twist()
        
        
        #-----------------------------------------------------------------

        make_route = Astar()
        bringup_dir = get_package_share_directory('grid_map_operator')
        png_img = os.path.join(bringup_dir, 'map', 'dogniel_map.png')
        png_img = cv2.imread(png_img,cv2.COLOR_BGR2GRAY)
        transmap = map_change(png_img)

        start = (25,69)  # AMCL 위치 사용
        end = (6,15)
        

        result_map, path = make_route.run(transmap, start, end)
        
        driving_bot(self,path,self.msg)
        #-----------------------------------------------------------------
    def execute_callback(self, goal_handle):
        goal_pos_x = goal_handle.request.pos_x
        goal_pos_y = goal_handle.request.pos_y
        goal_pos_orientation_z = goal_handle.request.pos_orientation_z
        self.get_logger().info(f"Received Goal: pos_x={goal_pos_x}, pos_y={goal_pos_y}, orientation_z={goal_pos_orientation_z}")
        
        # AMCL 위치 정보 가져오기
        start_pos_x, start_pos_y, start_pos_orientation_z = self.amcl_listener.get_current_position()
        

        # 상태를 'working'으로 갱신
        self.state_queue.put('working')  # 상태를 'working'으로 설정
        
        make_route = Astar()
        bringup_dir = get_package_share_directory('grid_map_operator')
        png_img = os.path.join(bringup_dir, 'map', 'dogniel_map.png')
        transmap = map_change(png_img)

        start = (int(start_pos_x), int(start_pos_y))  # AMCL 위치 사용
        end = (int(goal_pos_x), int(goal_pos_y))
        

        result_map, path = make_route.run(transmap, start, end)
        
        driving_bot(self,path) 

        # feedback = PathPlanner.Feedback()
        # feedback.pos_x = start_pos_x
        # feedback.pos_y = start_pos_y
        # feedback.pos_orientation_z = start_pos_orientation_z

        # goal_handle.publish_feedback(feedback)

        result_msg = PathPlanner.Result()
        result_msg.success = True
        result_msg.pos_x = self.amcl_listener.current_pos_x
        result_msg.pos_y = self.amcl_listener.current_pos_y
        result_msg.pos_orientation_z = self.amcl_listener.current_pos_orientation_z
        
        

        # 상태를 'standby'로 갱신
        self.state_queue.put('standby')  # 상태를 'standby'로 설정
        
        transmap = map_change(png_img)

        return result_msg


# 프로세스마다 ROS_DOMAIN_ID를 별도로 설정하는 함수
def bot_planner_process(domain_id, state_queue):
    os.environ['ROS_DOMAIN_ID'] = str(domain_id)  # 각 프로세스마다 ROS_DOMAIN_ID를 설정
    rp.init()
    
    # AMCL Listener 인스턴스를 먼저 생성
    amcl_listener_node = amcl_listener(domain_id, state_queue)
    
    # Botplanner 인스턴스 생성시 AMCL Listener 인스턴스를 전달
    bot_planner = Botplanner(domain_id, state_queue, amcl_listener_node)
    
    executor = rp.executors.MultiThreadedExecutor()
    
    executor.add_node(bot_planner)
    executor.add_node(amcl_listener_node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        rp.shutdown()


# 메인 함수
def main():
    queue_92 = Queue()
    queue_82 = Queue()

    process_92 = Process(target=bot_planner_process, args=(92, queue_92))
    process_82 = Process(target=bot_planner_process, args=(82, queue_82))

    process_92.start()
    process_82.start()

    process_92.join()
    process_82.join()


if __name__ == '__main__':
    main()


