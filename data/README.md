# Data

This project uses **BCI Competition IV, Dataset 2a**, a public motor-imagery EEG dataset recorded at Graz University of Technology.

- **Subjects:** 9
- **Task:** imagine moving the left hand, right hand, both feet, or the tongue (4 classes)
- **Signals:** 22 EEG channels (plus 3 EOG channels), sampled at 250 Hz
- **Sessions:** 2 per subject, recorded on different days, with 288 trials each

## The data is not stored in this repository

The dataset is about 750 MB, which is too large for GitHub. The first run of `src/part1_decoder.ipynb` downloads it automatically through [MOABB](https://moabb.neurotechx.com/) (dataset name `BNCI2014_001`) into `~/mne_data`. Later runs reuse that download, so you don't need to put any files in this folder.

## Sources

* [BCI Competition IV download page](https://www.bbci.de/competition/iv/download)
* [Dataset 2a description (PDF)](https://www.bbci.de/competition/iv/desc_2a.pdf)

If you use this data, cite: Tangermann et al., "Review of the BCI Competition IV", *Frontiers in Neuroscience*, 2012.
