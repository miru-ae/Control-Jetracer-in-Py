import gradio as gr
import cv2

def webcam():
    camera_id = "/dev/video2"
    video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

    if not video_capture.isOpened():
        return None

    _, frame = video_capture.read()

    video_capture.release()
    return frame

iface = gr.Interface(
    fn=webcam,
    inputs=None,
    outputs="image",
)

if __name__ == "__main__":
    iface.launch(share=True)
