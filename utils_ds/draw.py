import numpy as np
import cv2

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


def draw_boxes(img, bbox, identities=None, offset=(0,0)):
    for i,box in enumerate(bbox):
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0    
        color = compute_color_for_labels(id)
        label = '{}{:d}'.format("", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2 , 2)[0]
        cv2.rectangle(img,(x1, y1),(x2,y2),color,3)
        cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
        cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)
    return img

def putText(img, text, font=cv2.FONT_HERSHEY_PLAIN, font_scale=1, color=(0, 0, 255), thickness=1, margin=10, pos='top-right', bg_color=None):
    """
    Displays text on an image with an adjustable margin.

    Parameters:
    img (numpy.ndarray): The input image.
    text (str): The text to display.
    font (int): The font type to use (default: cv2.FONT_HERSHEY_PLAIN).
    font_scale (float): The font scale factor (default: 1).
    color (tuple): The text color in BGR format (default: (0, 0, 255)).
    thickness (int): The thickness of the text (default: 1).
    margin (int): The margin between the text and the edge of the image (default: 10).
    pos (str): The position of the text. Can be 'top-left', 'top-right', 'bottom-left', or 'bottom-right' (default: 'top-right').
    """

    # Get the size of the text
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness=thickness)

    # Define the position of the text
    if pos == 'top-left':
        text_x = margin
        text_y = margin + text_size[1]
    elif pos == 'top-right':
        text_x = img.shape[1] - text_size[0] - margin
        text_y = margin + text_size[1]
    elif pos == 'bottom-left':
        text_x = margin
        text_y = img.shape[0] - margin
    elif pos == 'bottom-right':
        text_x = img.shape[1] - text_size[0] - margin
        text_y = img.shape[0] - margin
    else:
        raise ValueError("Invalid position. Position should be 'top-left', 'top-right', 'bottom-left', or 'bottom-right'.")
    
    # Draw the text with or without background color
    if bg_color:
        # Calculate the background rectangle size and position
        bg_rect_width = text_size[0] + margin * 2
        bg_rect_height = text_size[1] + margin * 2
        bg_rect_x = text_x - margin
        bg_rect_y = text_y - text_size[1] - margin

        # Draw the background rectangle
        cv2.rectangle(img, (bg_rect_x, bg_rect_y), (bg_rect_x + bg_rect_width, bg_rect_y + bg_rect_height), bg_color, thickness=-1)

    # Draw the text on the image
    cv2.putText(img, text, (text_x, text_y), font, font_scale, color, thickness)


if __name__ == '__main__':
    for i in range(82):
        print(compute_color_for_labels(i))
