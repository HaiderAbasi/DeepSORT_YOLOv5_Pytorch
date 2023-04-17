import math
import cv2
from collections import deque
import random





# calculate the speed of the object
def estimate_speed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    ppm = 8.8
    d_meters = d_pixels / ppm
    fps = 30
    speed = d_meters * fps * 3.6
    return int(speed)


def predict_speed(img, box, id,data_deque,speed_line_queue,label,color):
    # extract the coordinates of the bounding box
    x1, y1, x2, y2 = [int(i) for i in box]

    # calculate the center of the bounding box
    center = int(x1+((x2-x1) / 2)), int(y1+(y2 - y1) / 2)

    # create a new buffer for a new object if one doesn't already exist
    if id not in data_deque:  
        data_deque[id] = deque(maxlen= 64)
        speed_line_queue[id] = []

    # add the center of the bounding box to the buffer
    data_deque[id].appendleft(center)

    # if the buffer has more than two points, calculate the speed of the object
    if len(data_deque[id]) >= 2:
        object_speed = estimate_speed(data_deque[id][1], data_deque[id][0])
        speed_line_queue[id].append(object_speed)

    pred_speed = 0
    # calculate the average speed of the object and add it to the label
    try:
        label = label + " " + str(sum(speed_line_queue[id])//len(speed_line_queue[id])) + "km/h"
        pred_speed = sum(speed_line_queue[id])//len(speed_line_queue[id])
    except:
        pass
    
    # draw the bounding box and label on the image
    line_thickness = 2
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))

    # if label:
    #     tf = max(tl - 1, 1)  # font thickness
    #     t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]

    #     # draw a filled rectangle behind the label
    #     img = cv2.rectangle(img, (c1[0], c1[1] - t_size[1] - 3), (c1[0] + t_size[0], c1[1] - 2), color, -1, cv2.LINE_AA)
        
    #     # draw the label
    #     cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

    return pred_speed

