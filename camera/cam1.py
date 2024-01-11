import threading
import cv2
import pygame
from pygame.locals import *

# Pygame 초기화
pygame.init()

# Pygame 창 설정
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pygame_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pygame 창')

# Pygame 창을 실행할 함수 정의
def run_pygame_window():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pygame_window.fill((255, 255, 255))
        pygame.display.flip()

# OpenCV 창을 실행할 함수 정의
def run_opencv_window():
    cv2.namedWindow('OpenCV 창')
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('OpenCV 창', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# 스레드 생성 및 실행
pygame_thread = threading.Thread(target=run_pygame_window)
opencv_thread = threading.Thread(target=run_opencv_window)

pygame_thread.start()
opencv_thread.start()
