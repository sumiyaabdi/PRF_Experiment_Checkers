# Attention PRF Experiment

Attention size task added onto standard PRF bar stimulus.

Participants will fixate on the central circle while cyan and magenta dots are presented on the screen. The aim of the task is to notice the proportion of cyan to magenta. The attention task can be small (noting dot proportions within the fixation circle) or large (noting proportions spanning the entire screen, excluding fixation).

There are two task paradigms which can be used:
1) **2AFC:** A two-alternative forced choice (discrimination) task where a stimulus with cyan and magenta dots is presented and the participant responds whether the proportion is more cyan or more magenta
2) **Yes / No:**  A yes/no (detection) task where stimuli with cyan and magenta dots are continuously presented and participant responds when the proportion changes from 0.5 to another proportion, showing that the stimulus is either more cyan or more magenta.

The discrimination (2AFC) task is used first with a variety of proportions (varying in difficulty) to determine where the 'just noticeable difference' (a proprotion correct of 20% or 80%) should be located for the detection (yes/no). This also ensure that the perceived difficulty of the two attentional conditions is matched.

## Usage

To run the either the 2AFC or yes/no experiment:

`python main.py sub-000 1 2`

where `sub-000` is this subject number, `1` is an example of the session number and `2` is the run number. All these values should be changed according to what the current subject, session, and run is.

Following this the terminal will prompt:

```
Which attention task ['2afc' / 'yesno']?:
Which attention size [small (s) / large (l)]?:
Eyetracking (y/n)?:
```

Once the task window opens up a fixation cross will appear. If simulating an experiment click `t` to begin, if scanning the scanner will send a trigger.

### Things to check:

In the settings file for your task `expsettings_{task}.yml`, double check that all settings (e.g. operating system, window size, monitor, simulating settings, etc.) are correct for your given experimental conditions.

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
