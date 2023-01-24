#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# Status of control sources
local = True
web = False

# Callback commands from cmd_local
def local_order(data):
    global local    
    if local:
        pub.publish(data)

# Callback commands from cmd_local
def web_order(data):
    global web
    #print(web)
    if web:
        pub.publish(data)        

# Source Controller
def command_switch(data):
    global local
    global web
    if data.data == 'local':
        local = True
        web = False        
    elif data.data == 'web':
        local = False
        web = True            
    elif data.data == 'both':
        local = True
        web = True

    print('local: ',local,'web: ',web)        
            

rospy.init_node('multiplexer', anonymous=True)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.Subscriber('cmd_local', Twist, local_order)
rospy.Subscriber('cmd_web', Twist, web_order)
rospy.Subscriber('change_origin_cmd', String, command_switch)

rospy.spin()