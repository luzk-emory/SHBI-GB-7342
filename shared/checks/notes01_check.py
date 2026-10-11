"""Arithmetic checks for notes01.tex (Causal Basics). Run: python3 notes01_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
import itertools
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)

# --- Section 1: response-type table, m=30, c=10 (cost per redemption)
m, c = 30, 10
types = {'Persuadable': (0, 1), 'Sure thing': (1, 1), 'Lost cause': (0, 0), 'Do-not-disturb': (1, 0)}
claimed = {'Persuadable': (0, 20, 20), 'Sure thing': (30, 20, -10), 'Lost cause': (0, 0, 0), 'Do-not-disturb': (30, 0, -30)}
for t, (y0, y1) in types.items():
    un, tr = m * y0, (m - c) * y1
    for lab, cl, co in zip(('untreated', 'treated', 'change'), claimed[t], (un, tr, tr - un)):
        check(f"type table {t} {lab}", cl, co)
# lift 0.10 = 10% P & 0 DND, or 30% P & 20% DND
check("lift 0.10 from 10%/0%", "0.10", 0.10 - 0.0)
check("lift 0.10 from 30%/20%", "0.10", 0.30 - 0.20)
# collider result: D,U iid Bern(1/2), Y=U, C=max(D,U)
cells = [(d, u) for d in (0, 1) for u in (0, 1)]
def cm(dv):
    sel = [u for d, u in cells if d == dv and max(d, u) == 1]
    return F(sum(sel), len(sel))
check("collider E[Y|D=1,C=1]=1/2", "0.5", cm(1)); check("collider E[Y|D=0,C=1]=1", "1", cm(0))
check("collider difference -1/2", "-0.5", cm(1) - cm(0))

# --- Section 2: Yangsi Fitness
check("break-even 300/1,000 = 0.30", "0.30", 300 / 1000)
tab = {'A': (1, 1, 1), 'B': (1, 1, 1), 'C': (0, 1, 1), 'D': (1, 1, 1), 'E': (0, 0, 0), 'F': (0, 1, 0), 'G': (0, 1, 0), 'H': (1, 1, 0)}
tau = {k: v[1] - v[0] for k, v in tab.items()}
claimed_tau = dict(A=0, B=0, C=1, D=0, E=0, F=1, G=1, H=0)
for k in tab: check(f"tau_{k}", claimed_tau[k], tau[k])
typ = {(1, 1): 'sure thing', (0, 1): 'persuadable', (0, 0): 'lost cause', (1, 0): 'do-not-disturb'}
claimed_typ = dict(A='sure thing', B='sure thing', C='persuadable', D='sure thing', E='lost cause', F='persuadable', G='persuadable', H='sure thing')
for k, v in tab.items():
    ok = typ[(v[0], v[1])] == claimed_typ[k]; print(f"{'OK ' if ok else 'MISMATCH'} | type of {k}: {claimed_typ[k]}")
    if not ok: FAIL.append(f"type {k}")
T = [k for k in tab if tab[k][2] == 1]; U = [k for k in tab if tab[k][2] == 0]
mean = lambda xs: F(sum(xs), len(xs))
ATE = mean([tau[k] for k in tab]); ATT = mean([tau[k] for k in T]); ATU = mean([tau[k] for k in U]); pi = F(len(T), 8)
check("ATE = 3/8 = 0.375", "0.375", ATE); check("ATT = 1/4 = 0.25", "0.25", ATT); check("ATU = 2/4 = 0.50", "0.50", ATU)
check("pi = 0.5", "0.5", pi)
check("0.5x0.25 + 0.5x0.50 = 0.375", "0.375", pi * ATT + (1 - pi) * ATU)
y1T = mean([tab[k][1] for k in T]); y0U = mean([tab[k][0] for k in U]); y0T = mean([tab[k][0] for k in T])
check("treated renewal 4/4 = 1.00", "1.00", y1T); check("untreated renewal 1/4 = 0.25", "0.25", y0U)
check("naive difference 0.75", "0.75", y1T - y0U)
check("E[Y(0)|D=1] = 3/4", "0.75", y0T)
check("selection bias 3/4-1/4 = 0.50", "0.50", y0T - y0U)
check("ATT + 0.50 = 0.75", "0.75", ATT + (y0T - y0U))
bias_ate = (y0T - y0U) + (1 - pi) * (ATT - ATU)
check("bias rel. ATE 0.50 + 0.5(0.25-0.50) = 0.375", "0.375", bias_ate)
check("ATE + bias = 0.75", "0.75", ATE + bias_ate)
print("decision: ATT 0.25 < 0.30:", ATT < F(3, 10), "; ATE 0.375 > 0.30:", ATE > F(3, 10))
# Section 2 exercise (a): Pr(P)-Pr(DND) = 3/8 = ATE
nP = sum(1 for v in tab.values() if (v[0], v[1]) == (0, 1)); nD = sum(1 for v in tab.values() if (v[0], v[1]) == (1, 0))
check("exercise (a) Pr(P)-Pr(DND) = 3/8", "0.375", F(nP - nD, 8))

# Simpson table
cellsS = {('New', 'inv'): (40, 200, '0.20'), ('New', 'not'): (9, 60, '0.15'),
          ('Long', 'inv'): (38, 50, '0.76'), ('Long', 'not'): (140, 200, '0.70')}
for k, (r, n, cl) in cellsS.items(): check(f"Simpson rate {k}", cl, r / n)
pi_r = 40 + 38; pi_n = 200 + 50; pn_r = 9 + 140; pn_n = 60 + 200
check("pooled invited renewed 78", "78", pi_r); check("pooled invited members 250", "250", pi_n)
check("pooled not-invited renewed 149", "149", pn_r); check("pooled not-invited members 260", "260", pn_n)
check("pooled invited rate 0.312", "0.312", pi_r / pi_n); check("pooled not-invited rate 0.573", "0.573", pn_r / pn_n)
dN = 40 / 200 - 9 / 60; dL = 38 / 50 - 140 / 200
check("within-new gap 0.05", "0.05", dN); check("within-long gap 0.06", "0.06", dL)
check("total members 510", "510", pi_n + pn_n)
nNew = 200 + 60; nLong = 50 + 200
check("new members 260 (weight in standardisation)", "260", nNew); check("long members 250", "250", nLong)
check("standardised ATE (260x0.05+250x0.06)/510 = 0.055", "0.055", (nNew * dN + nLong * dL) / 510)
check("standardised ATT (200x0.05+50x0.06)/250 = 0.052", "0.052", (200 * dN + 50 * dL) / 250)

# exercise (b): bounds with p1=0.80, p0=0.45
p1, p0 = 0.80, 0.45
check("lower bound max(0,0.80-0.45) = 0.35", "0.35", max(0, p1 - p0))
check("1-p0 = 0.55", "0.55", 1 - p0)
check("upper bound min(0.80,0.55) = 0.55", "0.55", min(p1, 1 - p0))
# brute-force: the bound is sharp (search over type shares consistent with p1,p0)
best = [1, 0]
for P100 in range(0, 101):
    for D100 in range(0, 101):
        P, Dn = P100 / 100, D100 / 100
        ST = p1 - P; LC = 1 - P - Dn - ST
        if ST >= -1e-9 and LC >= -1e-9 and abs((ST + Dn) - p0) < 1e-9:
            best = [min(best[0], P), max(best[1], P)]
check("bounds sharp: min feasible Pr(P)", "0.35", best[0]); check("bounds sharp: max feasible Pr(P)", "0.55", best[1])

print(f"\n{len(FAIL)} mismatches: {FAIL}")
