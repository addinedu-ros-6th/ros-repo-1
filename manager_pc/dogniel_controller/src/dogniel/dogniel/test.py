# main_program.py

import cv2
from path_planner import find_path  # path_planner 모듈에서 find_path 함수 임포트

def main():
    # 경로 맵 이미지 불러오기 (여기서는 예시 이미지 경로를 사용합니다)
    map_image_path = '/home/addinedu/python_test/ros_path_planning_test/dogniel_map.png'
    png_img = cv2.imread(map_image_path, cv2.IMREAD_GRAYSCALE)

    if png_img is None:
        print(f"Error: 이미지 파일을 찾을 수 없습니다. 경로: {map_image_path}")
        return
    
    # 사용자로부터 시작점과 도착점 입력받기 (예시로 하드코딩된 값 사용)
    start_point = (23, 68)  # 시작점 (x, y)
    end_point = (6, 10)     # 도착점 (x, y)
    
    #print(f"Start point: {start_point}")
    #print(f"End point: {end_point}")
    
    # find_path 함수 호출하여 경로 찾기
    path = find_path(start_point, end_point, png_img)
    
    # 결과 출력 (경로)
    #print("Calculated Path (from start to end):")
    #for point in path:
    #    print(point)
    print(path)

if __name__ == "__main__":
    main()
