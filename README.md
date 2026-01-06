# Informational Inertia (I)

Measuring irreducible structure beyond entropy

Status: Experimental v0.1.  
This repository provides falsifiable, minimal estimators for informational irreducibility beyond entropy and compression alone.

---

## What This Is

Informational Inertia (I) is a quantitative measure of how much structure remains in data after all *compressible* and *modelable* structure has been removed.

It is explicitly **not** a claim about meaning, intelligence, consciousness, or causality.

It answers a narrower question:

“How resistant is this signal to further simplification once obvious structure is removed?”

---

## Core Quantities

The analysis returns three primary values:

- entropy  
  A histogram-based entropy proxy (for contrast only)

- I_bar  
  Normalized irreducible variance fraction after detrending / model removal

- I_comp  
  Compression-resistance proxy after entropy normalization

A composite estimate may be formed as:

Ī = Σ wᵢ · Z(Iᵢ)

where:
- Z(Iᵢ) are normalized estimator outputs
- wᵢ are precision-weighted coefficients

This reduces estimator bias and allows uncertainty propagation.

---

## Installation

Requirements:
- Python ≥ 3.9 recommended

Install:

git clone https://github.com/eon715/informational-inertia.git  
cd informational-inertia  
pip install -r requirements.txt

---

## Quick Start (30 seconds)

Python example:

import numpy as np  
from inertia.analyze import analyze  

x = np.sin(np.linspace(0, 10*np.pi, 2000))  
np.savetxt("signal.csv", x, delimiter=",")  

r = analyze("signal.csv")  

print("Entropy:", r.entropy)  
print("I_bar:", r.I_bar)  
print("I_comp:", r.I_comp)  

r.plot()

---

## Expected Behavior

Typical ordering observed in v0.1 tests:

- Structured signals  
  → lower entropy, lower I_bar

- Random noise  
  → higher entropy, higher I_bar

- Linear trends  
  → very low I_bar (structure is removable)

- Trend + structure  
  → intermediate I_bar

Absolute values are not physically meaningful; comparisons are.

---

## Included Tests

The tests/ directory contains sanity and falsifiability tests, including:

- Noise vs. structured signal separation
- Permutation invariance
- Shift invariance
- Trend sensitivity
- Quantization and compression stress tests
- Polynomial overfitting failure modes

Tests are designed to fail loudly if assumptions break.

---

## When Informational Inertia Fails

Informational Inertia is not a universal structure detector.

Known limitations:

- Purely random noise may exhibit nonzero I_comp due to compression artifacts
- Highly nonlinear but trivial signals may appear irreducible under linear detrending
- Estimators are representation-dependent (scaling, encoding, discretization matter)
- Adversarial constructions can inflate scores without meaningful structure

These limitations are intentional and testable.

If Informational Inertia fails to add explanatory power beyond entropy or compression alone, that failure should be demonstrable using this code.

This repository intentionally includes tests designed to break the metric.

---

## What This Is Not

Informational Inertia:

- does NOT imply semantic meaning
- does NOT imply intelligence or agency
- does NOT require metaphysical interpretation
- does NOT claim universal optimality

It is a diagnostic statistic, not an ontology.

---

## License

MIT License.

---

## Citation

If you use this code or concept, please cite:

Informational Inertia (I), eon715, GitHub, 2026.
