# Methods — Informational Inertia (I)

## 1. Scope and Intent

This document specifies the construction, normalization, and limitations of the Informational Inertia (I) estimators implemented in this repository.

The purpose of Informational Inertia is to quantify **residual structure that persists after explicit, model-based simplification**, and to do so in a way that is falsifiable, reproducible, and intentionally vulnerable to counterexamples.

This method does **not** claim to measure meaning, intelligence, causality, or semantic content.

---

## 2. Signal Model

Let a signal be a one-dimensional real-valued sequence:

x = {x₁, x₂, …, xₙ}

Signals are treated as ordered sequences sampled at uniform index spacing. No assumptions are made about stationarity, ergodicity, or physical origin.

All estimators operate on finite-length signals and are representation-dependent.

---

## 3. Core Quantities

Three complementary quantities are computed:

### 3.1 Irreducible Variance Fraction (Ī)

Ī measures the fraction of variance that remains after removing an explicit parametric model.

Operationally:

Ī = Var(residual) / Var(original)

where the residual is computed after fitting and subtracting a model.

In v0.1, the model is a first-order (linear) least-squares fit.

Ī ∈ [0, 1], up to numerical precision.

---

### 3.2 Compression Resistance (I_comp)

I_comp is a heuristic proxy for resistance to algorithmic compression.

It is computed as:

I_comp = 1 − (compressed_size / raw_size)

using zlib compression on raw floating-point byte representations.

This estimator is intentionally crude and sensitive to encoding choices. It is included for contrast, not dominance.

---

### 3.3 Entropy Proxy (H)

Entropy is estimated using a histogram-based approximation of differential entropy.

This quantity serves only as a baseline comparator and is not treated as physically absolute.

Entropy values may be negative and are not directly comparable across representations.

---

## 4. Estimator Construction

### 4.1 Linear Irreducibility Estimator

Given signal x of length n:

1. Construct index vector t = {0, 1, …, n−1}
2. Fit linear model x̂(t) = a·t + b via least squares
3. Compute residual r = x − x̂
4. Compute Ī = Var(r) / Var(x)

This estimator intentionally removes trivial linear trends.

---

### 4.2 Polynomial Extension (Experimental)

An experimental extension fits polynomial models of increasing degree and selects the minimum residual variance:

Ī_poly = min_d Var(x − P_d(t)) / Var(x)

where P_d is a degree-d polynomial.

This extension is included for sensitivity analysis and is not the default.

---

## 5. Normalization and Scaling

All variance-based quantities are normalized by the total variance of the input signal.

No cross-signal normalization is performed.

Scaling, discretization, quantization, and encoding materially affect results.

---

## 6. Composite Scores

A composite Informational Inertia score may be formed as:

I_total = Σ wᵢ · Z(Iᵢ)

where:
- Iᵢ are individual estimator outputs
- Z(·) denotes normalization
- wᵢ are precision-weighted coefficients

Composite scores are optional and not used in the baseline tests.

---

## 7. Reproducibility and Determinism

All tests are deterministic given fixed random seeds.

Signal generation, estimator behavior, and outputs are fully reproducible using the provided scripts.

No learned parameters are used.

---

## 8. Golden Baseline Testing

Golden baseline tests generate canonical signal classes, including:

- Pure sinusoidal signals
- Gaussian white noise
- Linear trends
- Mixed trend + structure signals
- Quantized and compressed variants

Expected ordering (typical, not guaranteed):

- Linear trends → very low Ī
- Structured signals → intermediate Ī
- Random noise → high Ī

Deviations from this ordering are considered informative failures, not bugs.

---

## 9. Known Limitations and Failure Modes

Informational Inertia is **not universal**.

Known limitations include:

- Random noise may score high Ī under insufficient detrending
- Highly nonlinear but trivial signals may appear irreducible
- Compression artifacts can inflate I_comp
- Adversarial constructions can inflate scores without meaningful structure
- Estimators are representation-dependent

These limitations are intentional and testable.

---

## 10. Non-Claims

This method explicitly does **not** claim:

- Semantic meaning
- Intelligence or cognition
- Physical causality
- Universal optimality
- Independence from representation choice

If Informational Inertia fails to add explanatory power beyond entropy or compression alone, that failure should be demonstrable using this codebase.

---

## 11. Intended Use

This repository is intended as a falsifiable experimental framework for studying residual structure under explicit model removal.

Users are encouraged to break, extend, or refute the metric using adversarial tests.
