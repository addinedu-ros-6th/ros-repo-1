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
        #self.get_logger().info(f'x={y}, y={x},z={z}w={w}')
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
        self.direction_value = {'N': self.north_value, 'E': self.east_value,'S': self.south_value,'W': self.west_value}
        
        self.path = ['S', 3, 'W', 5, 'S', 4, "E", 3] #40, 12, 12
        self.next_command = None

        # 0.5초마다 퍼블리시 메서드 실행
        self.timer = self.create_timer(0.5, self.publish_message)

    def merge_motor_data(self, right_motor, left_motor):
        # 모터 데이터 수신
        self.right_motor = right_motor
        self.left_motor = left_motor
        #self.get_logger().info(f'Received motor data: Right={self.right_motor}, Left={self.left_motor}')
        
    def merge_amcl_data(self, x, y, z):
        print(1818181818)
        print(z)
        self.amcl_x = x
        self.amcl_y = y
        self.amcl_z = z
        if self.amcl_z < 0.:
            self.south_value = -1.
            if  self.south_value + 0.02 <= self.amcl_z <= -1:
                self.present_direction = 'S'
                print("현재 방향", self.present_direction)
        elif self.amcl_z > 0:
            self.south_value = 1.
            if  self.south_value - 0.02 <= self.amcl_z <= 1:
                self.present_direction = 'S'
                print("현재 방향", self.present_direction)
                
        if self.north_value - 0.02 <= self.amcl_z <= self.north_value + 0.02:
            self.present_direction = 'N'
            print("현재 방향", self.present_direction)
        elif self.east_value - 0.02 <= self.amcl_z <= self.east_value + 0.02:
            self.present_direction = 'E'
            print("현재 방향", self.present_direction)
        elif self.west_value - 0.02 <= self.amcl_z <= self.west_value + 0.02:
            self.present_direction = 'W'
            print("현재 방향", self.present_direction)
        else:
            self.present_direction = None
            print("현재 방향", self.present_direction)
        #if self.present_direction == None:
        #    print("calib")
        #    self.calibration_turn()
            
        #self.get_logger().info(f'Received motor data: x={self.amcl_x}, y={self.amcl_y}, z={self.amcl_z}')

    def publish_message(self):
        print("다음 명령",self.path[0])
        if self.amcl_z < 0:
            self.south_value = -1
        print(self.present_direction)
        if self.path is not None:    
            self.next_command = self.path[0]
            if isinstance(self.next_command, str) and self.running == False and self.right_motor is not None:
                #if self.path[0] == 'N':
                #    if self.direction_lock == False:
                #        if self.present_direction == 'E':
                #            self.ccw_90()
#
                #        elif self.present_direction == 'S':
                #            self.ccw_90()
#
                #        elif self.present_direction == 'W':
                #            self.cw_90()
#
#
                #elif self.path[0] == 'E':
                #    if self.direction_lock == False:
                #        if self.present_direction == 'S':
                #            self.ccw_90()
                #        elif self.present_direction == 'W':
                #            self.ccw_90()
                #        elif self.present_direction == 'N':
                #            self.cw_90()
                #    #self.east_turn()
                #elif self.path[0] == 'S':
                #    if self.direction_lock == False:
                #        if self.present_direction == 'W':
                #            self.ccw_90()
                #        elif self.present_direction == 'N':
                #            self.ccw_90()
                #        elif self.present_direction == 'E':
                #            self.cw_90()
                #elif self.path[0] =='W':
                #    if self.direction_lock == False:
                #        if self.present_direction == 'N':
                #            self.ccw_90()
                #        elif self.present_direction == 'E':
                #            self.ccw_90()
                #        elif self.present_direction == 'S':
                #            self.cw_90()
                if self.next_command == 'N':
                    self.north_turn()
                elif self.next_command == 'E':
                    self.east_turn()
                elif self.next_command == 'S':
                    self.south_turn()
                elif self.next_command == 'W':
                    self.west_turn()

                if self.next_command == self.present_direction:
                    self.path.pop(0)
                    print("방향일치")
                    self.direction_lock = False

            elif isinstance(self.next_command, int) and self.running == False and self.right_motor is not None:
                self.straigt(self.next_command)

    #def ccw_90(self):
    #    if self.step_turn == False:
    #        self.error_init = 2.55 * (np.pi / 2)
    #        self.g = self.right_motor + self.error_init
    #        self.step_turn = True
#
    #    self.error = round(self.g - self.right_motor, 4)
    #    self.msg.linear.x = 0.0
    #    self.msg.angular.z = 0.35
    #    self.publisher.publish(self.msg)
    #    print(self.g)
    #    if self.g <= self.right_motor:
    #        self.direction_lock = False
    #        self.msg.linear.x = 0.0
    #        self.msg.angular.z = 0.0
    #        self.publisher.publish(self.msg)
    #        print("회전 완료")
    #        print("last_error",self.error)
    #        self.angular_z = 0
    #        self.path.pop(0)
    #        self.step_turn = False
    #        
    #def cw_90(self):
    #    if self.step_turn == False:
    #        self.error_init = 2.55 * (np.pi / 2)
    #        self.g = self.left_motor + self.error_init
    #        self.step_turn = True
#
    #    self.error = round(self.g - self.left_motor, 4)
    #    self.msg.linear.x = 0.0
    #    self.msg.angular.z = -0.35
    #    self.publisher.publish(self.msg)
    #    print(self.g)
    #    print(self.left_motor)
    #    if self.g <= self.left_motor:
    #        self.direction_lock = False
    #        self.msg.linear.x = 0.0
    #        self.msg.angular.z = 0.0
    #        self.publisher.publish(self.msg)
    #        print("회전 완료")
    #        print("last_error",self.error)
    #        self.angular_z = 0
    #        self.path.pop(0)
    #        self.step_turn = False
            
    def north_turn(self):
        print("turn to north")
        if self.north_value - self.amcl_z > 0:
            self.pm = self.north_value - self.amcl_z 
            w = self.pm / abs(self.pm) * 0.4
            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
        elif self.north_value - self.amcl_z < 0:
            self.pm = self.north_value - self.amcl_z 
            w = self.pm / abs(self.pm) * 0.4
            self.msg.linear.x = 0.0
            self.msg.angular.z = w

            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
            
        if self.north_value - 0.03 <= self.amcl_z <= self.north_value + 0.35:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.15
            self.publisher.publish(self.msg)
            
        elif self.north_value - 0.01 <= self.amcl_z <= self.north_value + 0.12:
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
        print("turn to east")
        if self.east_value - self.amcl_z > 0:
            self.pm = self.east_value - self.amcl_z
 
            if abs(self.pm) > 1 and self.step_turn == False:
                self.alpha = self.pm * -1
                self.step_turn = True
            elif abs(self.pm) < 1 and self.step_turn == False:
                self.alpa = self.pm
                self.step_turn = True
            
            w = self.alpha / abs(self.alpha) * 0.4
            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
        elif self.east_value - self.amcl_z < 0:
            self.pm = self.east_value - self.amcl_z
 
            if abs(self.pm) > 1 and self.step_turn == False:
                self.alpha = self.pm * -1
                self.step_turn = True
            elif abs(self.pm) < 1 and self.step_turn == False:
                self.alpa = self.pm
                self.step_turn = True
            
            w = self.alpha / abs(self.alpha) * 0.4
            self.msg.linear.x = 0.0
            self.msg.angular.z = w

            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
            
        if self.east_value - 0.03 <= self.amcl_z <= self.east_value + 0.03:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.15
            self.publisher.publish(self.msg)
            
        elif self.east_value - 0.01 <= self.amcl_z <= self.east_value + 0.01:
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
            
    def south_turn(self):
        print("turn to south")
        print("asd",self.south_value)
        if self.south_value - self.amcl_z > 0:
            self.pm = self.south_value - self.amcl_z 
            w = self.pm / abs(self.pm) * 0.4
            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
        elif self.south_value - self.amcl_z < 0:
            self.pm = self.south_value - self.amcl_z 
            w = self.pm / abs(self.pm) * 0.4
            self.msg.linear.x = 0.0
            self.msg.angular.z = w

            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
        print("self.pm",abs(self.pm))
            
        if abs(self.pm) < 0.03:
            self.msg.linear.x = 0.0
            self.msg.angular.z = (self.pm / abs(self.pm)) * 0.15
            self.publisher.publish(self.msg)
            
        if abs(self.pm) < 0.01:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            self.angular_z = 0
            self.step_turn = False
            self.path.pop(0)
            self.south = True
            self.running = False
            
    def west_turn(self):
        print("turn to west")
        if self.west_value - self.amcl_z > 0:
            self.pm = self.west_value - self.amcl_z
 
            if abs(self.pm) > 1 and self.step_turn == False:
                self.alpha = self.pm * -1
                self.step_turn = True
            elif abs(self.pm) < 1 and self.step_turn == False:
                self.alpa = self.pm
                self.step_turn = True
            
            w = self.alpha / abs(self.alpha) * 0.4
            print(w)
            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
        elif self.west_value - self.amcl_z < 0:
            self.pm = self.west_value - self.amcl_z

            if abs(self.pm) > 1 and self.step_turn == False:
                self.alpha = self.pm * -1
                self.step_turn = True
            elif abs(self.pm) < 1 and self.step_turn == False:
                self.alpa = self.pm
                self.step_turn = True
            
            w = self.alpha / abs(self.alpha) * 0.4
            self.msg.linear.x = 0.0
            self.msg.angular.z = w

            self.msg.linear.x = 0.0
            self.msg.angular.z = w
            self.publisher.publish(self.msg)
            
        if self.west_value - 0.03 <= self.amcl_z <= self.west_value + 0.03:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.15
            self.publisher.publish(self.msg)
            
        elif self.west_value - 0.01 <= self.amcl_z <= self.west_value + 0.01:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher.publish(self.msg)
            print("회전 완료")
            print("last_error",self.error)
            self.angular_z = 0
            self.step_turn = False
            self.path.pop(0)
            self.south = True
            self.running = False
           
    def straigt(self, grid):
        if self.step_go == False:
            print(grid)
            self.error_init = round(3 * 0.288 * grid, 4)
            print(self.left_motor, self.error_init)
            self.g = self.left_motor + self.error_init
            self.step_go = True
        self.error = round(self.g - self.left_motor, 4)
        
        if self.error / self.error_init <= 0.2:
            self.msg.linear.x = 0.08
            self.msg.angular.z = 0.
            print("linear_x", self.msg.linear.x)
            self.publisher.publish(self.msg)
        else:
            self.msg.linear.x = 0.23
            print("linear_x", self.msg.linear.x)
            self.msg.angular.z = 0.
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
            
    def calibration_turn(self):
        print(self.direction_value)
        if self.present_direction == None:
            if isinstance(self.next_command, str):
                calib = self.direction_value.get(self.next_command[0]) - self.amcl_z
                print(self.direction_value.get(self.next_command[0]), self.amcl_z, self.direction_value.get(self.next_command[0]) - self.amcl_z)
                self.msg.angular.z = calib / abs(calib) * 0.4
                self.publisher.publish(self.msg)
                print(1)
                if abs(calib) <= 0.02:
                    self.msg.angular.z = calib / abs(calib) * 0.4
                    self.publisher.publish(self.msg)
                    self.path.pop(0)
                    print(self.path)
                    print("gjldas;hlkwe;")
            else:
                self.publisher.publish(self.msg)



            
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