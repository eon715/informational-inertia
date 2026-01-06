"""
Basic sanity checks for informational-inertia v0.1

This test verifies that the analyzer:
1. Runs without error
2. Returns expected fields
3. Orders simple signals sensibly:
   PURE sine < MIX < NOISE in compression resistance
"""

import numpy as np
from inertia.analyze import analyze


def run_basic_sanity():
    np.random.seed(0)
    t = np.linspace(0, 10 * np.pi, 2000)

    signals = {
        "PURE": np.sin(t),
        "MIX": np.sin(t) + 0.5 * np.random.randn(2000),
        "NOISE": np.random.randn(2000),
    }

    results = {}

    for name, x in signals.items():
        np.savetxt(f"{name}.csv", x, delimiter=",")
        r = analyze(f"{name}.csv")

        # Structural checks
        assert hasattr(r, "I_bar")
        assert hasattr(r, "I_comp")
        assert hasattr(r, "entropy")
        assert hasattr(r, "values")

        results[name] = r

        print(
            name,
            "I_bar:", round(r.I_bar, 3),
            "I_comp:", round(r.I_comp, 3),
            "H:", round(r.entropy, 3),
        )

    # Weak ordering expectations (heuristic, not strict laws)
    assert results["PURE"].I_comp > results["MIX"].I_comp
    assert results["MIX"].I_comp >= results["NOISE"].I_comp


if __name__ == "__main__":
    run_basic_sanity()
