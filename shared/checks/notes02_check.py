"""Arithmetic checks for notes02.tex (Experiments). Run: python3 notes02_check.py"""
from decimal import Decimal, ROUND_HALF_UP
import math, numpy as np
from scipy import stats
FAIL = []
def check(label, claimed, computed, tol=None):
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)
z = stats.norm.ppf

# --- Section 1: Neyman example (300 ST, 200 P, 100 DND, 400 LC; 500/500)
y0 = np.r_[np.ones(300), np.zeros(200), np.ones(100), np.zeros(400)]
y1 = np.r_[np.ones(300), np.ones(200), np.zeros(100), np.zeros(400)]
t = y1 - y0; n, n1, n0 = 1000, 500, 500
check("tau_S = 0.10", "0.10", t.mean())
check("S1^2 = 250/999", "250", y1.var(ddof=1) * 999); check("S0^2 = 240/999", "240", y0.var(ddof=1) * 999)
check("Stau^2 = 290/999", "290", t.var(ddof=1) * 999)
vtrue = y1.var(ddof=1) / n1 + y0.var(ddof=1) / n0 - t.var(ddof=1) / n
check("true SD over draws 0.026", "0.026", math.sqrt(vtrue))
check("usual SE 0.031", "0.031", math.sqrt(y1.var(ddof=1) / n1 + y0.var(ddof=1) / n0))
# Monte Carlo confirmation of the randomisation SD
rng = np.random.default_rng(1); est = []
for _ in range(20000):
    idx = rng.permutation(n); T = idx[:n1]; C = idx[n1:]
    est.append(y1[T].mean() - y0[C].mean())
check("simulated randomisation SD ~0.026", "0.026", np.std(est), tol=0.001)
# Figure 1 uses SDs 0.026 and 0.031 centred at 0.10 (matches the above)

# MDE multiplier
check("MDE ~2.8 SEs at alpha .05, 80% power", "2.8", z(.975) + z(.80))
check("halving MDE needs 4x sample", "4", (1 / 0.5) ** 2)
check("DEFF rho=.01, m=400 -> 4.99", "4.99", 1 + 399 * 0.01)
# Peeking: 10 equally spaced looks, stop at first p<0.05 (two-sided)
rng = np.random.default_rng(2); S = 200000
inc = rng.standard_normal((S, 10)); cum = inc.cumsum(1); zs = cum / np.sqrt(np.arange(1, 11))
fp = (np.abs(zs) > z(.975)).any(1).mean()
check("peeking 10 looks -> about 19%", "0.19", fp, tol=0.01)
check("20 metrics x 5% -> about 1 false positive", "1", 20 * 0.05)

# --- Section 2: Pujiang Delivery
check("SRM chi2 = 2 x 240^2/10,000 = 11.52", "11.52", ((10240 - 10000) ** 2 + (9760 - 10000) ** 2) / 10000)
check("SRM p = 0.0007", "0.0007", stats.chi2.sf(11.52, 1))
se = 18 * math.sqrt(2 / 4000); tau = 21.80 - 19.90
check("tau_hat = 1.90", "1.90", tau); check("SE = 0.402", "0.402", se)
check("CI lower 1.11", "1.11", tau - 1.96 * se); check("CI upper 2.69", "2.69", tau + 1.96 * se)
check("z vs 0 = 4.72", "4.72", tau / se)
check("z vs break-even = 0.99", "0.99", (tau - 1.5) / se)
check("one-sided p = 0.16", "0.16", stats.norm.sf((tau - 1.5) / se))
tcv = tau - 0.75 * 0.08; secv = se * math.sqrt(1 - 0.7 ** 2)
check("rho^2 = 0.49", "0.49", 0.7 ** 2)
check("CUPED estimate 1.84", "1.84", tcv); check("CUPED SE 0.287", "0.287", secv)
check("CUPED SE with rounded 0.402", "0.287", 0.402 * math.sqrt(0.51))
check("CUPED CI lower 1.28", "1.28", tcv - 1.96 * secv); check("CUPED CI upper 2.40", "2.40", tcv + 1.96 * secv)
check("CUPED z = 1.18", "1.18", (tcv - 1.5) / secv); check("CUPED p = 0.12", "0.12", stats.norm.sf((tcv - 1.5) / secv))
check("narrower by 29%", "0.29", 1 - math.sqrt(0.51))
var_cv = 18 ** 2 * 0.51
check("CUPED variance 18^2 x 0.51 = 165.2", "165.2", var_cv)
n_text = (1.645 + 0.842) ** 2 * 2 * 165.2 / 0.5 ** 2
n_exact = (z(.95) + z(.80)) ** 2 * 2 * var_cv / 0.5 ** 2
print(f"INFO | follow-up n: text-inputs {n_text:.1f}, exact z & 165.24 {n_exact:.1f}; rounded up {math.ceil(n_text)} / {math.ceil(n_exact)}")
check("follow-up n = 8,175 per arm (rounded up)", "8175", math.ceil(n_text))
check("follow-up n = 8,174.3 before rounding", "8174.3", n_text, tol=0.1)
check("one-sided MDE multiplier 2.486", "2.486", z(.95) + z(.80))
check("one-sided MDE 2.486 x 0.287 = 0.71", "0.71", 2.486 * 0.287)
deff = 1 + 499 * 0.01
check("zone DEFF = 5.99", "5.99", deff); check("20 zones x 500 = 10,000", "10000", 20 * 500)
check("effective n ~1,670", "1670", 10000 / deff, tol=5)
# Step 6: one-sided noncompliance, 15% of offered customers used the discount
check("cost per offer 0.15 x 10 = 1.50", "1.50", 0.15 * 10)
check("ratio 1.84/0.15 = 12.27", "12.27", 1.84 / 0.15)
check("ratio minus cost per user 12.27 - 10", "2.27", 1.84 / 0.15 - 10)
check("same test rescaled (1.84 - 1.50)/0.15", "2.27", (1.84 - 1.50) / 0.15)
check("recommendation ~8,200 per arm is 8,175 rounded", "8200", round(n_text, -2))
# exercise
deff2 = 1 + 399 * 0.005
check("exercise DEFF 2.995", "2.995", deff2)
check("exercise customers 8,175 x 2.995 ~ 24,480", "24480", 8175 * deff2, tol=5)
check("exercise zones 24,480/400 ~ 61.2", "61.2", 24480 / 400)
check("exercise 62 zones per arm (ceil)", "62", math.ceil(8175 * deff2 / 400))
check("exercise 62 zones also with exact n", "62", math.ceil(math.ceil(n_exact) * deff2 / 400))
print(f"\n{len(FAIL)} mismatches: {FAIL}")
