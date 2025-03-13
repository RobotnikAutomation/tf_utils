#!/usr/bin/python

from rosbags.highlevel import AnyReader
from pathlib import Path
import sys


if len(sys.argv) != 4:
  print('Script to extract direct transformations in TUM format (stamp x y z qx qy qz qw) from a bag file. Usage: ')
  print(sys.argv[0], 'bag_file', 'parent_frame', 'child_frame') 

bag_filename = sys.argv[1]
parent_frame = sys.argv[2]
child_frame = sys.argv[3]


file = Path(sys.argv[1])

with AnyReader([file]) as reader:
    connections = [x for x in reader.connections if x.msgtype == 'tf2_msgs/msg/TFMessage']
    for connection, timestamp, rawdata in reader.messages(connections=connections):
        msg = reader.deserialize(rawdata, connection.msgtype)
        for t in msg.transforms:
            if t.header.frame_id == parent_frame and t.child_frame_id == child_frame:
                print("%d.%09d" % (t.header.stamp.sec, t.header.stamp.nanosec), t.transform.translation.x, t.transform.translation.y, t.transform.translation.z, t.transform.rotation.x, t.transform.rotation.y, t.transform.rotation.z, t.transform.rotation.w)
