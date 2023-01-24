#!/usr/bin/env python3

# import the necessary packages
import apriltag
import argparse
import cv2
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to input image containing AprilTag")
args = vars(ap.parse_args())

# load the input image and convert it to grayscale
print("[INFO] loading image...")
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# define the AprilTags detector options and then detect the AprilTags in the input image
print("[INFO] detecting AprilTags...")
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
results = detector.detect(gray)
print("[INFO] {} total AprilTags detected".format(len(results)))

# loop over the AprilTag detection results
for r in results:
    
    # extract the bounding box (x, y)-coordinates for the AprilTag
    # and convert each of the (x, y)-coordinate pairs to integers
    (ptA, ptB, ptC, ptD) = r.corners
    ptB = (int(ptB[0]), int(ptB[1]))
    ptC = (int(ptC[0]), int(ptC[1]))
    ptD = (int(ptD[0]), int(ptD[1]))
    ptA = (int(ptA[0]), int(ptA[1]))
    # draw the bounding box of the AprilTag detection
    cv2.line(image, ptA, ptB, (0, 255, 0), 2)
    cv2.line(image, ptB, ptC, (0, 255, 0), 2)
    cv2.line(image, ptC, ptD, (0, 255, 0), 2)
    cv2.line(image, ptD, ptA, (0, 255, 0), 2)
    # draw the center (x, y)-coordinates of the AprilTag
    (cX, cY) = (int(r.center[0]), int(r.center[1]))
    cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
    # draw the tag ID on the image
    tagID = str(r.tag_id)
    cv2.putText(image, tagID, (ptA[0], ptA[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)    
    print("[INFO] tag ID: {}".format(tagID))
    
# show the output image after AprilTag detection
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 500, 500)
cv2.imshow("Image", image)
cv2.waitKey(0)

rospy.init_node('send_goal_tag')
# Initialize the action client
client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

# Create the goal
goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"

if results[0].tag_id == 20:
    goal.target_pose.pose.position.x = 1
    goal.target_pose.pose.position.y = 2
    goal.target_pose.pose.orientation.z = 1
elif results[0].tag_id == 21:
    goal.target_pose.pose.position.x = -1
    goal.target_pose.pose.position.y = 2
    goal.target_pose.pose.orientation.z = 1
elif results[0].tag_id == 22:
    goal.target_pose.pose.position.x = 1
    goal.target_pose.pose.position.y = -2
    goal.target_pose.pose.orientation.z = 1

# Send the goal
client.send_goal(goal)
client.wait_for_result()
print("fin")
rospy.spin()
    
