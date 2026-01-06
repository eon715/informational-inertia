import zlib
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


# -------------------------
# Public result container
# -------------------------

@dataclass
class InertiaResult:
    """
    Result container for the Informational Inertia analyzer.
    """
    I_bar: float      # irreducible variance fraction (0..~1)
    I_comp: float     # compression resistance proxy (0..~1)
    entropy: float    # histogram-based differential-entropy proxy (can be negative)
    values: np.ndarray

    def plot(self):
        plt.figure(figsize=(6, 3))
        plt.plot(self.values, label="signal")
        plt.title(f"Informational Inertia Ī = {self.I_bar:.3f}")
        plt.legend()
        plt.tight_layout()
        plt.show()


# -------------------------
# Metric helpers
# -------------------------

def compression_resistance(data, *, level: int = 9) -> float:
    """
    Compression-resistance estimator (zlib applied to raw float64 bytes).

    Important: float byte streams often compress poorly; treat this as a heuristic.
    """
    x = np.asarray(data, dtype=np.float64).ravel()
    raw = x.tobytes()
    if len(raw) == 0:
        return 0.0

    comp = zlib.compress(raw, level=level)
    return float(1.0 - (len(comp) / len(raw)))


def shannon_entropy_hist(data, *, bins: int = 50) -> float:
    """
    Histogram-based entropy proxy.

    Uses density=True histogram as a differential-entropy-like proxy.
    This can be negative; that's normal for differential entropy proxies.
    """
    x = np.asarray(data, dtype=np.float64).ravel()
    if x.size == 0:
        return 0.0

    hist, _ = np.histogram(x, bins=bins, density=True)
    p = hist[hist > 0]
    return float(-np.sum(p * np.log(p)))


def _total_variance(data) -> float:
    x = np.asarray(data, dtype=np.float64).ravel()
    # epsilon prevents divide-by-zero when the signal is constant
    return float(np.var(x) + 1e-12)


def irreducible_fraction_linear(data) -> float:
    """
    Linear irreducibility proxy:
      Ī = var(x - best_linear_fit(x)) / var(x)
    """
    x = np.asarray(data, dtype=np.float64).ravel()
    n = x.size
    if n < 2:
        return 0.0

    t = np.arange(n, dtype=np.float64)
    coeffs = np.polyfit(t, x, 1)
    fit = np.polyval(coeffs, t)
    residual = x - fit

    return float(np.var(residual) / _total_variance(x))


def irreducible_fraction_poly(data, *, max_degree: int = 5) -> float:
    """
    Polynomial irreducibility proxy (Option B):
      Fit degrees 1..max_degree and take the BEST fit (smallest residual variance).
      Ī = min_d var(x - polyfit_d(x)) / var(x)

    Interpretation:
      - If structure is explainable by low-degree polynomials (trend/curvature),
        Ī decreases.
      - If structure survives these fits, Ī stays higher.
    """
    x = np.asarray(data, dtype=np.float64).ravel()
    n = x.size
    if n < 2:
        return 0.0

    t = np.arange(n, dtype=np.float64)
    denom = _total_variance(x)

    # cap degree so polyfit doesn't blow up on short signals
    max_degree = int(max(1, min(max_degree, n - 1)))

    residual_vars = []
    for d in range(1, max_degree + 1):
        coeffs = np.polyfit(t, x, d)
        fit = np.polyval(coeffs, t)
        residual_vars.append(np.var(x - fit))

    return float(min(residual_vars) / denom)


# -------------------------
# Main API
# -------------------------

def analyze(
    path: str,
    *,
    bins: int = 50,
    mode: str = "linear",     # "linear" or "poly"
    max_degree: int = 5,
    comp_level: int = 9,
) -> InertiaResult:
    """
    Load a 1D CSV signal and compute:
      - entropy proxy (histogram-based)
      - Ī (irreducible variance fraction)
      - compression resistance proxy

    Parameters
    ----------
    path : str
        CSV path (1D values).
    bins : int
        Histogram bins for entropy proxy.
    mode : str
        "linear" uses a best linear fit residual.
        "poly" uses degrees 1..max_degree and takes best residual.
    max_degree : int
        Only used when mode="poly".
    comp_level : int
        zlib compression level for compression_resistance.
    """
    data = np.loadtxt(path, delimiter=",")
    data = np.asarray(data, dtype=np.float64).ravel()

    I_comp_value = compression_resistance(data, level=comp_level)
    entropy_value = shannon_entropy_hist(data, bins=bins)

    if mode == "poly":
        I_bar_value = irreducible_fraction_poly(data, max_degree=max_degree)
    else:
        # default to linear so you don't break existing notebooks
        I_bar_value = irreducible_fraction_linear(data)

    return InertiaResult(
        I_bar=float(I_bar_value),
        I_comp=float(I_comp_value),
        entropy=float(entropy_value),
        values=data,
    )
