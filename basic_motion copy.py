#!/usr/bin/env python
# coding: utf-8

# Execute the following block of code by selecting it and clicking ``ctrl + enter`` to create an ``NvidiaRacecar`` class.  

# In[1]:


from jetracer.nvidia_racecar import NvidiaRacecar

car = NvidiaRacecar()


# The ``NvidiaRacecar`` implements the ``Racecar`` class, so it has two attributes ``throttle`` and ``steering``. 
# 
# We can assign values in the range ``[-1, 1]`` to these attributes.  Execute the following to set the steering to 0.4.
# 
# > If the car does not respond, it may still be in ``manual`` mode.  Flip the manual override switch on the RC transmitter.

# In[2]:


car.steering = 0.0

# The ``NvidiaRacecar`` class has two values ``steering_gain`` and ``steering_bias`` that can be used to calibrate the steering.
# 
# We can view the default values by executing the cells below.

# In[3]:


print(car.steering_gain)


# In[4]:


print(car.steering_offset)


# The final steering value is computed using the equation
# 
# $y = a \times x + b$
# 
# Where,
# 
# * $a$ is ``car.steering_gain``
# * $b$ is ``car.steering_offset``
# * $x$ is ``car.steering``
# * $y$ is the value written to the motor driver
# 
# You can adjust these values calibrate the car so that setting a value of ``0`` moves forward, and setting a value of ``1`` goes fully right, and ``-1`` fully left.

# To set the throttle of the car to ``0.2``, you can call the following.
# 
# > Give JetRacer lots of space to move, and be ready on the manual override, JetRacer is *fast*

# In[5]:


#car.throttle = 0.2


# The throttle also has a gain value that could be used to control the speed response.  The throttle output is computed as
# 
# $y = a \times x$
# 
# Where,
# 
# * $a$ is ``car.throttle_gain``
# * $x$ is ``car.throttle``
# * $y$ is the value written to the speed controller
# 
# Execute the following to print the default gain

# In[6]:


print(car.throttle_gain)


# Set the following to limit the throttle to half

# In[7]:


car.throttle_gain = 0.8


# Please note the throttle is directly mapped to the RC car.  When the car is stopped and a negative throttle is set, it will reverse.  If the car is moving forward and a negative throttle is set, it will brake.

# That's it for this notebook!


import csv
import time
import os
import numpy as np

data=[]

def tick():
    # Record the start time
    start_time = time.time()
    return start_time

def tock():
    #record the end time
    end_time = time.time()
    return end_time

def tick_tock(start_time,end_time):
    # Calculate the execution time
    tot_time = end_time - start_time
    # Print the result and execution time
    print(f"Execution time: {tot_time} seconds")

def lap_time(start_time,count):
    current_time = time.time()
    lap_time = current_time - start_time
    print(f"lap {count}: {lap_time} sec")
    count+=1
    return count,lap_time,current_time

# Record the start time
start_time = tick()
time.sleep(0.265)
# Record the end time
end_time = tock()
tick_tock(start_time,end_time)

def list_files_in_folder(folder_path):
    # Get the list of files in the specified folder
    file_names = os.listdir(folder_path)

    # Print the list of files
    print(f"Files in the folder '{folder_path}':")
    for file_name in file_names:
        print(file_name)

def create_csv():
    create_new = input("Want to create a new CSV file? Y/N")
    if create_new.lower() in ['yes', 'y']:
        # Code to execute when create_new is 'yes' or 'y'
        print("Create a new file.")
        # Get the title from the user
        title = input("Enter the title of the CSV file: ")

        # Use the user-entered title as the file name
        file_path = f'{title}.csv'

        # Get data from the user
        #data = []

        # while True:
        #     row_data = input("Enter data to be added to the CSV (press Enter to finish): ")
        #     if not row_data:
        #         break
        #     data.append(row_data.split(','))

        # Write the entered data to the CSV file
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)

        print(f'{file_path} file has been created.')

    else:
        # Code to execute when create_new is any other value
        print("Do not create a new file.")

def delete_file():
    file_name = input("Name of the file to delete: ")
    # Combine the file path using the current working directory as the base
    file_path = os.path.join(os.getcwd(), file_name)

    # Delete the file
    try:
        os.remove(file_path)
        print(f'{file_name} file has been deleted.')
    except FileNotFoundError:
        print(f'{file_name} file does not exist.')
    except Exception as e:
        print(f'Error occurred during file deletion: {e}')

def modify_csv_place(file_path, target_row, new_data):
    # Modify the CSV file directly
    with open(file_path, 'r+', newline='') as csvfile:
        # Create a CSV reader
        csv_reader = csv.reader(csvfile)

        # Convert CSV data to a list
        data = list(csv_reader)

        # Modify the desired row
        if target_row < len(data):
            data[target_row] = new_data
        else:
            print(f"Row {target_row} is out of the range of the CSV file.")

        # Move the file pointer to the beginning to erase the existing content and write new data
        csvfile.seek(0)
        csvfile.truncate()

        # Create a CSV writer and write the modified data to the CSV file
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

def modify_file():
    file_path = input('File path: ')
    target_row = input('Target row: ')
    new_data = input('New data: ')
    modify_csv_place(file_path, target_row, new_data)

def read_csv(file_path):
    # Read the CSV file and return it as a list
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        data = list(csv_reader)
    return data

def write_csv(file_path, data):
    # Write a list to a CSV file
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

def change_file():
    file_name = input('Filename: ')
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    try:
        prev_written = read_csv(file_name)
        print(f'{file_name} file reading.')
        print(prev_written)
    except FileNotFoundError:
        print(f'{file_name} does not exist.')
        return
    except Exception as e:
        print(f'ERROR: {e}')
        return

    try:
        write_csv(file_name, data)
        print(f'{file_name} file writing.')
    except Exception as e:
        print(f'ERROR: {e}')

def get_matrix(count,steering,throttle):
    count, temp_lap_time, current_time = lap_time(start_time,count)
    new_row=[f"{count}",f"{temp_lap_time}",f"{steering}",f"{throttle}"]
    data.append(new_row)
    return count

# import pygame
# from pygame.locals import *

# # Initialize Pygame
# pygame.init()

# # Set up the font
# font = pygame.font.SysFont(None, 72)

# # Create a small display for smooth keyboard input
# WINDOWWIDTH = 600
# WINDOWHEIGHT = 600
# windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 60)
# pygame.display.set_caption('DashBoard')


# def control_car():
#     moveForward = False
#     moveBack = False
#     moveLeft = False
#     moveRight = False
#     spacePressed = False  # Flag to track if spacebar is pressed
#     qPressed = False

#     running = True
#     while running:
#         windowSurface.fill((0, 0, 0))  # Clear the window
#         keys_pressed = pygame.key.get_pressed()  # Get the currently pressed keys
        
#         # Update the key flags based on the keys that are currently pressed
#         moveLeft = keys_pressed[K_LEFT] or keys_pressed[K_a]
#         moveRight = keys_pressed[K_RIGHT] or keys_pressed[K_d]
#         spacePressed = keys_pressed[K_SPACE]
#         moveForward = keys_pressed[K_UP] or keys_pressed[K_w]
#         moveBack = keys_pressed[K_DOWN] or keys_pressed[K_s]
#         qPressed = keys_pressed[K_q]

#         # Render text to display the currently pressed keys
#         text = ""

#         if moveLeft:
#             text += "Left "
#         if moveRight:
#             text += "Right "
#         if spacePressed:
#             text += "Space "
#         if moveForward:
#             text += "Up "
#         if moveBack:
#             text += "Down "
#         if qPressed:
#             text += "Brake"
#         text += f"Throttle: {car.throttle:.2f}"  # Include the throttle value


#         # Create a text surface
#         text_surface = font.render(text, True, (255, 255, 255))

#         # Draw the text surface onto the window
#         windowSurface.blit(text_surface, (10, 100))

#         # Update the display
#         pygame.display.update()

#         # Handle events
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 running = False

#         # Adjust the steering based on the key states
#         if moveLeft:
#             car.steering -= 0.001
#         elif moveRight:
#             car.steering += 0.001
#         # Gradually adjust the steering to 0.0 if the spacebar is pressed
#         if spacePressed:
#             if car.steering > 0.0:
#                 car.steering -= 0.001
#             elif car.steering < 0.0:
#                 car.steering += 0.001
#         elif moveForward:
#             car.throttle += 0.0005
#         elif moveBack:
#             car.throttle -= 0.0009
#         if qPressed:
#             car.throttle = default_throttle
        
#         # Limit the steering to the range [-1.0, 1.0]
#         car.steering = max(-1.0, min(1.0, car.steering))
#         car.throttle = max(-1.0, min(1.0, car.throttle))





def get_data():
    #Guessing if we could apply angle change in the camera direct to this code,
    #data structure be better
    #time_start, time_end, total_time, steering&gain, throttle&gain
    #car start
    steering=0
    steering_gain=1.0
    steering_bias=0
    throttle=0.2
    throttle_gain=0.5
    count=0
    

    cont_data=input("continue modifying state? Y/N: ")
    start_time=tick()

    while cont_data.lower() in ['yes','y']:
        control_car()
        # a = input("Enter what you want to change (Throttle:T, Steering:S): ")
        # if a.lower() == "t":
        #     try:
        #         throttle_input = float(input("Enter throttle value (-1.0 <= x <= 1.0): "))
        #         if -1.0 <= throttle_input <= 1.0:
        #             throttle=throttle_input
        #             car.throttle = throttle_input
        #             count=get_matrix(count,steering,throttle)
        #         else:
        #             throttle = 0.2
        #             car.throttle = 0.2
        #             count=get_matrix(count,steering,throttle)
        #             print("Throttle value must be between -1.0 and 1.0")
        #             break
        #     except ValueError:
        #         print("Invalid input. Please enter a valid floating-point number.")
        # elif a.lower() == "s":
        #     try:
        #         steering_input = float(input("Enter steering value (-1.0 <= x <= 1.0): "))
        #         if -1.0 <= steering_input <= 1.0:
        #             steering = steering_input
        #             car.steering=steering_input
        #             count=get_matrix(count,steering,throttle)
        #         else:
        #             throttle = 0.2
        #             car.throttle=0.2
        #             count=get_matrix(count,steering,throttle)
        #             print("Steering value must be between -1.0 and 1.0")
        #             break
        #     except ValueError:
        #         print("Invalid input. Please enter a valid floating-point number.")
        # else:
        #     print("Invalid input. Please enter 'T' for throttle or 'S' for steering.")
        #     continue

        cont_data=input("continue modifying state? Y/N: ")


        # if input("Do you want to continue (Y/N)? ").upper() != "Y":
        #     cont_data='n'
        #     break

    Q=input("Do you want to save the data?: ")
    if Q.lower() in ['yes','y']:
        create_csv()
        data=[]
    
default_throttle = 0.2

def control_car():
    steering=0
    steering_gain=1.0
    steering_bias=0
    throttle=0.2
    throttle_gain=0.5
    count=0
    running = True
    while running:
        # Get user input
        user_input = input("Enter command (w: forward, s: backward, a: left, d: right, q: brake, e: stop): ")
        steering=car.steering
        throttle=car.throttle

        if user_input.lower() == 'e':
            running = False
        else:
            # Adjust the car controls based on user input
            if 'w' in user_input:
                car.throttle += 0.010
                throttle=car.throttle
                count=get_matrix(count,steering,throttle)
            elif 's' in user_input:
                car.throttle -= 0.030
                throttle=car.throttle
                count=get_matrix(count,steering,throttle)
            # else:
            #     car.throttle = default_throttle

            elif 'a' in user_input:
                car.throttle = car.throttle
                car.steering -= 0.03
                steering=car.steering
                count=get_matrix(count,steering,throttle)
                
            elif 'd' in user_input:
                car.throttle = car.throttle
                car.steering += 0.03
                steering=car.steering
                count=get_matrix(count,steering,throttle)

                #car.throttle = car.throttle
            else:
                #  car.throttle = default_throttle
                #  throttle=car.throttle
                #  count=get_matrix(count,steering,throttle)             
                print(';')

            if 'q' in user_input:
                Gear = True
                while Gear :
                    car.throttle = default_throttle
                    car.steering = 0.0
                    throttle=car.throttle
                    steering=car.steering
                    count=get_matrix(count,steering,throttle)
                    gear_shift = input("Change Gear: (i: forward, k: backward, p: park): ")
                    if 'i' in gear_shift:
                        car.throttle += 0.2
                        throttle=car.throttle
                        count=get_matrix(count,steering,throttle)
                        Gear = False
                    elif 'k' in gear_shift:
                        #car.throttle = 0.25
                        #car.throttle = -0.4
                        Gear = False
                    elif 'p' in gear_shift:
                        car.throttle = 0.2
                        throttle=car.throttle
                        count=get_matrix(count,steering,throttle)
                        print("Park the car")
                        Gear = False


            # Limit the controls to the range [-1.0, 1.0]
            car.steering = max(-1.0, min(1.0, car.steering))
            car.throttle = max(-1.0, min(1.0, car.throttle))

            # Display current controls
            print(f"Throttle: {car.throttle:.2f}, Steering: {car.steering:.3f}")

# Run the control function



            
    
while True:
    menu_input = input("0. ls\n1. Create CSV file\n2. Delete file\n"\
                       "3. Modify file\n4. Change file\n5. Get Data\n"\
                        "6. Exit\nSelect a menu (0-6): ")
    if menu_input == '0':
        list_files_in_folder(os.getcwd())
    elif menu_input == '1':
        create_csv()
    elif menu_input == '2':
        delete_file()
    elif menu_input == '3':
        modify_file()
    elif menu_input == '4':
        change_file()
    elif menu_input == '5':
        get_data()
    elif menu_input == '6':
        print("Exiting the program.")
        break  # Exit the loop to end the program
    else:
        print("Please enter a valid menu number.")
    print()


