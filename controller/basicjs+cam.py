from jetracer.nvidia_racecar import NvidiaRacecar

import cv2 
import threading

# Create an NvidiaRacecar instance
car = NvidiaRacecar()

# Default throttle value to stop the car
default_throttle = 0.33
car.throttle = default_throttle
car.steering = 0.0
car.throttle_gain = 0.5

   
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



def control_car():
    running = True
    while running:
        show_camera()
        # Get user input
        user_input = input("Enter command (w: forward, s: backward, a: left, d: right, q: brake, e: stop): ")
        

        if user_input.lower() == 'e':
            running = False
        else:
            # Adjust the car controls based on user input
            if 'w' in user_input:
                car.throttle += 0.010
            elif 's' in user_input:
                car.throttle -= 0.030
            # else:
            #     car.throttle = default_throttle

            elif 'a' in user_input:
                car.throttle = car.throttle
                car.steering -= 0.03
                
            elif 'd' in user_input:
                car.throttle = car.throttle
                car.steering += 0.03
                #car.throttle = car.throttle
            else:
                 car.throttle = default_throttle

            if 'q' in user_input:
                Gear = True
                while Gear :
                    car.throttle = default_throttle
                    car.steering = 0.0
                    gear_shift = input("Change Gear: (i: forward, k: backward, p: park): ")
                    if 'i' in gear_shift:
                        car.throttle += 0.2
                        Gear = False
                    elif 'k' in gear_shift:
                        #car.throttle = 0.25
                        #car.throttle = -0.4
                        Gear = False
                    elif 'p' in gear_shift:
                        car.throttle = 0.25
                        print("Park the car")
                        Gear = False


            # Limit the controls to the range [-1.0, 1.0]
            car.steering = max(-1.0, min(1.0, car.steering))
            car.throttle = max(-1.0, min(1.0, car.throttle))

            # Display current controls
            print(f"Throttle: {car.throttle:.2f}, Steering: {car.steering:.3f}")
            


# Run the control function
control_car()
# if __name__ == "__main__":
#     show_camera()


# def gstreamer_pipeline(
#     sensor_id=0,
#     capture_width=1920,
#     capture_height=1080,
#     display_width=960,
#     display_height=540,
#     framerate=30,
#     flip_method=0,
# ):
#     return (
#         "nvarguscamerasrc sensor-id=%d ! "
#         "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
#         "nvvidconv  flip-method=%d ! "
#         "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
#         "videoconvert ! "
#         "video/x-raw, format=(string)BGR ! appsink drop=1"
#          % (
#             sensor_id,
#             capture_width,
#             capture_height,
#             framerate,
#             flip_method,
#             display_width,
#             display_height,
#         )
#     )


# def show_camera():
#     window_title = "CSI Camera"

#     # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
#     print(gstreamer_pipeline(flip_method=0))
#     video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
#     if video_capture.isOpened():
#         try:
#             window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
#             while True:
#                 ret_val, frame = video_capture.read()
#                 # Check to see if the user closed the window
#                 # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
#                 # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
#                 if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
#                     cv2.imshow(window_title, frame)
#                 else:
#                     break 
#                 keyCode = cv2.waitKey(10) & 0xFF
#                 # Stop the program on the ESC key or 'q'
#                 if keyCode == 27 or keyCode == ord('q'):
#                     break
#         finally:
#             video_capture.release()
#             cv2.destroyAllWindows()
#     else:
#         print("Error: Unable to open camera")


# if __name__ == "__main__":
#     show_camera()