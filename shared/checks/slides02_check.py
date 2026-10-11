"""Arithmetic checks for meetings/m02/slides.tex (lecture case: Lena's coupon programme, Houtan Coffee, M2 releases).
The slides use their own numbers, not the notes' worked example. Run: python3 slides02_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import comb, sqrt, erf
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
p2 = lambda z: 2 * (1 - Phi(abs(z)))

m, c = 30, 10
n1 = n0 = 500
p1, p0 = F(250, 500), F(200, 500)
tau = p1 - p0
check("rates 0.50", "0.50", p1); check("rates 0.40", "0.40", p0); check("tau-hat 0.10", "0.10", tau)
be = c * p1 / m
check("break-even 0.167", "0.167", be); check("break-even 0.1667", "0.1667", be)

# sample-ratio mismatch
chi2 = lambda a, b: ((a - 500) ** 2 + (b - 500) ** 2) / 500
check("SRM Q2 chi2 0", "0", chi2(500, 500)); check("SRM broken chi2 14.4", "14.4", chi2(560, 440))
from math import exp
p_chi1 = lambda x: p2(sqrt(x))  # chi-square(1) tail = two-sided normal tail at sqrt(x)
check("SRM broken p 0.0001", "0.0001", p_chi1(14.4))

# Fisher
check("tea C(8,4) = 70", "70", comb(8, 4)); check("tea 1/70", "0.014", 1 / 70)
check("buyers 450", "450", 250 + 200); check("non-buyers 550", "550", 1000 - 450)
pp = 0.45; se0 = sqrt(2 * pp * (1 - pp) / 500)
check("pooled SE0 0.0315", "0.0315", se0); check("Fisher z 3.18", "3.18", 0.10 / se0)
check("Fisher p 0.0015", "0.0015", p2(0.10 / se0))

# Neyman on the M1 type region
types = {'LC': (0, 0, 400), 'ST': (1, 1, 300), 'P': (0, 1, 200), 'DND': (1, 0, 100)}
Y0 = sum(([y0] * k for y0, y1, k in types.values()), []); Y1 = sum(([y1] * k for y0, y1, k in types.values()), [])
n = len(Y1); assert n == 1000
var = lambda v: sum((x - sum(v) / len(v)) ** 2 for x in v) / (len(v) - 1)
S1, S0, St = var(Y1), var(Y0), var([a - b for a, b in zip(Y1, Y0)])
check("S1^2 = 250/999", "0.25025", S1, tol=1e-5); check("S0^2 = 240/999", "0.24024", S0, tol=1e-5)
check("Stau^2 = 290/999", "0.29029", St, tol=1e-5)
check("true SD over draws 0.026", "0.026", sqrt(S1 / 500 + S0 / 500 - St / 1000))
check("usual SE 0.031", "0.031", sqrt(S1 / 500 + S0 / 500))
se = sqrt(0.25 / 500 + 0.24 / 500)
check("Q2 SE 0.0313", "0.0313", se); check("z vs 0 = 3.19", "3.19", 0.10 / se); check("p 0.0014", "0.0014", p2(0.10 / se))
check("1.96 x SE = 0.061", "0.061", 1.96 * se)
check("CI low 0.039", "0.039", 0.10 - 1.96 * se); check("CI high 0.161", "0.161", 0.10 + 1.96 * se)
check("z vs break-even -2.13", "-2.13", (0.10 - float(be)) / se)

# net value
V = (m - c) * p1 - m * p0; check("net -2.00", "-2.00", V)
vV = 400 * 0.0005 + 900 * 0.00048; check("net variance 0.632", "0.632", vV); check("net SE 0.795", "0.795", sqrt(vV))
check("net CI low -3.56", "-3.56", -2 - 1.96 * sqrt(vV)); check("net CI high -0.44", "-0.44", -2 + 1.96 * sqrt(vV))
check("0.25/500 = 0.0005", "0.0005", 0.25 / 500); check("0.24/500 = 0.00048", "0.00048", 0.24 / 500)

# transport
seg = {'active': (F(80, 100), F(75, 100)), 'lapsed': (F(30, 100), F(10, 100))}
eff = {k: a - b for k, (a, b) in seg.items()}
for name, w, tau_c, p1_c, be_c, net_c in [("active only", 1, "0.050", "0.800", "0.267", "-6.50"),
                                          ("campaign A", F(2, 3), "0.100", "0.633", "0.211", "-3.33"),
                                          ("whole base", F(1, 2), "0.125", "0.550", "0.183", "-1.75"),
                                          ("campaign B", F(1, 3), "0.150", "0.467", "0.156", "-0.17"),
                                          ("lapsed only", 0, "0.200", "0.300", "0.100", "3.00")]:
    t = w * eff['active'] + (1 - w) * eff['lapsed']; q = w * seg['active'][0] + (1 - w) * seg['lapsed'][0]
    check(f"{name} tau", tau_c, t); check(f"{name} p1", p1_c, q); check(f"{name} break-even", be_c, c * q / m)
    check(f"{name} net", net_c, m * t - c * q)
check("campaign arms 300 per arm", "300", 600 / 2)
check("base forecast -20,000", "-20000", 10000 * V)

# power
zsum = 1.96 + 0.84; check("2.80", "2.80", zsum)
check("Q2 n 384.2", "384.2", zsum ** 2 * 0.49 / 0.01); check("Q2 MDE 0.088", "0.088", zsum * 0.0313)
check("CFO gap 0.067", "0.067", float(be) - 0.10)
v = 0.30 * 0.70 + 0.10 * 0.90; check("lapsed variance 0.30", "0.30", v)
check("lapsed n 235.2", "235.2", 7.84 * v / 0.01); check("lapsed SE 0.0414", "0.0414", sqrt(v / 175))
check("lapsed MDE 0.116", "0.116", zsum * sqrt(v / 175))
check("1 - 0.6^2 = 0.64", "0.64", 1 - 0.6 ** 2)
check("CUPED n 151", "151", -(-0.64 * 235.2 // 1)); check("CUPED MDE 0.093", "0.093", zsum * sqrt(0.64 * v / 175))
check("85 fewer members per arm", "85", 236 - 151)

# design effect
deff = 1 + 399 * 0.01; check("DEFF 4.99", "4.99", deff); check("sqrt 2.23", "2.23", sqrt(deff))
check("effective customers ~4,000", "4000", 20000 / deff, tol=10)
check("20 metrics x 5% = 1 false positive", "1", 20 * 0.05)

# noncompliance (Case A, Part M2-R6)
check("openers-only 0.075", "0.075", F(230, 400) - F(180, 360))
check("coupon openers 0.575", "0.575", F(230, 400)); check("control openers 0.500", "0.500", F(180, 360))
check("not seen 220/600 = 0.367", "0.367", F(20 + 200, 100 + 500)); check("as treated 0.208", "0.208", F(230, 400) - F(220, 600))
pi = F(400, 500); check("first stage 0.80", "0.80", pi)
check("pi_N 0.20", "0.20", F(100, 500)); check("never-taker rate 0.20", "0.20", F(20, 100))
check("LATE 0.125", "0.125", tau / pi)
muC0 = (p0 - F(1, 5) * F(20, 100)) / pi; check("complier untreated 0.45", "0.45", muC0)
check("0.36", "0.36", p0 - F(1, 5) * F(20, 100)); check("0.575 - 0.45", "0.125", F(230, 400) - muC0)
check("complier break-even 0.192", "0.192", c * F(230, 400) / m)
check("complier cost 5.75", "5.75", c * F(230, 400)); check("net per seen coupon -2.00", "-2.00", m * tau / pi - c * F(230, 400))
check("never-taker cost 2.00", "2.00", c * F(20, 100))

check("1 - 0.40 = 0.60", "0.60", 1 - 0.40)
check("350 lapsed members = 2 x 175", "350", 2 * 175)
check("segments of 5,000 make the 10,000 base", "5000", 10000 / 2)
print(f"\n{len(FAIL)} mismatches: {FAIL}")
