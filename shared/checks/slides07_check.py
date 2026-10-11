"""Arithmetic checks for meetings/m07/slides.tex (lecture case: Lena's coupon programme, Houtan Coffee, the review of
the Q3 programme from its logs, M7 releases R1 to R4b). The slides use their own numbers, not the notes' worked example.
Run: python3 slides07_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import sqrt
import numpy as np
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)

m, c = 30, 10                                  # margin per purchase; coupon cost per redemption

# ── Block A: the two segments (M7-R1, R2) ──
N = {'A': 5000, 'L': 5000}
n1 = {'A': 1000, 'L': 4000}; n0 = {s: N[s] - n1[s] for s in N}
mu1 = {'A': F(80, 100), 'L': F(30, 100)}; mu0 = {'A': F(75, 100), 'L': F(10, 100)}
tau = {s: mu1[s] - mu0[s] for s in N}
e = {s: F(n1[s], N[s]) for s in N}
check("base 10,000", "10000", sum(N.values())); check("coupons 5,000", "5000", sum(n1.values()))
check("half the base", "0.5", F(sum(n1.values()), sum(N.values())))
check("non-recipients 5,000", "5000", sum(n0.values()))
check("active no coupon 4,000", "4000", n0['A']); check("lapsed no coupon 1,000", "1000", n0['L'])
check("coupon share active 0.20", "0.20", e['A']); check("coupon share lapsed 0.80", "0.80", e['L'])
Y1bar = sum(n1[s] * mu1[s] for s in N) / sum(n1.values()); Y0bar = sum(n0[s] * mu0[s] for s in N) / sum(n0.values())
check("pooled coupon 0.40", "0.40", Y1bar); check("pooled no coupon 0.62", "0.62", Y0bar)
check("pooled difference -0.22", "-0.22", Y1bar - Y0bar)
check("within active +0.05", "0.05", tau['A']); check("within lapsed +0.20", "0.20", tau['L'])

# break-even
tstar = c * Y1bar / m
check("break-even 0.133", "0.133", tstar); check("10 x 0.40 = 4", "4", c * Y1bar)

# decomposition
w1 = {s: F(n1[s], sum(n1.values())) for s in N}
check("recipients 0.2 active", "0.2", w1['A']); check("recipients 0.8 lapsed", "0.8", w1['L'])
att = sum(w1[s] * tau[s] for s in N); check("ATT 0.17", "0.17", att)
y0t = sum(w1[s] * mu0[s] for s in N); check("E[Y(0)|D=1] 0.23", "0.23", y0t)
check("selection bias -0.39", "-0.39", y0t - Y0bar); check("ATT + bias = -0.22", "-0.22", att + (y0t - Y0bar))

# estimands
w0 = {s: F(n0[s], sum(n0.values())) for s in N}
ate = sum(F(N[s], 10000) * tau[s] for s in N); atu = sum(w0[s] * tau[s] for s in N)
check("ATE 0.125", "0.125", ate); check("ATU 0.08", "0.08", atu)
check("ATU weights 0.8 active", "0.8", w0['A']); check("ATU weights 0.2 lapsed", "0.2", w0['L'])
net_att = m * att - c * Y1bar; check("net per coupon +1.10", "1.10", net_att)
ey1 = sum(F(N[s], 10000) * mu1[s] for s in N); check("E[Y(1)] 0.55", "0.55", ey1)
check("everyone break-even 0.183", "0.183", c * ey1 / m); assert c * ey1 / m > ate
check("everyone loses 1.75 per member", "-1.75", m * ate - c * ey1)

# IPW for the ATE
wt = {('A', 1): 1 / e['A'], ('L', 1): 1 / e['L'], ('A', 0): 1 / (1 - e['A']), ('L', 0): 1 / (1 - e['L'])}
check("weight 1/0.2 = 5", "5", wt[('A', 1)]); check("weight 1/0.8 = 1.25", "1.25", wt[('L', 1)])
check("weight active none 1.25", "1.25", wt[('A', 0)]); check("weight lapsed none 5", "5", wt[('L', 0)])
for (s, d), w in wt.items():
    check(f"weighted members {s}{d} 5,000", "5000", (n1[s] if d else n0[s]) * w)
ipw1 = sum(n1[s] * wt[(s, 1)] * mu1[s] for s in N) / 10000; ipw0 = sum(n0[s] * wt[(s, 0)] * mu0[s] for s in N) / 10000
check("IPW E[Y(1)] 0.55", "0.55", ipw1); check("IPW E[Y(0)] 0.425", "0.425", ipw0); check("IPW ATE 0.125", "0.125", ipw1 - ipw0)

# IPW for the ATT and the effective sample size
odds = {s: e[s] / (1 - e[s]) for s in N}
check("odds active 0.25", "0.25", odds['A']); check("odds lapsed 4", "4", odds['L'])
check("weighted active non-recipients 1,000", "1000", n0['A'] * odds['A']); check("weighted lapsed 4,000", "4000", n0['L'] * odds['L'])
sw = sum(n0[s] * odds[s] for s in N); sw2 = sum(n0[s] * odds[s] ** 2 for s in N)
check("sum of ATT weights 5,000", "5000", sw)
check("Hajek control mean 0.23", "0.23", sum(n0[s] * odds[s] * mu0[s] for s in N) / sw)
check("IPW ATT 0.17", "0.17", Y1bar - sum(n0[s] * odds[s] * mu0[s] for s in N) / sw)
check("sum w^2 16,250", "16250", sw2); check("5,000^2 = 25,000,000", "25000000", sw ** 2)
check("ESS 1,538", "1538", sw ** 2 / sw2)
for d in (1, 0):
    ws = [((n1 if d else n0)[s], wt[(s, d)]) for s in N]
    check(f"ATE ESS arm {d} 3,200", "3200", sum(n * w for n, w in ws) ** 2 / sum(n * w * w for n, w in ws))

# Result 1.7 on the segments: OLS on a coupon dummy and a lapsed dummy, on the exact 10,000 rows
def rows(cells):
    out = []
    for g, d, n, buy in cells: out += [(g, d, 1)] * buy + [(g, d, 0)] * (n - buy)
    return out
segcells = [(s, 1, n1[s], int(n1[s] * mu1[s])) for s in N] + [(s, 0, n0[s], int(n0[s] * mu0[s])) for s in N]
R = rows(segcells)
D = np.array([r[1] for r in R], float); Y = np.array([r[2] for r in R], float); L = np.array([r[0] == 'L' for r in R], float)
b = np.linalg.lstsq(np.column_stack([np.ones_like(Y), D, L]), Y, rcond=None)[0]
check("OLS weight n e(1-e) = 800", "800", N['A'] * e['A'] * (1 - e['A'])); assert N['L'] * e['L'] * (1 - e['L']) == 800
check("OLS coefficient 0.125", "0.125", b[1]); assert b[1] < tstar < att

# collider (M7-R3)
open_c, buy_c, open_n, buy_n = 500, 250, 250, 250
check("1,000 members", "1000", 4 * 250)
check("buy | coupon, open 0.50", "0.50", F(buy_c, open_c)); check("buy | no coupon, open 1.00", "1.00", F(buy_n, open_n))
check("effect among openers -0.50", "-0.50", F(buy_c, open_c) - F(buy_n, open_n))
check("true effect 0 (randomised, no effect)", "0", F(250, 500) - F(250, 500))

# ── Block B: the four score bands (M7-R4, R4b) ──
bands = {1: (2500, 200, 'A'), 2: (2500, 800, 'A'), 3: (2500, 1550, 'L'), 4: (2500, 2450, 'L')}
Nb = {k: v[0] for k, v in bands.items()}; n1b = {k: v[1] for k, v in bands.items()}; n0b = {k: Nb[k] - n1b[k] for k in bands}
seg = {k: v[2] for k, v in bands.items()}
for k, s in [(1, "2300"), (2, "1700"), (3, "950"), (4, "50")]: check(f"band {k} no coupon", s, n0b[k])
check("bands total 10,000", "10000", sum(Nb.values())); check("bands coupons 5,000", "5000", sum(n1b.values()))
check("bands no coupon 5,000", "5000", sum(n0b.values()))
check("bands refine segments: active 1,000", "1000", n1b[1] + n1b[2]); check("lapsed 4,000", "4000", n1b[3] + n1b[4])
assert n0b[1] + n0b[2] == n0['A'] and n0b[3] + n0b[4] == n0['L'] and Nb[1] + Nb[2] == N['A']
eb = {k: F(n1b[k], Nb[k]) for k in bands}
for k, s in [(1, "0.08"), (2, "0.32"), (3, "0.62"), (4, "0.98")]: check(f"e-hat band {k}", s, eb[k])
ob = {k: eb[k] / (1 - eb[k]) for k in bands}
for k, s in [(1, "0.087"), (2, "0.47"), (3, "1.63"), (4, "49")]: check(f"ATT weight band {k}", s, ob[k])
check("band 4: 98% got one", "98", 100 * eb[4]); assert all(0 < eb[k] < 1 for k in bands)  # Lena's third sentence holds
for k, s in [(1, "200"), (2, "800"), (3, "1550"), (4, "2450")]:
    check(f"weighted non-recipients band {k}", s, n0b[k] * ob[k]); assert n0b[k] * ob[k] == n1b[k]
SW = sum(n0b[k] * ob[k] for k in bands); SW2 = sum(n0b[k] * ob[k] ** 2 for k in bands)
check("weighted total 5,000", "5000", SW)
for k, s in [(1, "4"), (2, "16"), (3, "31"), (4, "49")]: check(f"share of weight band {k} %", s, 100 * n0b[k] * ob[k] / SW)
check("50 is 1% of non-recipients", "1", 100 * F(n0b[4], sum(n0b.values())))
check("ESS all bands 203", "203", SW ** 2 / SW2)
check("largest weight 49", "49", max(ob.values()))

# trimming at [0.05, 0.95]
a = F(5, 100); keep = [k for k in bands if a <= eb[k] <= 1 - a]; assert keep == [1, 2, 3]
n1k = sum(n1b[k] for k in keep); check("trimmed recipients 2,550", "2550", n1k)
check("all recipients 20% active", "20", 100 * F(n1b[1] + n1b[2], 5000))
check("trimmed recipients 39% active", "39", 100 * F(n1b[1] + n1b[2], n1k))
check("twice as active", "2", F(n1b[1] + n1b[2], n1k) / F(1000, 5000), tol=0.05)
check("trimmed largest weight 1.63", "1.63", max(ob[k] for k in keep))
swk = sum(n0b[k] * ob[k] for k in keep); sw2k = sum(n0b[k] * ob[k] ** 2 for k in keep)
check("trimmed ESS 2,225", "2225", swk ** 2 / sw2k); check("trimmed non-recipients 4,950", "4950", sum(n0b[k] for k in keep))

# balance of the lapsed share
p_t = F(n1b[3] + n1b[4], 5000); p_c = F(n0b[3] + n0b[4], 5000)
check("recipients 0.80 lapsed", "0.80", p_t); check("non-recipients 0.20 lapsed", "0.20", p_c)
check("0.8 x 0.2 = 0.16", "0.16", p_t * (1 - p_t)); assert p_c * (1 - p_c) == F(16, 100)
check("SMD before 1.50", "1.50", (p_t - p_c) / sqrt((p_t * (1 - p_t) + p_c * (1 - p_c)) / 2))
p_cw = sum(n0b[k] * ob[k] for k in (3, 4)) / SW
check("weighted non-recipients 80% lapsed", "80", 100 * p_cw); check("SMD after 0", "0", p_t - p_cw)

# outcomes by band (R4b)
buy1 = {1: 160, 2: 640, 3: 465, 4: 735}; buy0 = {1: 1725, 2: 1275, 3: 95, 4: 5}
p1 = {k: F(buy1[k], n1b[k]) for k in bands}; p0 = {k: F(buy0[k], n0b[k]) for k in bands}
for k, a1, a0, dd in [(1, "0.80", "0.75", "0.05"), (2, "0.80", "0.75", "0.05"), (3, "0.30", "0.10", "0.20"), (4, "0.30", "0.10", "0.20")]:
    check(f"band {k} coupon rate", a1, p1[k]); check(f"band {k} no-coupon rate", a0, p0[k]); check(f"band {k} difference", dd, p1[k] - p0[k])
    assert p1[k] == mu1[seg[k]] and p0[k] == mu0[seg[k]]       # the bands reproduce the segment rates
check("bands pooled coupon 0.40", "0.40", F(sum(buy1.values()), 5000)); check("bands pooled none 0.62", "0.62", F(sum(buy0.values()), 5000))
check("bands pooled difference -0.22", "-0.22", F(sum(buy1.values()) - sum(buy0.values()), 5000))

# OLS on coupon and band dummies, on the exact rows
bandcells = [(k, 1, n1b[k], buy1[k]) for k in bands] + [(k, 0, n0b[k], buy0[k]) for k in bands]
R = rows(bandcells)
D = np.array([r[1] for r in R], float); Y = np.array([r[2] for r in R], float)
Z = np.column_stack([np.ones_like(Y), D] + [np.array([r[0] == k for r in R], float) for k in (2, 3, 4)])
bb = np.linalg.lstsq(Z, Y, rcond=None)[0]
vw = {k: Nb[k] * eb[k] * (1 - eb[k]) for k in bands}
check("band 4 OLS weight 49", "49", vw[4]); check("OLS weights total 1,366", "1366", sum(vw.values()))
check("OLS on band dummies 0.120", "0.120", bb[1])
check("Result 1.7 formula = OLS", "0.120", sum(vw[k] * (p1[k] - p0[k]) for k in bands) / sum(vw.values()))

# standardisation by segment, IPW by band, trimmed IPW, SEs
def std_seg(b0):
    p0L = F(b0[3] + b0[4], n0b[3] + n0b[4]); p0A = F(b0[1] + b0[2], n0b[1] + n0b[2])
    return sum(n1b[k] * (p1[k] - (p0A if seg[k] == 'A' else p0L)) for k in bands) / 5000
def ipw_band(b0, ks):
    n = sum(n1b[k] for k in ks)
    return sum(n1b[k] * (p1[k] - F(b0[k], n0b[k])) for k in ks) / n
def se_band(ks):
    n = sum(n1b[k] for k in ks)
    return sqrt(sum(float(F(n1b[k], n)) ** 2 * (float(p1[k] * (1 - p1[k])) / n1b[k] + float(p0[k] * (1 - p0[k])) / n0b[k]) for k in ks))
check("standardisation by segment 0.17", "0.17", std_seg(buy0))
check("Hajek IPW by band 0.17", "0.17", ipw_band(buy0, [1, 2, 3, 4]))
# Hajek IPW with the band propensity, computed as weighting, equals the stratified estimate
hj = F(sum(buy1.values()), 5000) - sum(buy0[k] * ob[k] for k in bands) / SW
check("Hajek IPW as weighting 0.17", "0.17", hj)
check("SE untrimmed 0.022", "0.022", se_band([1, 2, 3, 4]))
check("IPW trimmed 0.141", "0.141", ipw_band(buy0, keep)); check("SE trimmed 0.011", "0.011", se_band(keep))
v4 = float(F(n1b[4], 5000)) ** 2 * (float(p1[4] * (1 - p1[4])) / n1b[4] + float(p0[4] * (1 - p0[4])) / n0b[4])
check("band 4 share of variance 93%", "93", 100 * v4 / se_band([1, 2, 3, 4]) ** 2)

# trimming changed the decision
mu1k = sum(n1b[k] * p1[k] for k in keep) / n1k; attk = ipw_band(buy0, keep)
check("trimmed E[Y(1)|D=1] 0.496", "0.496", mu1k); check("trimmed break-even 0.165", "0.165", c * mu1k / m)
check("trimmed net -0.73", "-0.73", m * attk - c * mu1k); assert attk < c * mu1k / m
check("band 4 lift 0.20", "0.20", p1[4] - p0[4]); check("band 4 E[Y(1)] 0.30", "0.30", p1[4])
check("band 4 break-even 0.100", "0.100", c * p1[4] / m); check("band 4 net +3.00", "3.00", m * (p1[4] - p0[4]) - c * p1[4])
check("band 4 recipients 2,450", "2450", n1b[4])
check("0.3 x 0.7 = 0.21", "0.21", p1[4] * (1 - p1[4])); check("0.1 x 0.9 = 0.09", "0.09", p0[4] * (1 - p0[4]))
se4 = sqrt(0.21 / 2450 + 0.09 / 50); check("band 4 SE 0.043", "0.043", se4)
check("band 4 interval starts 0.115", "0.115", 0.20 - 1.96 * se4); assert 0.20 - 1.96 * se4 > 0.100
check("untrimmed interval starts 0.127", "0.127", 0.17 - 1.96 * 0.022); assert 0.17 - 1.96 * se_band([1, 2, 3, 4]) < float(tstar)
check("active coupon net -6.50", "-6.50", m * tau['A'] - c * mu1['A'])
check("1,000 active coupons", "1000", n1b[1] + n1b[2])
# the parts add up: 5,000 x 1.10 = 2,550 x (-0.7255) + 2,450 x 3.00
assert 5000 * net_att == n1k * (m * attk - c * mu1k) + n1b[4] * (m * (p1[4] - p0[4]) - c * p1[4])

# silent extrapolation, loud weights: 10 of band 4's 50 had bought
alt = dict(buy0); alt[4] = 10
check("what-if standardisation by segment 0.166", "0.166", std_seg(alt))
check("what-if IPW by band 0.121", "0.121", ipw_band(alt, [1, 2, 3, 4]))
check("five purchases move IPW by 0.049", "0.049", ipw_band(buy0, [1, 2, 3, 4]) - ipw_band(alt, [1, 2, 3, 4]))
check("lapsed non-recipients 1,000", "1000", n0b[3] + n0b[4]); check("950 in band 3", "950", n0b[3])

# AIPW on the two segments
def aipw_seg(s, m1t, m0t, et):
    return (m1t - m0t) + e[s] / et * (mu1[s] - m1t) - (1 - e[s]) / (1 - et) * (mu0[s] - m0t)
rowsA = [("ignore segment, e right", Y1bar, Y1bar, Y0bar, Y0bar, e['A'], e['L'], "0.05", "0.20", "0.125"),
         ("mu right, e = 0.5", mu1['A'], mu1['L'], mu0['A'], mu0['L'], F(1, 2), F(1, 2), "0.05", "0.20", "0.125"),
         ("both wrong", Y1bar, Y1bar, Y0bar, Y0bar, F(1, 2), F(1, 2), "-0.268", "-0.172", "-0.22")]
for lab, m1A, m1L, m0A, m0L, eA, eL, sA, sL, sAll in rowsA:
    pA = aipw_seg('A', m1A, m0A, eA); pL = aipw_seg('L', m1L, m0L, eL)
    check(f"AIPW {lab} active", sA, pA); check(f"AIPW {lab} lapsed", sL, pL); check(f"AIPW {lab} ATE", sAll, (pA + pL) / 2)
check("pooled working model 0.40", "0.40", Y1bar); check("pooled working model 0.62", "0.62", Y0bar)
check("first row: 0.80 - 0.40", "0.40", mu1['A'] - Y1bar); check("first row: 0.75 - 0.62", "0.13", mu0['A'] - Y0bar)
check("first row total 0.05", "0.05", F(-22, 100) + F(40, 100) - F(13, 100))

# sensitivity
check("gd keep as run 0.037", "0.037", att - tstar)
check("lapsed break-even 0.100", "0.100", c * mu1['L'] / m); check("gd lapsed 0.100", "0.100", tau['L'] - c * mu1['L'] / m)
check("active break-even 0.267", "0.267", c * mu1['A'] / m); check("gd active 0.217", "0.217", c * mu1['A'] / m - tau['A'])
g = mu0['A'] - mu0['L']; dl = p_t - p_c
check("gamma 0.65", "0.65", g); check("delta 0.60", "0.60", dl); check("gamma delta 0.39", "0.39", g * dl)
check("gamma delta equals the selection bias", "0.39", -(y0t - Y0bar))
check("a tenth as strong", "0.1", (att - tstar) / (g * dl), tol=0.01)
assert (c * mu1['A'] / m - tau['A']) / (g * dl) > F(1, 2)            # "over half as strong"
assert max(att - tstar, tau['L'] - c * mu1['L'] / m, c * mu1['A'] / m - tau['A']) < g * dl   # none needs more than segment

print(f"\n{len(FAIL)} mismatches: {FAIL}")
