import cv2
import numpy as np
from jetracer.nvidia_racecar import NvidiaRacecar

# Create an NvidiaRacecar instance
car = NvidiaRacecar()

# GStreamer pipeline for CSI camera
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

# Function to detect lanes and control steering
def detect_and_control(frame):
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

# Function to define region of interest
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
        #steering_range = 45.0  # Adjust this value based on your car's steering range
        steering_range = 1.0
        steering_angle = np.clip(average_angle, -steering_range, steering_range)

        return steering_angle
    else:
        # If no lines were detected, return a default steering angle
        return 0.0


# Main function
def main():
    # Create a video capture object for the CSI camera
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    try:
        while True:
            # Read a frame from the camera
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame")
                break

            # Detect lanes and control steering
            processed_frame = detect_and_control(frame)

            # Display the processed frame
            cv2.imshow("Lane Detection", processed_frame)

            # Check for user input to exit the loop
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        # Release the camera and close all windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Run the main function
    main()
