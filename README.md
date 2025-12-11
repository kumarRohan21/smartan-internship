&nbsp;

This project demonstrates a simple form correctness detection system using MediaPipe Pose.  

It detects human pose landmarks, calculates joint angles, and applies basic rule-based checks 

for exercises like bicep curl, lateral raise, and posture.



---



 **How to Run**



1\. **Create Virtual Environment**

py -3.10 -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

2\. **Run on Webcam**

python src/run\_demo.py



3\. **Run on Sample Video**

python src/run\_demo.py data/sample\_videos/demo.mp4 data/sample\_results/demo\_out.mp4







 **Output**

\- Annotated video saved in **data/sample\_results/**

\- JSON file with angles + flags generated automatically







 **Project Structure**

src/

data/

docs/

README.md

requirements.txt







&nbsp;**Notes**

\- Rules can be modified in `evaluate\_form.py`

\- This project is for internship demonstration only









