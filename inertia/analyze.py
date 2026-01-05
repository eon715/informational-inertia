import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class InertiaResult:
    I_bar: float
    entropy: float
    values: np.ndarray

    def plot(self):
        plt.figure(figsize=(6, 3))
        plt.plot(self.values, label="signal")
        plt.title(f"Informational Inertia Ī = {self.I_bar:.3f}")
        plt.legend()
        plt.tight_layout()
        plt.show()


def _shannon_entropy(x, bins=50):
    hist, _ = np.histogram(x, bins=bins, density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log(hist))


def analyze(path):
    """
    Minimal v0.1 analyzer.

    Loads a 1D CSV signal and returns:
    - entropy proxy
    - simple irreducibility proxy
    """

    data = np.loadtxt(path, delimiter=",")
    data = np.asarray(data).flatten()

    entropy = _shannon_entropy(data)

    # Irreducibility proxy:
    # variance not explained by linear trend
    t = np.arange(len(data))
    coeffs = np.polyfit(t, data, 1)
    trend = np.polyval(coeffs, t)

    residual = data - trend
    irreducible_energy = np.var(residual)
    total_energy = np.var(data) + 1e-12

    I_bar = irreducible_energy / total_energy

    return InertiaResult(
        I_bar=float(I_bar),
        entropy=float(entropy),
        values=data,
    )
