# Convex Fair Partition for Biomedical Scaffolds

This repository presents a stronger Convex Fair Partition workflow for scaffold design in tissue engineering. The workflow stabilizes both stages of the pipeline.

First, Lloyd updates use a Gaussian weighted or “fuzzy” centroid. The scale parameter sigma is chosen from polygon features. This reduces oscillation in skewed or boundary clipped cells and lowers the repetition count.

Second, the normal flow stage uses an adaptive step size delta that is scale aware and edge capped. Forward difference probes remain numerically resolvable and safe near boundaries. On five hundred convex polygons with five thousand random seeds per configuration, the learned sigma centroid yields about ninety nine percent time reduction at four regions while remaining competitive at seven to ten regions. The adaptive delta reduces iterations and wall time for six or more regions by about twenty to thirty five percent and up to about thirty seven percent for larger sizes.

## Project Structure

Create the following layout in your repository. The code files can be added later.

```
.
├─ src/
│  ├─ lloyd/
│  │  ├─ fuzzy_centroid.py
│  │  └─ learn_sigma.py
│  ├─ normal_flow/
│  │  ├─ delta_fixed.py
│  │  └─ delta_adaptive.py
│  ├─ features/
│  │  └─ polygon_features.py
│  └─ pipeline/
│     └─ run_cfp.py
├─ experiments/
│  ├─ exp_lloyd_centroid.yaml
│  ├─ exp_sigma_models.yaml
│  ├─ exp_normalflow_delta.yaml
│  └─ exp_end2end.yaml
├─ data/
├─ results/
└─ README.md
```

## Installation

Use Python version 3.10 or newer. Required libraries are NumPy, SciPy, scikit learn, Shapely, Matplotlib, Pandas, and TQDM.

1) Create a virtual environment.  
2) Activate the environment.  
3) Upgrade pip with `pip install -U pip`.  
4) Install the packages with `pip install numpy scipy scikit-learn shapely matplotlib pandas tqdm`.

## Methods

### Lloyd stage with fuzzy centroid

Given convex cell vertices, compute coordinate means x bar and y bar. Define memberships

- mu_x(x_i) = exp(−(x_i − x_bar)^2 / (2 sigma^2))
- mu_y(y_i) = exp(−(y_i − y_bar)^2 / (2 sigma^2))

Compute the centroid as weighted averages:

- x_c = sum(mu_x * x_i) / sum(mu_x)
- y_c = sum(mu_y * y_i) / sum(mu_y)

Round both coordinates to four decimals for deterministic stopping tests.

#### Learning sigma

Represent each polygon using geometric descriptors including perimeter, angle mean, angle standard deviation, circularity, diagonal ratio, principal component aspect ratio, orientation of a canonical start vertex, normalized start radius, area, and number of sides. Train Multiple Regression, Support Vector Regression, and Elastic Net to predict a suitable sigma. A simple deployment rule is sigma equals kappa times the square root of area when size effects must be separated from shape.

### Normal flow with adaptive delta

Two policies are considered. The fixed schedule uses delta equal to 5e−3 for the first ten iterations, then 4e−4 until iteration twenty, then 5e−5 until convergence. The adaptive policy is scale aware and uses hull bounds together with machine epsilon to keep forward differences resolvable. It also applies an edge cap on intermediate edge points so the step never exceeds a quarter of the incident edge length. A clip operator enforces lower and upper bounds.

## Reproducible Dataset

1) Polygons: generate five hundred convex polygons by sampling eight points uniformly in a ten by ten square, then take the convex hull.  
2) Seeds: use five thousand random seeds per configuration for initial Voronoi centers.  
3) Region counts: for Lloyd experiments use three through ten regions. For normal flow comparisons use five through ten and also fifteen and thirty and fifty and one hundred.  
4) Metrics: wall time in seconds, repetition count, and total Lloyd iterations.  
5) Reference environment: Intel Xeon at 2.20 GHz, memory 13.61 GB, Ubuntu 22.04.4 LTS.

## Experiments and How to Test

### Experiment A: Lloyd with fuzzy centroid and sigma sweep

Goal: measure stability and speed from Gaussian weighted centroids and build a calibration table over sigma from one to two hundred fifty.

Procedure: for every polygon and seed compute fuzzy centroid using the formulas above and apply rounding to four decimals. Sweep sigma across the range. Record per iteration convergence diagnostics and aggregate runtime, repetition, and total Lloyd iterations per region.

Baselines: uniform polygon centroid and any existing centroid heuristics.

Outputs: write `results/expA_sigma_sweep.csv` and plots of time versus regions and total iterations versus regions using logarithmic y axes.

### Experiment B: Sigma prediction models

Goal: learn a mapping from polygon shape to sigma.

Procedure: from Experiment A choose sigma* that optimizes stability and progress for each polygon. Train Multiple Regression, SVR, and Elastic Net with cross validation. Report root mean squared error and rank correlation between predicted sigma and sigma*.

Outputs: write `results/expB_sigma_models.csv` and save trained model files.

### Experiment C: Normal flow delta policies

Goal: compare the fixed schedule and the adaptive policy that is scale aware and edge capped.

Procedure: start from the best Lloyd seeds from either uniform or learned sigma. Run normal flow under each policy. Measure iterations, wall time, overshoot rollbacks, and failure rate. Use the region counts listed in the dataset section.

Outputs: write `results/expC_delta_compare.csv` and plot normal flow time versus regions on a logarithmic y axis. Report percent time reduction relative to the fixed variant.

### Experiment D: End to end CFP with scaffold constraints

Goal: integrate learned sigma Lloyd updates and adaptive delta normal flow in one pipeline with two checkpoints.

Procedure: initialize the polygon and scale it to manufacturing bounds. Apply light jitter to seeds. Run Lloyd with learned sigma and check a geometric error tolerance. If the tolerance is met, run normal flow with the adaptive delta and then rescale. If the tolerance is not met, keep the best seeds, apply light re randomization, and rerun Lloyd before returning to the normal flow stage.

Outputs: write `results/expD_end2end.csv` and export final partition geometries for qualitative inspection.

## Quick Start Run Order

1) Prepare the dataset in the `data` folder.  
2) Run the experiments in order A, B, C, then D with your runner script.  
3) Each run writes exactly one CSV into `results` and plots that reproduce the logarithmic y figures for time and iteration counts.

## Notes for Contributors

Keep functions pure when possible. Use deterministic rounding where it affects stopping tests. Always log the random seed and a configuration hash for each run. Write one CSV per experiment with the fields runtime_sec, repetition_max, lloyd_iter_total, success_flag, and a configuration hash.
