import pygame
from pygame.locals import *

from jetracer.nvidia_racecar import NvidiaRacecar

# Initialize Pygame
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
        moveLeft = keys_pressed[K_LEFT] or keys_pressed[K_a]
        moveRight = keys_pressed[K_RIGHT] or keys_pressed[K_d]
        spacePressed = keys_pressed[K_SPACE]
        moveForward = keys_pressed[K_UP] or keys_pressed[K_w]
        moveBack = keys_pressed[K_DOWN] or keys_pressed[K_s]
        qPressed = keys_pressed[K_q]

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
        # text += f"Throttle: {car.throttle:.2f}"  # Include the throttle value
        # text += f"\nSteering: {car.steering:.2f}"

        lines = [
            "",
            "Throttle: {:.2f}".format(car.throttle),
            "Steering: {:.2f}".format(car.steering)
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
            car.steering = -1.0
        elif moveRight:
            car.steering = 1.0
        # Gradually adjust the steering to 0.0 if the spacebar is pressed
        if spacePressed:
            if car.steering != 0.0:    
                car.steering = 0.0
        elif moveForward:
            car.throttle += 0.0005
        elif moveBack:
            car.throttle -= 0.0009
        if qPressed:
            car.throttle = default_throttle
        
        # Limit the steering to the range [-1.0, 1.0]
        car.steering = max(-1.0, min(1.0, car.steering))
        car.throttle = max(-1.0, min(1.0, car.throttle))

# Run the control function
control_car()