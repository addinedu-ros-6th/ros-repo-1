import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.executors import MultiThreadedExecutor
from dogniel_msgs.msg import DognielAmcl

class AmclPoseSub(Node):
    def __init__(self, dogniel_amcl):
        super().__init__('amcl_pose_sub')
        self.dogniel_amcl = dogniel_amcl
        # PoseWithCovarianceStamped 토픽 구독
        self.amcl_subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.amcl_callback,
            10
        )
        
    def amcl_callback(self, data):
        x = round(data.pose.pose.position.x,4)
        y = round(data.pose.pose.position.y,4)
        z = round(data.pose.pose.orientation.z,4)
        w = round(data.pose.pose.orientation.w,4)
        self.get_logger().info(f'x={x}, y={y},z={z}w={w}')
        self.tranceform_to_dogniel(x, y, z, w)
        
    def tranceform_to_dogniel(self, x, y, z, w):
        old_min_x = 0.
        old_max_x = 2.4
        old_min_y = 1.5
        old_max_y = 0.
        new_min_x = 0.
        new_max_x = 80.
        new_min_y = 0.
        new_max_y = 50.
        tranceformed_x = round(((x - old_min_x) / (old_max_x - old_min_x)) * (new_max_x - new_min_x) + new_min_x, 0)
        tranceformed_y = round(((y - old_min_y) / (old_max_y - old_min_y)) * (new_max_y - new_min_y) + new_min_y, 0)
        tranceformed_z = z
        tranceformed_w = w
        self.dogniel_amcl.x = int(tranceformed_x)
        self.dogniel_amcl.y = int(tranceformed_y)
        self.dogniel_amcl.z = tranceformed_z
        self.dogniel_amcl.w = tranceformed_w
        
class DognielAmclPosePub(Node):
    def __init__(self):
        super().__init__('dogniel_amcl')
        self.publisher = self.create_publisher(DognielAmcl, "dogniel_amcl", 10)
        self.x = None
        self.y = None
        self.z = None
        self.w = None

        # 0.1초마다 퍼블리시 메서드 실행
        self.timer = self.create_timer(0.1, self.publish_message)

    def publish_message(self):
        if self.x is not None: 
            msg = DognielAmcl()
            msg.x = int(self.x)
            msg.y = int(self.y)
            msg.z = self.z
            msg.w = self.w
            self.publisher.publish(msg)
            self.get_logger().info(f' x={msg.x}, y={msg.y}, z={msg.z}')

def main():
    rclpy.init()
    dogniel_amcl = DognielAmclPosePub()
    amcl_pose_sub = AmclPoseSub(dogniel_amcl)
    executor = MultiThreadedExecutor()
    executor.add_node(dogniel_amcl)
    executor.add_node(amcl_pose_sub)
    executor.spin()
    rclpy.shutdown()
if __name__ == "__main__":
    main()
