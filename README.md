# Convex Fair Partition for Biomedical Scaffolds

This README presents the English only version.

---

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
---

## Installation
Use Python version 3.10 or newer. Install the following libraries: NumPy, SciPy, scikit learn, Shapely, Matplotlib, Pandas, TQDM.

```
python -m venv .venv
# Windows: .venv\Scriptsctivate
# macOS or Linux:
source .venv/bin/activate
pip install -U pip
pip install numpy scipy scikit-learn shapely matplotlib pandas tqdm
```

---

## Methods

### Lloyd stage with fuzzy centroid and learned sigma
Compute coordinate means x bar and y bar for the convex cell vertices. Define axis wise Gaussian memberships

- mu_x(x_i) = exp(−(x_i − x_bar)^2 / (2 sigma^2))  
- mu_y(y_i) = exp(−(y_i − y_bar)^2 / (2 sigma^2))

Compute the centroid as weighted averages

- x_c = sum(mu_x * x_i) / sum(mu_x)  
- y_c = sum(mu_y * y_i) / sum(mu_y)

Round both coordinates to four decimals for deterministic stopping checks.

**Learning sigma**  
Represent each polygon with geometric descriptors such as perimeter, area, number of sides, angle mean, angle standard deviation, circularity, diagonal ratio, principal component aspect ratio, start angle, and normalized start radius. Train Multiple Regression, Support Vector Regression, and Elastic Net. A simple deployment rule is sigma equals kappa times the square root of area in order to separate size from shape when needed.

### Normal flow with adaptive delta
Two policies are considered.

**Fixed schedule**  
Delta equals 5e−3 for the first ten iterations, then 4e−4 until iteration twenty, then 5e−5 until convergence.

**Adaptive policy**  
A scale aware base step uses hull scale and machine epsilon so forward differences are resolvable. An edge cap limits the step at intermediate edge points to at most twenty five percent of the incident edge length. Use a clip operator to enforce lower and upper bounds. Reject steps that would cross the hull.

---

## Reproducible Dataset
1) Polygons: generate five hundred convex polygons by sampling eight points uniformly in a ten by ten square, then take the convex hull.  
2) Seeds: use five thousand random seeds per configuration for initial Voronoi centers.  
3) Region counts: for Lloyd experiments use three through ten regions. For normal flow comparisons use five through ten and also fifteen and thirty and fifty and one hundred.  
4) Metrics: wall time in seconds, repetition count, and total Lloyd iterations.  
5) Reference environment: Intel Xeon at 2.20 GHz, memory 13.61 GB, Ubuntu 22.04.4 LTS.

---

## Experiments and How to Test  
Only Experiments B and C are included. Experiments A and D are removed.

### Experiment B: Sigma prediction models for the Lloyd stage

**Goal**  
Learn a data driven mapping from polygon features to a suitable sigma so Lloyd updates converge stably with fewer iterations.

**Data split and protocol**  
- Instances: five hundred convex polygons as described above  
- Labels: for each polygon define sigma star as the value that maximizes stability and progress on a calibration table  
- Seeds: five thousand initializations per configuration to average out sensitivity  
- Split: five fold cross validation with a fixed global seed, stratified by coarse bins of region count

**Features**  
Perimeter, area, number of sides, angle mean, angle standard deviation, circularity, diagonal ratio, PCA aspect ratio of the vertex cloud, start angle, normalized start radius, and optionally the square root of area to decouple size from shape.

**Models and hyperparameters**  
Multiple Linear Regression with ridge like regularization chosen by inner cross validation.  
Support Vector Regression with RBF kernel and a grid over C, gamma, and epsilon.  
Elastic Net with a grid over alpha and l1 ratio.  
Baseline rule sigma equals kappa times square root of area with kappa tuned by cross validation.

**Evaluation metrics**  
Primary metrics are RMSE of sigma prediction and Spearman rank correlation between predicted sigma and sigma star.  
Secondary metrics are the induced Lloyd performance when plugging the predicted sigma back into the pipeline including total iterations, repetition count, and wall time.

**Outputs**  
- File `results/expB_sigma_models.csv` with columns  
  `polygon_id, model, fold, sigma_star, sigma_pred, rmse_fold, spearman_fold`  
- Trained model files per fold and a final refit on all data  
- Plots  
  - Predicted sigma versus target sigma with a y equals x reference line  
  - Iterations versus regions when using predicted sigma compared with the baseline rule  
  - Wall time versus regions with log y for a Lloyd only pass with predicted sigma

**Reproducibility and logging**  
Log `global_seed, fold_seed, model_config_hash, feature_set_hash`.  
Use four decimal rounding for centroid coordinates.  
Save all cross validation splits and seeds to `results/expB_cv_splits.json`.

---

### Experiment C: Normal flow delta policies

**Goal**  
Compare the fixed step schedule against the adaptive scale aware edge capped policy while keeping the upstream Lloyd stage constant.

**Policies**  
- Fixed schedule as defined above  
- Adaptive policy with scale aware base step, edge cap of twenty five percent of edge length at edge midpoints, and clipped bounds for interior and vertex updates

**Test grid**  
- Regions: five to ten, fifteen, thirty, fifty, one hundred  
- Seeds: reuse the best Lloyd seeds per instance to isolate the effect of delta  
- Instances: the same five hundred polygons

**Stopping and safety criteria**  
Convergence when the objective change is below tolerance or when the iteration cap is reached.  
Overshoot rollback when an update crosses an edge or increases the objective beyond a small margin, then halve the step for that point.  
Failure when halving reaches delta minimum with no progress for a set number of checks.


