import rclpy
from rclpy.node import Node
from dogniel_msgs.msg import DataMerge
from geometry_msgs.msg import Twist
from rclpy.executors import MultiThreadedExecutor
import numpy as np
import time

class DataMergeSub(Node):
    def __init__(self, aruco_parking):
        super().__init__('data_merge_sub')
        self.aruco_parking = aruco_parking

        # JointState 토픽 구독
        self.motor_subscription = self.create_subscription(
            DataMerge,
            '/data_merge',
            self.data_merge_callback,
            10
        )
        
    def data_merge_callback(self, data):
        self.right_motor = round(data.right, 2)
        self.left_motor = round(data.left, 2)
        self.id = data.id
        self.theta = round(data.theta, 2)
        self.z = round(data.z, 2)
        x = self.z * abs(np.sin(self.theta/2))
        z = self.z * np.cos(self.theta/2)
        print(f"{self.id}번 아르코 마커와 {self.theta / 2}라디안 차이, x={x}m, z={z} 차이")
        self.aruco_parking.update(self.right_motor, self.left_motor, self.id, self.theta, self.z)
        
class ArUcoRobotController(Node):
    def __init__(self):
        super().__init__('aruco_parking')
        self.publisher_ = self.create_publisher(Twist, '/base_controller/cmd_vel_unstamped', 10)
        
        # Initialize Twist message
        self.msg = Twist()

        # Initialize internal states
        self.id_temp = 404
        #self.x = None
        self.id = None
        self.z = None
        self.theta = None
        self.pm = None
        
        self.right_motor = None
        self.left_motor = None

        self.g = None

        self.step_1 = False
        self.step_2 = False
        self.step_3 = False
        self.step_4 = False
        
        self.step_1_1 = False
        self.step_2_1 = False
        self.step_3_1 = False
        self.step_4_1 = False
        
        self.v = 0.2
        self.w = 0.8

    def update(self, right, left, id, theta, z):
        self.right_motor = right
        self.left_motor = left
        if  self.step_1_1 == False:
            self.id = id
            self.theta = theta / 2
            self.x = z * abs(np.sin(self.theta))
            self.z = z * np.cos(self.theta)
            self.pm = self.theta / abs(theta)
        self.turn_theta()

    def turn_theta(self):
        print("보정 시작")
        """Rotate the robot to align with ArUco marker orientation."""
        if self.step_1 == False:
            if self.theta == 0.:
                if self.x > 0:
                    self.theta = 0.01
                else:
                    self.theta = -0.01
            print(self.theta)
            print(self.right_motor)
            if self.theta > 0.:
                self.theta = abs(np.pi / 2 - abs(self.theta))
                alpha = self.theta
                if self.step_1_1 == False:
                    self.g = self.right_motor + 2.7 * alpha
                    self.step_1_1 = True
                print(self.g)
                print(self.right_motor)
                if self.g - self.right_motor < 0.5:
                    self.w = 0.3

                self.msg.angular.z = self.w * self.pm / abs(self.pm)
                print("각속도", self.msg.angular.z)
                print(self.pm)
                self.publisher_.publish(self.msg)
                print(self.right_motor)
                self.get_logger().info(f"Rotating robot_1 by {self.theta} radians. {round(self.g - self.right_motor, 2)}asd{self.right_motor}")

                if self.g <= self.right_motor:
                    self.msg.linear.x = 0.0
                    self.msg.angular.z = 0.0
                    self.publisher_.publish(self.msg)
                    print("회전 완료")
                    print("1단계 완료")
                    self.step_1 = True
                    self.w = 0.8

            elif self.theta < 0.:
                self.theta = -abs(np.pi / 2 - abs(self.theta))
                alpha = -self.theta
                if self.step_1_1 == False:
                    self.g = self.left_motor + 2.7 * alpha
                    self.step_1_1 = True
                    
                if self.g - self.left_motor < 0.5:
                    self.w = 0.3

                self.msg.angular.z = self.w * self.pm / abs(self.pm)
                self.publisher_.publish(self.msg)
                print(self.pm)
                print(self.msg)
                self.get_logger().info(f"Rotating robot_1 by {self.theta} radians. {round(self.g - self.left_motor, 2)}")
                if self.g <= self.left_motor:
                    self.msg.linear.x = 0.0
                    self.msg.angular.z = 0.0
                    self.publisher_.publish(self.msg)
                    print("회전 완료")
                    print("회전 완료")
                    print("1단계 완료")
                    self.step_1 = True
                    self.w = 0.8
                    
        if self.step_1 == True:
            self.go_x()
    def go_x(self):
        if self.step_2 == False:
            alpha = abs(self.x)
            print(self.x)
            #if self.pm > 0:
            if self.step_2_1 == False:
                self.g = alpha * 45 + self.right_motor
                print(self.g)
                print(self.right_motor)
                self.step_2_1 = True

            if self.g - self.right_motor <= 1.5:
                self.v = 0.05
            self.msg.linear.x = self.v
            self.msg.angular.z = 0.0
            self.publisher_.publish(self.msg)
            self.get_logger().info(f"Moving robot_2 {self.x} meters along the x-axis. {round(self.g - self.right_motor, 2)}")
            if self.g <= self.right_motor:
                self.msg.linear.x = 0.0
                self.msg.angular.z = 0.0
                self.publisher_.publish(self.msg)
                self.step_2 = True
                print("2단계 완료")
                self.v = 0.2
                """Move the robot along the x-axis relative to the marker."""

        #elif self.pm < 0:
        #    if self.step_2_1 == False:
        #        g = alpha * 0.27 + self.left_motor
        #        self.step_2_1 = True
#
        #    self.msg.linear.x = self.v
        #    self.msg.angular.z = 0.0
        #    self.publisher_.publish(self.msg)
        #    self.get_logger().info(f"Moving robot_2 {self.x} meters along the x-axis. {round(g - self.right_motor, 2)}")
        #    if g <= self.left_motor:
        #        self.msg.linear.x = 0.0
        #        self.msg.angular.z = 0.0
        #        self.publisher_.publish(self.msg)
        #        self.step_2 = True

        if self.step_2 == True:
            self.turn_90degrees()
        
    def turn_90degrees(self):
        if self.step_3 == False:
            alpha = (np.pi / 2)
            if self.pm > 0:
                if self.step_3_1 == False:
                    self.g = self.right_motor + 2.8 * alpha
                    self.step_3_1 = True
                    print(self.g)
                    print(self.left_motor)

                if self.g - self.right_motor < 0.5:
                    self.w = 0.4
                self.msg.linear.x = 0.0
                self.msg.angular.z = self.pm / abs(self.pm) * self.w
                self.publisher_.publish(self.msg)
                self.get_logger().info(f"Rotating robot_3 by {np.pi / 2} radians.{round(self.g - self.right_motor, 2)}")
                if self.g <= self.right_motor:
                    self.msg.linear.x = 0.0
                    self.msg.angular.z = 0.0
                    self.publisher_.publish(self.msg)
                    print("회전 완료")
                    self.step_3 = True
                    print("3단계 완료")
                    self.w = 0.8
                    """Turn the robot 90 degrees in the direction of pm (1 or -1)."""

            elif self.pm < 0:
                if self.step_3_1 == False:
                    self.g = self.left_motor + 2.8 * alpha
                    self.step_3_1 = True
                    
                if self.g - self.left_motor < 0.5:
                    self.w = 0.4

                self.msg.linear.x = 0.0
                self.msg.angular.z = self.pm / abs(self.pm) * self.w
                self.publisher_.publish(self.msg)
                self.get_logger().info(f"Rotating robot_3 by {np.pi / 2} radians. {round(self.g - self.left_motor, 2)}")
                if self.g <= self.left_motor:
                    self.msg.linear.x = 0.0
                    self.msg.angular.z = 0.0
                    self.publisher_.publish(self.msg)
                    print("회전 완료")
                    self.step_3 = True
                    print("3단계 완료")
                    self.w = 0.8
                    """Turn the robot 90 degrees in the direction of pm (1 or -1)."""
                
        if self.step_3 == True:
            self.go_remain_6cm()

    def go_remain_6cm(self):
        if self.step_4 == False:
            alpha = (self.z -0.1)
            if self.step_4_1 == False:
                self.g = -alpha * 27  + self.right_motor
                self.step_4_1 = True

            if abs(self.g - self.right_motor) <= 1.5:
                self.v = 0.05
            self.msg.linear.x = -self.v * alpha / abs(alpha)
            self.msg.angular.z = 0.0
            print(self.msg)
            self.publisher_.publish(self.msg)
            self.get_logger().info(f"Moving robot_4 {self.x} meters along the x-axis.")
            if self.g >= self.right_motor:
                self.msg.linear.x = 0.0
                self.msg.angular.z = 0.0
                self.publisher_.publish(self.msg)
                print("4단계 완료")
                self.step_4 = True

        if self.step_4 == True:
            #self.create_timer(15.0, self.shutdown_node)
            pass

def main():
    rclpy.init()
    controller = ArUcoRobotController()
    data_merge_sub = DataMergeSub(controller)
    executor = MultiThreadedExecutor()
    executor.add_node(controller)
    executor.add_node(data_merge_sub)
    executor.spin()
    executor.shutdown()

if __name__ == "__main__":
    main()