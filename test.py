
import cv2
import numpy as np

# Open the video file
cap = cv2.VideoCapture(r'input\a.mkv')

# Check if the video file was opened successfully
if not cap.isOpened():
    print('Error opening video file')

# Loop through the frames in the video
while cap.isOpened():
    # Read the next frame
    ret, img = cap.read()
    
    gray = cv2.cvtColor(img, 0)
    cv2.imshow('img', gray)

    #read haarcascade
    #plates_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml') #does not give me error, but result is not correct
    #plates_cascade = cv2.CascadeClassifier('haarcascade_licence_plate_rus_16stages.xml') #gives me error
    # Load the pre-trained cascade classifier for license plate detection
    cascade_path = cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml'
    plates_cascade = cv2.CascadeClassifier(cascade_path)
    
    plates = plates_cascade.detectMultiScale(gray, 1.2, 4)


    for (x,y,w,h) in plates:

        #detect plate with rectangle
        #rec. start point (x,y), rec. end point (x+w, y+h), blue color(255,0,0), line width 1

        plates_rec = cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)        
        #cv2.putText(plates_rec, 'Text', (x, y-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        gray_plates = gray[y:y+h, x:x+w]
        color_plates = img[y:y+h, x:x+w]

        #cv2.imshow('img', gray_plates)
        #cv2.waitKey(0)

        height, width, chanel = gray_plates.shape
        print(height, width)

    cv2.imshow('img', img)
    cv2.waitKey(1)
    print('Number of detected licence plates:', len(plates))