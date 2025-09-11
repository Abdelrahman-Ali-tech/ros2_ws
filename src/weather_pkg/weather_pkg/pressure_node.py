
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random
class PressurePublisher(Node):
    def __init__(self):
        super().__init__('pressure_publisher')
        self.publisher_ = self.create_publisher(Int32, '/pressure', 10)
        self.timer = self.create_timer(3.0, self.pressure_callback)
       

    def pressure_callback(self):
        msg = Int32()
        msg.data = random.randint(900, 1100)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Pressure: "{msg.data} hPa"')
       

 
        
def main():
    rclpy.init()
    node = PressurePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

#colcon build --packages-select pkg_py
#source install/setup.bash
#ros2 run pkg_py pressure_node 