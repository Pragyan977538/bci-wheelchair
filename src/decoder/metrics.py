import numpy as np


def _bins(conf, n_bins):
    edges = np.linspace(0, 1, n_bins + 1)
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        yield (conf >= lo) & (conf <= hi) if i == 0 else (conf > lo) & (conf <= hi)


def compute_ece(conf, pred, y_true, n_bins=10):
    correct = (pred == y_true).astype(float)
    ece = 0.0
    for m in _bins(conf, n_bins):
        if m.any():
            ece += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(ece)


def reliability_curve(conf, pred, y_true, n_bins=10):
    # for reliability diagram
    correct = (pred == y_true).astype(float)
    confs, accs = [], []
    for m in _bins(conf, n_bins):
        if m.any():
            confs.append(conf[m].mean())
            accs.append(correct[m].mean())
    return np.array(confs), np.array(accs)


def evaluate_latency(model, X_long, kept, sfreq=250, win_s=2.0, step_s=0.1,
                     threshold=0.5, horizon=4.0):
    win, step = int(win_s * sfreq), int(step_s * sfreq)
    kept_idx = np.flatnonzero(kept)
    latencies = np.full(len(kept), horizon)  # censored default
    reached = np.zeros(len(kept), dtype=bool)

    for start in range(0, X_long.shape[2] - win + 1, step):
        top = model.predict_proba(X_long[:, :, start:start + win]).max(axis=1)
        rows = kept_idx[(top >= threshold) & ~reached[kept_idx]]
        latencies[rows] = (start + win) / sfreq  # window end
        reached[rows] = True
        if reached[kept_idx].all():
            break

    return latencies, ~reached
