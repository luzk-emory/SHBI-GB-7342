"""Arithmetic checks for meetings/m03/slides.tex (lecture case: Lena's coupon programme, Houtan Coffee, M3 releases).
The slides use their own numbers, not the notes' worked example. Run: python3 slides03_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import sqrt, erf
import numpy as np
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))

m, c = 30, 10
mu0 = {'A': F(75, 100), 'L': F(10, 100)}; mu1 = {'A': F(80, 100), 'L': F(30, 100)}
tau = {k: mu1[k] - mu0[k] for k in mu0}
check("lift active 0.05", "0.05", tau['A']); check("lift lapsed 0.20", "0.20", tau['L'])
check("base 10,000 = 2 x 5,000", "10000", 2 * 5000)
ate = (tau['A'] + tau['L']) / 2; check("tau_T base 0.125", "0.125", ate)

# prognostic vs modifier
v0 = ((mu0['A'] - mu0['L']) / 2) ** 2; vt = ((tau['A'] - tau['L']) / 2) ** 2
check("sd mu0 0.325", "0.325", (mu0['A'] - mu0['L']) / 2); check("Var mu0 0.106", "0.106", v0)
check("sd tau 0.075", "0.075", abs(tau['A'] - tau['L']) / 2); check("Var tau 0.0056", "0.0056", vt)
check("ratio about nineteen", "19", v0 / vt, tol=0.5)

# targeting rule
V = {k: m * tau[k] - c * mu1[k] for k in tau}
check("bar active 0.267", "0.267", mu1['A'] / 3); check("bar lapsed 0.100", "0.100", mu1['L'] / 3)
check("V active -6.50", "-6.50", V['A']); check("V lapsed 3.00", "3.00", V['L'])
check("marketing list -32,500", "-32500", 5000 * V['A']); check("Lena list 15,000", "15000", 5000 * V['L'])
check("E[V] -1.75", "-1.75", (V['A'] + V['L']) / 2)
check("E[max(V,0)] 1.50", "1.50", (max(V['A'], 0) + max(V['L'], 0)) / 2)
check("1.50 x 10,000 = 15,000", "15000", 10000 * F(3, 2))

# interaction model (X = 1 active)
a, t, b, g = mu0['L'], tau['L'], mu0['A'] - mu0['L'], tau['A'] - tau['L']
check("alpha 0.10", "0.10", a); check("tau 0.20", "0.20", t); check("beta 0.65", "0.65", b); check("gamma -0.15", "-0.15", g)
check("mu0 active 0.75", "0.75", a + b); check("mu1 active 0.80", "0.80", a + b + t + g)
check("mu0 lapsed 0.10", "0.10", a); check("mu1 lapsed 0.30", "0.30", a + t)
check("recode L: 0.05 + 0.15L", "0.15", -g)
check("ATE from coefficients 0.125", "0.125", t + g * F(1, 2)); check("80% active list 0.08", "0.08", t + g * F(4, 5))
check("200 per 1,000", "200", 1000 * tau['L'])

# gap test (200 per arm per segment)
se = lambda p1, p0: sqrt(p1 * (1 - p1) / 200 + p0 * (1 - p0) / 200)
seA, seL = se(0.80, 0.75), se(0.30, 0.10)
check("cell counts 160/200", "0.80", F(160, 200)); check("150/200", "0.75", F(150, 200))
check("60/200", "0.30", F(60, 200)); check("20/200", "0.10", F(20, 200))
check("0.80 x 0.20 = 0.16", "0.16", 0.8 * 0.2); check("0.75 x 0.25 = 0.1875", "0.1875", 0.75 * 0.25)
check("0.3 x 0.7 = 0.21", "0.21", 0.3 * 0.7); check("0.1 x 0.9 = 0.09", "0.09", 0.1 * 0.9)
check("SE active 0.042", "0.042", seA); check("SE lapsed 0.039", "0.039", seL)
segap = sqrt(seA ** 2 + seL ** 2); check("gap 0.15", "0.15", tau['L'] - tau['A'])
check("SE gap 0.057", "0.057", segap); check("z 2.64", "2.64", 0.15 / segap)
check("active CI low -0.03", "-0.03", 0.05 - 1.96 * seA); check("active CI high 0.13", "0.13", 0.05 + 1.96 * seA)
p = 2 * (1 - Phi(0.15 / segap)); check("gap p 0.008", "0.008", p)
check("1 - 0.95^14 = 0.51", "0.51", 1 - 0.95 ** 14); check("Bonferroni 0.05/14", "0.0036", 0.05 / 14)
assert p > 0.05 / 14 and p < 0.05

# S-learner shrinkage on the 800-member segment test, with the exact cell counts
rows = []
for x, d, buy, n in [(1, 1, 160, 200), (1, 0, 150, 200), (0, 1, 60, 200), (0, 0, 20, 200)]:
    rows += [(x, d, 1)] * buy + [(x, d, 0)] * (n - buy)
X, D, Y = (np.array(z, float) for z in zip(*rows))
Xt, Dt = X - 0.5, D - 0.5; W = Dt * Xt
check("members 800", "800", len(Y)); check("SS of X-tilde 200", "200", (Xt ** 2).sum()); check("SS of interaction 50", "50", (W ** 2).sum())
lam = 50
Z = np.column_stack([np.ones_like(Y), Dt, Xt, W])
def fit(pen):
    P = np.diag(pen); return np.linalg.solve(Z.T @ Z + P, Z.T @ Y)
ols = fit([0, 0, 0, 0]); ridge = fit([0, 0, 0, lam])
check("OLS gamma -0.15", "-0.15", ols[3]); check("penalised gamma -0.075", "-0.075", ridge[3])
check("kept 50/100 = 0.50", "0.50", ridge[3] / ols[3]); check("other coefficients unchanged", "0", abs(ridge[:3] - ols[:3]).max(), tol=1e-12)
check("same penalty on X keeps 0.80", "0.80", fit([0, 0, lam, 0])[2] / ols[2])
tA = ridge[1] + ridge[3] * 0.5; tL = ridge[1] - ridge[3] * 0.5
check("tau-hat active 0.0875", "0.0875", tA); check("tau-hat lapsed 0.1625", "0.1625", tL)
check("gap halves to 0.075", "0.075", tL - tA); check("average 0.125", "0.125", ridge[1])

# T-learner fits
for lab, f1, f0, e1, e0, tc, err_c in [("A", 0.35, 0.15, "0.05", "0.05", "0.20", "0"),
                                      ("B", 0.33, 0.07, "0.03", "-0.03", "0.26", "0.06")]:
    check(f"T-learner {lab} error mu1", e1, f1 - 0.30); check(f"T-learner {lab} error mu0", e0, f0 - 0.10)
    check(f"T-learner {lab} tau-hat", tc, f1 - f0); check(f"T-learner {lab} error in tau", err_c, (f1 - f0) - 0.20)
assert abs(0.33 - 0.30) < abs(0.35 - 0.30) and abs(0.07 - 0.10) < abs(0.15 - 0.10)  # B fits both outcomes better

# X-learner weights
check("holdout 10% => e = 0.9", "0.9", 1 - 0.10)

# transformed outcome and DR pseudo-outcome, e = 0.5, by enumeration
def moments(seg, kind):
    e = 0.5; vals = []
    for d, pd in [(1, e), (0, 1 - e)]:
        py = float(mu1[seg] if d else mu0[seg])
        for y, pyy in [(1, py), (0, 1 - py)]:
            if kind == 'Y*': v = y * (d - e) / (e * (1 - e))
            else:
                m1, m0 = float(mu1[seg]), float(mu0[seg])
                v = m1 - m0 + d * (y - m1) / e - (1 - d) * (y - m0) / (1 - e)
            vals.append((v, pd * pyy))
    mean = sum(v * w for v, w in vals); var = sum((v - mean) ** 2 * w for v, w in vals)
    return mean, sqrt(var)
check("Y* lapsed mean 0.20", "0.20", moments('L', 'Y*')[0]); check("Y* active mean 0.05", "0.05", moments('A', 'Y*')[0])
check("0.5 x 2 x 0.30 - 0.5 x 2 x 0.10", "0.20", 0.5 * 2 * 0.30 - 0.5 * 2 * 0.10)
check("SD Y* active 1.76", "1.76", moments('A', 'Y*')[1]); check("SD Y* lapsed 0.87", "0.87", moments('L', 'Y*')[1])
check("phi active mean 0.05", "0.05", moments('A', 'phi')[0]); check("phi lapsed mean 0.20", "0.20", moments('L', 'phi')[0])
check("SD phi active 0.83", "0.83", moments('A', 'phi')[1]); check("SD phi lapsed 0.77", "0.77", moments('L', 'phi')[1])

# R-learner
check("ell lapsed 0.20", "0.20", mu0['L'] + F(1, 2) * tau['L']); check("ell active 0.775", "0.775", mu0['A'] + F(1, 2) * tau['A'])

# Result 1.11 and the two models
check("1/4 Var tau 0.0014", "0.0014", vt / 4); check("= 0.0375^2", "0.0375", sqrt(vt / 4))
cells = [mu1['A'], mu0['A'], mu1['L'], mu0['L']]
irr = sum(q * (1 - q) for q in cells) / 4
check("irreducible 0.16188", "0.16188", irr); check("p(1-p) near 0.16", "0.16", irr, tol=0.005)
check("RMSE I 0.4023", "0.4023", sqrt(irr)); check("RMSE A 0.4041", "0.4041", sqrt(irr + 0.0375 ** 2))
# Model A is the least-squares additive fit, and is Result 1.11's best constant-effect predictor
Xc = np.array([1, 1, 0, 0], float); Dc = np.array([1, 0, 1, 0], float); Yc = np.array([float(q) for q in cells])
coefA = np.linalg.lstsq(np.column_stack([np.ones(4), Xc, Dc]), Yc, rcond=None)[0]
check("Model A intercept 0.1375", "0.1375", coefA[0]); check("Model A x 0.575", "0.575", coefA[1]); check("Model A D 0.125", "0.125", coefA[2])
check("Model A off by 0.0375", "0.0375", abs(np.column_stack([np.ones(4), Xc, Dc]) @ coefA - Yc).max())
check("best g(active) = mu0 + (tau - taubar)/2", "0.7125", float(mu0['A'] + (tau['A'] - ate) / 2))
check("Model A active, no coupon", "0.7125", coefA[0] + coefA[1])
check("random list -8,750", "-8750", 5000 * (V['A'] + V['L']) / 2)
check("RMSE gap 0.4%", "0.4", 100 * (sqrt(irr + 0.0375 ** 2) / sqrt(irr) - 1))
check("decision gap 23,750", "23750", 15000 - (-8750))

print(f"\n{len(FAIL)} mismatches: {FAIL}")
