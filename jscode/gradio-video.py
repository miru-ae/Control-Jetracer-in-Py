import gradio as gr
from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames():
    camera_id = "/dev/video2"
    video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

    if not video_capture.isOpened():
        return None

    while True:
        _, frame = video_capture.read()

        if frame is None:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

iface = gr.Interface(
    fn=None,
    inputs=None,
    outputs=gr.Image(),  # Use gr.Image instead of gr.Video
)

if __name__ == "__main__":
    iface.launch(app)
