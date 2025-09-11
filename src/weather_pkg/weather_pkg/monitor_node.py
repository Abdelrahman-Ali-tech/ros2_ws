
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random
class MonitorSubscriber(Node):
    def __init__(self):
        super().__init__('Monitor_Subscriber')
        self._sub_temp= self.create_subscription(Int32, '/temperature',self.temperature_callback,10)
        self._sub_hum= self.create_subscription(Int32, '/humidity',self.humidity_callback,10)
        self._sub_press= self.create_subscription(Int32, '/pressure',self.pressure_callback,10)
        self.temperature=None
        self.humidity=None
        self.pressure=None


    def temperature_callback(self,msg):
        self.temperature=msg.data
        self.monitor()
    def humidity_callback(self,msg):
        self.humidity=msg.data
        self.monitor()
    def pressure_callback(self,msg):
        self.pressure=msg.data
        self.monitor()

 
       
    def monitor(self):
      line=f'Temp = {self.temperature} ◦ C, Humidity = {self.humidity} %, Pressure = {self.pressure} hPa.'
      print(line)
      with open('readings.txt','a')as f:
          f.write(line+'\n')
          

     
 
        
def main():
    rclpy.init()
    node = MonitorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

#colcon build --packages-select pkg_py
#source install/setup.bash
#ros2 run pkg_py monitor_node 