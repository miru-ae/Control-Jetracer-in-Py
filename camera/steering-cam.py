import cv2
import numpy as np
from jetracer.nvidia_racecar import NvidiaRacecar

# Create an NvidiaRacecar instance
car = NvidiaRacecar()

# Set up the camera
camera_id = "/dev/video1"
video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

# Function to detect and calculate steering angle based on lines
# def detect_and_steering(frame):
#     # Your line detection code here...
#     # For example:
#     # lines = detect_lines(frame)
#      # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Apply Gaussian blur to reduce noise
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#     # Apply Canny edge detection
#     edges = cv2.Canny(blurred, 50, 150)

#     # Define region of interest (ROI)
#     height, width = frame.shape[:2]
    
#     vertices = np.array([[(0, height), (width / 2, height / 2), (width, height)]], dtype=np.int32)
    
#     masked_edges = region_of_interest(edges, vertices)

#     # Apply Hough transform to detect lines
#     lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=100)
#     # Calculate steering angle based on the detected lines
#     steering_angle = calculate_steering_angle(lines)

#     # Set the steering angle of the car
#     car.steering = steering_angle

def detect_and_steering(frame):
    # Your line detection code here...
    # For example:
    # lines = detect_lines(frame)
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Define region of interest (ROI)
    height, width = frame.shape[:2]
    vertices = np.array([[(0, height), (width / 2, height / 2), (width, height)]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)

    # Apply Hough transform to detect lines
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=100)
    
    if lines is not None:
        # Calculate the steering angle based on the detected lines and image width
        steering_angle = calculate_steering_angle(lines, width)

        # Set the steering angle of the car
        car.steering = -steering_angle

        # Visualize detected lanes on the frame
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return frame

    # Calculate the steering angle based on the detected lines and image width
    #steering_angle = calculate_steering_angle(lines, width)

    # Set the steering angle of the car
    #car.steering = steering_angle

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def calculate_steering_angle(lines, image_width):
    if lines is not None:
        # Initialize variables for accumulating angles and counts
        total_angle = 0.0
        total_lines = 0

        # Iterate over the detected line segments
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Calculate the angle of the line segment
            angle = np.arctan2(y2 - y1, x2 - x1)

            # Convert the angle from radians to degrees
            angle_degrees = np.degrees(angle)

            # Accumulate the angle
            total_angle += angle_degrees
            total_lines += 1

        # Calculate the average angle
        average_angle = total_angle / total_lines if total_lines > 0 else 0.0

        # Map the average angle to the steering range of your car
        # For example, if your car has a steering range of [-45, 45] degrees,
        # you can map the average angle to this range
        steering_range = 45.0  # Adjust this value based on your car's steering range
        steering_angle = np.clip(average_angle, -steering_range, steering_range)

        return steering_angle
    else:
        # If no lines were detected, return a default steering angle
        return 0.0

# Main loop for processing frames
while True:
    ret_val, frame = video_capture.read()
    if not ret_val:
        break

    # Perform line detection and set steering angle
    detect_and_steering(frame)

    # Show the frame (optional)
    cv2.imshow('Lane Detection', frame)

    # Check for user input to exit the loop
    keyCode = cv2.waitKey(10) & 0xFF
    if keyCode == 27 or keyCode == ord('q'):
        break

# Release the camera and close all windows
video_capture.release()
cv2.destroyAllWindows()
