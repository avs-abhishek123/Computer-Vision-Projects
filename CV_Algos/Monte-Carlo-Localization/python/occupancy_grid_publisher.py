#!/usr/bin/env python
import rospy
import tf
import sys
import numpy
from nav_msgs.msg import OccupancyGrid
import pickle

if __name__ == '__main__':
    rospy.init_node('occupancy_grid_publisher')
    og_filename = rospy.get_param("~occupancy_grid_filename")
    pkl_file = open(og_filename, 'rb')
    og = pickle.load(pkl_file)

    rate = rospy.Rate(1)
    og_pub = rospy.Publisher("/projected_map", OccupancyGrid, queue_size=1)
    while not rospy.is_shutdown():
        if og_pub.get_num_connections() > 0:
            og_pub.publish(og)
        rate.sleep()
        

