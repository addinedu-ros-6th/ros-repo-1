import cv2
import socket
import struct
import pickle
import threading
# 전역 변수로 캡처 객체와 연결을 관리
cap = None
conn = None
# 비디오 캡처와 프레임 전송을 관리하는 함수
def capture_and_send_frame():
    global cap, conn
    ret, frame = cap.read()
    if not ret:
        print("프레임 캡처 실패")
        return
    # 프레임 크기 조정
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, dsize=(320, 240))
    try:
        # 이미지 직렬화
        data = pickle.dumps(frame)
        # 데이터 전송
        conn.sendall(struct.pack("L", len(data)) + data)
    except (BrokenPipeError, ConnectionResetError) as e:
        print(f"클라이언트와의 연결이 끊어졌습니다: {e}")
        stop_video_streaming()  # 연결 끊어지면 스트리밍 중지
        return
    except Exception as e:
        print(f"비디오 전송 중 오류 발생: {e}")
    # 0.1초 뒤에 다시 캡처 및 전송
    threading.Timer(0.1, capture_and_send_frame).start()
# 카메라 스트리밍 시작 함수
def start_video_streaming(new_conn):
    global cap, conn
    conn = new_conn
    cap = cv2.VideoCapture(0)  # 카메라 장치 열기
    if not cap.isOpened():
        print("카메라 열기 실패")
        return
    # 최초 실행 후 0.1초마다 프레임 캡처 및 전송 시작
    capture_and_send_frame()
# 서버 함수
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 4000))  # 포트 4000에서 수신
    server_socket.listen(1)
    print("클라이언트 연결 대기 중...")
    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"클라이언트 {addr} 연결됨.")
            # 비디오 스트리밍 쓰레드 시작
            video_thread = threading.Thread(target=start_video_streaming, args=(conn,))
            video_thread.start()
        except Exception as e:
            print(f"서버 오류 발생: {e}")
# 연결 끊어지면 스트리밍 중지
def stop_video_streaming():
    global cap, conn
    if cap:
        cap.release()
    if conn:
        conn.close()
    print("스트리밍 종료")
if __name__ == "__main__":
    start_server()
