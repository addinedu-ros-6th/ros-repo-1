import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import Twist
import numpy as np
import math

class JointStateSub(Node):
    def __init__(self, queen_move):
        super().__init__('queen_joint_states')
        self.queen_move = queen_move
        
        # JointState 토픽 구독
        self.motor_subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.motor_callback,
            10
        )

    def motor_callback(self, msg):
        # 모터 엔코더 값 처리
        self.right_motor = round(msg.position[0], 3)  # 오른쪽 모터
        self.left_motor = round(msg.position[1], 3)   # 왼쪽 모터
        #self.get_logger().info(f'Received motor data: Right={self.right_motor}, Left={self.left_motor}')
        self.queen_move.merge_motor_data(self.right_motor, self.left_motor)
        
class QueenVector(Node):
    def __init__(self, queen_move):
        super().__init__('queen_vector_sub')
        self.queen_move = queen_move
        
        self.motor_subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.queen_vector_callback,
            10
        )

    def queen_vector_callback(self, msg):
        self.linear_x = round(msg.linear.x, 4)  # 오른쪽 모터
        self.angular_z = round(msg.angular.z, 4)   # 왼쪽 모터
        
        self.get_logger().info(f'Received grid data: tvec={self.linear_x}, rvec={self.angular_z}')
        self.queen_move.merge_grid_data(self.linear_x, self.angular_z)
        
class QueenMove(Node):
    def __init__(self):
        super().__init__('queen_move')
        self.publisher = self.create_publisher(Twist, "/base_controller/cmd_vel_unstamped", 10)
        self.msg = Twist()
        self.step_turn = False
        self.step_go = False
        
        # 초기값 설정
        self.right_motor = None
        self.left_motor = None
        self.linear_x = 0.
        self.angular_z = 0.

        # 0.2초마다 퍼블리시 메서드 실행
        self.timer = self.create_timer(0.2, self.publish_message)

    def merge_motor_data(self, right_motor, left_motor):
        # 모터 데이터 수신
        self.right_motor = right_motor
        self.left_motor = left_motor
        #self.get_logger().info(f'Received motor data: Right={self.right_motor}, Left={self.left_motor}')
    
    def merge_grid_data(self, x, z):
        # 방향 데이터 수신
        self.linear_x = x
        self.angular_z = z
        self.get_logger().info(f'Merged aruco data: linear_x={self.linear_x}, angular_z={self.angular_z}')

    def publish_message(self):
        # 데이터가 모두 준비되었으면 메시지 생성
        if self.angular_z > 0:
            msg = Twist()
            msg.linear.x
            msg.angular.z
            
            # 메시지 발행
            self.ccw_45()
            self.get_logger().info(f'ccw activated{self.angular_z}')
        elif self.angular_z < 0:
                        # 메시지 발행
            self.cw_45()
            self.get_logger().info(f'cw activated{self.angular_z}')
        elif self.linear_x > 0 and self.right_motor is not None:
            self.straigt()
            
    def ccw_45(self):
        if self.step_turn == False:
            self.error_init = 2.7 * (np.pi / 4)
            self.g = self.right_motor + 2.7 * (np.pi / 4)
            self.step_turn = True

        self.error = round(self.g - self.right_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.4
        self.publisher.publish(self.msg)
        if self.g <= self.right_motor:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.step_turn = False
            
    def cw_45(self):
        if self.step_turn == False:
            self.error_init = 2.7 * (np.pi / 4)
            self.g = self.left_motor + 2.7 * (np.pi / 4)
            self.step_turn = True

        self.error = round(self.g - self.left_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = -0.4
        self.publisher.publish(self.msg)
        if self.g <= self.left_motor:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.step_turn = False
            
    def straigt(self):
        if self.step_go == False:
            self.error_init = round(3 * 0.288 * self.linear_x, 4)
            print(self.left_motor, self.error_init)
            self.g = self.left_motor + self.error_init
            self.step_go = True
        self.error = round(self.g - self.left_motor, 4)
        
        if self.error / self.error_init >= 0.8:
            self.msg.linear.x = (math.exp(0.5308 * (self.error_init - self.error) / self.error_init)) - 0.882
            self.maintain = (math.exp(0.5308 * (self.error_init - self.error) / self.error_init)) - 0.882
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
        elif 0.2 < self.error / self.error_init < 0.8:
            self.msg.linear.x = self.maintain
            self.publisher.publish(self.msg)
        elif self.error / self.error_init <= 0.2:
            self.msg.linear.x = (math.exp(-1.6729 * (self.error_init - self.error) / self.error_init)) - math.exp(-1.8365)
            print("linear_x", self.msg.linear.x)
            self.publisher.publish(self.msg)
            
        if self.g <= self.left_motor:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            self.linear_x = 0
            self.step_go = False
            print("last_error",self.error)
        
def main():
    rclpy.init()
    queen_move = QueenMove()
    queen_joint_states = JointStateSub(queen_move)
    queen_vector = QueenVector(queen_move)
    executor = MultiThreadedExecutor()
    executor.add_node(queen_joint_states)
    executor.add_node(queen_vector)
    executor.add_node(queen_move)
    executor.spin()
    executor.shutdown()
if __name__ == '__main__':
    main()