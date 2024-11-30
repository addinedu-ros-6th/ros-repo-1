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
        self.south_value =  1
        self.west_value =  0.7068
        
        self.step_turn = False
        self.step_go = False
        
        self.calib = False
        
        self.path = [(52, 25), (52, 26), (52, 27), (53.27), (54, 27)]

        # 0.2초마다 퍼블리시 메서드 실행
        self.timer = self.create_timer(0.2, self.publish_message)

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
        if z < 0:
            s = -1
            
        if n - 0.02 < z < n + 0.02:
            self.north = True
            self.calib =True
        elif e + 0.02 < z < e - 0.02:
            self.east = True
            self.calib =True
        elif s + 0.02 < z < s - 0.02:
            self.south = True
            self.calib =True
        elif w - 0.02 < z < w + 0.02:
            self.west = True
            self.calib =True
        else:
            self.north = False
            self.east = False
            self.south = False
            self.west = False
            self.calib =False
            
        #self.get_logger().info(f'Received motor data: Right={self.right_motor}, Left={self.left_motor}')

    def publish_message(self):
        # 데이터가 모두 준비되었으면 메시지 생성
        if self.north is True or self.east is True or self.south is True or self.west is True:
            self.calib = True
        else:
            self.calib = False
        print(self.north)
        print(self.east)
        print(self.south)
        print(self.west)
        if self.amcl_z < 0:
            self.south_value = -1
            
        next_row = self.path[1][0] - self.amcl_x #변화 없을시 0
        next_col = self.path[1][1] - self.amcl_y
        
        #if self.calib == False:
        #    print(self.amcl_z)
        #    n = self.amcl_z - self.north_value
        #    e = self.amcl_z - self.east_value
        #    w = self.amcl_z - self.west_value
        #    s = self.amcl_z - self.south_value
        #    #print(n)
        #    #print(s)
        #        
        #    print(n, e, s, w)
        #    calib = sorted([n, e, s, w])
        #    self.calibration_turn(calib[0])
        #else:
        print(next_row, next_row)
        if next_row == 1 and self.right_motor is not None:
            if self.east is True:
                self.straigt()
                self.get_logger().info(f'전진')
            else:
                self.east_turn()
        elif next_row == -1 and self.right_motor is not None:
            if self.west is True:
                self.straigt()
                self.get_logger().info(f'전진')
            else:
                self.west_turn()
            self.get_logger().info(f'cw_90 activated')
            self.straigt()
        elif next_col == 1 and self.right_motor is not None:
            if self.north is True:
                self.straigt()
                self.get_logger().info(f'전진')
            else:
                self.north_turn()
        elif next_col == -1 and self.right_motor is not None:
            if self.south is True:
                self.straigt()
                self.get_logger().info(f'전진')
            else:
                self.south_turn()
            self.get_logger().info(f'cw_90 activated')
            self.straigt()
            
    def north_turn(self):
        if self.step_turn == False:
            self.error_init = 2.7 * (0.0- self.amcl_z)
            self.g = self.right_motor + self.error_init
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
            self.path.pop(0)
            self.north = True
            
    def east_turn(self):
        if self.step_turn == False:
            self.error_init = 2.7 * (-0.7068 - self.amcl_z)
            self.g = self.right_motor + self.error_init
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
            self.path.pop(0)
            
    def south_turn(self):
        if self.step_turn == False:
            if self.amcl_z > 0:
                self.error_init = 2.7 * (1.0 - self.amcl_z)
                self.g = self.right_motor + self.error_init
                self.step_turn = True
            elif self.amcl_z < 0:
                self.error_init = 2.7 * (-1.0 - self.amcl_z)
                self.g = self.right_motor + self.error_init
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
            self.path.pop(0)
            
    def west_turn(self):
        if self.step_turn == False:
            self.error_init = 2.7 * (0.7068 - self.amcl_z)
            self.g = self.right_motor + self.error_init
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
            self.path.pop(0)
            
    def straigt(self):
        if self.step_go == False:
            self.error_init = round(3 * 0.288 * 1, 4)
            print(self.left_motor, self.error_init)
            self.g = self.left_motor + self.error_init
            self.step_go = True
        self.error = round(self.g - self.left_motor, 4)
        
        self.msg.linear.x = 0.02
        self.msg.angular.z = 0.0
        self.publisher.publish(self.msg)
        
        #if self.error / self.error_init >= 0.8:
        #    self.msg.linear.x = (math.exp(0.5308 * (self.error_init - self.error) / self.error_init)) - 0.882
        #    self.maintain = (math.exp(0.5308 * (self.error_init - self.error) / self.error_init)) - 0.882
        #    self.msg.angular.z = 0.0
        #    self.publisher.publish(self.msg)
        #elif 0.2 < self.error / self.error_init < 0.8:
        #    self.msg.linear.x = self.maintain
        #    self.publisher.publish(self.msg)
        #elif self.error / self.error_init <= 0.2:
        #    self.msg.linear.x = (math.exp(-1.6729 * (self.error_init - self.error) / self.error_init)) - math.exp(-1.8365)
        #    print("linear_x", self.msg.linear.x)
        #    self.publisher.publish(self.msg)
            
        if self.g <= self.left_motor:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            self.linear_x = 0
            self.step_go = False
            print("last_error",self.error)
        self.path.pop(0)
        self.amcl_x = self.path[0][0]
        self.amcl_y = self.path[0][1]
            
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