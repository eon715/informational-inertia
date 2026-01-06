# tests/golden_baseline.py
"""
Golden baseline test (v0.1.x)

Goal:
- Reproduce a stable, human-readable baseline on each run.
- Not a strict unit test (no hard-coded numeric asserts).
- Useful for quick "is it still working?" checks after edits.

Run:
  python tests/golden_baseline.py
(or)
  pytest -q  (if you later convert it into strict asserts)
"""

import numpy as np

from inertia.analyze import analyze


def _save_csv(path: str, x: np.ndarray) -> None:
    x = np.asarray(x, dtype=np.float64).ravel()
    np.savetxt(path, x, delimiter=",")


def _run(name: str, x: np.ndarray, *, bins: int = 50):
    csv_path = f"{name}.csv"
    _save_csv(csv_path, x)
    r = analyze(csv_path, bins=bins)
    return r


def main():
    np.random.seed(0)
    N = 2000
    t = np.linspace(0, 10 * np.pi, N)

    # Canonical signals
    pure_sin = np.sin(t)
    noise = np.random.randn(N)
    trend = np.linspace(-1.0, 1.0, N)
    trend_plus_sin = trend + 0.2 * np.sin(t)
    sin_plus_noise = np.sin(t) + 0.25 * np.random.randn(N)

    cases = [
        ("PURE_SIN", pure_sin),
        ("NOISE", noise),
        ("TREND", trend),
        ("TREND_PLUS_SIN", trend_plus_sin),
        ("SIN_PLUS_NOISE", sin_plus_noise),
    ]

    print("=== Informational Inertia: golden baseline (v0.1.x) ===")
    print("seed=0  N=2000  bins=50")
    print()

    for name, x in cases:
        r = _run(name, x, bins=50)
        print(
            f"{name:14s}  "
            f"I_bar={r.I_bar: .6f}  "
            f"I_comp={r.I_comp: .6f}  "
            f"H={r.entropy: .6f}"
        )

    print()
    print("Notes:")
    print("- Values may differ slightly across platforms/NumPy versions.")
    print("- Look for stable ordering and sanity (TREND should be ~0 I_bar).")


if __name__ == "__main__":
    main()
