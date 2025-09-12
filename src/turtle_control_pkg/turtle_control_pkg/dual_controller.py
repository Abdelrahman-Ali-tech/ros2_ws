import sys
import termios
import tty
import rclpy
from rclpy.qos import QoSProfile
from rclpy.node import Node
from geometry_msgs.msg import Twist
import select
msg = """
Control Your Turtle!
---------------------------
Moving around:
   Up Arrow
Left Arrow   Down Arrow   Right Arrow

CTRL-C to quit
"""
movekeys_arrows={'\x1b[A':(1,0),'\x1b[B':(-1,0),'\x1b[C':(0,-1),'\x1b[D':(0,1)}
movekeys_wasd={'w':(1,0),'s':(-1,0),'a':(0,1),'d':(0,-1)}
def getkey(settings,timeout=0.1):
    tty.setraw(sys.stdin.fileno())
    rlist,_,_=select.select([sys.stdin],[],[],timeout)
    key=''
    if rlist :
        ch=sys.stdin.read(1)
        if ch=='\x1b':
            key=ch+sys.stdin.read(2)
        else :
            key=ch
    termios.tcsetattr(sys.stdin,termios.TCSADRAIN,settings) 
    return key
class TeleopTurtle(Node):
    def __init__(self):
        super().__init__('teleop_turtle')
        self.pub1 = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        self.settings=termios.tcgetattr(sys.stdin)

    def run(self):
        print(msg)
        while True:
            key=getkey(self.settings)
            twist1=Twist()
            twist2=Twist()
            if key in movekeys_arrows :
                x,th=movekeys_arrows[key]
                twist1.linear.x=x*2.0
                twist1.angular.z=th*2.0
                self.pub1.publish(twist1)
            elif key in movekeys_wasd:
                x,th=movekeys_wasd[key]
                twist2.linear.x=x*2.0
                twist2.angular.z=th*2.0
                self.pub2.publish(twist2)
            elif key =='\x03':
                break 
         
        twist1=Twist() 
        twist2=Twist() 
        twist1.linear.x=0
        twist2.linear.x=0
        twist1.angular.z=0
        twist2.angular.z=0
        self.pub1.publish(twist1)
        self.pub2.publish(twist2)
       
                    


        
def main():
    rclpy.init()
    node = TeleopTurtle()
    node.run()
    node.destroy_node()
    rclpy.shutdown()
