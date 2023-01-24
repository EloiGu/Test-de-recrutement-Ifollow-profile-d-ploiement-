#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

class ImagePublisher:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_pub = rospy.Publisher("tag_AR", Image, queue_size=1)
        #rospy.Timer(rospy.Duration(1), self.timer_callback)
        self.timer_callback()

    def timer_callback(self):
        # Read the image from file        
        cv_image = cv2.imread("ar_tag_1.JPG")
        if cv_image is None:            
        else:
            img = Image()
            img.header.stamp = rospy.Time.now()
            img.encoding = "bgr8"
            img.header.frame_id = "base_link"
            img.data = cv2.imencode('.jpg',cv_image)[1].tostring()
            self.image_pub.publish(img)
            

if __name__ == '__main__':
    rospy.init_node('image_publisher')
    ImagePublisher()
    rospy.spin()
