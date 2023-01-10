#!/usr/bin/env python
import rospy
import tf
import sys
import numpy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Point, Quaternion, PolygonStamped, PointStamped, Point32
from tf import transformations

br = tf.TransformBroadcaster()
p_map_odom1 = None
q_map_odom1 = None

def odom1_callback(data):
    global br
    p = data.pose.pose.position
    q = data.pose.pose.orientation
    p_map_baselink = numpy.array([p.x, p.y, p.z])
    q_map_baselink = numpy.array([q.x, q.y, q.z, q.w])

    q_odom1_map = transformations.quaternion_inverse(q_map_odom1)
    R_odom1_map = transformations.quaternion_matrix(q_odom1_map)
    p_odom1_baselink = numpy.dot(R_odom1_map[0:3,0:3], p_map_baselink - p_map_odom1)

    q_odom1_baselink = transformations.quaternion_multiply(q_odom1_map, q_map_baselink)

    br.sendTransform(p_odom1_baselink,
                     q_odom1_baselink,
                     data.header.stamp,
                     'husky_1/base_link',
                     'husky_1/odom')


    
if __name__ == '__main__':
    rospy.init_node('ground_truth_tf_publisher')
    tf_listener = tf.TransformListener()
    
    rate = rospy.Rate(100)
    received_odometry_to_map = False
    while not rospy.is_shutdown() and not received_odometry_to_map:
        try:
            (p_map_odom1, q_map_odom1) = tf_listener.lookupTransform('map', 'husky_1/odom', rospy.Time(0))
            received_odometry_to_map = True
        except Exception as e:
            pass
        
        rate.sleep()

    if received_odometry_to_map:
        real_odom_sub1 = rospy.Subscriber("/husky_1/odometry/ground_truth", Odometry, odom1_callback)
        while not rospy.is_shutdown():
            rate.sleep()


