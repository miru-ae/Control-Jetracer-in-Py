from jetracer.nvidia_racecar import NvidiaRacecar

# Create an NvidiaRacecar instance
car = NvidiaRacecar()

print('\ncar steering')

# Set the steering attribute to 0.3
car.steering = 0.5


# Print the default steering gain and offset
print(car.steering_gain)
print(car.steering_offset)

# Set the throttle attribute to 0.0
car.throttle = 0.2


# Set the throttle gain to 0.5
car.throttle_gain = 0.8

# Print the default throttle gain
print('\ncar throttle')
print(car.throttle)
print(car.throttle_gain)

