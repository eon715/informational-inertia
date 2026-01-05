# Informational Inertia (I)

**Measuring irreducible structure beyond entropy**

---

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
