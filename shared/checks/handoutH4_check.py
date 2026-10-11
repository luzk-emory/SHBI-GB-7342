"""Arithmetic check for handout-H4-iv.tex (Instrumental variables, outside shifters). Run: python3 handoutH4_check.py"""
import numpy as np

fails = []


def chk(label, claimed, computed, tol):
    ok = abs(claimed - computed) <= tol
    print(f"[{'OK ' if ok else 'BAD'}] {label}: text {claimed}, computed {computed:.5f}")
    if not ok:
        fails.append(label)


# Worked example: Pujiang Plus, campaign chosen by city managers (instrument not randomised)
cust = {("big", 1): 8000, ("big", 0): 4000, ("small", 1): 2000, ("small", 0): 6000}
plus = {1: 0.30, 0: 0.05}
orders = {("big", 1): 5.30, ("big", 0): 5.00, ("small", 1): 3.30, ("small", 0): 3.00}
N = sum(cust.values()); chk("20,000 customers", 20000, N, 0)
nZ1 = cust[("big", 1)] + cust[("small", 1)]; nZ0 = cust[("big", 0)] + cust[("small", 0)]
chk("10,000 in campaign cities", 10000, nZ1, 0); chk("10,000 elsewhere", 10000, nZ0, 0)
chk("big cities 12,000", 12000, cust[("big", 1)] + cust[("big", 0)], 0)
# ---- Step 1: pooled ----------------------------------------------------------
y1 = (cust[("big", 1)] * orders[("big", 1)] + cust[("small", 1)] * orders[("small", 1)]) / nZ1
y0 = (cust[("big", 0)] * orders[("big", 0)] + cust[("small", 0)] * orders[("small", 0)]) / nZ0
chk("pooled orders, campaign 4.90", 4.90, y1, 1e-9); chk("pooled orders, no campaign 3.80", 3.80, y0, 1e-9)
chk("pooled ITT 1.10", 1.10, y1 - y0, 1e-9)
pi = plus[1] - plus[0]; chk("first stage 0.25", 0.25, pi, 1e-12)
chk("pooled ratio 4.4", 4.4, (y1 - y0) / pi, 1e-9)
# ---- Step 2: within city size ---------------------------------------------------
for size in ("big", "small"):
    itt_s = orders[(size, 1)] - orders[(size, 0)]
    chk(f"{size}: ITT 0.30", 0.30, itt_s, 1e-9); chk(f"{size}: ratio 1.2", 1.2, itt_s / pi, 1e-9)
# 2SLS with size indicators: weights Var(Z|X) * pi(X); equal LATEs give 1.2
vz = {sz: (cust[(sz, 1)] / (cust[(sz, 1)] + cust[(sz, 0)])) * (cust[(sz, 0)] / (cust[(sz, 1)] + cust[(sz, 0)])) for sz in ("big", "small")}
w = {sz: (cust[(sz, 1)] + cust[(sz, 0)]) * vz[sz] * pi for sz in vz}
tsls = sum(w[sz] * (orders[(sz, 1)] - orders[(sz, 0)]) / pi for sz in w) / sum(w.values())
chk("2SLS with strata 1.2", 1.2, tsls, 1e-9)
chk("Var(Z|X) big = 2/9", 2 / 9, vz["big"], 1e-12); chk("Var(Z|X) small = 0.1875", 0.1875, vz["small"], 1e-12)
evz = sum((cust[(sz, 1)] + cust[(sz, 0)]) * vz[sz] for sz in vz) / N
se_2sls = 3.5 / np.sqrt(N * evz * pi ** 2)
chk("2SLS SE about 0.22 (outcome SD 3.5)", 0.22, se_2sls, 5e-3)
se_pi_big = np.sqrt(0.30 * 0.70 / 8000 + 0.05 * 0.95 / 4000); se_pi_small = np.sqrt(0.30 * 0.70 / 2000 + 0.05 * 0.95 / 6000)
chk("F about 1,600 in big cities", 1600, (pi / se_pi_big) ** 2, 50)
chk("F about 550 in small cities", 550, (pi / se_pi_small) ** 2, 10)
# ---- Step 3: compliers in big cities ---------------------------------------------
EYD1, EYD0, EY1D0, EY1D1 = 2.15, 0.40, 4.60, 3.15
chk("consistency: E[Y|Z=1] = 2.15 + 3.15 = 5.30", 5.30, EYD1 + EY1D1, 1e-9)
chk("consistency: E[Y|Z=0] = 0.40 + 4.60 = 5.00", 5.00, EYD0 + EY1D0, 1e-9)
chk("E[Y(0)|C] = (4.60 - 3.15)/0.25 = 5.8", 5.8, (EY1D0 - EY1D1) / pi, 1e-9)
chk("E[Y(1)|C] = (2.15 - 0.40)/0.25 = 7.0", 7.0, (EYD1 - EYD0) / pi, 1e-9)
chk("complier means differ by the LATE 1.2", 1.2, 7.0 - 5.8, 1e-9)
chk("always-takers 0.40/0.05 = 8.0", 8.0, EYD0 / plus[0], 1e-9)
chk("never-takers 3.15/0.70 = 4.5", 4.5, EY1D1 / (1 - plus[1]), 1e-9)
# ---- Step 4: exclusion -------------------------------------------------------
delta = 0.05
chk("exclusion bias delta/pi = 0.2", 0.2, delta / pi, 1e-12)
chk("corrected complier effect 1.0", 1.0, (0.30 - delta) / pi, 1e-9)
# ---- Step 5: decisions ----------------------------------------------------------
chk("margin per customer 10 x 0.30 = 3.00", 3.00, 10 * 0.30, 1e-9)
chk("waived fees 0.25 x 15 = 3.75", 3.75, pi * 15, 1e-9)
chk("net -0.75", -0.75, 10 * 0.30 - pi * 15, 1e-9)
chk("complier value, corrected 10 x 1.0 = 10", 10, 10 * 1.0, 1e-9); chk("complier value, uncorrected 12", 12, 10 * 1.2, 1e-9)
assert 10 * 1.2 < 15
print("[OK ] complier: Y12 < Y15 -> no, either way")
n1 = n0 = 10000

# ---- Exercise (weak instrument) -------------------------------------------
pi2 = 0.07 - 0.05
chk("ex: pi = 0.02", 0.02, pi2, 1e-12)
se_pi2 = np.sqrt(0.07 * 0.93 / n1 + 0.05 * 0.95 / n0)
chk("ex: SE(pi_hat) approx 0.0034 (binomial, 10,000 per arm)", 0.0034, se_pi2, 1e-4)
F2 = (0.02 / 0.0034) ** 2
chk("ex answer: F approx 35 (with stated SE 0.0034)", 35, F2, 0.5)
print(f"      (ref) F with unrounded SE {se_pi2:.5f}: {(pi2 / se_pi2) ** 2:.1f}")
chk("ex answer: ratio 15", 15, 0.30 / pi2, 1e-9)
chk("ex answer: SE before first-stage term 2.5", 2.5, 0.05 / pi2, 1e-9)
se_full2 = np.sqrt(0.05**2 + 15**2 * 0.0034**2) / pi2
print(f"      (ref) SE after first-stage term (cov=0): {se_full2:.2f}  ('and more after it')")
assert se_full2 > 2.5
chk("ex answer: delta multiplied by 1/0.02 = 50", 50, 1 / pi2, 1e-9)
assert 10 < F2 < 100
print("[OK ] ex answer: F in (10, 100) -> AR-set branch of the stated guard")

# ---- Section 1 constants ---------------------------------------------------
print("      Lee et al. (2022) 104.7 threshold: literature constant, not recomputed")

print("\nFAILURES:", fails if fails else "none")
