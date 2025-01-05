#!/usr/bin/env python
import Jetson.GPIO as GPIO
from time import sleep
import rospy
from std_msgs.msg import Float64, Float64MultiArray

def server_out_put(SERVO_PERIOD):
    high_time = 0.0005 + (ratio-2.5)/10*(0.002)
    GPIO.output(servopin, GPIO.HIGH)
    sleep(high_time)
    GPIO.output(servopin, GPIO.LOW)
    sleep(SERVO_PERIOD - high_time)


if __name__ == "__main__":
    # rospub init-------------------------
    rospy.init_node("servoping")
    rospy.logwarn("servoping is successfully initialized")
    pub = rospy.Publisher("servoping", Float64MultiArray, queue_size=10)
    rate = rospy.Rate(10)
    
    
    # ideal 2.5-12.5
    MAX = 11.7
    MIN = 4.8
    
    STEP = 0.2
    DELAY = 0.005   # f = 100hz
    SERVO_PERIOD = 0.02

    # init--------------------------------
    ratio = 12.5    
    servopin = 18
    key_open = 11
    key_close = 13
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servopin, GPIO.OUT, initial=False)
    
    GPIO.setup(key_close, GPIO.IN)
    GPIO.setup(key_open, GPIO.IN)
    
    
    while not rospy.is_shutdown():
        GPIO.setup(key_close, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(key_open, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(key_close, GPIO.IN)
        GPIO.setup(key_open, GPIO.IN)


        k1 = GPIO.input(key_open)
        k2 = GPIO.input(key_close)
        
        # print(k1,k2,ratio)
        msg = Float64MultiArray()
        msg.data = [k1, k2, ratio]
        pub.publish(msg)
        # rate.sleep()



        if k1 == False:
            ratio -= STEP
            if ratio < MIN:
                ratio = MIN
            server_out_put(SERVO_PERIOD)
            
        elif k2 == False:
            ratio += STEP
            if ratio > MAX:
                ratio = MAX
            server_out_put(SERVO_PERIOD)
        
    
