import math
import time
from servo import Servo

# Initialize servos
base_servo = Servo(1)  # Base servo (rotates horizontally)
top_servo = Servo(2)   # Top servo (rotates vertically)

# Arm lengths
L1 = 8  # Length of the first arm
L2 = 4  # Length of the second arm

# Initial angles
INITIAL_BASE_ANGLE = 90  # Base servo starts at 90° (neutral)
INITIAL_TOP_ANGLE = 90   # Top servo starts at 90° (arm vertical)

# Inverse kinematics function
def calculate_angles(x, y):
    # Distance to target point
    d = math.sqrt(x**2 + y**2)
    if d > (L1 + L2) or d < abs(L1 - L2):
        raise ValueError("Point out of reach")
    
    # Calculate the angle for the second arm
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = max(-1, min(1, cos_theta2))  # Clamp to avoid math domain errors
    theta2 = math.acos(cos_theta2)  # Result in radians
    
    # Calculate the angle for the first arm
    theta1 = math.atan2(y, x) - math.atan2(L2 * math.sin(theta2), L1 + L2 * math.cos(theta2))
    
    # Convert radians to degrees
    theta1_deg = math.degrees(theta1)
    theta2_deg = math.degrees(theta2)
    
    # Adjust for servo orientations
    base_servo_angle = theta1_deg  # Base servo: No adjustment needed
    top_servo_angle = theta2_deg - 90  # Top servo: Adjust by -90° for vertical alignment
    
    return base_servo_angle, top_servo_angle

# Function to move servos
def move_servos(angle1, angle2):
    print(f"Moving base to {angle1:.2f}° and top to {angle2:.2f}°")
    base_servo.write(angle1)
    top_servo.write(angle2)
    time.sleep(0.5)

# Function to reset servos
def reset_servos():
    print("Resetting servos to initial positions")
    move_servos(INITIAL_BASE_ANGLE, INITIAL_TOP_ANGLE)

# Function to draw a circle
def draw_circle(radius, center_x=6, center_y=0, steps=50):
    # Initialize current servo angles
    current_angle1 = INITIAL_BASE_ANGLE
    current_angle2 = INITIAL_TOP_ANGLE

    for i in range(steps):
        phi = 2 * math.pi * i / steps  # Angle in radians
        x = center_x + radius * math.cos(phi)
        y = center_y + radius * math.sin(phi)

        try:
            angle1, angle2 = calculate_angles(x, y)
            print(f"Moving to ({x:.2f}, {y:.2f}) with angles: Base={angle1:.2f}°, Top={angle2:.2f}°")
            move_servos(angle1, angle2)
            current_angle1, current_angle2 = angle1, angle2
        except ValueError as e:
            print(f"Error: {e} at point ({x:.2f}, {y:.2f})")
            continue

    # Reset servos after drawing
    reset_servos()

# Main routine
if __name__ == "__main__":
    reset_servos()  # Reset to initial positions
    draw_circle(radius=3, center_x=6, center_y=0)  # Draw a circle

