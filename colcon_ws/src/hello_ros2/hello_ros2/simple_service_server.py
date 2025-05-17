import rclpy, time
from rclpy.node import Node
from std_srvs.srv import SetBool

class Service_server(Node):
    def __init__(self):
        super().__init__("service_server") # 노드 이름
        self.create_service(SetBool, 'setBool', self.setBool_callback) # 서비스 이름

    def setBool_callback(self, request:SetBool.Request, response:SetBool.Response):
        self.bool = request.data
        self.get_logger().info('This is an info message.')
        response.message='변경 성공'
        response.success=True
        time.sleep(5)
        return response



def main():
    rclpy.init()
    node=Service_server()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__=='__main__':
    main()