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

# def driving_bot(self,path):
#     linear_cmd_3cm = 0.08
#     angular_cmd_45 = 0.785
#     angular_cmd_90 = 1.57
#     current_direction = 'west'
#     if self.current_pos_orientation_z == 1:
#         current_direction = 'west'
#     elif 
    
#     index,item = path
    



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


# Botplanner 클래스, 경로 계획을 수행하는 부분
class Botplanner(Node):
    def __init__(self, domain_id, state_queue):
        super().__init__('Bot_planner_' + str(domain_id))
        self._action_server = ActionServer(self, PathPlanner, 'pathplanner', self.execute_callback)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.current_pos_x = None
        self.current_pos_y = None
        self.current_pos_orientation_z = None
        self.state_queue = state_queue

    def execute_callback(self, goal_handle):
        goal_pos_x = goal_handle.request.pos_x
        goal_pos_y = goal_handle.request.pos_y
        goal_pos_orientation_z = goal_handle.request.orientation_z
        self.get_logger().info(f"Received Goal: pos_x={goal_pos_x}, pos_y={goal_pos_y}, orientation_z={goal_pos_orientation_z}")
        
        # 상태를 'working'으로 갱신
        self.state_queue.put('working')  # 상태를 'working'으로 설정
        
        make_route = Astar()
        bringup_dir = get_package_share_directory('grid_map_operator')
        png_img = os.path.join(bringup_dir, 'map', 'dogniel_map.png')
        transmap = map_change(png_img)

        start = (int(self.current_pos_x), int(self.current_pos_y))
        end = (int(goal_pos_x), int(goal_pos_y))

        result_map, path = make_route.run(transmap, start, end)
        
        # driving_bot(path)

        feedback = PathPlanner.Feedback()
        feedback.pos_x = self.current_pos_x
        feedback.pos_y = self.current_pos_y
        feedback.pos_orientation_z = self.current_pos_orientation_z

        goal_handle.publish_feedback(feedback)

        result_msg = PathPlanner.Result()
        result_msg.success = True
        result_msg.pos_x = self.current_pos_x
        result_msg.pos_y = self.current_pos_y
        result_msg.pos_orientation_z = self.current_pos_orientation_z

        
        # 상태를 'standby'로 갱신
        self.state_queue.put('standby')  # 상태를 'standby'로 설정

        return result_msg


# AMCL Listener 클래스
class amcl_listener(Node):
    def __init__(self, bot_planner_node, domain_id, state_queue):
        super().__init__('amcl_listener_' + str(domain_id))
        self.bot_planner_node = bot_planner_node
        self.domain_id = domain_id
        self.state_queue = state_queue
        
        # 구독 설정
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            'amcl_pose',  # 동일한 주제 이름
            self.listener_callback,
            10
        )
        self.get_logger().info(f"AMCL Listener node initialized for domain_id={domain_id}")

    def listener_callback(self, msg):
        self.current_pos_x = msg.pose.pose.position.x
        self.current_pos_y = msg.pose.pose.position.y
        self.current_pos_orientation_z = msg.pose.pose.orientation.z

        self.bot_planner_node.current_pos_x = self.current_pos_x
        self.bot_planner_node.current_pos_y = self.current_pos_y
        self.bot_planner_node.current_pos_orientation_z = self.current_pos_orientation_z
        self.get_logger().info(f"Received amcl_pose: pos_x={self.bot_planner_node.current_pos_x}, pos_y={self.bot_planner_node.current_pos_y}, orientation_z={self.bot_planner_node.current_pos_orientation_z}")


# 프로세스마다 ROS_DOMAIN_ID를 별도로 설정하는 함수
def bot_planner_process(domain_id, state_queue):
    os.environ['ROS_DOMAIN_ID'] = str(domain_id)  # 각 프로세스마다 ROS_DOMAIN_ID를 설정
    rp.init()
    bot_planner = Botplanner(domain_id, state_queue)
    amcl_listener_node = amcl_listener(bot_planner, domain_id, state_queue)
    
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



#-------------------------------------------------------------------------------------------------------------#

# import time
# import queue
# from concurrent.futures import ThreadPoolExecutor
# import rclpy as rp
# from rclpy.node import Node
# from geometry_msgs.msg import PoseWithCovarianceStamped
# from nav_msg.action import PathPlanner
# from ament_index_python.packages import get_package_share_directory
# from multiprocessing import Queue

# # 상태 갱신을 담당하는 함수
# def update_robot_state(queue_92, queue_82, robot_92_state, robot_82_state):
#     # 큐에 상태가 있으면 상태 갱신
#     if not queue_92.empty():
#         robot_92_state = queue_92.get()  # 큐에서 상태 가져오기
#         print(f"Robot 92 State Updated: {robot_92_state}")

#     if not queue_82.empty():
#         robot_82_state = queue_82.get()  # 큐에서 상태 가져오기
#         print(f"Robot 82 State Updated: {robot_82_state}")
    
#     return robot_92_state, robot_82_state

# # A* 알고리즘을 위한 클래스
# class Astar:
#     def __init__(self, parent=None, position=None):
#         self.parent = parent
#         self.position = position
#         self.g = 0
#         self.h = 0
#         self.f = 0

#     def __eq__(self, other):
#         return self.position == other.position

#     def heuristic(self, node, goal, D=1):
#         dx = abs(node.position[0] - goal.position[0])
#         dy = abs(node.position[1] - goal.position[1])
#         return D * (dx + dy)

#     def is_safe_from_obstacles(self, maze, position):
#         """이동할 위치가 2칸 내에 1이나 3이 있는지 체크"""
#         x, y = position
#         for i in range(max(0, x - 2), min(len(maze), x + 2)):
#             for j in range(max(0, y - 2), min(len(maze[0]), y + 2)):
#                 if maze[i][j] == 1 or maze[i][j] == 3:
#                     return False  # 장애물 근처는 안전하지 않음
#         return True

#     def aStar(self, maze, start, end):
#         startNode = Astar(None, start)
#         endNode = Astar(None, end)
#         openList = [startNode]
#         closedList = []
        
#         while openList:
#             currentNode = openList[0]
#             currentIdx = 0
#             for index, item in enumerate(openList):
#                 if item.f < currentNode.f:
#                     currentNode = item
#                     currentIdx = index
#             openList.pop(currentIdx)
#             closedList.append(currentNode)
#             if currentNode == endNode:
#                 path = []
#                 current = currentNode
#                 while current is not None:
#                     x, y = current.position
#                     maze[x][y] = 2
#                     path.append(current.position)
#                     current = current.parent
#                 return path[::-1]

#             children = []
#             for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
#                 nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
#                 if (0 <= nodePosition[0] < len(maze)) and (0 <= nodePosition[1] < len(maze[0])) and maze[nodePosition[0]][nodePosition[1]] == 0:
#                     if not self.is_safe_from_obstacles(maze, nodePosition):  # 장애물 근처는 피하도록 추가
#                         continue
#                     new_node = Astar(currentNode, nodePosition)
#                     children.append(new_node)

#             for child in children:
#                 if child in closedList:
#                     continue
#                 child.g = currentNode.g + 1
#                 child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
#                 child.f = child.g + child.h
#                 if len([openNode for openNode in openList if child == openNode and child.g > openNode.g]) > 0:
#                     continue
#                 openList.append(child)

#     def run(self, maze, start, end):
#         path = self.aStar(maze, start, end)
#         return maze, path

# # Botplanner 노드 (경로 계획 및 상태 관리)
# class Botplanner(Node):
#     def __init__(self, domain_id, queue):
#         super().__init__('Bot_planner_' + str(domain_id))
#         os.environ['ROS_DOMAIN_ID'] = str(domain_id)  # Set the ROS domain ID
#         self._action_server = ActionServer(self, PathPlanner, 'pathplanner', self.execute_callback)
#         self.current_pos_x = None
#         self.current_pos_y = None
#         self.current_pos_orientation_z = None
#         self.queue = queue

#     def execute_callback(self, goal_handle):
#         goal_pos_x = goal_handle.request.pos_x
#         goal_pos_y = goal_handle.request.pos_y
#         goal_pos_orientation_z = goal_handle.request.orientation_z
#         self.get_logger().info(f"Received Goal: pos_x={goal_pos_x}, pos_y={goal_pos_y}, orientation_z={goal_pos_orientation_z}")

#         make_route = Astar()
#         bringup_dir = get_package_share_directory('grid_map_operator')
#         png_img = os.path.join(bringup_dir, 'map', 'dogniel_map.png')
#         transmap = map_change(png_img)

#         start = (int(self.current_pos_x), int(self.current_pos_y))
#         end = (int(goal_pos_x), int(goal_pos_y))

#         result_map, path = make_route.run(transmap, start, end)

#         feedback = PathPlanner.Feedback()
#         feedback.pos_x = self.current_pos_x
#         feedback.pos_y = self.current_pos_y
#         feedback.pos_orientation_z = self.current_pos_orientation_z

#         goal_handle.publish_feedback(feedback)

#         result_msg = PathPlanner.Result()
#         result_msg.success = True
#         result_msg.pos_x = self.current_pos_x
#         result_msg.pos_y = self.current_pos_y
#         result_msg.pos_orientation_z = self.current_pos_orientation_z

#         self.queue.put(result_msg)

#         return result_msg

# # AMCL listener 노드 (로봇 위치 정보 구독)
# class AmclListener(Node):
#     def __init__(self, bot_planner_node, domain_id, queue):
#         super().__init__('amcl_listener_' + str(domain_id))
#         self.bot_planner_node = bot_planner_node
#         self.domain_id = domain_id
#         self.queue = queue

#         self.get_logger().info(f"AMCL Listener Node (Domain {self.domain_id}) started, subscribing to 'amcl_pose' topic.")
        
#         self.subscription = self.create_subscription(
#             PoseWithCovarianceStamped,
#             'amcl_pose', 
#             self.listener_callback,
#             10
#         )

#     def listener_callback(self, msg):
#         self.current_pos_x = msg.pose.pose.position.x
#         self.current_pos_y = msg.pose.pose.position.y
#         self.current_pos_orientation_z = msg.pose.pose.orientation.z

#         self.get_logger().info(f"Received AMCL Pose (Domain {self.domain_id}): x={self.current_pos_x}, y={self.current_pos_y}, z={self.current_pos_orientation_z}")

#         self.bot_planner_node.current_pos_x = self.current_pos_x
#         self.bot_planner_node.current_pos_y = self.current_pos_y
#         self.bot_planner_node.current_pos_orientation_z = self.current_pos_orientation_z

#         self.queue.put((self.current_pos_x, self.current_pos_y, self.current_pos_orientation_z))

# # 상태 업데이트를 관리하는 클래스
# class StateUpdater:
#     def __init__(self, queue_92, queue_82):
#         self.queue_92 = queue_92
#         self.queue_82 = queue_82
#         self.robot_92_state = 'standby'
#         self.robot_82_state = 'standby'
#         self.executor = ThreadPoolExecutor(max_workers=1)  # 1개의 워커 스레드 사용

#     def start_updating(self):
#         # 큐에 변화가 있을 때마다 상태를 갱신
#         self.executor.submit(self._update_state)

#     def _update_state(self):
#         # 큐에서 상태를 갱신하는 비동기 작업
#         self.robot_92_state, self.robot_82_state = update_robot_state(
#             self.queue_92, self.queue_82, self.robot_92_state, self.robot_82_state
#         )

# # 전체 프로세스를 실행하는 함수
# def bot_planner_process(domain_id, queue):
#     rp.init()
#     bot_planner = Botplanner(domain_id, queue)
#     amcl_listener_node = AmclListener(bot_planner, domain_id, queue)

#     executor = rp.executors.MultiThreadedExecutor()
#     executor.add_node(bot_planner)
#     executor.add_node(amcl_listener_node)

#     try:
#         executor.spin()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         rp.shutdown()
#         bot_planner.destroy_node()
#         amcl_listener_node.destroy_node()

# # 메인 함수
# def main():
#     # 두 개의 큐 설정 (로봇 92와 82의 상태 관리)
#     queue_92 = Queue()
#     queue_82 = Queue()

#     # 상태 갱신기 설정
#     state_updater = StateUpdater(queue_92, queue_82)

#     # BotPlanner 프로세스 실행
#     domain_id_92 = 92
#     domain_id_82 = 82

#     # 비동기적으로 상태 갱신 시작
#     state_updater.start_updating()

#     bot_planner_process(domain_id_92, queue_92)
#     bot_planner_process(domain_id_82, queue_82)

# if __name__ == '__main__':
#     main()



# import cv2
# import numpy as np
# import os
# import rclpy as rp
# from rclpy.action import ActionServer
# from rclpy.node import Node
# from geometry_msgs.msg import PoseWithCovarianceStamped
# from nav_msg.action import PathPlanner
# from rclpy.executors import MultiThreadedExecutor
# from ament_index_python.packages import get_package_share_directory

# # 맵을 inflation 처리하는 함수
# def inflation_generator(x, y, map):
#     rows = x
#     cols = y
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#     changed = True
#     while changed:
#         changed = False
#         new_matrix = map.copy()
#         for i in range(rows):
#             for j in range(cols):
#                 if map[i][j] == 1:
#                     for di, dj in directions:
#                         ni, nj = i + di, j + dj
#                         if 0 <= ni < rows and 0 <= nj < cols and map[ni][nj] == 0:
#                             if new_matrix[ni][nj] == 0:
#                                 new_matrix[ni][nj] = 3
#                                 changed = True
#         map = new_matrix.copy()
#     return map

# def map_change(map):
#     origin_map = np.array(map)
#     height = origin_map.shape[0]
#     width = origin_map.shape[1]
#     for i in range(height):
#         for j in range(width):
#             point = origin_map[i][j]
#             if point == 0:
#                 origin_map[i][j] = 1
#             elif point == 205:
#                 origin_map[i][j] = 0
#     inflation_map = inflation_generator(height, width, origin_map)
#     return inflation_map

# # A* 알고리즘을 위한 클래스
# class Astar:
#     def __init__(self, parent=None, position=None):
#         self.parent = parent
#         self.position = position
#         self.g = 0
#         self.h = 0
#         self.f = 0

#     def __eq__(self, other):
#         return self.position == other.position

#     def heuristic(self, node, goal, D=1):
#         dx = abs(node.position[0] - goal.position[0])
#         dy = abs(node.position[1] - goal.position[1])
#         return D * (dx + dy)

#     def aStar(self, maze, start, end):
#         startNode = Astar(None, start)
#         endNode = Astar(None, end)
#         openList = [startNode]
#         closedList = []
#         while openList:
#             currentNode = openList[0]
#             currentIdx = 0
#             for index, item in enumerate(openList):
#                 if item.f < currentNode.f:
#                     currentNode = item
#                     currentIdx = index
#             openList.pop(currentIdx)
#             closedList.append(currentNode)
#             if currentNode == endNode:
#                 path = []
#                 current = currentNode
#                 while current is not None:
#                     x, y = current.position
#                     maze[x][y] = 2
#                     path.append(current.position)
#                     current = current.parent
#                 return path[::-1]

#             children = []
#             for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
#                 nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
#                 if (0 <= nodePosition[0] < len(maze)) and (0 <= nodePosition[1] < len(maze[0])) and maze[nodePosition[0]][nodePosition[1]] == 0:
#                     new_node = Astar(currentNode, nodePosition)
#                     children.append(new_node)

#             for child in children:
#                 if child in closedList:
#                     continue
#                 child.g = currentNode.g + 1
#                 child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
#                 child.f = child.g + child.h
#                 if len([openNode for openNode in openList if child == openNode and child.g > openNode.g]) > 0:
#                     continue
#                 openList.append(child)

#     def run(self, maze, start, end):
#         path = self.aStar(maze, start, end)
#         return maze, path

# class Botplanner(Node):
#     def __init__(self, domain_id):
#         super().__init__('Bot_planner_' + str(domain_id))
#         os.environ['ROS_DOMAIN_ID'] = str(domain_id)  # Set the ROS domain ID
#         self._action_server = ActionServer(self, PathPlanner, 'pathplanner', self.execute_callback)
#         self.current_pos_x = None
#         self.current_pos_y = None
#         self.current_pos_orientation_z = None
#         self.subscription = None

#     def execute_callback(self, goal_handle):
#         goal_pos_x = goal_handle.request.pos_x
#         goal_pos_y = goal_handle.request.pos_y
#         goal_pos_orientation_z = goal_handle.request.orientation_z
#         self.get_logger().info(f"Received Goal: pos_x={goal_pos_x}, pos_y={goal_pos_y}, orientation_z={goal_pos_orientation_z}")

#         make_route = Astar()
#         bringup_dir = get_package_share_directory('grid_map_operator')
#         png_img = os.path.join(bringup_dir, 'map', 'dogniel_map.png')
#         transmap = map_change(png_img)

#         start = (int(self.current_pos_x), int(self.current_pos_y))
#         end = (int(goal_pos_x), int(goal_pos_y))

#         result_map, path = make_route.run(transmap, start, end)

#         feedback = PathPlanner.Feedback()
#         feedback.pos_x = self.current_pos_x
#         feedback.pos_y = self.current_pos_y
#         feedback.pos_orientation_z = self.current_pos_orientation_z

#         goal_handle.publish_feedback(feedback)

#         result_msg = PathPlanner.Result()
#         result_msg.success = True
#         result_msg.pos_x = self.current_pos_x
#         result_msg.pos_y = self.current_pos_y
#         result_msg.pos_orientation_z = self.current_pos_orientation_z

#         return result_msg
    
# class amcl_listener(Node):
#     def __init__(self, bot_planner_node, domain_id):
#         super().__init__('amcl_listener_' + str(domain_id))
#         self.bot_planner_node = bot_planner_node
#         self.domain_id = domain_id
        
#         # ROS_DOMAIN_ID 설정 확인 로그
#         self.get_logger().info(f"AMCL Listener Node (Domain {self.domain_id}) started, subscribing to 'amcl_pose' topic.")
        
#         # 구독 설정
#         self.subscription = self.create_subscription(
#             PoseWithCovarianceStamped,
#             'amcl_pose',  # 동일한 주제 이름
#             self.listener_callback,
#             10
#         )

#     def listener_callback(self, msg):
#         self.current_pos_x = msg.pose.pose.position.x
#         self.current_pos_y = msg.pose.pose.position.y
#         self.current_pos_orientation_z = msg.pose.pose.orientation.z
#         # AMCL 포즈 출력
#         self.get_logger().info(f"Received AMCL Pose (Domain {self.domain_id}): x={self.current_pos_x}, y={self.current_pos_y}, z={self.current_pos_orientation_z}")





# def main():
#     rp.init()

#     # 두 개의 도메인 ID를 각각 설정하여 인스턴스 생성
#     bot_planner_92 = Botplanner(92)
#     amcl_listener_92 = amcl_listener(bot_planner_92, 92)

#     bot_planner_82 = Botplanner(82)
#     amcl_listener_82 = amcl_listener(bot_planner_82, 82)

#     executor = MultiThreadedExecutor()

#     # 두 개의 노드를 executor에 추가
#     executor.add_node(amcl_listener_92)
#     executor.add_node(bot_planner_92)
    
#     executor.add_node(amcl_listener_82)
#     executor.add_node(bot_planner_82)
    
#     try:
#         executor.spin()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         rp.shutdown()
#         bot_planner_92.destroy_node()
#         amcl_listener_92.destroy_node()
#         bot_planner_82.destroy_node()
#         amcl_listener_82.destroy_node()

# if __name__ == '__main__':
#     main()


# import cv2
# import numpy as np
# import os
# import rclpy as rp
# from rclpy.action import ActionServer
# from rclpy.node import Node
# from geometry_msgs.msg import PoseWithCovarianceStamped
# from nav_msg.action import PathPlanner
# from rclpy.executors import MultiThreadedExecutor
# from ament_index_python.packages import get_package_share_directory

# # 맵을 inflation 처리하는 함수
# def inflation_generator(x, y, map):
#     rows = x
#     cols = y
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#     changed = True
#     while changed:
#         changed = False
#         new_matrix = map.copy()
#         for i in range(rows):
#             for j in range(cols):
#                 if map[i][j] == 1:
#                     for di, dj in directions:
#                         ni, nj = i + di, j + dj
#                         if 0 <= ni < rows and 0 <= nj < cols and map[ni][nj] == 0:
#                             if new_matrix[ni][nj] == 0:
#                                 new_matrix[ni][nj] = 3
#                                 changed = True
#         map = new_matrix.copy()
#     return map

# def map_change(map):
#     origin_map = np.array(map)
#     height = origin_map.shape[0]
#     width = origin_map.shape[1]
#     for i in range(height):
#         for j in range(width):
#             point = origin_map[i][j]
#             if point == 0:
#                 origin_map[i][j] = 1
#             elif point == 205:
#                 origin_map[i][j] = 0
#     inflation_map = inflation_generator(height, width, origin_map)
#     return inflation_map

# # A* 알고리즘을 위한 클래스
# class Astar:
#     def __init__(self, parent=None, position=None):
#         self.parent = parent
#         self.position = position
#         self.g = 0
#         self.h = 0
#         self.f = 0

#     def __eq__(self, other):
#         return self.position == other.position

#     def heuristic(self, node, goal, D=1):
#         dx = abs(node.position[0] - goal.position[0])
#         dy = abs(node.position[1] - goal.position[1])
#         return D * (dx + dy)

#     def aStar(self, maze, start, end):
#         startNode = Astar(None, start)
#         endNode = Astar(None, end)
#         openList = [startNode]
#         closedList = []
#         while openList:
#             currentNode = openList[0]
#             currentIdx = 0
#             for index, item in enumerate(openList):
#                 if item.f < currentNode.f:
#                     currentNode = item
#                     currentIdx = index
#             openList.pop(currentIdx)
#             closedList.append(currentNode)
#             if currentNode == endNode:
#                 path = []
#                 current = currentNode
#                 while current is not None:
#                     x, y = current.position
#                     maze[x][y] = 2
#                     path.append(current.position)
#                     current = current.parent
#                 return path[::-1]

#             children = []
#             for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
#                 nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
#                 if (0 <= nodePosition[0] < len(maze)) and (0 <= nodePosition[1] < len(maze[0])) and maze[nodePosition[0]][nodePosition[1]] == 0:
#                     new_node = Astar(currentNode, nodePosition)
#                     children.append(new_node)

#             for child in children:
#                 if child in closedList:
#                     continue
#                 child.g = currentNode.g + 1
#                 child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
#                 child.f = child.g + child.h
#                 if len([openNode for openNode in openList if child == openNode and child.g > openNode.g]) > 0:
#                     continue
#                 openList.append(child)

#     def run(self, maze, start, end):
#         path = self.aStar(maze, start, end)
#         return maze, path

# class Botplanner(Node):
#     def __init__(self, domain_id):
#         super().__init__('Bot_planner_' + str(domain_id))
#         os.environ['ROS_DOMAIN_ID'] = str(domain_id)  # Set the ROS domain ID
#         self._action_server = ActionServer(self, PathPlanner, 'pathplanner', self.execute_callback)
#         self.current_pos_x = None
#         self.current_pos_y = None
#         self.current_pos_orientation_z = None
#         self.subscription = None

#     def execute_callback(self, goal_handle):
#         goal_pos_x = goal_handle.request.pos_x
#         goal_pos_y = goal_handle.request.pos_y
#         goal_pos_orientation_z = goal_handle.request.orientation_z
#         self.get_logger().info(f"Received Goal: pos_x={goal_pos_x}, pos_y={goal_pos_y}, orientation_z={goal_pos_orientation_z}")

#         make_route = Astar()
#         bringup_dir = get_package_share_directory('grid_map_operator')
#         png_img = os.path.join(bringup_dir, 'map', 'dogniel_map.png')
#         transmap = map_change(png_img)

#         start = (int(self.current_pos_x), int(self.current_pos_y))
#         end = (int(goal_pos_x), int(goal_pos_y))

#         result_map, path = make_route.run(transmap, start, end)

#         feedback = PathPlanner.Feedback()
#         feedback.pos_x = self.current_pos_x
#         feedback.pos_y = self.current_pos_y
#         feedback.pos_orientation_z = self.current_pos_orientation_z

#         goal_handle.publish_feedback(feedback)

#         result_msg = PathPlanner.Result()
#         result_msg.success = True
#         result_msg.pos_x = self.current_pos_x
#         result_msg.pos_y = self.current_pos_y
#         result_msg.pos_orientation_z = self.current_pos_orientation_z

#         return result_msg

# class amcl_listener(Node):
#     def __init__(self, bot_planner_node):
#         super().__init__('amcl_listener')
#         self.bot_planner_node = bot_planner_node
#         self.subscription = self.create_subscription(PoseWithCovarianceStamped, 'amcl_pose', self.listener_callback, 10)

#     def listener_callback(self, msg):
#         self.current_pos_x = msg.pose.pose.position.x
#         self.current_pos_y = msg.pose.pose.position.y
#         self.current_pos_orientation_z = msg.pose.pose.orientation.z
#         self.get_logger().info(f"Received AMCL Pose: x={self.current_pos_x}, y={self.current_pos_y}, z={self.current_pos_orientation_z}")
#         print(f" Received AMCL Pose: x={self.current_pos_x}, y={self.current_pos_y}, z={self.current_pos_orientation_z}" )

# def main():
#     rp.init()

#     # 두 개의 도메인 ID를 각각 설정하여 인스턴스 생성
#     bot_planner_92 = Botplanner(92)
#     amcl_listener_92 = amcl_listener(bot_planner_92)

#     bot_planner_82 = Botplanner(82)
#     amcl_listener_82 = amcl_listener(bot_planner_82)

#     executor = MultiThreadedExecutor()

#     # 두 개의 노드를 executor에 추가
#     executor.add_node(amcl_listener_92)
#     executor.add_node(bot_planner_92)
    
#     executor.add_node(amcl_listener_82)
#     executor.add_node(bot_planner_82)
    

#     try:
#         executor.spin()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         rp.shutdown()
#         bot_planner_92.destroy_node()
#         amcl_listener_92.destroy_node()
#         bot_planner_82.destroy_node()
#         amcl_listener_82.destroy_node()

# if __name__ == '__main__':
#     main()

