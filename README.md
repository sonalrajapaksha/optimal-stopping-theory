# Simulation and Analysis of the Secretary Problem

Interactive simulation and visualisation of the optimal stopping problem built in Python with Streamlit and Plotly

## Defining the Problem
`N` candidates are interviewed sequentially. After each interview, it must be decided if the candidate should be hired or not, with no opputunity to hire previous candidates.
What is the optimal stategy to hire the best candidate.

---

## Analytic Formula

The probability of hiring the best candidate with threshold `k` is:

$$P(N, k) = \frac{k}{N} \sum_{i=k+1}^{N} \frac{1}{i-1}$$

This is maximised at `k* = ⌊N/e⌋`, giving `P → 1/e` as `N → ∞`.

---

# Modes

### Classic
Plots the analytic `P(success)` curve over all `k`, marks your chosen `k` and the classical optimum `k* = ⌊N/e⌋`, and runs a Monte Carlo simulation to verify.

### Cost Penalty
Introduces a per-interview time cost. Each candidate interviewed reduces the net reward, shifting the optimal threshold earlier than `1/e`. Sweeps all `k` values via simulation to find the cost-adjusted optimum.

### Distribution
Tests the stopping rule when candidate scores are drawn from different distributions. Compares P(success) across uniform, normal, Pareto, and log-normal at a fixed `k`, and sweeps `k` for the selected distribution.

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/sonalrajapaksha/optimal-stopping-theory.git
cd optimal-stopping-explorer
```

**2. Install dependencies**
```bash
pip install streamlit plotly
```

**3. Run the app**
```bash
streamlit run app.py
```
---
