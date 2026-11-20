# Part 1 without the notebook: python -m src.evaluate (from the project root)
from pathlib import Path

import pandas as pd

from src.decoder.pipeline import run_subject


def main():
    rows = []
    for sub in range(1, 10):
        s = run_subject(sub)["summary"]
        print(f"S{sub}: acc {s['calib_acc']:.3f}  kappa {s['kappa']:.3f}  "
              f"censored {s['censored_fraction']:.3f}")
        rows.append(s)

    out = Path("results/part1")
    out.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows).round(4)
    df.to_csv(out / "summary_by_subject.csv", index=False)
    print("\n" + df.to_string(index=False))


if __name__ == "__main__":
    main()
