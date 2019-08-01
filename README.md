Cyclingdynamics

#Requirements
-Python
  -Matplotlib
  -Pandas
  -Numpy
-FFMPEG (with path setup)
-FitSDK
-Java runtime

Your fit file MUST have ALL L/R Balance, Pedal Smoothness, Torque Effectiveness and Cycling dynamics (Assioma OR Vector Series currently) to process. They all must be turned on and recorded or else the math used will fail.

They must be recorded with the correct fit descriptors and NOT developer fields

#instructions
See the youtube video for walkthrough

1) Use the fitsdk java commandline tool FitToCSV-data on your fitfile
2) place the <filename>-data.csv in this folder
3) Run fitcsvfileclean.py to delete duplicate entries and interpolate missing data
4) Run CyclingDynamics.py to decode to "High speed" and create a polar plot animation that is saved as an .mp4 x264 file
