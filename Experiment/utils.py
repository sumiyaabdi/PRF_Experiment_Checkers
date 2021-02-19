import numpy as np


def create_stim_list(n, signal, values):
    """

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
    baseline = np.ones(int(n - signal)) * np.median(values)

    for i in range(len(values)):
        targets = np.append(targets, (np.ones(int(signal / len(values))) * values[i]))
    np.random.shuffle(targets)

    ratio = int(len(baseline) / len(targets))
    locs = [i * ratio + np.random.choice(ratio) for i in range(len(targets))]
    stim_list = np.insert(baseline, locs, targets)

    while len(stim_list) != n:
        stim_list = np.insert(stim_list, 0, np.median(values))

    return stim_list