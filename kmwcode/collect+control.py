import pygame
from pygame.locals import *
import cv2
import time
import threading

from jetracer.nvidia_racecar import NvidiaRacecar

pygame.init()

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


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,  # Modify this parameter for different flipping
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,  # Pass the flip_method parameter here
            display_width,
            display_height,
        )
    )

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
        dPressed = keys_pressed[K_d]
        rPressed = keys_pressed[K_r]

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
            text += "Brake "

        lines = [
            "",
            "Throttle: {:.3f}".format(car.throttle),
            "Steering: {:.3f}".format(car.steering)
        ]
        rendered_lines = [font.render(line, True, (255, 255, 255)) for line in lines]

        # Draw the text onto the window
        for i, rendered_line in enumerate(rendered_lines):
            windowSurface.blit(rendered_line, (10, 100 + i * 36)) 

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
            if car.steering != 0.0:    
                car.steering = 0.0
        elif moveForward:
            car.throttle += 0.0001
        elif moveBack:
            car.throttle -= 0.0001

        if qPressed:
            car.throttle = default_throttle
        elif dPressed:
            car.throttle = 0.3
        elif rPressed:
            car.throttle = 0.0
        
        # Limit the steering to the range [-1.0, 1.0]
        car.steering = max(-1.0, min(1.0, car.steering))
        car.throttle = max(-1.0, min(1.0, car.throttle))

def capture_image():
    flip_method_to_test = 2  # Replace with the flip_method value to test
    camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=flip_method_to_test), cv2.CAP_GSTREAMER)
    if not camera.isOpened():
        print("Error: Unable to open camera")
        return

    i = 0  # Initialize the image index

    while True:
        # Capture frames from the camera
        _, image = camera.read()
        image = cv2.flip(image, -1)  # Apply additional flipping if needed

        # Convert the image to YUV format
        yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        yuv_image = cv2.resize(yuv_image, (200, 66))  # Resize the YUV image if needed

        # Display the original image
        cv2.imshow('Original', image)

        # Save the YUV image to a file with a unique filename
        filepath = "/home/miru/miru/kmwcode/dataset/data"
        cv2.imwrite("%s_%05d_%.3f_%.3f.png" %(filepath, i, car.steering, car.throttle), yuv_image)
        i += 1  # Increment the image index for the next image

        time.sleep(1.0)
        
        keyValue = cv2.waitKey(10)
        if keyValue == 27:  # ESC key
            break
        elif keyValue == ord('q'):
            print("Break")
        elif keyValue == 82:
            print("up")
        elif keyValue == 84:
            print("down")
        elif keyValue == 83:
            print("right")
        elif keyValue == 81:
            print("left")

    # Release the camera and close the OpenCV windows
    camera.release()
    cv2.destroyAllWindows() 

# Create a thread for capturing images from the camera
camera_thread = threading.Thread(target=capture_image)

# Start the camera thread
camera_thread.start()

# Run the control function
control_car()

# Run the control function
control_car()
