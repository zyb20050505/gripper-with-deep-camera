#!/usr/bin/env python

import rospy
import rosbag
import Jetson.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)

bag_dir = "/home/z/bag"
if not os.path.exists(bag_dir):
    os.makedirs(bag_dir)

def record_bag(bag_filename):
    rospy.init_node("bag_recorder")
    topics_to_record = [
           '/camera/color/image_raw',
           '/camera/imu',
           '/servoping'
           ]
    bag_filename = bag_filename
    start = 0
    stop = 0
    button_pressed = 0

    with rosbag.Bag(bag_filename, 'w') as bag:
        while not rospy.is_shutdown():
            GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(26, GPIO.IN)
            if stop == 1 and GPIO.input(26) == GPIO.LOW:
                stop = 0
            if button_pressed == 0 and GPIO.input(26) == GPIO.LOW:
                button_pressed = 1
            if button_pressed == 1 and start == 1 and GPIO.input(26) == GPIO.HIGH:
                start = 0
                rospy.logwarn("stop to record!!!!")
                button_pressed = 0
                stop = 1
            if stop == 0 and button_pressed == 1 and GPIO.input(26) == GPIO.HIGH:
                start = 1
                rospy.logwarn("okk, start to record!!!!  Press the button again to stop.")
                button_pressed = 0



            if start == 1 and stop == 0:
                for topic in topics_to_record:
                    msg = rospy.wait_for_message(topic, rospy.AnyMsg, timeout=1)
                    bag.write(topic, msg)

if __name__ == '__main__':
    bag_filename = "/home/z/bag/gripper_data.bag"
    record_bag(bag_filename)



