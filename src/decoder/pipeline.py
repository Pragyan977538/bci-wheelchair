import numpy as np
from mne.decoding import CSP
from sklearn.calibration import CalibratedClassifierCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import cohen_kappa_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .data import load_session
from .metrics import compute_ece, evaluate_latency

SEED = 20260901


def build_csp_lda_pipeline(n_components=6):
    return Pipeline([
        ("csp", CSP(n_components=n_components, log=True, norm_trace=False)),
        ("lda", LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto")),
    ])


def calibrate_pipeline(pipe, X_calib, y_calib):
    # Platt scaling, CSP/LDA stay frozen
    try:
        from sklearn.frozen import FrozenEstimator
        model = CalibratedClassifierCV(FrozenEstimator(pipe), method="sigmoid")
    except ImportError:
        model = CalibratedClassifierCV(estimator=pipe, cv="prefit", method="sigmoid")
    return model.fit(X_calib, y_calib)


def run_subject(subject, seed=SEED):
    X_train, y_train = load_session(subject, "0train")
    X_test, y_test = load_session(subject, "1test")

    # day 1: 75% fit, 25% calib
    X_fit, X_calib, y_fit, y_calib = train_test_split(
        X_train, y_train, test_size=0.25, stratify=y_train, random_state=seed)

    pipe = build_csp_lda_pipeline().fit(X_fit, y_fit)
    cal_model = calibrate_pipeline(pipe, X_calib, y_calib)

    raw_proba = pipe.predict_proba(X_test)
    cal_proba = cal_model.predict_proba(X_test)
    raw_pred, cal_pred = raw_proba.argmax(1), cal_proba.argmax(1)

    # 0-4 s post-cue for latency
    X_long, _, kept = load_session(subject, "1test", tmin=2.0, tmax=6.0, return_kept=True)
    latencies, censored = evaluate_latency(cal_model, X_long, kept)

    return {
        "subject": subject,
        "pipe": pipe,
        "cal_model": cal_model,
        "y_test": y_test,
        "raw_proba": raw_proba,
        "cal_proba": cal_proba,
        "latencies": latencies,
        "censored": censored,
        "summary": {
            "subject": subject,
            "raw_acc": float(np.mean(raw_pred == y_test)),
            "calib_acc": float(np.mean(cal_pred == y_test)),
            "kappa": float(cohen_kappa_score(y_test, cal_pred)),
            "raw_ece": compute_ece(raw_proba.max(1), raw_pred, y_test),
            "calib_ece": compute_ece(cal_proba.max(1), cal_pred, y_test),
            "median_latency": float(np.median(latencies)),
            "censored_fraction": float(np.mean(censored)),
        },
    }
