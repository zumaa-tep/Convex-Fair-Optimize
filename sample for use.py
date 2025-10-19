from dbm.dumb import error
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import copy
import time, timeit
import skfuzzy as fuzz
from scipy.spatial import Voronoi
import pandas as pd
from scipy.spatial import ConvexHull
from matplotlib.path import Path
from matplotlib import cm
from numpy.ma.core import sqrt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import path
import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
import concurrent.futures
import ctypes
import glob
import functools
import random # Import the random module

def log_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🛈 Entering `{func.__name__}`")
        result = func(*args, **kwargs)
        print(f"✔ Exiting  `{func.__name__}`")
        return result
    return wrapper

import os, json, math, warnings
from typing import Dict, List, Tuple, Optional
from itertools import combinations
import numpy as np

warnings.filterwarnings("ignore", category=RuntimeWarning)
np.set_printoptions(suppress=True)

def _np(a):
    return np.asarray(a, dtype=float)

def close_polygon(P: np.ndarray) -> np.ndarray:
    P = _np(P)
    if len(P) >= 2 and not np.allclose(P[0], P[-1]):
        return np.vstack([P, P[0]])
    return P

def perimeter(P: np.ndarray) -> float:
    Pc = close_polygon(P)
    return float(np.sum(np.linalg.norm(np.diff(Pc, axis=0), axis=1)))

def area(P: np.ndarray) -> float:
    P = _np(P)
    x, y = P[:, 0], P[:, 1]
    return float(abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) * 0.5)

def centroid(P: np.ndarray) -> Tuple[float, float]:
    P = _np(P)
    x, y = P[:,0], P[:,1]
    cross = x * np.roll(y, -1) - y * np.roll(x, -1)
    A = np.sum(cross) / 2.0
    if abs(A) < 1e-18:
        c = P.mean(axis=0)
        return float(c[0]), float(c[1])
    cx = np.sum((x + np.roll(x, -1)) * cross) / (6.0 * A)
    cy = np.sum((y + np.roll(y, -1)) * cross) / (6.0 * A)
    return float(cx), float(cy)

def angles(P: np.ndarray) -> np.ndarray:
    """มุมภายใน (เรเดียน) ของรูปหลายเหลี่ยม"""
    P = _np(P); n = len(P)
    angs = np.zeros(n)
    for i in range(n):
        p_prev, p_cur, p_next = P[(i-1) % n], P[i], P[(i+1) % n]
        v1 = p_prev - p_cur
        v2 = p_next - p_cur
        a = np.linalg.norm(v1); b = np.linalg.norm(v2)
        if a < 1e-18 or b < 1e-18:
            angs[i] = np.nan; continue
        v1 /= a; v2 /= b
        dotp = float(np.clip(np.dot(v1, v2), -1.0, 1.0))
        angs[i] = math.acos(dotp)
    return angs

def angle_mean(P: np.ndarray) -> float:
    angs = angles(P); angs = angs[np.isfinite(angs)]
    return float(np.mean(angs)) if angs.size else np.nan

def angle_std(P: np.ndarray) -> float:
    angs = angles(P); angs = angs[np.isfinite(angs)]
    return float(np.std(angs)) if angs.size else np.nan

def circularity(P: np.ndarray) -> float:
    A = area(P); per = perimeter(P)
    if per == 0: return np.nan
    return 4.0 * math.pi * A / (per ** 2)

def diagonal_ratio(P: np.ndarray) -> float:
    """max(diag)/min(diag) ระหว่างคู่จุดที่ไม่ติดกัน (n>=4)"""
    P = _np(P); n = len(P)
    if n < 4: return np.nan
    dists = []
    for i, j in combinations(range(n), 2):
        if abs(i - j) in (1, n-1):  # ข้ามขอบ
            continue
        dists.append(np.linalg.norm(P[i] - P[j]))
    if not dists: return np.nan
    dists = np.asarray(dists)
    dmin, dmax = dists.min(), dists.max()
    if dmin < 1e-18: return 1e12  # กัน inf
    return float(dmax / dmin)

def bbox_aspect(P: np.ndarray) -> float:
    P = _np(P)
    xmin, ymin = P.min(axis=0); xmax, ymax = P.max(axis=0)
    w, h = xmax - xmin, ymax - ymin
    if h < 1e-18: return 1e12   # กัน inf
    return float(w / h)

def pca_aspect(P: np.ndarray) -> float:
    X = _np(P)
    Xc = X - X.mean(axis=0, keepdims=True)
    C = np.cov(Xc.T)
    vals = np.real(np.linalg.eigvals(C))
    vmin, vmax = float(np.min(vals)), float(np.max(vals))
    if vmin < 1e-18: return 1e12  # กัน inf
    return float(np.sqrt(vmax / vmin))

def start_angle(P: np.ndarray) -> float:
    cx, cy = centroid(P)
    v = _np(P[0]) - np.array([cx, cy], dtype=float)
    return float(np.arctan2(v[1], v[0]))

def start_radius_norm(P: np.ndarray) -> float:
    cx, cy = centroid(P)
    d = np.linalg.norm(_np(P) - np.array([cx, cy]), axis=1)
    Rmax = float(np.max(d))
    if Rmax < 1e-18: return 0.0
    r0 = float(np.linalg.norm(_np(P[0]) - np.array([cx, cy])))
    return float(r0 / Rmax)

def n_sides(P: np.ndarray) -> int:
    return int(len(P))

DEFAULT_FEATURE_ORDER = [
    "perimeter",
    "angle_mean",
    "angle_std",
    "circularity",
    "diagonal_ratio",
    "aspect_bbox",
    "aspect_pca",
    "start_angle",
    "start_radius_norm",
    "area",
    "n_sides"
]

def compute_features_dict(P: np.ndarray) -> Dict[str, float]:
    """คำนวณฟีเจอร์ทั้งหมด (dict)"""
    feats = {
        "perimeter": perimeter(P),
        "angle_mean": angle_mean(P),
        "angle_std": angle_std(P),
        "circularity": circularity(P),
        "diagonal_ratio": diagonal_ratio(P),
        "aspect_bbox": bbox_aspect(P),
        "aspect_pca": pca_aspect(P),
        "start_angle": start_angle(P),
        "start_radius_norm": start_radius_norm(P),
        "area": area(P),
        "n_sides": n_sides(P),
    }
    # แปลง non-finite -> 0.0 เป็น safety net เวลา infer
    for k, v in feats.items():
        if not np.isfinite(v):
            feats[k] = 0.0
    return feats

def _load_json(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def build_feature_vector(P: np.ndarray,
                         feature_order: Optional[List[str]] = None,
                         medians: Optional[Dict[str, float]] = None) -> np.ndarray:
    """
    สร้างเวกเตอร์ฟีเจอร์ตามลำดับ feature_order
    - ถ้า medians มีให้ จะใช้แทนค่าที่ไม่ finite/ไม่มี
    """
    d = compute_features_dict(P)
    order = feature_order or DEFAULT_FEATURE_ORDER
    vec = []
    for key in order:
        val = d.get(key, np.nan)
        if not np.isfinite(val):
            if medians and key in medians and np.isfinite(medians[key]):
                val = float(medians[key])
            else:
                val = 0.0
        vec.append(float(val))
    return np.array(vec, dtype=float)

# ------------------------ Predictor ------------------------
MODEL_FILES = {
    "elasticnet": "/content/drive/Shareddrives/เก็บข้อมูล 1000/file call/model_elasticnet.joblib",
    "linear":     "/content/drive/Shareddrives/เก็บข้อมูล 1000/file call/model_linear.joblib",
    "svr":        "/content/drive/Shareddrives/เก็บข้อมูล 1000/file call/model_svr.joblib",
    "nn_sklearn":   "/content/drive/Shareddrives/เก็บข้อมูล 1000/file call/model_nn.keras",
    "nn_sklearn1": "/content/drive/Shareddrives/เก็บข้อมูล 1000/file call/model_nn_sklearn.joblib",
}
SCALER_NN_FILE = "scaler_nn.joblib"
FEATURE_NAMES_FILE = "feature_names.json"     # บันทึกจากตอนเทรน
FEATURE_MEDIANS_FILE = "feature_medians.json" # บันทึกจากตอนเทรน (median อิมพิวท์)

def _detect_available_model(models_dir: str) -> Tuple[str, str]:
    """เลือกโมเดลที่มีอยู่ตามลำดับความเหมาะสม"""
    priority = ["elasticnet", "linear", "svr", "nn_keras", "nn_sklearn"]
    for k in priority:
        path = os.path.join(models_dir, MODEL_FILES[k])
        if os.path.exists(path):
            return k, path
    raise FileNotFoundError("ไม่พบไฟล์โมเดลที่รองรับในโฟลเดอร์ที่กำหนด")

def _load_feature_meta(models_dir: str) -> Tuple[List[str], Optional[Dict[str, float]]]:
    names = _load_json(os.path.join(models_dir, FEATURE_NAMES_FILE))
    meds  = _load_json(os.path.join(models_dir, FEATURE_MEDIANS_FILE))
    feature_order = names.get("feature_names", DEFAULT_FEATURE_ORDER) if isinstance(names, dict) else DEFAULT_FEATURE_ORDER
    return feature_order, meds if isinstance(meds, dict) else None

def predict_sigma(coords: np.ndarray,
                  model: str = "auto",
                  models_dir: str = ".") -> float:

    P = _np(coords).reshape(-1, 2)
    if P.shape[0] < 3:
        raise ValueError("ต้องมีจุดอย่างน้อย 3 จุด")

    # โหลดข้อมูลประกอบฟีเจอร์
    feature_order, medians = _load_feature_meta(models_dir)
    x = build_feature_vector(P, feature_order, medians).reshape(1, -1)

    # เลือกโมเดล
    if model == "auto":
        model_key, model_path = _detect_available_model(models_dir)
    else:
        if model not in MODEL_FILES:
            raise ValueError(f"model ต้องเป็น {list(MODEL_FILES.keys())} หรือ 'auto'")
        model_key = model
        model_path = os.path.join(models_dir, MODEL_FILES[model_key])
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ไม่พบไฟล์โมเดล: {model_path}")

    # โหลดและพยากรณ์
    if model_key in ("elasticnet", "linear", "svr", "nn_sklearn"):
        from joblib import load
        pipe = load(model_path)  # pipeline มี scaler ภายในเรียบร้อย
        yhat = float(pipe.predict(x).ravel()[0])
        return yhat

    elif model_key == "nn_keras":
        # ต้องมี scaler แยก
        from joblib import load
        import tensorflow as tf
        scaler_path = os.path.join(models_dir, SCALER_NN_FILE)
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"ไม่พบสเกลเลอร์ของ NN: {scaler_path}")
        scaler = load(scaler_path)
        Xs = scaler.transform(x)
        model_keras = tf.keras.models.load_model(model_path)
        yhat = float(model_keras.predict(Xs, verbose=0).ravel()[0])
        return yhat

    else:
        raise RuntimeError("ชนิดโมเดลไม่รองรับ")

trial_id = 35
round = 35

local_path  = f'/content/k99/regions_coordinates_{trial_id}_{round}.csv'           # ไฟล์ต้นทาง
drive_dir   = '/content/drive/Shareddrives/เก็บข้อมูล 1000/js conf 2'     # โฟลเดอร์ปลายทางใน Drive

for number_of_regions in range(3,4):
  for order in range(500):
    polygon = np.random.uniform(-10, 10, (8,2))
    a = []
    for i in range(100000):
      seed = np.random.randint(0,1000000)
      a.append(seed)

    _, _, _, pass_key = Equipartition.partition(polygon,number_of_regions,trial_id,round,order,a)

    if pass_key != 0:
      linear_fuzz_Equipartition.partition(polygon,number_of_regions,trial_id,round,order,a)
      svr_fuzz_Equipartition.partition(polygon,number_of_regions,trial_id,round,order,a)
      elasticnet_fuzz_Equipartition.partition(polygon,number_of_regions,trial_id,round,order,a)
      nn_pred_fuzz_Equipartition.partition(polygon,number_of_regions,trial_id,round,order,a)

    # Factor_Equipartition.partition(polygon,number_of_regions,trial_id,round,order,a)
    Cendif_Equipartition.partition(polygon,number_of_regions,trial_id,round,order,a)

    os.makedirs(drive_dir, exist_ok=True)
    shutil.copy2(local_path, drive_dir)
