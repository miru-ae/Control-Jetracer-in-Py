import torch
import torchvision

CATEGORIES = ['apex']

device = torch.device('cuda')
model = torchvision.models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(512, 2 * len(CATEGORIES))
model = model.cuda().eval().half()

model.load_state_dict(torch.load('road_following_model.pth'))

from torch2trt import torch2trt

data = torch.zeros((1, 3, 224, 224)).cuda().half()

model_trt = torch2trt(model, [data], fp16_mode=True)

torch.save(model_trt.state_dict(), 'road_following_model_trt.pth')


import torch
from torch2trt import TRTModule

model_trt = TRTModule()
model_trt.load_state_dict(torch.load('road_following_model_trt.pth'))


from jetracer.nvidia_racecar import NvidiaRacecar

car = NvidiaRacecar()

from jetcam.csi_camera import CSICamera

camera = CSICamera(width=224, height=224, capture_fps=65)

from utils import preprocess
import numpy as np

STEERING_GAIN = 1.3
STEERING_BIAS = 0.4

car.throttle = 0.2
car.throttle_gain = 0.2
car.steering = 0
car.steering_gain = -0.5
car.steering_offset = 0

# back wheel setting
# car.throttle means the maximum speed of back wheel
# car.throttle_gain means the maximum limitation speed of back wheel

# front wheel setting
# car.steering_gain means the maximum rotation of front wheel
# car.steering_offset means the init shifting of front wheel

while True:
    image = camera.read()
    image = preprocess(image).half()
    output = model_trt(image).detach().cpu().numpy().flatten()
    x = float(output[0])
    pid_steering = x * STEERING_GAIN + STEERING_BIAS
    print("[OUTPUT] AI-Output:{} PID-Steering:{}".format(x,pid_steering))
    car.steering = pid_steering