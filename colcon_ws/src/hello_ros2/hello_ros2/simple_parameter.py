# ros2 run hello_ros2 simple_parameter --ros-args -p use_sim_time:=True
# ros2 param set simple_parameter para1 4444
# ros2 param dump turtlesim >> turtlesim.yaml # 파라메타를 .yaml 파일로 저장
# ros2 run turtlesim turtlesim_node --ros-args --params-file:=turtlesim.yaml # 저장된 .yaml 파일 사용

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult

class Simple_parameter(Node):
    def __init__(self):
        super().__init__('simple_parameter')
        self.create_timer(1, self.update)
        self.para1=0
        self.declare_parameter('para1',0) # 파라메타의 선언과 변수의 사용은 독립적
        self.para1=self.get_parameter('para1').get_parameter_value().integer_value
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, parameters:list[Parameter]):# 외부에서 파라메타 변경에 의한 콜백
        for parameter in parameters:
            if parameter.name=='para1':
                self.para1=int(parameter.value)
        return SetParametersResult(successful=True)


    def update(self):
        self.get_logger().info(f'parameter:{self.para1}')
        self.para1+=1
        self.set_parameters([Parameter('para1', Parameter.Type.INTEGER, self.para1)]) # get으로 변경된 파라메타의 실시간 반영

def main():
    rclpy.init()
    node=Simple_parameter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__ == '__main__':
    main()
