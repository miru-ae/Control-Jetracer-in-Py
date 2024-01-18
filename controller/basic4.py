import gradio as gr
from jetracer.nvidia_racecar import NvidiaRacecar

# Create an NvidiaRacecar instance
car = NvidiaRacecar()

# Default throttle value to stop the car
default_throttle = 0.2
car.throttle = default_throttle
car.steering = 0.0

# Define the function to control the car
def control_car(left, right, up, down, space, q, drive, reverse):
    global car

    # Adjust the steering based on the button states
    if left:
        car.steering -= 0.05
    elif right:
        car.steering += 0.05

    # Gradually adjust the steering to 0.0 if the Space button is pressed
    if space:
        if car.steering != 0.0:
            car.steering = 0.0

    if up:
        car.throttle += 0.002
    elif down:
        car.throttle -= 0.002

    if q:
        car.throttle = default_throttle
        for i in range(20):
            car.throttle -= 0.0001

    if drive:
        car.throttle = 0.25

    if reverse:
        car.throttle = 0.00

    # Limit the steering to the range [-1.0, 1.0]
    car.steering = max(-1.0, min(1.0, car.steering))
    car.throttle = max(-1.0, min(1.0, car.throttle))

    # Render text to display the currently pressed buttons
    text = f"Throttle: {car.throttle:.2f}"  # Include the throttle value
    pressed_buttons = [btn for btn, state in zip(['Left', 'Right', 'Up', 'Down', 'Space', 'Q', 'Drive', 'Reverse'],
                                                  [left, right, up, down, space, q, drive, reverse]) if state]
    return f"Pressed Buttons: {', '.join(pressed_buttons)}\n{text}"

# Define Gradio interface with buttons
iface = gr.Interface(
    fn=control_car,
    inputs=[
        gr.Button("Left"),
        gr.Button("Right"),
        gr.Button("Up"),
        gr.Button("Down"),
        gr.Button("Space"),
        gr.Button("Q"),
        gr.Button("Drive"),
        gr.Button("Reverse"),
    ],
    outputs="text",
)

# Launch the Gradio interface
iface.launch()
