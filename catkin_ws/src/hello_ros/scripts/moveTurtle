import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import random

def main():
    rospy.init_node('hello', anonymous=True)
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    sndData=Twist()
    sndData.angular.z=1.0
    vel=0.0    

    rate=rospy.Rate(3)

    while not rospy.is_shutdown():
        # vel+=0.1
        # sndData.linear.x=vel
        # if vel > 10:
        #     vel = 0.0

        vel=random.uniform(0.0, 5.0)
        sndData.linear.x=vel
        pub.publish(sndData)
        rate.sleep()

    print("hello, ROS1 noetic!!")

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass