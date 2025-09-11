
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random
class TemperaturePublisher(Node):
    def __init__(self):
        super().__init__('temperature_publisher')
        self.publisher_ = self.create_publisher(Int32, '/temperature', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
       

    def timer_callback(self):
        msg = Int32()
        msg.data = random.randint(15, 40)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Temperature: "{msg.data} ◦ C"')
       

 
        
def main():
    rclpy.init()
    node = TemperaturePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

#colcon build --packages-select pkg_py
#source install/setup.bash
#ros2 run pkg_py temperature_node 