import pygame
import cv2
from pygame.locals import *

from jetracer.nvidia_racecar import NvidiaRacecar

# Initialize Pygame
pygame.init()

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

# Set up the font
font = pygame.font.SysFont(None, 72)

# Create a small display for smooth keyboard input
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 60)
pygame.display.set_caption('DashBoard')

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
    spacePressed = False  # Flag to track if spacebar is pressed
    qPressed = False

    running = True
    while running:
        windowSurface.fill((0, 0, 0))  # Clear the window
        keys_pressed = pygame.key.get_pressed()  # Get the currently pressed keys
        
        # Update the key flags based on the keys that are currently pressed
        moveLeft = keys_pressed[K_LEFT]
        moveRight = keys_pressed[K_RIGHT]
        spacePressed = keys_pressed[K_SPACE]
        moveForward = keys_pressed[K_UP]
        moveBack = keys_pressed[K_DOWN]
        qPressed = keys_pressed[K_q]
        Drive = keys_pressed[K_d]
        Reverse = keys_pressed[K_r]

        # Render text to display the currently pressed keys
        text = ""

        if moveLeft:
            text += "Left "
        if moveRight:
            text += "Right "
        if spacePressed:
            text += "Space "
        if moveForward:
            text += "Up "
        if moveBack:
            text += "Down "
        if qPressed:
            text += "Brake"
        text += f"Throttle: {car.throttle:.2f}"  # Include the throttle value


        # Create a text surface
        text_surface = font.render(text, True, (255, 255, 255))

        # Draw the text surface onto the window
        windowSurface.blit(text_surface, (10, 100))

        # Update the display
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                car.throttle = default_throttle
                pygame.quit()
                running = False

        # Adjust the steering based on the key states
        if moveLeft:
            car.steering -= 0.003
        elif moveRight:
            car.steering += 0.003
        # Gradually adjust the steering to 0.0 if the spacebar is pressed
        if spacePressed:
            if car.steering > 0.0:
                car.steering -= 0.002
            elif car.steering < 0.0:
                car.steering += 0.002
        elif moveForward:
            car.throttle += 0.0005
        elif moveBack:           
            car.throttle -= 0.0009
        elif qPressed:
            car.throttle = default_throttle
            for i in range(20):
                car.throttle -= 0.0001
        elif Drive:
            car.throttle = 0.25
        elif Reverse:
            car.throttle = 0.00
        
        # Limit the steering to the range [-1.0, 1.0]
        car.steering = max(-1.0, min(1.0, car.steering))
        car.throttle = max(-1.0, min(1.0, car.throttle))

# Run the control function
control_car()

