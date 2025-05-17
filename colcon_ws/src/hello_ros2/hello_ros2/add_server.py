# ros2 run hello_ros2 simple_service_server2

import rclpy, time
from rclpy.node import Node
from std_srvs.srv import SetBool
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from user_interface.srv import AddTwoInts

class Service_server(Node):
    def __init__(self):
        super().__init__("add_service_server") # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.create_service(AddTwoInts, 'add_ints', self.setBool_callback, callback_group=self.callback_group) # 서비스 이름
        self.bool = False
        self.cnt=0

    def setBool_callback(self, request:AddTwoInts.Request, response:AddTwoInts.Response):
        self.get_logger().info(f"{request.header.stamp}번째 요청 처리")
        self.get_logger().info(f"a : {request.a}")
        self.get_logger().info(f"b : {request.b}")
        response.result = request.a + request.b
        response.success = True
        response.message = "a 와 b 의 값을 더해서 반환 했다!"
        time.sleep(5)
        self.cnt += 1
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