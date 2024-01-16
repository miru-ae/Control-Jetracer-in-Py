import cv2
import numpy as np

# GStreamer 파이프라인을 생성하여 CSI 카메라에서 영상을 캡처합니다.
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

# 차선을 감지하여 시각화하는 함수입니다.
# def detect_lane(frame):
#     # 이미지를 그레이스케일로 변환합니다.
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # 가우시안 블러로 이미지를 블러 처리합니다.
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     # 캐니 엣지 감지를 사용하여 엣지를 검출합니다.
#     edges = cv2.Canny(blurred, 50, 150)

#     # 관심 영역을 정의합니다.
#     mask = np.zeros_like(edges)
#     height, width = edges.shape
#     polygon = np.array([[
#         (0, height),
#         (width, height),
#         (width // 2, height // 2)
#     ]], np.int32)
#     cv2.fillPoly(mask, polygon, 255)
#     masked_edges = cv2.bitwise_and(edges, mask)

#     # 허프 변환을 사용하여 직선을 감지합니다.
#     lines = cv2.HoughLinesP(masked_edges, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)

#     # 검출된 직선을 이미지에 그립니다.
#     for line in lines:
#         for x1, y1, x2, y2 in line:
#             cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

#     return frame

def detect_lane(frame):
    # 이미지를 그레이스케일로 변환합니다.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 가우시안 블러로 이미지를 블러 처리합니다.
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 캐니 엣지 감지를 사용하여 엣지를 검출합니다.
    edges = cv2.Canny(blurred, 50, 150)

    # 관심 영역을 정의합니다.
    mask = np.zeros_like(edges)
    height, width = edges.shape
    polygon = np.array([[
        (0, height),
        (width, height),
        (width // 2, height // 2)
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # 허프 변환을 사용하여 직선을 감지합니다.
    lines = cv2.HoughLinesP(masked_edges, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)

    if lines is not None:  # lines가 None이 아닌지 확인합니다.
        # 검출된 직선을 이미지에 그립니다.
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return frame


# CSI 카메라로부터 영상을 캡처하여 차선 감지 함수를 호출하는 메인 함수입니다.
def main():
    # CSI 카메라에서 영상을 캡처합니다.
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    try:
        while True:
            # 카메라로부터 프레임을 읽습니다.
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame")
                break

            # 차선 감지 함수를 호출하여 시각화된 프레임을 받아옵니다.
            processed_frame = detect_lane(frame)

            # 시각화된 프레임을 화면에 출력합니다.
            cv2.imshow("Lane Detection", processed_frame)

            # ESC 키를 누르면 프로그램을 종료합니다.
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        # 카메라를 해제하고 윈도우를 모두 닫습니다.
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # main 함수를 실행합니다.
    main()
