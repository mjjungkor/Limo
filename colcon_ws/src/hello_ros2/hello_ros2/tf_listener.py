import rclpy
import rclpy.logging
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
import rclpy.time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):
    def __init__(self):
        super().__init__('tf2_listener')
        self.tf_buffer=Buffer()
        self.tf_listener=TransformListener(self.tf_buffer, self)
        self.timer=self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        try:
            t=self.tf_buffer.lookup_transform('joint', 'world', rclpy.time.Time())
        except Exception:
            self.get_logger().info('failed lookup!')
            return
        
        self.get_logger().info(f'x:{t.transform.translation.x}')
        self.get_logger().info(f'y:{t.transform.translation.y}')
        self.get_logger().info(f'z:{t.transform.translation.z}')

def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__=='__main__':
    main()
