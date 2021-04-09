# Attention PRF Experiment

Attention size task added onto standard PRF bar stimulus.

Participants will fixate on the central circle while cyan and magenta dots are presented on the screen. The aim of the task is to notice the proportion of cyan to magenta. The attention task can be small (noting dot proportions within the fixation circle) or large (noting proportions spanning the entire screen, excluding fixation).

There are two task paradigms which can be used:
1) **2AFC:** A two-alternative forced choice (discrimination) task where a stimulus with cyan and magenta dots is presented and the subject responds whether the proportion is more cyan or more magenta
2) **Yes / No:**  A yes / no (detection) task where stimuli with cyan and magenta dots are continuously presented 

The discrimination (2AFC) task is employed

### Two Alternative Forced Choice (2AFC)

**Usage**






---
Old Notes:

Requirements: psychopy and exptools2

Create setting files named expsettings_*Task*.yml within the Experiment folder. Change *Task* to your actual task name. Run the following line from within the Experient folder.

- python main.py sub ses run E.g. `python main.py 001 1 1`

The command line will prompt you to enter which task (2AFC or YesNo). This will select the settings file for you.
Subject SHOULD be specified according the the BIDS convention (sub-001, sub-002 and so on), Task MUST match one of the settings files in the Experiment folder, and Run SHOULD be an integer.

## Sumiya's Notes
- Press q to quit
- Press t to pass **Waiting for scanner** screen
