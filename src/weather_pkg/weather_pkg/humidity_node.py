
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random
class HumidityPublisher(Node):
    def __init__(self):
        super().__init__('humidity_publisher')
        self.publisher_ = self.create_publisher(Int32, '/humidity', 10)
        self.timer = self.create_timer(2.0, self.humidity_callback)
       

    def humidity_callback(self):
        msg = Int32()
        msg.data = random.randint(20, 100)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Humidity: "{msg.data}%"')
       

 
        
def main():
    rclpy.init()
    node = HumidityPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

#colcon build --packages-select pkg_py
#source install/setup.bash
#ros2 run pkg_py humidity_node 