# Shared control for a brain-controlled wheelchair

**Pragyan Mohanty — roll 24250**

A person imagines a movement (left hand, right hand, feet, tongue). An EEG decoder turns that into a driving command, but the decoder is wrong more than half the time and slow. This project asks: **how much control should the user get, and how much should an autopilot take, so the wheelchair still reaches its goal safely?**

The project has two parts, one notebook each:

| Part | Notebook | What it does |
|---|---|---|
| 1 | `src/part1_decoder.ipynb` | Trains and tests the EEG decoder (CSP + LDA, calibrated) on 9 subjects, measures accuracy, calibration and latency, and saves the decoder's trial-by-trial behaviour for Part 2. |
| 2 | `src/part2_shared_control.ipynb` | Builds the wheelchair simulator (command channel, user model, autopilot, six ways of sharing control), compares them, and derives and checks the delay stability boundary. |

The main report is `report/report.pdf`.

---

## 1. Folder map

```
pragyan_24250/
├── README.md                  this file
├── requirements.txt           exact package versions
├── src/
│   ├── part1_decoder.ipynb    Part 1 (run first)
│   ├── part2_shared_control.ipynb   Part 2 (run second)
│   ├── evaluate.py            Part 1 numbers without Jupyter (optional)
│   └── decoder/               decoder code used by Part 1
│       ├── data.py            loads BCI IV 2a through MOABB, 8–30 Hz filter, epochs
│       ├── pipeline.py        CSP + LDA, Platt calibration, run_subject()
│       └── metrics.py         ECE, reliability curve, decision latency
├── logs/
│   ├── decoder_models/        trained decoder for each subject (subject_01.joblib … subject_09.joblib)
│   ├── part1_run.log          Part 1 summary numbers
│   └── part2_run.log          Part 2 headline numbers
├── results/
│   ├── part1/
│   │   ├── summary_by_subject.csv   accuracy, kappa, ECE, latency per subject
│   │   ├── decoder_traces.csv       one row per test trial (input to Part 2)
│   │   └── figures/                 6 figures
│   └── part2/
│       ├── episodes.csv             log of all 32,400 simulated drives (input to Part 2)
│       ├── figures/                 17 figures (01_… to 17_…)
│       └── tables/                  11 CSV tables behind the report's results
└── report/
    ├── report.pdf             the main report
    └── report.tex             its LaTeX source
```

Everything in `logs/` and `results/` is already filled in from our own run. Running the notebooks again overwrites these files with identical (or, for a few continuous values, near-identical) results; see Section 5.

---

## 2. Setup (once)

You need **Python 3.12 or 3.13** (tested on 3.13) and an internet connection for the first run of Part 1.

All commands below are run from inside this folder (`pragyan_24250/`).

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Run the project

Run the two notebooks **in order**. Part 2 reads a file that Part 1 writes.

### Step 1 — Part 1, the decoder (about 5–10 minutes, plus the first download)

```bash
jupyter nbconvert --to notebook --execute --inplace src/part1_decoder.ipynb --ExecutePreprocessor.timeout=-1
```

On the first run, MOABB downloads BCI Competition IV dataset 2a (about 750 MB) into `~/mne_data`. If it asks to confirm the download location, answer yes. Later runs reuse the download.

This writes:
- `results/part1/summary_by_subject.csv` and `results/part1/decoder_traces.csv`
- `results/part1/figures/` (6 PNGs)
- `logs/decoder_models/` (9 trained decoders) and `logs/part1_run.log`

### Step 2 — Part 2, shared control (about 1 minute)

```bash
jupyter nbconvert --to notebook --execute --inplace src/part2_shared_control.ipynb --ExecutePreprocessor.timeout=-1
```

Part 2 needs no download. It reads `results/part1/summary_by_subject.csv`, `results/part1/decoder_traces.csv` and `results/part2/episodes.csv`, and writes:
- `results/part2/figures/` (17 PNGs) and `results/part2/tables/` (11 CSVs)
- `logs/part2_run.log`

### Prefer to read along?

Open the notebooks interactively instead (`jupyter notebook`, then open `src/`), and run all cells top to bottom. The notebooks find the project folder by themselves, so they work whether Jupyter is started in `pragyan_24250/` or in `src/`.

### Optional — Part 1 numbers without Jupyter

```bash
python -m src.evaluate
```

Prints the per-subject table and rewrites `results/part1/summary_by_subject.csv`. It gives the same numbers as the notebook.

---

## 4. What you should see (and where it is in the report)

Quick check: open `logs/part1_run.log` and `logs/part2_run.log` after the run.

**Part 1 — decoder (report Table `tab:decoder`, Section "The BCI Data Pipeline")**

| Quantity | Value | File |
|---|---|---|
| Mean calibrated accuracy (chance = 0.25) | 0.443 | `results/part1/summary_by_subject.csv` |
| Mean Cohen's kappa | 0.258 | same |
| Mean ECE, calibrated | 0.096 | same |
| Mean ECE, raw (as the report defines it) | 0.196 | `logs/part1_run.log` |

**Part 2 — shared control (report Section "Results")**

| Quantity | Value | File | Report |
|---|---|---|---|
| Success, user only | 0.119 | `tables/headline_main.csv` | Table `tab:headline` |
| Success, autopilot only | 1.000 | same | same |
| Success, adaptive (risk-gated) | 0.996 | same | same |
| Mean authority given to the user, adaptive | 0.118 | same | same |
| Adaptive minus user only, subject-level 95% CI | 0.878 [0.791, 0.957] | `tables/paired_subject_level.csv` | Table `tab:paired` |
| Subjects with significant error bursts | 0 of 9 | `logs/part2_run.log` | Table `tab:markov` |
| Pooled confidence AUC | 0.676 | `logs/part2_run.log` | Section "Calibration" |

**Part 2 — stability (report Section "Stability results", Tables `tab:stability`, `tab:pade`, `tab:checks`)**

| Quantity | Value | File |
|---|---|---|
| LQR gains K1, K2 | 3.162, 1.885 | `logs/part2_run.log` |
| τ_max at α = 1 | 0.529 s | `tables/tau_max_formula_vs_simulation.csv` |
| Delay-independent below α* | 0.441 | `logs/part2_run.log` |
| Heading loop: α*, τ_max(1) | 0.613, 0.647 s | `logs/part2_run.log` |
| Formula vs direct DDE simulation | agree to better than 1e-5 (relative) | `tables/tau_max_formula_vs_simulation.csv` |

Figures for every result above are in `results/part1/figures/` and `results/part2/figures/`; the file names give the notebook section they come from (for example `14_s6_success_vs_kappa.png` is the headline plot from Section 6.9, success versus decoder quality).

---

## 5. Notes for checking

- **Why Part 2 reads a saved drive log.** All experiments together are 32,400 simulated drives (the main comparison alone is 3,240 = 9 subjects × 6 sharing rules × 3 rooms × 20 seeds; the rest are the authority sweep, the burstiness sweep and the ablations), which took hours on the original simulator. `results/part2/episodes.csv` is that log. Part 2 does not just trust it: Section 6.4 of the notebook re-simulates 72 drives from scratch with the notebook's own code and checks they match the log. Expected: *72 of 72 same outcome, time and decisions*, largest relative difference about 1e-9 (floating-point rounding across machines).
- **Two raw-ECE numbers.** Part 1 shows two raw ECE values. 0.162 scores the raw confidence against the raw prediction; 0.196 scores it against the calibrated prediction, which is the decision the wheelchair actually uses. The report uses 0.196. The notebook prints both side by side.
- **Small differences on another computer.** Decoder numbers are rounded to 4 decimals and should match exactly. Continuous simulation values (times, risk) may differ in the 9th significant digit on a different CPU or library build; this does not change any number shown in the report.
- **MATLAB cross-check.** The report's independent MATLAB verification of the stability boundary (the figure titled "Independent MATLAB verification") was a separate check and is not part of this run; the Python stability results it confirms are reproduced in Part 2, Section 7.
- **Random seeds** are fixed (decoder seed 20260901, simulation seeds 0–19), so reruns give the same results.
