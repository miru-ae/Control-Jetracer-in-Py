import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from pygame.locals import *

from jetracer.nvidia_racecar import NvidiaRacecar

# Initialize Pygame
pygame.init()

# Create an NvidiaRacecar instance
car = NvidiaRacecar()

# Default throttle value to stop the car
default_throttle = 0.2
car.throttle = default_throttle
car.steering = 0.0

def control_car():
    moveForward = False
    moveBack = False
    moveLeft = False
    moveRight = False
    spacePressed = False
    qPressed = False

    running = True
    clock = pygame.time.Clock()

    # Create a small display for smooth keyboard input
    WINDOWWIDTH = 600
    WINDOWHEIGHT = 600
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 60 | pygame.NOFRAME)
    pygame.display.set_caption('DashBoard')

    while running:
        keys_pressed = pygame.key.get_pressed()

        # Update the key flags based on the keys that are currently pressed
        moveLeft = keys_pressed[K_LEFT] or keys_pressed[K_a]
        moveRight = keys_pressed[K_RIGHT] or keys_pressed[K_d]
        spacePressed = keys_pressed[K_SPACE]
        moveForward = keys_pressed[K_UP] or keys_pressed[K_w]
        moveBack = keys_pressed[K_DOWN] or keys_pressed[K_s]
        qPressed = keys_pressed[K_q]

        # Adjust the controls based on the key states
        if moveLeft:
            car.steering -= 0.003
        elif moveRight:
            car.steering += 0.003

        if spacePressed:
            if car.steering > 0.0:
                car.steering -= 0.002
            elif car.steering < 0.0:
                car.steering += 0.002
        elif moveForward:
            car.throttle += 0.0005
        elif moveBack:
            car.throttle -= 0.0009

        if qPressed:
            car.throttle = default_throttle

        # Limit the controls to the range [-1.0, 1.0]
        car.steering = max(-1.0, min(1.0, car.steering))
        car.throttle = max(-1.0, min(1.0, car.throttle))

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                running = False

        # Display current controls
        print(f"Throttle: {car.throttle:.2f}, Steering: {car.steering:.3f}")

        clock.tick(60)  # Cap the frame rate at 60 FPS

# Run the control function
control_car()

# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2 
#print(cv.__version__)
""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

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
        # "nvarguscamerasrc sensor_id=0 !"
        # "video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1 !"
        # "nvvidconv flip-method=0 !" 
        # "video/x-raw,width=960, height=540, format=(string)BGRx!"
        # "nvvidconv !"
        # "nvegltransform !"
        # "nveglglessink -e"
        # "videoconvert ! "
        # "video/x-raw, format=(string)BGR ! appsink drop=1"

        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        # "!" nvvideoconvert
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


def show_camera():
    window_title = "CSI Camera"

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


if __name__ == "__main__":
    show_camera()
