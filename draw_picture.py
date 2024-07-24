#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2024
# License: GPL v3


import socket
from datetime import datetime
import json
import random
import time
import sys
import cv2

UDP_IP = "127.0.0.1"
UDP_PORT = 13337
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_count(count, line_id, offset=0, frame=0):
    now = int((datetime.now() - datetime(1970, 1, 1)).total_seconds()) - offset - 60 * 60 * 3
    MESSAGE = '{"metrics":[{"name":"my_metric2",' + '"ts":' + str(now) + ', "tags":{"frame":"' + str(frame) + '","line_id":"' + str(line_id) +'"},"value":[' + str(count) + ']}]}'
    print(MESSAGE)
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

def send_frame(arr, line_id, frame=0):
    for i in range(0, len(arr)):
        if arr[i] >= 0:
            send_count(arr[i], line_id, len(arr) - i, frame)

import cv2

image = cv2.imread(sys.argv[1])

w = image.shape[0]
h = image.shape[1]

lines_num = 4
if len(sys.argv) > 3:
    lines_num = int(sys.argv[3])


lines = []
for line_id in range(0, lines_num):
    lines.append([])
    for x in range(0, h):
        y_start = 0
        appended = False
        if line_id > 0:
            y_start = w - lines[line_id - 1][x] + 5
            if y_start < 0:
                y_start = 10000
        for y in range(y_start, w):
            if line_id % 2 == 0:
                if (image[y, x] < [127, 127, 127]).all():
                    lines[line_id].append(w - y)
                    appended = True
                    break
            else:
                if (image[y, x] > [127, 127, 127]).all():
                    lines[line_id].append(w - y)
                    appended = True
                    break

        if not appended:
            lines[line_id].append(-10000)

    send_frame(lines[line_id], line_id, int(sys.argv[2]))
