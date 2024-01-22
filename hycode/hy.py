# List attached devices
#$ v4l2-ctl --list-devices

import cv2
import numpy as numpy

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv  flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=1"
         % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def main():
    window_title = "JS CSI Camera"

     # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)

                    #import crop image
                    crop_img = frame[250:1920, 0:1080] #cut half

                    #change color
                    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                    #blur effect
                    blur = cv2.GaussianBlur(gray, (5,5), 0)
                    #cv2.imshow('copy+gray+blur', blur)

                    #change value for better contrast
                    ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
                    #cv2.imshow('thresh1', thresh1)
                    
                    mask = cv2.erode(thresh1, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)
                    cv2.imshow('mask', mask)

                    contours, hierachy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

                    if len(contours) >0:
                        # Sorting lines with area and save top 3 lines
                        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
                        c1, c2, c3 = sorted_contours[:3]
                        
                        #slope
                        point11 = c1[0][0]
                        point12 = c1[-1][0]
                        point21 = c2[0][0]
                        point22 = c2[-1][0]
                        point31 = c3[0][0]
                        point32 = c3[-1][0]
                        slope1 = (point12[1] - point11[1]) / (point12[0] - point11[0])
                        slope2 = (point22[1] - point21[1]) / (point22[0] - point21[0])
                        slope3 = (point32[1] - point31[1]) / (point32[0] - point31[0])

                        weighted_slope=(5*slope1+3*slope2+slope3)/9
                       
                        print(weighted_slope)
                        

                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == '__main__' :
    main()