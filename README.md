# Convex Fair Partition for Biomedical Scaffolds

## Overview
This repository strengthens the Convex Fair Partition workflow for scaffold design in tissue engineering. The Lloyd stage uses a Gaussian weighted centroid with a learned sigma from polygon features to improve stability and reduce oscillation. The normal flow stage uses an adaptive step size delta that is scale aware and edge capped so forward differences remain numerically resolvable and safe near boundaries.  
On five hundred convex polygons with five thousand random seeds per configuration the learned sigma centroid delivers very large time savings at four regions and remains competitive at seven to ten regions. The adaptive delta reduces iterations and wall time for six or more regions by about twenty to thirty five percent and up to about thirty seven percent for larger sizes.

---

## Project Structure
```
├─ experiments/
│  ├─ exp_sigma_models
│  │  ├─ fuzzy_centroid.py
│  │     ├─ mutiple
│  │     ├─ svr
│  │     ├─ elastic
│  │  
│  └─ exp_normalflow_delta
│  │  ├─ delta_fixed.py
│  │  └─ delta_adaptive.py
│
├─ scaffolds (Future work)
```

---

## Installation
Use Python version 3.10 or newer. Install the following libraries: NumPy, SciPy, scikit learn, Shapely, Matplotlib, Pandas, TQDM.

for more detail https://drive.google.com/drive/folders/1FP7-zI_b0xvFNCW_srfofHUaVRmqUCcV?usp=sharing

