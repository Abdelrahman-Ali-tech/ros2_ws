
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 10

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2: {self.count}'
        self.publisher_.publish(msg)
        print(f'Publishing: "{msg.data}"')
        self.count -=1
        
        if self.count <0:
              print(f'Time is up!') 
              self.timer.cancel()
              self.destroy_node() 
              rclpy.shutdown()


 
        
def main():
    rclpy.init()
    node = MinimalPublisher()
    rclpy.spin(node)
    

#colcon build --packages-select pkg_py
#source install/setup.bash
#ros2 run pkg_py publisher_node