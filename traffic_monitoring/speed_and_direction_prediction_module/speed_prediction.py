#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------
# --- Author         : Ahmet Ozlu
# --- Mail           : ahmetozlu93@gmail.com
# --- Date           : 27th January 2018
# ----------------------------------------------
from traffic_monitoring.image_utils import image_saver

is_vehicle_detected = [0]
curr_frame_no_list = [0]
curr_frame_no_lst_2 = [0]
prev_bottom = [0]
lft_car = [0]
fps = 30

def predict_speed__(top,bottom,right,left,curr_frame_num,crop_img,roi_position):
    speed = 'n.a.'  # means not available, it is just initialization
    direction = 'n.a.'  # means not available, it is just initialization
    scale_constant = 1  # manual scaling because we did not performed camera calibration
    isInROI = True  # is the object that is inside Region Of Interest
    update_csv = False
    fps = 30
    ppm = 44 # pixels per meter
    # 
    # (0,0)       ______________\ + X (1280)              
    #            |              /
    #            |
    #            |
    # (1050) + Y \/
    #
    # Camera is facing the road. Farther out things would be smaller
    #                            Closer to the camera mean object will appear larger.
    if   bottom < 500:
        scale_constant = 1  # Farther away ---> Smaller multiplier as car will be smaller as rows go from top to bottom
    elif bottom > 500 and bottom < 640:
        scale_constant = 2  # Top > Center ---> Larger closer to camera
    #else:
    #    isInROI = False
    # scale_constant = 1
    
    # They are all checking if the position of the car and ROI meet certain requirements.
    #   # If the car's bottom position is above the ROI, then it cannot be intersecting with the ROI, 
    #   # so car_is_below_roi is checking for that. Similarly, car_is_in_range is checking if the car's horizontal position 
    #   # is within a certain range, and roi_above_car is checking if the ROI is above the car's top position.

    has_btm_car = len(prev_bottom) != 0
    car_is_below_roi = bottom - prev_bottom[0] > 0
    car_is_in_range = 400 < prev_bottom[0] < 600
    roi_above_car = roi_position < bottom + 100
    enough_frames_passed = curr_frame_num - curr_frame_no_lst_2[0] > fps

    if has_btm_car and car_is_below_roi and car_is_in_range and roi_above_car and enough_frames_passed:
        is_vehicle_detected.insert(0, 1)
        update_csv = True
        image_saver.save_image(crop_img)  # save detected vehicle image
        curr_frame_no_lst_2.insert(0, curr_frame_num)
    # for debugging
    # print("prev_bottom[0]: " + str(prev_bottom[0]))
    # print("bottom: " + str(bottom))
    if bottom > prev_bottom[0]:
        direction = 'down'
    else:
        direction = 'up'

    if isInROI:
        pixel_length = bottom - prev_bottom[0]
        scale_real_length = pixel_length * ppm  # multiplied by 44 to convert pixel length to real length in meters (chenge 44 to get length in meters for your case)
        total_time_passed = curr_frame_num - curr_frame_no_list[0]
        scale_real_time_passed = total_time_passed * fps  # get the elapsed total time for a vehicle to pass through ROI area (24 = fps)
        if scale_real_time_passed != 0:
            speed = scale_real_length / scale_real_time_passed / scale_constant  # performing manual scaling because we have not performed camera calibration
            speed_kmh = speed * 3.6  # use reference constant to get vehicle speed prediction in kilometer unit
            curr_frame_no_list.insert(0, curr_frame_num)
            prev_bottom.insert(0, bottom)
    return (direction, speed_kmh, is_vehicle_detected, update_csv)



def predict_speed_odd(top,bottom,right,left,curr_frame_num,crop_img,roi_position):
    
    speed = 'n.a.'  # means not available, it is just initialization
    direction = 'n.a.'  # means not available, it is just initialization
    scale_constant = 1  # manual scaling because we did not performed camera calibration
    isInROI = True  # is the object that is inside Region Of Interest
    update_csv = False

    if left < 500:
        scale_constant = 1  # scale_constant is used for manual scaling because we did not performed camera calibration
    elif left > 500 and left < 640:
        scale_constant = 2  # scale_constant is used for manual scaling because we did not performed camera calibration
    else:
        isInROI = False

    if len(prev_bottom) != 0 and left - lft_car[0] > 0 and 195 \
        < prev_bottom[0] and prev_bottom[0] < 240 \
        and roi_position < left and (curr_frame_num - curr_frame_no_lst_2[0])>24:
        is_vehicle_detected.insert(0, 1)
        update_csv = True
        image_saver.save_image(crop_img)  # save detected vehicle image
        curr_frame_no_lst_2.insert(0, curr_frame_num)
    # for debugging
    # print("prev_bottom[0]: " + str(prev_bottom[0]))
    # print("bottom: " + str(bottom))
    if left > lft_car[0]:
        direction = 'right'
    else:
        direction = 'left'

    if isInROI:
        pixel_length = bottom - prev_bottom[0]
        scale_real_length = pixel_length * 44  # multiplied by 44 to convert pixel length to real length in meters (chenge 44 to get length in meters for your case)
        total_time_passed = curr_frame_num - curr_frame_no_list[0]
        scale_real_time_passed = total_time_passed * 24  # get the elapsed total time for a vehicle to pass through ROI area (24 = fps)
        if scale_real_time_passed != 0:
            speed = scale_real_length / scale_real_time_passed / scale_constant  # performing manual scaling because we have not performed camera calibration
            speed = speed / 6 * 40  # use reference constant to get vehicle speed prediction in kilometer unit
            curr_frame_no_list.insert(0, curr_frame_num)
            prev_bottom.insert(0, bottom)
            lft_car.insert(0, left)
    return (direction, speed, is_vehicle_detected, update_csv)



def predict_speed__(top,bottom,right,left,curr_frame_num,crop_img,roi_position):
    speed = 'n.a.'  # means not available, it is just initialization
    direction = 'n.a.'  # means not available, it is just initialization
    scale_constant = 1  # manual scaling because we did not performed camera calibration
    isInROI = True  # is the object that is inside Region Of Interest
    update_csv = False

    # 
    # (0,0)       ______________\ + X (1280)              
    #            |              /
    #            |
    #            |
    # (1050) + Y \/
    #
    # Camera is facing the road. Farther out things would be smaller
    #                            Closer to the camera mean object will appear larger.
    if   bottom < 500:
        scale_constant = 1  # Farther away ---> Smaller multiplier as car will be smaller as rows go from top to bottom
    elif bottom > 500 and bottom < 640:
        scale_constant = 2  # Top > Center ---> Larger closer to camera
    #else:
    #    isInROI = False
    scale_constant = 1
    
    if  len(prev_bottom)   != 0  and bottom - prev_bottom[0] > 0     and 195  < prev_bottom[0]  and \
            prev_bottom[0] < 240 and roi_position < bottom + 100 and  (curr_frame_num - curr_frame_no_lst_2[0]) > 24:
            
        is_vehicle_detected.insert(0, 1)
        update_csv = True
        image_saver.save_image(crop_img)  # save detected vehicle image
        curr_frame_no_lst_2.insert(0, curr_frame_num)
    # for debugging
    # print("prev_bottom[0]: " + str(prev_bottom[0]))
    # print("bottom: " + str(bottom))
    if bottom > prev_bottom[0]:
        direction = 'down'
    else:
        direction = 'up'

    if isInROI:
        pixel_length = bottom - prev_bottom[0]
        scale_real_length = pixel_length * 44  # multiplied by 44 to convert pixel length to real length in meters (chenge 44 to get length in meters for your case)
        total_time_passed = curr_frame_num - curr_frame_no_list[0]
        scale_real_time_passed = total_time_passed * fps  # get the elapsed total time for a vehicle to pass through ROI area (24 = fps)
        if scale_real_time_passed != 0:
            speed = scale_real_length / scale_real_time_passed / scale_constant  # performing manual scaling because we have not performed camera calibration
            speed = speed / 6 * 40  # use reference constant to get vehicle speed prediction in kilometer unit
            curr_frame_no_list.insert(0, curr_frame_num)
            prev_bottom.insert(0, bottom)
    return (direction, speed, is_vehicle_detected, update_csv)
