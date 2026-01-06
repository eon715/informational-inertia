# Informational Inertia (I)

**Measuring irreducible structure beyond entropy**

Status: Experimental v0.1. This repository provides falsifiable, minimal estimators for informational irreducibility beyond entropy.

---
Quick Start (30 seconds)
This project measures structure that survives entropy.
Install dependencies
pip install -r requirements.txt
Run analysis on a sample signal
from inertia import analyze
result = analyze("inertia/data/example_signal.csv")
print("Entropy:", result.entropy)
print("I_bar:", result.I_bar)
print("I_comp:", result.I_comp)
result.plot()
Expected behavior:
Random noise → high entropy, low I
Structured signals → lower entropy, higher I

## Overview

This repository introduces **Informational Inertia (I)** — a measurable quantity intended to distinguish **irreducible structure** from **entropy, noise, or compressible complexity** in data.

Many systems exhibit high entropy without meaningful structure (e.g. noise), while others contain persistent structure that resists compression even when entropy is held constant. Existing metrics often conflate these cases.

Informational Inertia is designed to operationalize this distinction.

This project provides:
- concrete estimators of Informational Inertia
- reference implementations
- falsifiability tests
- diagnostic visualizations

No prior commitment to any broader theoretical framework is required to use or evaluate this software.

---
When Informational Inertia Fails
Informational Inertia is not a universal structure detector.
Known limitations:
Purely random noise may exhibit nonzero I_comp due to compression artifacts
Highly nonlinear but trivial signals may score high irreducibility under linear detrending
Estimators are representation-dependent (scaling, encoding, discretization matter)
I does not imply semantic meaning, causality, or usefulness
Adversarial constructions can inflate I without genuine structure
This repository intentionally includes tests designed to break Informational Inertia.
If I fails to add explanatory power beyond entropy or compression alone, that failure should be demonstrable using this code.

## What Informational Inertia Is

Informational Inertia (I) quantifies **resistance to further reduction after all compressible structure has been removed**.

Operationally, I captures:
- structured residuals after optimal modeling
- persistence across representations or scales
- resistance to lossless or controlled-loss compression

Key properties:
- Noise can increase entropy while *reducing* I
- Structure can increase I without increasing entropy
- I is estimator-dependent but convergence is testable

---

## What This Project Does *Not* Claim

This software:
- does **not** redefine entropy
- does **not** assume information is a substance
- does **not** require metaphysical interpretation
- does **not** claim universal optimality

If Informational Inertia fails to add explanatory power beyond existing metrics, that failure should be demonstrable using this code.

---

## Core Estimators

The reference implementation includes three complementary estimators:

### 1. Curve-Fit Irreducibility (`I_curve`)
Measures residual structure after optimal parametric fitting with complexity penalties.

Best suited for:
- time series
- trajectories
- low-dimensional signals

---

### 2. Compression Resistance (`I_comp`)
Measures resistance to compression after entropy normalization.

Best suited for:
- arbitrary data streams
- images
- symbolic sequences

---

### 3. Multiscale Persistence (`I_wave`)
Measures structural persistence across scales using spectral or wavelet decompositions.

Best suited for:
- fields
- images
- signals with scale structure

---

### Composite Informational Inertia

A composite estimate is provided:

Ī = Σ wᵢ · z(Iᵢ)

where:
- `z(Iᵢ)` are normalized estimator outputs
- `wᵢ` are precision-weighted coefficients

This reduces estimator bias and allows uncertainty propagation.

---

## Installation

```bash
git clone https://github.com/your-username/informational-inertia.git
cd informational-inertia
pip install -r requirements.txt
```
Python ≥ 3.9 recommended.
Quick Start
from inertia import analyze
result = analyze("data/example_signal.csv")
print(result.I_bar)
result.plot()

## Quick example

```python
import numpy as np
from inertia.analyze import analyze

x = np.sin(np.linspace(0, 10*np.pi, 2000))
np.savetxt("signal.csv", x, delimiter=",")

r = analyze("signal.csv")
print(r.I_bar, r.I_comp, r.entropy)
r.plot()
