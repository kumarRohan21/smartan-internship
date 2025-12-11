from utils import angle_between, vertical_diff, spine_angle

def check_bicep_curl(shoulder, elbow, wrist):
    angle = angle_between(shoulder, elbow, wrist)

    if angle < 45:
        return "Arm contracted (top of curl)"

    if angle > 160:
        return "Arm fully extended (bottom position)"

    return None  

def check_lateral_raise(shoulder, wrist):
    diff = vertical_diff(shoulder, wrist)

    if diff > 0.12:  
        return "Wrist not at shoulder height"

    return None

def check_posture(left_sh, right_sh, left_hip, right_hip):
    mid_sh = ((left_sh[0] + right_sh[0]) / 2, (left_sh[1] + right_sh[1]) / 2)
    mid_hip = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)

    angle = spine_angle(mid_sh, mid_hip)

    if angle > 15:
        return f"Back leaning ({angle:.1f}°)"

    return None
