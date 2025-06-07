# sudo apt install ros-humble-tf-transformations
# ros2 run turtlesim turtlesim_node
# ros2 run hello_ros2 follow_turtlesim
# rviz2 -> tf 확인
# ros2 run turtlesim turtle_teleop_key

import rclpy
import rclpy.logging
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, Twist
import rclpy.time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from turtlesim.srv import Spawn
from turtlesim.msg import Pose 

from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf_transformations import quaternion_from_euler, euler_from_quaternion # sudo apt install ros-humble-tf-transformations
import math


class Follow_trutle(Node):
    def __init__(self):
        super().__init__('follow_trutle')
        self.tf_buffer=Buffer()
        self.tf_listener=TransformListener(self.tf_buffer, self)
        self.timer=self.create_timer(0.1, self.on_timer)
        self.spawer=self.create_client(Spawn, 'spawn')
        request=Spawn.Request() # 터틀심의 면적 : 11 x 11
        request.x=3.0
        request.y=3.0
        request.theta=0.0
        self.result=self.spawer.call_async(request)

        self.tf_br=TransformBroadcaster(self)
        self.sub=self.create_subscription(Pose, '/turtle1/pose', self.sub_cb, 10)
        self.sub2=self.create_subscription(Pose, '/turtle2/pose', self.sub_cb2, 10)
        self.pub = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)

    def sub_cb(self, msg:Pose):
        t=TransformStamped()
        t.header.stamp=self.get_clock().now().to_msg()
        t.header.frame_id='world'
        t.child_frame_id='turtle1'
        t.transform.translation.x=msg.x
        t.transform.translation.y=msg.y
        t.transform.translation.z=0.0

        quat=quaternion_from_euler(0,0,msg.theta) # r y p
        t.transform.rotation.x=quat[0]
        t.transform.rotation.y=quat[1]
        t.transform.rotation.z=quat[2]
        t.transform.rotation.w=quat[3]
        
        self.tf_br.sendTransform(t)

    def sub_cb2(self, msg:Pose):
        t=TransformStamped()
        t.header.stamp=self.get_clock().now().to_msg()
        t.header.frame_id='world'
        t.child_frame_id='turtle2'
        t.transform.translation.x=msg.x
        t.transform.translation.y=msg.y
        t.transform.translation.z=0.0

        quat=quaternion_from_euler(0,0,msg.theta) # r y p
        t.transform.rotation.x=quat[0]
        t.transform.rotation.y=quat[1]
        t.transform.rotation.z=quat[2]
        t.transform.rotation.w=quat[3]
        
        self.tf_br.sendTransform(t)

    def on_timer(self):

        try:
            t=self.tf_buffer.lookup_transform('turtle1', 'turtle2', rclpy.time.Time())
        except Exception:
            self.get_logger().info('failed lookup!')
            return
        
        self.get_logger().info(f'x:{t.transform.translation.x}')
        self.get_logger().info(f'y:{t.transform.translation.y}')
        self.get_logger().info(f'z:{t.transform.translation.z}')

        msg=Twist()
        angular=euler_from_quaternion((t.transform.rotation.x, t.transform.rotation.y, t.transform.rotation.z, t.transform.rotation.w))
        # msg.angular.x=angular[0]
        # msg.angular.y=angular[1]
        # msg.angular.z=angular[2]
        # msg.linear.x=t.transform.translation.x+t.transform.translation.y

        msg.angular.x=0.0
        msg.angular.y=0.0

        if (math.atan2(t.transform.translation.x ,t.transform.translation.y) - angular[2]) > 0:
            msg.angular.z=2.0
        else:
            msg.angular.z=-2.0

        if t.transform.translation.x**2 + t.transform.translation.y**2 > 0.2:
            msg.linear.x=1.0
        else:    
            msg.linear.x=0.0

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = Follow_trutle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__=='__main__':
    main()
