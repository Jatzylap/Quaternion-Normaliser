'''
Title: Transformation Normaliser
Author: Jatzylap
Version: 1.0
'''

import os
from math import sqrt, sin, cos, radians, pi

matrix = False

print("\n\n\n=========================")
print("Transformation Normaliser")
print("     - by Jaztylap -")
print("=========================\n\n")

class InvalidMode(Exception):
    def __init__(self, mode):
        super().__init__(f"EXCEPTION => Input must contain the letters: (D) or (M)!")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_mode():
    global matrix
    mode = input("\n\nMode (D / M): ").strip().upper()
    if mode not in ['D', 'M']:
        raise InvalidMode(mode)
    matrix = (mode == 'M')
    clear_console()

def get_float_input(prompt):
    running_input = True
    while running_input:
        try:
            return float(input(prompt))
        except ValueError:
            print("EXCEPTION => Input must be a number!")

def translation_inputs():
    print("Translation")
    x, y, z = get_float_input("X offset: "), get_float_input("Y offset: "), get_float_input("Z offset: ")
    clear_console()
    return x, y, z

def scale_input():
    scale = get_float_input("Scale: ")
    clear_console()
    return scale

def rotation_inputs(rotation_side):
    print(f"{rotation_side} Rotation")
    x, y, z = get_float_input("X degrees: "), get_float_input("Y degrees: "), get_float_input("Z degrees: ")
    return x, y, z

def normalise_components(x, y, z):
    sum_value = abs(x + y + z)
    remainder = 90 - sum_value
    x, y, z = sin(radians(x/2)), sin(radians(y/2)), sin(radians(z/2))
    if sum_value != 90:
        if x+remainder < 1: x += remainder
        elif y+remainder < 1: y += remainder
        elif z+remainder < 1: z += remainder
    squared_magnitude = x**2 + y**2 + z**2
    w = sqrt(1 - squared_magnitude)
    return round(x, 3), round(y, 3), round(z, 3), round(w, 3)

def multiply_matrix(mat0, mat1):
    mat = [[0, 0, 0, 0] for row in range(4)]
    for i in range(len(mat0)):
        for j in range(len(mat1[0])):
            for k in range(len(mat1)):
                mat[i][j] += mat0[i][k] * mat1[k][j]
    return mat

def get_inputs():
    translation, scale = translation_inputs(), scale_input()
    left_rot, right_rot = rotation_inputs("Left"), rotation_inputs("Right")
    return translation, scale, left_rot, right_rot

def decomposed_quaternions():
    q0, q1, q2, q3 = get_inputs()
    q2, q3 = normalise_components(*q2), normalise_components(*q3)
    return q0, q1, q2, q3

def composed_quaternions():
    translation, scale, left_rot, right_rot = get_inputs()
    scale = (scale, scale, scale)

    # Translation
    tr = [[1,0,0,translation[0]],
          [0,1,0,translation[1]],
          [0,0,1,translation[2]],
          [0,0,0,1]]

    # Scale
    sc = [[scale[0],0,0,0],
          [0,scale[1],0,0],
          [0,0,scale[2],0],
          [0,0,0,1]]

    # Right rotations
    rr_x = [[1,0,0,0],
            [0,round(cos(radians(right_rot[0])),3),-round(sin(radians(right_rot[0])),3),0],
            [0,round(sin(radians(right_rot[0])),3),round(cos(radians(right_rot[0])),3),0],
            [0,0,0,1]]

    rr_y = [[round(cos(radians(right_rot[1])),3),0,round(sin(radians(right_rot[1])),3),0],
            [0,1,0,0],
            [-round(sin(radians(right_rot[1])),3),0,round(cos(radians(right_rot[1])),3),0],
            [0,0,0,1]]

    rr_z = [[round(cos(radians(right_rot[2])),3),-round(sin(radians(right_rot[2])),3),0,0],
            [round(sin(radians(right_rot[2])),3),round(cos(radians(right_rot[2])),3),0,0],
            [0,0,1,0],
            [0,0,0,1]]

    # Left rotations
    lr_x = [[1,0,0,0],
            [0,round(cos(radians(left_rot[0])),3),-round(sin(radians(left_rot[0])),3),0],
            [0,round(sin(radians(left_rot[0])),3),round(cos(radians(left_rot[0])),3),0],
            [0,0,0,1]]

    lr_y = [[round(cos(radians(left_rot[1])),3),0,round(sin(radians(left_rot[1])),3),0],
            [0,1,0,0],
            [-round(sin(radians(left_rot[1])),3),0,round(cos(radians(left_rot[1])),3),0],
            [0,0,0,1]]

    lr_z = [[round(cos(radians(left_rot[2])),3),-round(sin(radians(left_rot[2])),3),0,0],
            [round(sin(radians(left_rot[2])),3),round(cos(radians(left_rot[2])),3),0,0],
            [0,0,1,0],
            [0,0,0,1]]

    # Multiply affine matrices
    ts = multiply_matrix(tr, sc)
    rr_xy = multiply_matrix(rr_x, rr_y)
    rr = multiply_matrix(rr_xy, rr_z)
    lr_xy = multiply_matrix(lr_x, lr_y)
    lr = multiply_matrix(lr_xy, lr_z)
    r = multiply_matrix(lr, rr)

    rot_mat = multiply_matrix(ts, r)

    return rot_mat

def main():
    global matrix
    running_main = True
    while running_main:
        try:
            check_mode()
            if matrix:
                result = composed_quaternions()
                print("Quaternion matrix: ")
                print(f"[{result[0][0]}f,{result[0][1]}f,{result[0][2]}f,{result[0][3]}f,")
                print(f"{result[1][0]}f,{result[1][1]}f,{result[1][2]}f,{result[1][3]}f,")
                print(f"{result[2][0]}f,{result[2][1]}f,{result[2][2]}f,{result[2][3]}f,")
                print(f"{result[3][0]}f,{result[3][1]}f,{result[3][2]}f,{result[3][3]}f]")
            else:
                translation, scale, left_rot, right_rot = decomposed_quaternions()
                print("Decomposed quaternions: ")
                print("{"+f"translation:[{translation[0]}f,{translation[1]}f,{translation[2]}f],")
                print(f"scale:[{scale}f,{scale}f,{scale}f],")
                print(f"left_rotation:[{left_rot[0]}f,{left_rot[1]}f,{left_rot[2]}f,{left_rot[3]}f],")
                print(f"right_rotation:[{right_rot[0]}f,{right_rot[1]}f,{right_rot[2]}f,{right_rot[3]}f]"+"}")
        except ValueError as e:
            print("EXCEPTION =>", e)
            break
        except KeyboardInterrupt:
            clear_console()
            break

if __name__ == '__main__':
    main()