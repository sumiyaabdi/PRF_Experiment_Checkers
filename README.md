# PRF_Experiment
Repository for PRF mapping experiment stimulus

Requirements: psychopy and exptools2

**Usage**

Create setting files named expsettings_*Task*.yml within the Experiment folder. Change *Task* to your actual task name. Run the following line from within the Experient folder. 

- python main.py sub-*xxx* ses-*x* task-*NameTask* run-*x*

Subject SHOULD be specified according the the BIDS convention (sub-001, sub-002 and so on), Task MUST match one of the settings files in the Experiment folder, and Run SHOULD be an integer.

**Marco's PRF mapping**

The Experiment folder contains 5 setting files, which can be used as examples. The Task names are:

- 2R: 2 squares, Regular speed (20TR bar passes, aka 30 seconds with our standard sequence)
- 4R: 4 squares, Regular speed 
- 1R: 1 square, Regular speed
- 4F: 4 squares, Fast speed (10TR bar passes, double the normal speed)
- 1S: 1 square, Slow speed (40TR bar passes, half the normal speed)

Note that the actual task (fixation dot color discrimination) is identical in all 5 cases.
