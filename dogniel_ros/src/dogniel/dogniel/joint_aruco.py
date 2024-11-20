import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from dogniel_msgs.msg import ArucoData, DataMerge
from rclpy.executors import MultiThreadedExecutor

class JointStateSub(Node):
    def __init__(self, data_merge_pub):
        super().__init__('joint_states_sub')
        self.data_merge_pub = data_merge_pub
        
        # JointState 토픽 구독
        self.motor_subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.motor_callback,
            10
        )

    def motor_callback(self, msg):
        # 모터 엔코더 값 처리
        self.right_motor = round(msg.position[0], 4)  # 오른쪽 모터
        self.left_motor = round(msg.position[1], 4)   # 왼쪽 모터
        self.get_logger().info(f'Received motor data: Right={self.right_motor}, Left={self.left_motor}')
        
        # 두 데이터가 모두 준비되면 병합 데이터를 퍼블리시
        self.data_merge_pub.merge_motor_data(self.right_motor, self.left_motor)


class ArucoDataSub(Node):
    def __init__(self, data_merge_pub):
        super().__init__('aruco_data_sub')
        self.data_merge_pub = data_merge_pub
        
        # ArucoData 토픽 구독
        self.marker_subscription = self.create_subscription(
            ArucoData,
            '/aruco_data',
            self.marker_callback,
            10
        )

    def marker_callback(self, msg):
        # 아르코 마커 데이터 처리
        self.id = msg.id
        self.theta = msg.theta
        self.z = msg.z
        self.get_logger().info(f'Received aruco data: id={self.id}, theta={self.theta}, z={self.z}')
        
        # 두 데이터가 모두 준비되면 병합 데이터를 퍼블리시
        self.data_merge_pub.merge_marker_data(self.id, self.theta, self.z)


class DataMergePub(Node):
    def __init__(self):
        super().__init__('data_merge_pub')
        self.publisher = self.create_publisher(DataMerge, "data_merge", 10)
        
        # 초기값 설정
        self.right_motor = None
        self.left_motor = None
        self.id = None
        self.theta = None
        self.z = None

        # 1초마다 퍼블리시 메서드 실행
        self.timer = self.create_timer(.2, self.publish_message)

    def merge_motor_data(self, right_motor, left_motor):
        # 모터 데이터 수신
        self.right_motor = right_motor
        self.left_motor = left_motor
        self.get_logger().info(f'Merged motor data: Right={self.right_motor}, Left={self.left_motor}')
    
    def merge_marker_data(self, id, theta, z):
        # 아르코 마커 데이터 수신
        self.id = id
        self.theta = theta
        self.z = z
        self.get_logger().info(f'Merged aruco data: id={self.id}, theta={self.theta}, z={self.z}')

    def publish_message(self):
        # 데이터가 모두 준비되었으면 메시지 생성
        if self.right_motor is not None and self.left_motor is not None and self.id is not None:
            msg = DataMerge()
            msg.right = self.right_motor
            msg.left = self.left_motor
            msg.id = self.id
            msg.theta = self.theta
            msg.z = self.z
            
            # 메시지 발행
            self.publisher.publish(msg)
            self.get_logger().info(f'Publishing merged data: Right={msg.right}, Left={msg.left}, id={msg.id}, theta={msg.theta}, z={msg.z}')

    def reset_data(self):
        # 데이터를 초기화하여 다음 데이터를 받을 준비
        self.right_motor = None
        self.left_motor = None
        self.id = None
        self.theta = None
        self.z = None


def main(args=None):
    rclpy.init(args=args)
    
    # 퍼블리셔와 서브스크라이버를 연결
    data_merge_pub = DataMergePub()
    joint_state_sub = JointStateSub(data_merge_pub)
    aruco_data_sub = ArucoDataSub(data_merge_pub)

    # 멀티 스레드로 노드 실행
    executor = MultiThreadedExecutor()
    executor.add_node(data_merge_pub)
    executor.add_node(joint_state_sub)
    executor.add_node(aruco_data_sub)
    
    # 노드 실행
    executor.spin()
    
    # 종료 시 정리
    executor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
