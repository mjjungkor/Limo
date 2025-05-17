# ros2 run hello_ros2 simple_service_server2
# ros2 action sned_goal --feedback /fibonacci user_interface/Fibonacci "{step: 10}""

import rclpy, time
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from user_interface.action import Fibonacci
from rclpy.action import ActionServer

class Action_server(Node):
    def __init__(self):
        super().__init__("fibonacci_server") # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.action_server=ActionServer(self, Fibonacci, 'fibonacci', execute_callback=self.execute_callback) # 서비스 이름

    def execute_callback(self, goal_handle):
        #goal
        request:Fibonacci.Goal=goal_handle.request
        self.get_logger().info(f"{request.step}")
        feedback=Fibonacci.Feedback()
        feedback.temp_seq=[0,1]
        result=Fibonacci.Result()

        #feedback
        for i in range(1, request.step):
            feedback.temp_seq.append(feedback.temp_seq[i]+feedback.temp_seq[i-1])
            goal_handle.publish_feedback(feedback)
            time.sleep(1)

        #result
        goal_handle.succeed() # 완료 상태 보내기
        # goal_handle.abort()
        result.seq=feedback.temp_seq
        return result # action종료

def main():
    rclpy.init()
    node=Action_server()
    excutor = MultiThreadedExecutor(num_threads=5)
    excutor.add_node(node)
    try:
        excutor.spin()
    except KeyboardInterrupt:
        excutor.shutdown()
        node.destroy_node()        

if __name__=='__main__':
    main()