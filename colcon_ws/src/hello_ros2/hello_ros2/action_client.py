# ros2 run hello_ros2 simple_service_server2
# ros2 action sned_goal --feedback /fibonacci user_interface/Fibonacci "{step: 10}""
# ros2 launch gazebo_ros gazebo.launch.py

from asyncio import Future
import rclpy, time
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from user_interface.action import Fibonacci
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from rclpy.action.client import ClientGoalHandle
from user_interface.action._fibonacci import Fibonacci_GetResult_Response


class Action_client(Node):
    def __init__(self):
        super().__init__("fibonacci_client") # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.action_client=ActionClient(self, Fibonacci, 'fibonacci') # 서비스 이름
        self.future=Future()
        self.get_result_future=Future()
        #서버접속
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info('connecting server...')

        self.send_goal()
        

    def send_goal(self):
        goal=Fibonacci.Goal()
        goal.step=8

        self.future:Future=self.action_client.send_goal_async(goal, feedback_callback=self.feedback_callback)
        self.future.add_done_callback(self.goal_response_callback)


    def feedback_callback(self, msg):
        feedback:Fibonacci.Feedback=msg.feedback
        self.get_logger().info(f'저리 결과 seq{feedback.temp_seq}')

    # ros1에 없는 부분(goal이 접수 될때 확인)
    def goal_response_callback(self, future:Future):
        goal_handle:ClientGoalHandle=future.result()
        if not goal_handle.accepted:
            self.get_logger().info(f'목표 접수 실패')
            return
        self.get_result_future:Future=goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.done_callback)
        
    #result
    def done_callback(self, future: Future):
        result: Fibonacci_GetResult_Response = future.result()  # type : ignore
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f"result: {result.result.seq} 성공!!")
        if result.status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info(f"result: aborted 실패!!")



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
        result.seq=feedback.temp_seq
        return result # action종료

def main():
    rclpy.init()
    node=Action_client()
    excutor = MultiThreadedExecutor(num_threads=5)
    excutor.add_node(node)
    try:
        excutor.spin()
    except KeyboardInterrupt:
        excutor.shutdown()
        node.destroy_node()        

if __name__=='__main__':
    main()