import numpy as np
import cv2
import csv
import datetime
import atexit
import os
from traffic_monitoring.color_recognition_module import color_recognition_api
from traffic_monitoring.speed_and_direction_prediction_module import speed_prediction

from utilities import find_centroid

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)

def write_to_csv(file_path, bbox, class_name):
    # Create header if file is new
    is_new_file = not os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if is_new_file:
            writer.writerow(['Timestamp', 'BBox', 'Class'])
        
        # Write data to file
        current_time = datetime.datetime.now()
        writer.writerow([current_time.strftime("%Y-%m-%d %H:%M:%S"), bbox, class_name])
    
    # Close file when program terminates
    @atexit.register
    def close_csv_file():
        csv_file.close()


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)

def overlay_on_image(image,clr_trails):
    h, w = clr_trails.shape[:2]
    overlay = np.zeros((h, w, 3), dtype=np.uint8)
    
    gray = cv2.cvtColor(clr_trails,cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)[1]
    inverted_mask = cv2.bitwise_not(mask)
    image = cv2.bitwise_and(image, image, mask=inverted_mask)
    overlay = cv2.bitwise_and(clr_trails, clr_trails, mask=mask)
    image = cv2.bitwise_or(overlay, image)
    return image

def inc_int(color,factor = 1.4):
    b,g,r = color
    new_b = b*factor if b*factor < 255 else 255
    new_g = g*factor if g*factor < 255 else 255
    new_r = r*factor if r*factor < 255 else 255
    return (new_b,new_g,new_r)

def find_keys_not_in_dict(a, b, c):
    if type(a) == dict:
        # handle dictionary case
        a_keys = set(a.keys())
    else:
        a_keys = set(a)
    if type(b) == dict:
        b_keys = set(b.keys())
    else:
        b_keys = set(b)
    if type(c) == dict:
        c_keys = set(c.keys())
    else:
        c_keys = set(c)

    # Find keys that are in a but not in b or c
    result = list(a_keys - (b_keys | c_keys))

    return result

def count_vehicles(img, counter_num):

    # Get the size of the image
    height, width, _ = img.shape

    # Define the font and size of the counter
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = height / 1000.0

    # Define the position of the counter
    text = "Cars entered: "+ str(counter_num)
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness=1)
    x_pos = int(width - text_size[0] - 10)
    y_pos = int(text_size[1] + 10)
    # Create a black rectangle behind the text
    cv2.rectangle(img, (x_pos, y_pos - text_size[1]), (width, y_pos + 10), (0, 0, 0), -1)

    # Draw the counter on the image
    cv2.putText(img, text, (x_pos, y_pos), font, font_scale, (40, 255, 40), thickness=2)

def draw_arrow(image, direction, start_point):
    color = (0, 0, 255)  # red color
    thickness = 4
    length = 100
    if direction == 'left':
        end_point = (start_point[0] - length, start_point[1])
        cv2.arrowedLine(image, start_point, end_point, color, thickness)
    elif direction == 'right':
        end_point = (start_point[0] + length, start_point[1])
        cv2.arrowedLine(image, start_point, end_point, color, thickness)
        
        
def draw_boxes_m(img, bbox, identities=None, offset=(0,0),current_frame_number = 0):
    for i,box in enumerate(bbox):
        left, top, right , bottom = box
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        ##
        ROI_POSITION = int(img.shape[0]*0.5)
        # bbox = [left , top, right, down]
        detected_vehicle_image = img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        predicted_color = color_recognition_api.color_recognition(detected_vehicle_image)
        if(bottom > ROI_POSITION): # if the vehicle get in ROI area, vehicle predicted_speed predicted_color algorithms are called - 200 is an arbitrary value, for my case it looks very well to set position of ROI line at y pixel 200
            predicted_direction, predicted_speed,  is_vehicle_detected, update_csv = speed_prediction.predict_speed(top, bottom, right, left, current_frame_number, detected_vehicle_image, ROI_POSITION)
        else:
            predicted_direction, predicted_speed = "",0
        draw_arrow(img,predicted_direction,find_centroid(box))
        ##
        color = compute_color_for_labels(id)
        #label = '{}{:d}'.format("", id) + predicted_color + "car"
        label = f" {predicted_color} car - {predicted_speed} km/h"
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2 , 2)[0]
        cv2.rectangle(img,(x1, y1),(x2,y2),color,3)
        cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
        cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)
    return img


def draw_boxes(img, bbox, identities=None, offset=(0,0),mask = None, trajectories = None,id_to_track = None,t_classes = None,categories = None):
    for i,box in enumerate(bbox):
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0    
        color = compute_color_for_labels(id)
        
        bbox_thickness = 3
        draw_trajectory = True
        if id_to_track and id == id_to_track:
            color = (0,255,0)
            write_to_csv("john_doe.csv",box,t_classes[i])
        elif id_to_track:
            color = (0,0,40)
            bbox_thickness = 1
            draw_trajectory = False
        
        
        label = '{}{:d}'.format("", id)
        label_fscale = 2
        if categories:
            # If categories are avaible display them along the tracked object
            label = categories[t_classes[i]]
            label_fscale = 1.5
        
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, label_fscale , 2)[0]
        cv2.rectangle(img,(x1, y1),(x2,y2),color,bbox_thickness)
        cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
        cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, label_fscale, [255,255,255], 2)
        
        if draw_trajectory and trajectories is not None and len(trajectories[id])==2:
            cv2.line(mask,trajectories[id][0],trajectories[id][1],inc_int(color),3)
        img = overlay_on_image(img,mask)
        
    return img


if __name__ == '__main__':
    for i in range(82):
        print(compute_color_for_labels(i))
