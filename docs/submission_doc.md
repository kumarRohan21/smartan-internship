&nbsp;Smartan Internship – Form Correctness Detector

&nbsp;    Submission Document  

&nbsp;    Author: Rohan Kumar  









This project demonstrates a simple \*\*form correctness detection system\*\* using \*\*MediaPipe Pose\*\*.  

The system identifies human pose landmarks from video or webcam input, calculates joint angles, and applies rule-based checks to give basic feedback on exercise posture.



The goal is to show understanding of:

\- Keypoint extraction  

\- Angle calculation  

\- Rule-based evaluation  

\- Annotated video generation  

\- JSON-based result logging  



---



&nbsp;2. How It Works



&nbsp;  2.1 Pose Detection

The system uses MediaPipe to detect major body landmarks such as:

\- Shoulder  

\- Elbow  

\- Wrist  

\- Hip  



Each landmark provides coordinates (x, y), which are then used for angle calculations.



&nbsp;2.2 Angle Calculation

A simple geometric formula is used to find the angle at the elbow or other joints:



This helps in identifying:

\- Arm contraction  

\- Arm extension  

\- Shoulder height differences  

\- Spine tilt  



&nbsp;2.3 Rule-Based Form Checks

The following basic rules are applied:



&nbsp;    Bicep Curl Rule

\- If elbow angle < \*\*45°\*\* → arm fully contracted  

\- If elbow angle > \*\*160°\*\* → arm fully extended  



Provides simple “top” and “bottom” curl feedback.



&nbsp;     Lateral Raise Rule

\- Compares wrist height and shoulder height  

\- If wrist significantly below shoulder → “not enough raise”



&nbsp;      Posture Rule

\- Mid-shoulder vs mid-hip vertical alignment  

\- If spine angle > \*\*15°\*\* → “back leaning” detected  



---



&nbsp;3. Input \& Output



&nbsp;	3.1 Input

\- Webcam feed (`python src/run\_demo.py`)  

\- Video file (`.mp4`)  



&nbsp;	 3.2 Output

1\. Annotated Video

&nbsp;  - Skeleton overlay  

&nbsp;  - Angle reading  

&nbsp;  - Feedback messages on screen  



2\. JSON Report

&nbsp;  - Saved in `data/sample\_results/`  

&nbsp;  - Contains:

&nbsp;    - Frame number  

&nbsp;    - Angles  

&nbsp;    - Flags (warnings or feedback)  



Example JSON snippet:

{

"frame": 42,

"angles": {

"elbow\_left\_smooth": 75.2

},

"flags": \[

{ "rule": "bicep\_curl\_left", "msg": "Arm contracted" }

]

}



---



&nbsp;5. Limitations



\- Only basic single-person detection  

\- Rules are simple thresholds (not ML-based)  

\- Lighting or low-resolution video may reduce accuracy  



---



&nbsp;6. Future Improvements



\- Add rep counting with peak detection  

\- Add symmetry checks for both arms  

\- Support multiple exercises  

\- Improve smoothing filters for noisy data  

\- Extend for real-time coaching feedback  



---



&nbsp;7. Conclusion



This project demonstrates a functional pipeline for form detection using computer vision:

\- Pose extraction  

\- Angle analysis  

\- Rule evaluation  

\- Annotated video creation  

\- JSON result logging  



It fulfills the internship task requirements and provides a modular foundation that can be extended for more advanced exercise tracking.









