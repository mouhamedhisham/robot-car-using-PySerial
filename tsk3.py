import pygame
import sys
import serial
import serial.tools.list_ports

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Controls")

# Main loop
ports = list(serial.tools.list_ports.comports())
arduino_port = None
for p in ports:
    if "CH340" in p[1]:
        arduino_port = p[0]

print(arduino_port)
with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = arduino_port
    ser.open()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Up arrow key pressed")
                    ser.write(b'F')  # Send 'F' for forward
                elif event.key == pygame.K_DOWN: 
                    print("Down arrow key pressed")
                    ser.write(b'B')  # Send 'B' for backward
                elif event.key == pygame.K_LEFT:
                    print("Left arrow key pressed")
                    ser.write(b'L')  # Send 'L' for left
                elif event.key == pygame.K_RIGHT:
                    print("Right arrow key pressed")
                    ser.write(b'R')  # Send 'R' for right
                elif event.key == pygame.K_SPACE:
                    print("Spacebar pressed")
                    ser.write(b'S')  # Send 'S' for stop
                elif event.key == pygame.K_l:
                    print("L pressed")
                    ser.write(b'E')  # Send 'S' for stop
                    

        # Fill screen with a color
        screen.fill((0, 0, 0))

        # Update display
        pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
 