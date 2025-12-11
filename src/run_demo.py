import sys
import os
import json
import time
from collections import deque

import cv2
import mediapipe as mp

from utils import angle_between, vertical_diff, spine_angle
from evaluate_form import check_bicep_curl, check_lateral_raise, check_posture

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def lm_xy(landmarks, idx):
    lm = landmarks[idx]
    return (lm.x, lm.y)

def denorm(pt, width, height):
    return int(pt[0] * width), int(pt[1] * height)

def run(source=0, output_path=None, save_json=True):
    cap = cv2.VideoCapture(int(source) if str(source).isdigit() else source)
    if not cap.isOpened():
        print("ERROR: Cannot open video source:", source)
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    writer = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    results_list = []
    frame_idx = 0
    elbow_q = deque(maxlen=5)

    pose = mp_pose.Pose(static_image_mode=False, 
                        min_detection_confidence=0.5, 
                        min_tracking_confidence=0.5)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1
            t0 = time.time()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = pose.process(rgb)

            frame_feedback = {"frame": frame_idx, "flags": [], "angles": {}}

            if res.pose_landmarks:
                lm = res.pose_landmarks.landmark

                left_sh = lm_xy(lm, mp_pose.PoseLandmark.LEFT_SHOULDER)
                right_sh = lm_xy(lm, mp_pose.PoseLandmark.RIGHT_SHOULDER)
                left_el = lm_xy(lm, mp_pose.PoseLandmark.LEFT_ELBOW)
                right_el = lm_xy(lm, mp_pose.PoseLandmark.RIGHT_ELBOW)
                left_wr = lm_xy(lm, mp_pose.PoseLandmark.LEFT_WRIST)
                right_wr = lm_xy(lm, mp_pose.PoseLandmark.RIGHT_WRIST)
                left_hip = lm_xy(lm, mp_pose.PoseLandmark.LEFT_HIP)
                right_hip = lm_xy(lm, mp_pose.PoseLandmark.RIGHT_HIP)

                elbow_ang_left = angle_between(left_sh, left_el, left_wr)
                elbow_q.append(elbow_ang_left)
                elbow_smoothed = sum(elbow_q) / len(elbow_q)

                frame_feedback["angles"]["elbow_left_raw"] = elbow_ang_left
                frame_feedback["angles"]["elbow_left_smooth"] = elbow_smoothed

                bicep_msg = check_bicep_curl(left_sh, left_el, left_wr)
                if bicep_msg:
                    frame_feedback["flags"].append({"rule": "bicep_curl_left", "msg": bicep_msg})

                lateral_msg = check_lateral_raise(left_sh, left_wr)
                if lateral_msg:
                    frame_feedback["flags"].append({"rule": "lateral_raise_left", "msg": lateral_msg})

                posture_msg = check_posture(left_sh, right_sh, left_hip, right_hip)
                if posture_msg:
                    frame_feedback["flags"].append({"rule": "posture_symmetry", "msg": posture_msg})

                # ❌ NO radius= used anywhere — FIXED
                mp_drawing.draw_landmarks(
                    frame,
                    res.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0,255,0), thickness=1, circle_radius=3
                    ),
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0,255,0), thickness=2
                    )
                )

                fps_now = 1.0 / (time.time() - t0 + 1e-8)
                cv2.putText(frame, f"FPS:{fps_now:.1f}", (width - 140, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,0), 2)

                y0 = 30
                for i, f in enumerate(frame_feedback["flags"][:6]):
                    cv2.putText(frame, f"{f['msg']}", (10, y0 + i*25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

                cv2.putText(frame, f"Elbow L: {elbow_smoothed:.1f} deg", 
                            (10, height - 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

            cv2.imshow("Form Checker", frame)
            if writer:
                writer.write(frame)

            results_list.append(frame_feedback)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()

        if save_json:
            out_dir = "data/sample_results"
            os.makedirs(out_dir, exist_ok=True)
            json_path = os.path.join(out_dir, f"results_{int(time.time())}.json")
            with open(json_path, "w") as f:
                json.dump(results_list, f, indent=2)
            print("Saved JSON to:", json_path)

if __name__ == "__main__":
    src_arg = sys.argv[1] if len(sys.argv) > 1 else "0"
    out_arg = sys.argv[2] if len(sys.argv) > 2 else None
    run(src_arg, out_arg)
