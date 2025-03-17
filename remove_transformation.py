#!/usr/bin/python3
# 

import sys
import rosbag


if len(sys.argv) != 5:
    print('Script to remove a direct transformation from a bag file. Usage: ')
    print(sys.argv[0], 'input_file', 'output_file', 'parent_frame', 'child_frame') 
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]
parent_frame = sys.argv[3]
child_frame = sys.argv[4]


with rosbag.Bag(output_filename, 'w') as outbag:
    for topic, msg, t in rosbag.Bag(input_filename).read_messages():
        if topic == "/tf" or topic == "/tf_static":
            new_transforms = [
                tf for tf in msg.transforms if not (tf.header.frame_id == parent_frame and tf.child_frame_id == child_frame)
            ]
            if not new_transforms:
                continue
            msg.transforms = new_transforms
            outbag.write(topic, msg, msg.transforms[0].header.stamp)
        else:
            outbag.write(topic, msg, msg.header.stamp if msg._has_header else t)