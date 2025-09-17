import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn,Kill
import random
import sys
import math
from std_msgs.msg import Int32
from functools import partial
class TurtleChase(Node):
    
    def __init__(self):
        super().__init__('turtle_chase')
        self.score_pub=self.create_publisher(Int32,'/score',10)
        self.score=0
        #=====parameters====
        self.declare_parameter('num_turtles',3)
        num_turtles=self.get_parameter('num_turtles').get_parameter_value().integer_value

        #===clients====
        self.spawn_client=self.create_client(Spawn,'/spawn')
        self.kill_client=self.create_client(Kill,"/kill")

        #===subscription===
        self.turtle1_pose=None
        self.enemy_positions ={}
        self.create_subscription(Pose,'/turtle1/pose',self. player_callback,10)
        self.create_timer(0.5,self.check_collisions)
        for i in range(1,num_turtles+1):
            name=f'enemy{i}'
            self.enemy_positions [name] = None
            self.spawn(name)

    def  player_callback(self,msg):
        self.turtle1_pose=msg
    
    def  enemy_callback(self,name,msg):
        self.enemy_positions [name]=[msg.x,msg.y]
        

    def spawn (self,name):
        req=Spawn.Request()
        req.x=random.uniform(0.5,10.5)    
        req.y=random.uniform(0.5,10.5)   
        req.theta=random.uniform(-3.14,3.14) 
        req.name=name  
        future=self.spawn_client.call_async(req)
        future.add_done_callback(partial(self.spawn_callback,name=name,x=req.x,y=req.y))
    def spawn_callback(self,future,name,x,y):    
        try:
            resp=future.result()
            ac_name=resp.name 
            self.create_subscription(Pose,f'/{ac_name}/pose',partial(self.enemy_callback,name),10) 
            self.get_logger().info(f'Spawned turtle  {ac_name} at x={x:.2f} y={y:.2f}')
              
        except:
            self.get_logger().info(f'Fail to Spawned turtle requested: {ac_name}')      

    def check_collisions(self):   
        for name,pose_enemy in self.enemy_positions .items():
           if pose_enemy is None:    
            continue
           dist=math.sqrt((self.turtle1_pose.x-pose_enemy[0])**2+(self.turtle1_pose.y-pose_enemy[1])**2)
           if dist<0.5:
               self.score+=1
               msg=Int32()
               msg.data=self.score
               self.score_pub.publish(msg)
               self.get_logger().info(f'Great Job ! Score is {self.score}')
               self.kill(name)
    def kill(self,name):
        req=Kill.Request()
        req.name=name
        future=self.kill_client.call_async(req)
        future.add_done_callback(partial(self.kill_callback,name=name))

    def kill_callback(self,future,name):
        
        try:
            resp=future.result()
            self.get_logger().info(f'Turtle {name} Killed')
            self.enemy_positions [name]=None
            self.spawn(name)
        except:    
            self.get_logger().info(f"Failed to kill {name}")   
    
            
def main (args=None):   
    rclpy.init(args=args)
    node=TurtleChase()     
    rclpy.spin(node)   
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()