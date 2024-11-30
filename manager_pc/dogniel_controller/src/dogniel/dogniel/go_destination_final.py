import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.executors import MultiThreadedExecutor
from dogniel_msgs.msg import DognielAmcl
from geometry_msgs.msg import Twist
import numpy as np
import math

class JointStateSub(Node):
    def __init__(self, go_destination):
        super().__init__('queen_joint_states')
        self.go_destination = go_destination
        
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
        self.go_destination.merge_motor_data(self.right_motor, self.left_motor)

class DognielAmclPoseSub(Node):
    def __init__(self, go_destination):
        super().__init__('dogniel_amcl_pose_sub')
        self.go_destination = go_destination
        # PoseWithCovarianceStamped 토픽 구독
        self.amcl_subscription = self.create_subscription(
            DognielAmcl,
            '/dogniel_amcl',
            self.amcl_callback,
            10
        )
        
    def amcl_callback(self, data):
        x = round(data.x,4)
        y = round(data.y,4)
        z = round(data.z,4)
        w = round(data.w,4)
        self.get_logger().info(f'x={y}, y={x},z={z}w={w}')
        self.go_destination.merge_amcl_data(x, y, z)
        
class GoDestination(Node):
    def __init__(self):
        super().__init__('go_destination')
        self.publisher = self.create_publisher(Twist, "/base_controller/cmd_vel_unstamped", 10)
        self.msg = Twist()
        
        self.x = None
        self.y = None
        self.z = None
        self.w = None
        self.amcl_x = 54
        self.amcl_y = 17
        self.amcl_z = 0.0
        self.north = False
        self.east = False
        self.south = False
        self.west = False
        
        self.right_motor = None
        self.left_motor = None
        
        self.north_value = 0.
        self.east_value = -0.7068
        self.south_value =  1.
        self.west_value =  0.7068
        self.present_direction = None
        self.goal_directon = None
        self.direction_lock = False
        
        self.step_turn = False
        self.step_go = False
        
        self.running = False
        
        self.path = ['S', 20, 'W', 12, 'S',10]

        # 0.5초마다 퍼블리시 메서드 실행
        self.timer = self.create_timer(0.5, self.publish_message)

    def merge_motor_data(self, right_motor, left_motor):
        # 모터 데이터 수신
        self.right_motor = right_motor
        self.left_motor = left_motor
        #self.get_logger().info(f'Received motor data: Right={self.right_motor}, Left={self.left_motor}')
        
    def merge_amcl_data(self, x, y, z):
        # 모터 데이터 수신
        n = 0.
        e = -0.7068
        s = 1.
        w = 0.7068
        self.amcl_x = x
        self.amcl_y = y
        self.amcl_z = z
            
        self.get_logger().info(f'Received motor data: x={self.amcl_x}, y={self.amcl_y}, y={self.amcl_z}')

    def publish_message(self):
        print(self.path[0])
        print(self.amcl_z)
        if self.amcl_z < 0:
            self.south_value = -1
        if self.path is not None:    
            next_command = self.path[0]
            if isinstance(next_command, str) and self.running == False and self.right_motor is not None:
                if self.path[0] == 'N':
                    if self.direction_lock == False:
                        self.goal_directon = self.north_value
                    #self.north_turn()
                elif self.path[0] == 'E':
                    if self.direction_lock == False:
                        self.goal_directon = self.east_value
                    #self.east_turn()
                elif self.path[0] == 'S':
                    if self.direction_lock == False:
                        self.goal_directon = self.south_value
                    #self.south_turn()
                elif self.path[0] =='W':
                    if self.direction_lock == False:
                        self.goal_directon = self.west_value
                    #self.west_turn()
                print(self.direction_lock)
                if self.direction_lock == False:
                    self.diretion_error = self.goal_directon - self.amcl_z
                    self.direction_lock = True
                print(self.goal_directon)
                print(self.diretion_error)
                if abs(self.diretion_error) < 0.1:
                    self.path.pop(0)
                    print("방향일치")
                elif self.diretion_error > 0.1:
                    self.ccw_90()   
                elif self.diretion_error < -0.1:
                    self.cw_90()

            elif isinstance(next_command, int) and self.running == False and self.right_motor is not None:
                self.straigt(next_command)

    def ccw_90(self):
        if self.step_turn == False:
            self.error_init = 2.7 * (np.pi / 2)
            self.g = self.right_motor + 2.7 * (np.pi / 2)
            self.step_turn = True

        self.error = round(self.g - self.right_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.4
        self.publisher.publish(self.msg)
        print(self.g)
        if self.g <= self.right_motor:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.path.pop(0)
            self.step_turn = False
            self.direction_lock = False
            
    def cw_90(self):
        if self.step_turn == False:
            self.error_init = 2.7 * (np.pi / 2)
            self.g = self.left_motor + 2.7 * (np.pi / 2)
            self.step_turn = True
            print(123)

        self.error = round(self.g - self.left_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = -0.4
        self.publisher.publish(self.msg)
        print(self.g)
        print(self.left_motor)
        if self.g <= self.left_motor:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.path.pop(0)
            self.step_turn = False
            self.direction_lock = False
            
    def north_turn(self):
        if self.step_turn == False:
            if self.south_value < self.amcl_z < self.north_value:
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = -1
                self.step_turn = True
            elif -0.9999 <= self.amcl_z <= self.south_value: 
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = +1
                self.step_turn = True

        self.error = round(self.g - self.right_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.4
        self.publisher.publish(self.msg)
        if self.north_value - 0.05 <= self.amcl_z <= self.north_value + 0.05:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.step_turn = False
            self.path.pop(0)
            self.north = True
            self.running = False
            
    def east_turn(self):
        if self.step_turn == False:
            if self.east_value < self.amcl_z < self.west_value:
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = -1
                self.step_turn = True
            elif self.west_value <= self.amcl_z <= 1. or -0.9999 < self.amcl_z <= self.east_value: 
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = +1
                self.step_turn = True
            
            self.error_init = 2.7 * (-0.7068 - self.amcl_z)
            self.g = self.right_motor + self.error_init
            self.step_turn = True

        self.error = round(self.g - self.right_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.4
        self.publisher.publish(self.msg)
        if self.east_value - 0.05 <= self.amcl_z <= self.east_value + 0.05:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.step_turn = False
            self.path.pop(0)
            self.running = False
            
    def south_turn(self): 
        if self.step_turn == False:
            if -0.9999 <= self.amcl_z < self.north_value:
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = -1
                self.step_turn = True
            elif self.north_value <= self.amcl_z <= 1.:
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = +1
                self.step_turn = True

        self.error = round(self.g - self.right_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.4 * self.pm
        self.publisher.publish(self.msg)
        if self.amcl_z > 0:
            if 1 - 0.05 <=self.amcl_z <=1 or -0.9999 + 0.05 <= self.amcl_z <= -0.9999:
                self.msg.linear.x = 0.0
                self.msg.angular.z = 0.0
                self.publisher.publish(self.msg)
                print("회전 완료")
                print("last_error",self.error)
                self.angular_z = 0
                self.step_turn = False
                self.path.pop(0)
                self.running = False
            
    def west_turn(self):
        if self.step_turn == False:
            if -0.9999 <= self.amcl_z < self.east_value or 1 <= self.amcl_z < self.west_value:
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = -1
                self.step_turn = True
            elif self.east_value <= self.amcl_z < self.west_value: 
                self.error_init = 2.7 * (self.west_value - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.pm = +1
                self.step_turn = True
                
        self.error = round(self.g - self.right_motor, 4)
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.4 * self.pm
        self.publisher.publish(self.msg)
        if self.west_value - 0.05 <= self.amcl_z <= self.west_value + 0.05:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.step_turn = False
            self.path.pop(0)
            self.running = False
            
    def straigt(self, grid):
        if self.step_go == False:
            print(grid)
            self.error_init = round(3 * 0.288 * grid, 4)
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
            self.path.pop(0)
            self.running = False
            
    def calibration_turn(self, calib):
        print(calib)
        if calib > 0.:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.2
            self.publisher.publish(self.msg)
            if self.north == True or self.east == True or self.south == True or self.west == True:
                self.msg.linear.x = 0.0
                self.msg.angular.z = 0.0
                self.publisher.publish(self.msg)
                self.calib =True
        elif calib < 0.:
            self.msg.linear.x = 0.0
            self.msg.angular.z = -0.2
            self.publisher.publish(self.msg)
            if self.north == True or self.east == True or self.south == True or self.west == True:
                self.msg.linear.x = 0.0
                self.msg.angular.z = 0.0
                self.publisher.publish(self.msg)
                self.calib =True
            
def main():
    rclpy.init()
    go_destination = GoDestination()
    queen_joint_states = JointStateSub(go_destination)
    dogniel_pose_sub = DognielAmclPoseSub(go_destination)
    executor = MultiThreadedExecutor()
    executor.add_node(go_destination)
    executor.add_node(queen_joint_states)
    executor.add_node(dogniel_pose_sub)
    executor.spin()
    executor.shutdown()
if __name__ == '__main__':
    main()