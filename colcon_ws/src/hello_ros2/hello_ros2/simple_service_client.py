# ros2 run hello_ros2 simple_service_client

import rclpy, time
from rclpy.node import Node
from std_srvs.srv import SetBool
from rclpy.executors import MultiThreadedExecutor
from asyncio import Future

class Service_client(Node):
    def __init__(self):
        super().__init__("service_client") # 노드 이름
        self.client = self.create_client(SetBool, 'setBool') # 서비스 이름
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")        
        
        self.create_timer(1, self.update) #현재 프로그램 상태 확인 타이머
        self.create_timer(2, self.send_request) #서버 요청 타이머
        self.bool = False
        self.cnt=0
        self.request=SetBool.Request()
        self.future = Future()

    def update(self):
        self.get_logger().info("main Thread is running!")

    def send_request(self):
        self.get_logger().info(f"{self.cnt} request")
        self.request.data=not self.request.data
        self.future = self.client.call_async(self.request)
        self.future.add_done_callback(self.done_callback)
        self.cnt += 1 

    def done_callback(self, future):
        response : SetBool.Response=future.result()
        self.get_logger().info(f"처리 상태 : {response.success}")
        self.get_logger().info(f"서버에서 온 메시지 : {response.message}")



def main():
    rclpy.init()
    node=Service_client()
    excutor = MultiThreadedExecutor(num_threads=5)
    excutor.add_node(node)
    try:
        excutor.spin()
    except KeyboardInterrupt:
        excutor.shutdown()
        node.destroy_node()        

if __name__=='__main__':
    main()