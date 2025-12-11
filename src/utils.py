import numpy as np
import math

def angle_between(a, b, c):
   
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-7)
    cosine = np.clip(cosine, -1.0, 1.0)

    angle = math.degrees(math.acos(cosine))
    return angle

def vertical_diff(p1, p2):
   
    return abs(p1[1] - p2[1])

def spine_angle(shoulder_mid, hip_mid):
   
    dx = shoulder_mid[0] - hip_mid[0]
    dy = shoulder_mid[1] - hip_mid[1]
    angle = abs(math.degrees(math.atan2(dx, dy)))
    return angle
