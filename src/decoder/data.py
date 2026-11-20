import warnings

import mne
import numpy as np
from moabb.datasets import BNCI2014_001

warnings.filterwarnings("ignore", message="Montage name 'standard_1005' is deprecated")

CLASSES = ["left_hand", "right_hand", "feet", "tongue"]


def load_session(subject, session, tmin=2.5, tmax=4.5, return_kept=False):
    # tmin/tmax are from trial start (cue at 2 s)
    mne.set_log_level("WARNING")
    runs = BNCI2014_001().get_data(subjects=[subject])[subject][session]

    X_list, y_list, kept_list = [], [], []
    for run_id in sorted(runs):
        raw = runs[run_id].copy().pick("eeg")
        raw.filter(8.0, 30.0, method="iir",
                   iir_params={"order": 4, "ftype": "butter"}, verbose=False)

        events, event_ids = mne.events_from_annotations(raw, verbose=False)
        mapping = {event_ids[c]: i for i, c in enumerate(CLASSES)}  # by name

        epochs = mne.Epochs(raw, events, tmin=tmin, tmax=tmax,
                            baseline=None, preload=True, verbose=False)

        # trials past recording end get dropped
        kept = np.zeros(len(events), dtype=bool)
        kept[epochs.selection] = True

        X_list.append(epochs.get_data())
        y_list.append(np.array([mapping[e] for e in events[:, 2]]))
        kept_list.append(kept)

    X = np.concatenate(X_list)
    y = np.concatenate(y_list)
    kept = np.concatenate(kept_list)

    if return_kept:
        return X, y, kept
    return X, y[kept]
