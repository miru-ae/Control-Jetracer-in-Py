import cv2
import time

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

def main():
    # Try different flip_method values (0, 1, 2, 3) to see which one resolves the flipping issue
    flip_method_to_test = 2  # Replace with the flip_method value to test
    camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=flip_method_to_test), cv2.CAP_GSTREAMER)
    if not camera.isOpened():
        print("Error: Unable to open camera")
        return

    #filepath = "/Home/miru/kmwcode/dataset/test"  # Define the filepath for saving images
    i = 0  # Initialize the image index

    while True:
        _, image = camera.read()
        image = cv2.flip(image, -1)  # Apply additional flipping if needed
        cv2.imshow('Original', image)

        # Convert the image to YUV format
        yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        yuv_image = cv2.GaussianBlur(image, (3,3), 0)
        yuv_image = cv2.resize(image, (200,66))

        # Save the YUV image to a file with a unique filename
        cv2.imwrite("/home/miru/miru/kmwcode/dataset/test_%05d.png" % i, yuv_image)
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

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
