import numpy as np

def psyc_stim_list(stim_range, n_stim, baseline):
    " Creates stim list for psychophysics task"
    stim_list = stim_range*int(n_stim/len(stim_range))
    [stim_list.append(i) for i in [baseline]*(n_stim-len(stim_list))]
    np.random.shuffle(stim_list)

    return stim_list

def get_stim_nr(trial,phase,stim_per_trial):
    phase = phase-1 if phase % 2 == 1 else phase
    return int(trial * stim_per_trial + (phase)/2)

def create_stim_list(n, signal, values,midpoint):
    """

    Creates stim list for main attention (i.e. detection)
    task.

    Parameters
    ----------
    n (int) :   number of stimuli to be presented
    signal (int) :  number of target stimuli
    values (1D arr) :   array containing range of target values

    Returns
    -------
    stim_list (array):  array of length n, target stimuli spaced
                        between non-target trials.
    """

    targets = []
    baseline = np.ones(int(n - signal)) * midpoint

    for i in range(len(values)):
        targets = np.append(targets, (np.ones(int(signal / len(values))) * values[i]))
    np.random.shuffle(targets)

    ratio = int(len(baseline) / len(targets))
    locs = [i * ratio + np.random.choice(ratio) for i in range(len(targets))]
    stim_list = np.insert(baseline, locs, targets)

    while len(stim_list) != n:
        stim_list = np.insert(stim_list, 0, midpoint)

    return stim_list