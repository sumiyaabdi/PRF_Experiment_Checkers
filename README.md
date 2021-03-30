# Attention PRF Experiment
Repository for PRF mapping experiment stimulus

Requirements: psychopy and exptools2

**Usage**

Create setting files named expsettings_*Task*.yml within the Experiment folder. Change *Task* to your actual task name. Run the following line from within the Experient folder. 

- python main.py sub ses run E.g. `python main.py 001 1 1`

The command line will prompt you to enter which task (2AFC or YesNo). This will select the settings file for you.
Subject SHOULD be specified according the the BIDS convention (sub-001, sub-002 and so on), Task MUST match one of the settings files in the Experiment folder, and Run SHOULD be an integer.

## Sumiya's Notes
- Press q to quit 
- Press t to pass **Waiting for scanner** screen
