import cv2
import numpy as np

# 맵을 변화시키는 함수
def map_change(png_img):
    def inflation_generator(x, y, map):
        rows = x
        cols = y
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우
        changed = True
        while changed:
            changed = False
            new_matrix = map.copy()
            for i in range(rows):
                for j in range(cols):
                    if map[i][j] == 1:
                        for di, dj in directions:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < rows and 0 <= nj < cols and map[ni][nj] == 0:
                                if new_matrix[ni][nj] == 0:
                                    new_matrix[ni][nj] = 3
                                    changed = True
            map = new_matrix.copy()
        return map
    
    origin_map = np.array(png_img)
    height = origin_map.shape[0]
    width = origin_map.shape[1]
    for i in range(height):
        for j in range(width):
            point = origin_map[i][j]
            if point == 0:
                origin_map[i][j] = 1  # 벽은 1
            elif point == 205:
                origin_map[i][j] = 0  # 길은 0
    return inflation_generator(height, width, origin_map)


# A* 알고리즘 클래스
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
        x, y = position
        for i in range(max(0, x - 3), min(len(maze), x + 3)):
            for j in range(max(0, y - 3), min(len(maze[0]), y + 3)):
                if maze[i][j] == 1 or maze[i][j] == 3:
                    return False
        return True

    def aStar(self, maze, start, end):
        startNode = Astar(None, start)
        endNode = Astar(None, end)
        openList = []
        closedList = []
        openList.append(startNode)
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
                    maze[x][y] = 2  # 경로 표시
                    path.append(current.position)
                    current = current.parent
                return path[::-1]
            children = []
            for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nodePosition = (
                    currentNode.position[0] + newPosition[0], 
                    currentNode.position[1] + newPosition[1])
                if not (0 <= nodePosition[0] < len(maze) and 0 <= nodePosition[1] < len(maze[0])):
                    continue
                if maze[nodePosition[0]][nodePosition[1]] != 0:
                    continue
                if not self.is_safe_from_obstacles(maze, nodePosition):
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


# 경로 계산 함수
def find_path(start, end, png_img):
    transmap = map_change(png_img)  # 이미지에서 맵을 처리한 후
    make_route = Astar()
    result, path = make_route.run(transmap, start, end)

    path_list = []
    for index, item in enumerate(path):
        path_list.append(item)
    command_list = []

    # 방향을 저장할 리스트
    directions = []

    # 처음 시작 위치
    current_position = path_list[0]
    current_direction = None

    # 좌표들을 돌면서 방향을 결정
    for i in range(1, len(path_list)):
        next_position = path_list[i]

        # 방향 계산
        if next_position[0] == current_position[0]:  # x 값이 변하지 않으면, y 값만 변한다
            if next_position[1] < current_position[1]:
                direction = 'S'
                distance = current_position[1] - next_position[1]
            else:
                direction = 'N'
                distance = next_position[1] - current_position[1]

        elif next_position[1] == current_position[1]:  # y 값이 변하지 않으면, x 값만 변한다
            if next_position[0] > current_position[0]:
                direction = 'E'
                distance = next_position[0] - current_position[0]
            else:
                direction = 'W'
                distance = current_position[0] - next_position[0]

        # 방향이 바뀔 때마다 출력
        if current_direction != direction:
            directions.append(direction)

        directions.append(distance)

        # 현재 위치와 방향 업데이트
        current_position = next_position
        current_direction = direction

    # 결과 출력
    for line in directions:
        #print(line)
        command_list.append(line)
    result = []
    current_char = None
    current_sum = 0

    for item in command_list:
        if isinstance(item, int):
            current_sum += item  # 숫자이면 계속 더함
        else:
            if current_char is not None:
                result.append(current_char)  # 이전 문자가 있으면 추가
                result.append(current_sum)  # 이전 숫자 합계 추가
            current_char = item  # 새로운 문자 설정
            current_sum = 0  # 숫자 합계를 초기화

    # 마지막 문자와 숫자 합계 추가
    if current_char is not None:
        result.append(current_char)
        result.append(current_sum + 1)  # 마지막 1을 더함 (마지막 문자는 1번만 등장)    

    return result
