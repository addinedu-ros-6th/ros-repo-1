import cv2
import sys
import numpy as np


#import matplotlib.pyplot as plt
png_img = cv2.imread('/home/jun/ros-repo-1/image_source/dogniel_map_grid.png',cv2.COLOR_BGR2GRAY)
#plt.imshow(png_img)
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
transmap = map_change(png_img)
class Astar:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position
    def heuristic(self, node, goal, D=1, D2=2 ** 0.5):  # Diagonal Distance
        dx = abs(node.position[0] - goal.position[0])
        dy = abs(node.position[1] - goal.position[1])
        return D * (dx + dy)
    def is_safe_from_obstacles(self, maze, position):
        x, y = position  # x는 세로(행), y는 가로(열)
        # 주변 7칸 범위 확인 (상하좌우 3칸, 대각선 포함)
        # x - 3부터 x + 3 (세로 방향), y - 3부터 y + 3 (가로 방향)
        for i in range(max(0, x - 3), min(len(maze), x + 3)):  # 세로 방향: x - 3부터 x + 3까지 범위
            for j in range(max(0, y - 3), min(len(maze[0]), y + 3)):  # 가로 방향: y - 3부터 y + 3까지 범위
                # 장애물인 경우 (1 또는 3)
                if maze[i][j] == 1 or maze[i][j] == 3:
                    return False  # 장애물이 있는 위치는 안전하지 않음
        return True  # 장애물이 없다면 안전한 위치
    def aStar(self, maze, start, end):
        startNode = Astar(None, start)
        endNode = Astar(None, end)
        openList = []
        closedList = []
        openList.append(startNode)
        while openList:
            currentNode = openList[0]
            currentIdx = 0
            # 가장 적은 f 값을 가진 노드를 선택
            for index, item in enumerate(openList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIdx = index
            openList.pop(currentIdx)
            closedList.append(currentNode)
            # 목표 지점에 도달하면 경로 반환
            if currentNode == endNode:
                path = []
                current = currentNode
                while current is not None:
                    x, y = current.position
                    maze[x][y] = 2  # 경로 표시
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # reverse path to get correct order
            children = []
            # 4방향으로 이동 (상, 하, 좌, 우)
            for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nodePosition = (
                    currentNode.position[0] + newPosition[0],  # X
                    currentNode.position[1] + newPosition[1])  # Y
                # 미로 maze index 범위 안에 있어야함
                within_range_criteria = [
                    nodePosition[0] > (len(maze) - 1),
                    nodePosition[0] < 0,
                    nodePosition[1] > (len(maze[len(maze) - 1]) - 1),
                    nodePosition[1] < 0,
                ]
                if any(within_range_criteria):  # 하나라도 true면 범위 밖임
                    continue
                # 장애물이 있으면 다른 위치 불러오기
                if maze[nodePosition[0]][nodePosition[1]] != 0:
                    continue
                # 2칸 이내에 1이나 3이 없으면 자식으로 추가
                if not self.is_safe_from_obstacles(maze, nodePosition):
                    continue
                new_node = Astar(currentNode, nodePosition)
                children.append(new_node)
            # 자식들 모두 loop
            for child in children:
                # 자식이 closedList에 있으면 continue
                if child in closedList:
                    continue
                # f, g, h값 업데이트
                child.g = currentNode.g + 1
                child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
                child.f = child.g + child.h
                # 자식이 openList에 있으고, g값이 더 크면 continue
                if len([openNode for openNode in openList if child == openNode and child.g > openNode.g]) > 0:
                    continue
                openList.append(child)
    def run(self, maze, start, end):
        path = self.aStar(maze, start, end)
        return maze, path
def main():
    path_list = []
    transmap = map_change(png_img)
    temp_map = transmap
    make_route = Astar()
    start = (24,69) #시작 위치
    end = (6, 15) # 도착 위치
    result, path = make_route.run(temp_map , start, end)
    for index, item in enumerate(path):
        #print("좌표 : ", item)
        path_list.append(item)
    print(path_list)
    np.savetxt('plan_map_6.txt',result.astype(int),fmt="%.0f")
    
if __name__ == '__main__':
    main()