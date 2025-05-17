# ros2 run hello_ros2 simple_service_server2

import rclpy, time
from rclpy.node import Node
from std_srvs.srv import SetBool
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class Service_server(Node):
    def __init__(self):
        super().__init__("service_server") # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.create_service(SetBool, 'setBool', self.setBool_callback, callback_group=self.callback_group) # 서비스 이름
        self.bool = False
        self.cnt=0

    def setBool_callback(self, request:SetBool.Request, response:SetBool.Response):
        #self.bool = request.data
        self.get_logger().info(f'This is an info message.({self.cnt})')
        if request.data != self.bool:
            self.bool = not self.bool
            response.message=f'#{self.cnt} Request 변경 성공'
            response.success=True
        else:
            response.message=f'#{self.cnt} Request 변경 실패'
            response.success=False
        time.sleep(5)
        self.cnt+=1
        return response



def main():
    rclpy.init()
    node=Service_server()
    excutor = MultiThreadedExecutor(num_threads=5)
    excutor.add_node(node)
    try:
        excutor.spin()
    except KeyboardInterrupt:
        excutor.shutdown()
        node.destroy_node()        

if __name__=='__main__':
    main()