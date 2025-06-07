# ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
# ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=/home/aa/kuLimo/map.yaml
# initial pose 잡아서 amcl 활성화
# ros2 run hello_ros2 patrol

from asyncio import Future
import rclpy, time
from rclpy.node import Node


from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from rclpy.action.client import ClientGoalHandle
from nav2_msgs.action import FollowWaypoints
from nav2_msgs.action._follow_waypoints import FollowWaypoints_GetResult_Response
from geometry_msgs.msg import PoseStamped
import math


class Action_client(Node):
    def __init__(self):
        super().__init__("fibonacci_client") # 노드 이름
        self.action_client=ActionClient(self, FollowWaypoints, 'follow_waypoints') # 서비스 이름(ros2 action list -t 명령어를 통해서 확인)
        self.future=Future()
        self.get_result_future=Future()
        # patrol_points는 map tf 기준(nav2가 실행된 rviz2에서 publish point 클릭하여 지도에서 위치 확인)
        self.patrol_points=[(4.0,0.0),(4.0,1.0),(2.0,2.5),(0.0,1.0)]
        self.patrol_degree=[0,90,180,90]
        self.patrol_index=0
        self.goal=FollowWaypoints.Goal()
        self.go_next()

    def go_next(self):
        self.send_goal(self.patrol_points[self.patrol_index][0], self.patrol_points[self.patrol_index][1],self.patrol_degree[self.patrol_index])
        self.patrol_index+=1
        if self.patrol_index>=len(self.patrol_points):
            self.patrol_index=0


    def send_goal(self, x:float, y:float, theta:int):
        pose=PoseStamped()
        pose.header.frame_id='map'
        pose.header.stamp=self.get_clock().now().to_msg()
        pose.pose.position.x=x
        pose.pose.position.y=y
        pose.pose.position.z=0.0
        rad=math.radians(theta)
        pose.pose.orientation.x=0.0 # 쿼터니언 : x,y,z,w를 각각 제곱후 더한 값은 '1'
        pose.pose.orientation.y=0.0
        pose.pose.orientation.z=math.sin(rad/2.0)
        pose.pose.orientation.w=math.cos(rad/2.0)

        self.goal.poses.clear()
        self.goal.poses.append(pose) 
        #서버접속
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info('connecting nav2 server...')
        self.future:Future=self.action_client.send_goal_async(self.goal, feedback_callback=self.feedback_callback)
        self.future.add_done_callback(self.goal_response_callback)


    def feedback_callback(self, msg):
        feedback:FollowWaypoints.Feedback=msg.feedback
        self.get_logger().info(f' 처리 결과 seq{feedback.current_waypoint}')
        self.get_logger().info(f" patrol index{self.patrol_index}")

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
        result: FollowWaypoints_GetResult_Response = future.result()  # type : ignore
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f"result: {result.result.missed_waypoints} 성공!!")
            self.go_next()
        if result.status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    rclpy.init()
    node=Action_client()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        rclpy.shutdown()
        node.destroy_node()        

if __name__=='__main__':
    main()