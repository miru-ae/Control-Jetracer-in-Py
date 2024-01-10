from jetracer.nvidia_racecar import NvidiaRacecar

# Create an NvidiaRacecar instance
car = NvidiaRacecar()

# Default throttle value to stop the car
default_throttle = 0.33
car.throttle = default_throttle
car.steering = 0.0
car.throttle_gain = 0.5

def control_car():
    running = True
    while running:
        # Get user input
        user_input = input("Enter command (w: forward, s: backward, a: left, d: right, q: brake, e: stop): ")
        

        if user_input.lower() == 'e':
            running = False
        else:
            # Adjust the car controls based on user input
            if 'w' in user_input:
                car.throttle += 0.010
            elif 's' in user_input:
                car.throttle -= 0.030
            # else:
            #     car.throttle = default_throttle

            elif 'a' in user_input:
                car.throttle = car.throttle
                car.steering -= 0.03
                
            elif 'd' in user_input:
                car.throttle = car.throttle
                car.steering += 0.03
                #car.throttle = car.throttle
            else:
                 car.throttle = default_throttle

            if 'q' in user_input:
                Gear = True
                while Gear :
                    car.throttle = default_throttle
                    car.steering = 0.0
                    gear_shift = input("Change Gear: (i: forward, k: backward, p: park): ")
                    if 'i' in gear_shift:
                        car.throttle += 0.2
                        Gear = False
                    elif 'k' in gear_shift:
                        #car.throttle = 0.25
                        #car.throttle = -0.4
                        Gear = False
                    elif 'p' in gear_shift:
                        car.throttle = 0.25
                        print("Park the car")
                        Gear = False


            # Limit the controls to the range [-1.0, 1.0]
            car.steering = max(-1.0, min(1.0, car.steering))
            car.throttle = max(-1.0, min(1.0, car.throttle))

            # Display current controls
            print(f"Throttle: {car.throttle:.2f}, Steering: {car.steering:.3f}")

# Run the control function
control_car()
