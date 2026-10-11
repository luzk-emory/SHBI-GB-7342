"""Arithmetic checks for notes03.tex (Conditional Effects). Run: python3 notes03_check.py"""
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

# --- Section 1 numeric illustrations
check("T-learner fits 0.34-0.14 = 0.20", "0.20", 0.34 - 0.14)
check("miss 0.04 each (0.34 vs 0.30)", "0.04", 0.34 - 0.30); check("miss 0.04 (0.14 vs 0.10)", "0.04", 0.14 - 0.10)
check("T-learner fits 0.32-0.08 = 0.24", "0.24", 0.32 - 0.08)
check("miss 0.02 (0.32 vs 0.30)", "0.02", 0.32 - 0.30); check("miss 0.02 (0.08 vs 0.10)", "0.02", 0.10 - 0.08)
# Result 'shrink': s = 1/4 sum X~^2 when D~ = +-1/2
rng = np.random.default_rng(0); X = rng.standard_normal(1000); X -= X.mean(); Dt = np.repeat([0.5, -0.5], 500)
check("s = 1/4 sum X^2 (ratio)", "0.25", ((Dt * X) ** 2).sum() / (X ** 2).sum())
# Result 'blind': excess MSE = 1/4 Var(tau) under 50/50, verified numerically on a discrete X
px = np.array([.2, .3, .5]); mu0 = np.array([.3, .5, .8]); tx = np.array([.25, .05, -.1])
tbar = px @ tx
excess = 0.5 * (px @ (0.5 * (tx - tbar)) ** 2) * 2  # errors +-1/2(tau - tbar) in each arm, equal weight
check("blind: excess MSE = 1/4 Var(tau)", f"{0.25 * (px @ (tx - tbar) ** 2):.6f}", excess)
# Figure 1: curves 0.45+0.045x and 0.67+0.025x on [0,10] stay within ymin/ymax and gap shrinks
xs = np.linspace(0, 10, 60); f0 = 0.45 + 0.045 * xs; f1 = f0 + 0.22 - 0.02 * xs
ok = f0.min() >= 0.3 and f1.max() <= 1 and np.all(np.diff(f1 - f0) < 0) and np.all(np.diff(f0) > 0)
print(f"{'OK ' if ok else 'MISMATCH'} | Figure 1: curves in [0.3,1], both rise, gap shrinks (gap {f1[0]-f0[0]:.2f} -> {f1[-1]-f0[-1]:.2f})")
if not ok: FAIL.append("figure 1")

# --- Section 2: Yangsi Fitness retention offer
be = 80 / 600
check("break-even 80/600 = 0.133", "0.133", be)
seg = {'Short, low': (0.62, 0.50), 'Short, high': (0.70, 0.48), 'Long, low': (0.84, 0.80), 'Long, high': (0.93, 0.90)}
txt = {'Short, low': ('0.12', '0.031', '0.059', '0.181', '-0.43'),
       'Short, high': ('0.22', '0.030', '0.161', '0.279', '2.86'),
       'Long, low': ('0.04', '0.024', '-0.008', '0.088', '-3.85'),
       'Long, high': ('0.03', '0.018', '-0.005', '0.065', '-5.87')}
SE = {}
for k, (p1, p0) in seg.items():
    t, s, lo, hi, zz = txt[k]
    se = math.sqrt(p1 * (1 - p1) / 500 + p0 * (1 - p0) / 500); SE[k] = se
    check(f"{k} tau", t, p1 - p0); check(f"{k} SE", s, se)
    check(f"{k} CI lower (unrounded SE)", lo, p1 - p0 - 1.96 * se); check(f"{k} CI upper (unrounded SE)", hi, p1 - p0 + 1.96 * se)
    check(f"{k} z vs 80/600", zz, (p1 - p0 - be) / se)
taus = np.array([p1 - p0 for p1, p0 in seg.values()])
check("ATE = 0.1025", "0.1025", taus.mean())
check("blanket net 600x0.1025-80 = -18.50", "-18.50", 600 * taus.mean() - 80)
for k, v in zip(seg, ['-8', '52', '-56', '-62']): check(f"net value {k}", v, 600 * (seg[k][0] - seg[k][1]) - 80)
check("targeted value 52/4 = 13", "13", max(0, 52) / 4)
check("Bonferroni 0.05/4 = 0.0125", "0.0125", 0.05 / 4)
check("short-high p = 0.002 (one-sided vs break-even)", "0.002", stats.norm.sf((0.22 - be) / SE['Short, high']))
print(f"INFO | short-high two-sided p vs break-even = {2*stats.norm.sf((0.22-be)/SE['Short, high']):.4f} (still < 0.0125)")
# Step 2
check("control renewal short 0.49", "0.49", (0.50 + 0.48) / 2); check("control renewal long 0.85", "0.85", (0.80 + 0.90) / 2)
check("short-low loses 8 per offer", "-8", 600 * 0.12 - 80)
# Step 3: S-learner without interactions on the 8 balanced cells (500 obs each, use cell means)
rows, y = [], []
for (long_, high), (p1, p0) in zip([(0, 0), (0, 1), (1, 0), (1, 1)], seg.values()):
    for d, p in ((1, p1), (0, p0)):
        rows.append([1, d, long_, high]); y.append(p)
b = np.linalg.lstsq(np.array(rows, float), np.array(y), rcond=None)[0]
check("S-learner beta_hat = 0.1025", "0.1025", b[1]); print("INFO | S-learner 0.1025 < 0.133 -> offer to nobody:", b[1] < be)
# Step 4: T-learner additive in each arm
coef = {}
for d in (1, 0):
    A = np.array([[1, l, h] for l, h in [(0, 0), (0, 1), (1, 0), (1, 1)]], float)
    yy = np.array([v[0] if d == 1 else v[1] for v in seg.values()])
    coef[d] = np.linalg.lstsq(A, yy, rcond=None)[0]
for lab, cl, co in zip(('a1', 'b1', 'c1'), ('0.6175', '0.225', '0.085'), coef[1]): check(f"T-learner offered {lab}", cl, co)
for lab, cl, co in zip(('a0', 'b0', 'c0'), ('0.47', '0.36', '0.04'), coef[0]): check(f"T-learner control {lab}", cl, co)
for (l, h), cl in zip([(0, 0), (0, 1), (1, 0), (1, 1)], ('0.148', '0.193', '0.013', '0.058')):
    x = np.array([1, l, h]); check(f"T-learner implied effect long={l},high={h}", cl, x @ (coef[1] - coef[0]))
print("INFO | T-learner short-low 0.1475 > 0.133:", (coef[1] - coef[0])[0] > be, "(exact values end in 5; text rounds half-up)")
# Step 5
check("transformed outcome segment mean short-high = 0.22", "0.22", 0.5 * 2 * 0.70 - 0.5 * 2 * 0.48)
# Exercise
check("exercise SE short-high 0.0303", "0.0303", SE['Short, high']); check("exercise SE short-low 0.0312", "0.0312", SE['Short, low'])
segap = math.sqrt(0.0303 ** 2 + 0.0312 ** 2)
check("exercise SE diff 0.0435", "0.0435", segap); check("exercise z 2.30", "2.30", 0.10 / 0.0435)
check("exercise p ~ 0.02", "0.02", 2 * stats.norm.sf(0.10 / segap))
print(f"\n{len(FAIL)} mismatches: {FAIL}")
