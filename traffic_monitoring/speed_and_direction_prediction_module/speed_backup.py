import math
import cv2
import numpy as np
from collections import deque
import random

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    if label == 0: #person
        color = (85,45,255)
    elif label == 2: # Car
        color = (222,82,175)
    elif label == 3:  # Motobike
        color = (0, 204, 255)
    elif label == 5:  # Bus
        color = (0, 149, 255)
    else:
        color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


totalCountUp = [] # total count of objects that crossed the line going up
totalCountDown = [] # total count of objects that crossed the line going down

# draw the bounding box and the speed of the object
def UI_box(x, img, color=None, label=None, id=id, line_thickness=None):
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))

    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        
        img = cv2.rectangle(img, (c1[0], c1[1] - t_size[1] - 3), (c1[0] + t_size[0], c1[1] - 2), color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)



        

# setup line coordinates
limitsDown = [612, 1056, 1350, 1000] # down line coordinates [x1, y1, x2, y2]
limitsUp = [1440, 928, 1850, 876] # up line coordinates [x1, y1, x2, y2]


speed_line_queue = {}
data_deque = {}


# draw the bounding box and the speed of the object
def draw_boxes_orig(img, bbox, names,object_id, identities=None, offset=(0, 0)):

    cv2.line(img,(limitsUp[0],limitsUp[1]),(limitsUp[2],limitsUp[3]),(0,255,0),5)
    cv2.putText(img,"up",(limitsUp[0],limitsUp[1]-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.line(img,(limitsDown[0],limitsDown[1]),(limitsDown[2],limitsDown[3]),(0,0,255),5)
    cv2.putText(img,"Down",(limitsDown[0],limitsDown[1]-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    global totalCountUp
    global totalCountDown

    height, width, _ = img.shape
    for key in list(data_deque):
      if key not in identities:
        data_deque.pop(key)

    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]

        # bounding box center
        center = int(x1+((x2-x1) / 2)), int(y1+(y2 - y1) / 2)

        # get ID of object
        id = int(identities[i]) if identities is not None else 0

        # create new buffer for new object
        if id not in data_deque:  
            data_deque[id] = deque(maxlen= 64)
            speed_line_queue[id] = []


        color = compute_color_for_labels(object_id[i])
        obj_name = names[object_id[i]]
        label = '{}{:d}'.format("", id) + ":"+ '%s' % (obj_name)

        # add center to buffer
        data_deque[id].appendleft(center)
        # if data deque has more than two value, calculate speed
        if len(data_deque[id]) >= 2:
            object_speed = estimate_speed(data_deque[id][1], data_deque[id][0])
            speed_line_queue[id].append(object_speed)
          

        try:
            label = label + " " + str(sum(speed_line_queue[id])//len(speed_line_queue[id])) + "km/h"
        except:
            pass
        
        UI_box(box, img, label=label, color=color, id=id ,line_thickness=2)
        # draw trail
        for i in range(1, len(data_deque[id])):
            # check if on buffer value is none
            if data_deque[id][i - 1] is None or data_deque[id][i] is None:
                continue
            # generate dynamic thickness of trails
            thickness = int(np.sqrt(64 / float(i + i)) * 1.5)
            # draw trails
            cv2.line(img, data_deque[id][i - 1], data_deque[id][i], color, thickness)

        # Display count in top right and left corner
        
        cv2.circle(img,(150,100),50,(0,0,255),-1)
        cv2.circle(img,(width-150,100),50,(0,255,0),-1)
        cv2.putText(img,str(len(totalCountDown)),(130,120),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),5)
        cv2.putText(img,str(len(totalCountUp)),(width-170,120),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),5)

        cv2.putText(img, "Total Down count: " , (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.putText(img, "Total Up count: ", (width - 280, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    return img


def unknown(img, bbox, identities=None):

    cv2.line(img,(limitsUp[0],limitsUp[1]),(limitsUp[2],limitsUp[3]),(0,255,0),5)
    cv2.putText(img,"up",(limitsUp[0],limitsUp[1]-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    # Removing Vehicles from data_deque that are no longer trackeds
    for key in list(data_deque):
      if key not in identities:
        data_deque.pop(key)

    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]

        # bounding box center
        center = int(x1+((x2-x1) / 2)), int(y1+(y2 - y1) / 2)

        # get ID of object
        id = int(identities[i]) if identities is not None else 0

        # create new buffer for new object
        if id not in data_deque:  
            data_deque[id] = deque(maxlen= 64)
            speed_line_queue[id] = []


        # add center to buffer
        data_deque[id].appendleft(center)
        # if data deque has more than two value, calculate speed
        if len(data_deque[id]) >= 2:
            object_speed = estimate_speed(data_deque[id][1], data_deque[id][0])
            speed_line_queue[id].append(object_speed)
          

        try:
            label = label + " " + str(sum(speed_line_queue[id])//len(speed_line_queue[id])) + "km/h"
        except:
            pass
        
        line_thickness = 2
        tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
        color = color or [random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))

        if label:
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            
            img = cv2.rectangle(img, (c1[0], c1[1] - t_size[1] - 3), (c1[0] + t_size[0], c1[1] - 2), color, -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)





    return img



# calculate the speed of the object
def estimate_speed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    ppm = 8.8
    d_meters = d_pixels / ppm
    fps = 12.5
    speed = d_meters * fps * 3.6
    return int(speed)