import zlib
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class InertiaResult:
    """Result container for the Informational Inertia analyzer."""
    I_bar: float     # irreducible variance fraction
    I_comp: float    # compression resistance proxy
    entropy: float   # entropy proxy (histogram-based)
    values: np.ndarray

    def plot(self):
        plt.figure(figsize=(6, 3))
        plt.plot(self.values, label="signal")
        plt.title(f"Informational Inertia Ī = {self.I_bar:.3f}")
        plt.legend()
        plt.tight_layout()
        plt.show()


def compression_resistance(data, level: int = 9) -> float:
    """
    Compression-resistance estimator.

    Note: because raw float bytes are often hard to compress, this proxy is
    best treated as a rough heuristic. (Later we can add quantization or a
    symbolic encoding step if you want it to behave more intuitively.)
    """
    x = np.asarray(data, dtype=np.float64).ravel()
    raw = x.tobytes()
    raw_size = len(raw)
    if raw_size == 0:
        return 0.0

    comp = zlib.compress(raw, level=level)
    return float(1.0 - (len(comp) / raw_size))


def shannon_entropy_hist(x, bins: int = 50) -> float:
    """
    Histogram-based entropy proxy.

    Uses a discrete histogram approximation of differential entropy.
    This can be negative (that's normal for differential entropy proxies).
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    if x.size == 0:
        return 0.0

    hist, _ = np.histogram(x, bins=bins, density=True)
    hist = hist[hist > 0]
    return float(-np.sum(hist * np.log(hist)))


def irreducible_energy_linear(data) -> float:
    """
    Irreducibility proxy: residual variance after best linear fit.
    """
    x = np.asarray(data, dtype=np.float64).ravel()
    n = x.size
    if n < 2:
        return 0.0

    t = np.arange(n, dtype=np.float64)
    coeffs = np.polyfit(t, x, 1)
    trend = np.polyval(coeffs, t)
    residual = x - trend
    return float(np.var(residual))


def analyze(path: str, *, bins: int = 50) -> InertiaResult:
    """
    Minimal analyzer.

    Loads a 1D CSV signal and returns:
      - entropy proxy (histogram-based)
      - irreducibility proxy I_bar (linear residual variance / total variance)
      - compression resistance proxy I_comp (zlib on float bytes)
    """
    data = np.loadtxt(path, delimiter=",")
    data = np.asarray(data, dtype=np.float64).ravel()

    I_comp_value = compression_resistance(data)
    entropy_value = shannon_entropy_hist(data, bins=bins)

    irreducible = irreducible_energy_linear(data)
    total = float(np.var(data) + 1e-12)
    I_bar_value = float(irreducible / total)

    return InertiaResult(
        I_bar=I_bar_value,
        I_comp=I_comp_value,
        entropy=entropy_value,
        values=data,
    )
