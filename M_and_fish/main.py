import math
import time
from servo import Servo

# Initialize servos
base_servo = Servo(1)   # Base servo
top_servo = Servo(2)    # Top servo (inverted orientation)

# Arm lengths
L1 = 8  # Length of the first arm
L2 = 4  # Length of the second arm

# Initial angles
INITIAL_BASE_ANGLE = 90  # Base servo starts at 90°
INITIAL_TOP_ANGLE = 90   # Top servo starts at 90°

# Function to calculate angles
def calculate_angles(x, y):
    d = math.sqrt(x**2 + y**2)
    if d > (L1 + L2) or d < abs(L1 - L2):
        raise ValueError("Point out of reach")
    
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = max(-1, min(1, cos_theta2))  # Clamp to avoid math domain errors
    theta2 = math.acos(cos_theta2)
    
    theta1 = math.atan2(y, x) - math.atan2(L2 * math.sin(theta2), L1 + L2 * math.cos(theta2))
    
    # Convert radians to degrees
    theta1_deg = max(0, min(180, math.degrees(theta1)))  # Clamp angles
    theta2_deg = max(0, min(180, math.degrees(theta2) - 90))  # Adjust for top servo
    
    return theta1_deg, theta2_deg

# Function to move servos slowly
def move_servos_slowly(current_angle1, target_angle1, current_angle2, target_angle2, steps=30, delay=0.05):
    for step in range(steps + 1):
        interpolated_angle1 = current_angle1 + (target_angle1 - current_angle1) * step / steps
        interpolated_angle2 = current_angle2 + (target_angle2 - current_angle2) * step / steps

        base_servo.write(interpolated_angle1)
        top_servo.write(interpolated_angle2)
        time.sleep(delay)

# Function to reset servos
def reset_servos():
    print("Resetting servos to initial positions")
    move_servos_slowly(base_servo.read(), INITIAL_BASE_ANGLE, top_servo.read(), INITIAL_TOP_ANGLE)

# Function to draw a shape
def draw_shape(shape_name, points):
    print(f"\nStarting to draw {shape_name}...")
    current_angle1 = INITIAL_BASE_ANGLE
    current_angle2 = INITIAL_TOP_ANGLE

    for x, y in points:
        try:
            angle1, angle2 = calculate_angles(x, y)
            print(f"{shape_name}: Moving to ({x:.2f}, {y:.2f}) with angles: Base={angle1:.2f}°, Top={angle2:.2f}°")
            move_servos_slowly(current_angle1, angle1, current_angle2, angle2, steps=30, delay=0.03)
            current_angle1, current_angle2 = angle1, angle2
        except ValueError as e:
            print(f"{shape_name}: Point out of reach ({x:.2f}, {y:.2f})")

    reset_servos()
    print(f"\nFinished drawing {shape_name}.")

# Define reachable "M" shape points
m_points = [
    (5, 3),  # Left leg bottom
    (6, 7),  # Left peak
    (7, 3),  # Middle valley
    (8, 7),  # Right peak
    (9, 3)   # Right leg bottom
]

# Define adjusted fish shape points
fish_points = [
    # Body
    (4, 3), (6, 5), (8, 3), (6, 1), (4, 3),
    # Tail
    (9, 3), (10, 4), (10, 2), (9, 3)
]

# Main routine
if __name__ == "__main__":
    reset_servos()
    draw_shape("M", m_points)
    time.sleep(1)
    draw_shape("Fish", fish_points)

