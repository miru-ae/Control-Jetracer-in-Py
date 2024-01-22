# List attached devices
#$ v4l2-ctl --list-devices
from jetracer.nvidia_racecar import NvidiaRacecar
car = NvidiaRacecar()
car.steering = 0.0
car.throttle = 0.36
car.throttle_gain = 0.7

import cv2
import numpy as numpy
import time

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
    window_title = "CSI Camera"

     # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    #print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            i = 0
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                _, image = video_capture.read()
                image = cv2.flip(image, -1)  # Apply additional flipping if needed

                # Convert the image to YUV format
                yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
                #yuv_image = cv2.GaussianBlur(image, (3,3), 0)
                yuv_image = cv2.resize(image, (200,66))

                # Save the YUV image to a file with a unique filename
                filepath = "/home/miru/miru/kmwcode/dataset/data"
                cv2.imwrite("%s_%05d_%.3f_%.3f.png" %(filepath, i, car.steering, car.throttle), yuv_image)
                i += 1  # Increment the image index for the next image

                time.sleep(1.0)

                ret_val, frame = video_capture.read()
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)

                    #import crop image
                    crop_img = frame[260:1920, 0:1080] #cut half

                    #change color
                    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                    #blur effect
                    blur = cv2.GaussianBlur(gray, (5,5), 0)
                    #cv2.imshow('copy+gray+blur', blur)

                    #change value for better contrast
                    ret, thresh1 = cv2.threshold(blur, 105, 255, cv2.THRESH_BINARY_INV)
                    #cv2.imshow('thresh1', thresh1)
                    
                    mask = cv2.erode(thresh1, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)
                    cv2.imshow('mask', mask)

                    contours, hierachy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

                    if len(contours) >0:
                        c = max(contours, key=cv2.contourArea)
                        M = cv2.moments(c)

                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])

                        # cv2.line(crop_img, (cx,0), (cx, 1080), (255,0,0),1)
                        # cv2.line(crop_img, (0,cy), (1920, cy), (255,0,0),1)
                        # cv2.drawContours(crop_img, contours,-1, (0,255,0), 1)

                        print(cx) #left:150~500 // right:500~850

                        if cx >= 120 and cx <=450:
                            print("Turn Left!")
                            car.steering -= 0.4
                        elif cx >= 550 and cx <=850:
                            print("Turn Right")
                            car.steering += 0.4
                        else:
                            print("go")
                            car.steering = 0.0

                        

                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    car.throttle = 0.2
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == '__main__' :
    main()
