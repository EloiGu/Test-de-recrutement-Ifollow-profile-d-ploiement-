#!/usr/bin/env python3
import rospy
import paho.mqtt.client as mqtt
from geometry_msgs.msg import Twist

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "speed_from_keyboard_topic"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    
    order = Twist()

    # Bit to string conversion
    message_received =  msg.payload.decode()

    # Separation of the message by / , the syntaxe is "order.linear.x/order.angular.z"
    Twist_tab = message_received.split("/")
    print(Twist_tab)
    order.linear.x = float(Twist_tab[0])    
    order.angular.z = float(Twist_tab[1])
    pub.publish(order)
    
    


def mqtt_subscriber():
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == '__main__':
    try:
        rospy.init_node('remote_teleoperation', anonymous=True)
        pub = rospy.Publisher('/cmd_web', Twist, queue_size=10)
        mqtt_subscriber()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

