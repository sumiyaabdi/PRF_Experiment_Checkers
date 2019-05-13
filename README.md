# PRF_Experiment
Repository for PRF mapping experiment stimulus

Requirements: psychopy and exptools2

Put your settings in files named expsettings_Condition.yml within the Experiment folder. Change 'Condition' to your actual condition name. Ask marco for explicit settings files examples.

Run line
python main.py SubjectName SessionNumber Condition RunNumber

For example, for Marco's experiment, currently there are 5 conditions, and 5 related settings files, coded as PRF+number of squares in bar+bar speed letter (Regular, Fast, Slow). 

In this experiment,the condition names are:
PRF2R: 2 squares, Regular speed (20TR bar passes, aka 30 seconds with our standard sequence)
PRF4R: 4 squares, Regular speed 
PRF1R: 1 square, Regular speed
PRF4F: 4 squares, Fast speed (10TR bar passes, double the normal speed)
PRF1S: 1 square, Slow speed (40TR bar passes, half the normal speed)





