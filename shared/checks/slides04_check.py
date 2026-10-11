"""Arithmetic checks for meetings/m04/slides.tex (lecture case: Lena's coupon programme, Houtan Coffee, M4 releases;
Region 2's four cells). The slides use their own numbers, not the notes' worked example. Run: python3 slides04_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import sqrt, erf
import numpy as np
from scipy import integrate, stats
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
def emax(k):
    """E[max of k iid N(0,1)] by numerical integration."""
    f = lambda z: z * k * stats.norm.pdf(z) * stats.norm.cdf(z) ** (k - 1)
    return integrate.quad(f, -12, 12)[0]
se = lambda p1, n1, p0, n0: sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)

m, c = 30, 10
# ── Region 2: the four cells (type, spending) ──
cells = {('E', 'H'): (F(65, 100), F(60, 100)), ('E', 'L'): (F(35, 100), F(30, 100)),
         ('A', 'H'): (F(50, 100), F(30, 100)), ('A', 'L'): (F(20, 100), F(0))}
share = F(1, 4)
tau = {k: v[0] - v[1] for k, v in cells.items()}
for k, lab in [(('E', 'H'), "0.05"), (('E', 'L'), "0.05"), (('A', 'H'), "0.20"), (('A', 'L'), "0.20")]:
    check(f"tau {k}", lab, tau[k])
check("shares 25% each", "25", 100 * share); assert sum([share] * 4) == 1
for t in 'EA':
    for d in (0, 1):
        check(f"spending moves rate by 0.30 ({t}, D={d})", "0.30", cells[(t, 'H')][1 - d] - cells[(t, 'L')][1 - d])
# test size and halves
check("4,000 members in two halves of 2,000", "2000", 4000 / 2)

# ── The number that decides each line ──
for k, be, a, b, net in [(('E', 'H'), "0.217", "1.50", "6.50", "-5.00"), (('E', 'L'), "0.117", "1.50", "3.50", "-2.00"),
                         (('A', 'H'), "0.167", "6.00", "5.00", "1.00"), (('A', 'L'), "0.067", "6.00", "2.00", "4.00")]:
    p1 = cells[k][0]
    check(f"tau* {k}", be, F(c, m) * p1); check(f"30 tau {k}", a, m * tau[k]); check(f"10 p1 {k}", b, c * p1)
    check(f"net {k}", net, m * tau[k] - c * p1)
check("A-High margin 0.20 - 0.167 = 0.033", "0.033", tau[('A', 'H')] - cells[('A', 'H')][0] / 3)
p1E = (cells[('E', 'H')][0] + cells[('E', 'L')][0]) / 2
check("executives p1 0.50", "0.50", p1E); check("executives tau* 0.167", "0.167", p1E / 3)
check("Meeting 3: active 0.05, lapsed 0.20", "0.15", F(20, 100) - F(5, 100))

# ── Splitting on the outcome vs on the effect (pooled, e = 1/2) ──
EY = {k: (v[0] + v[1]) / 2 for k, v in cells.items()}
Y_high = (EY[('E', 'H')] + EY[('A', 'H')]) / 2; Y_low = (EY[('E', 'L')] + EY[('A', 'L')]) / 2
Y_exec = (EY[('E', 'H')] + EY[('E', 'L')]) / 2; Y_an = (EY[('A', 'H')] + EY[('A', 'L')]) / 2
Y1 = sum(v[0] for v in cells.values()) / 4; Y0 = sum(v[1] for v in cells.values()) / 4
check("Ybar high 0.5125", "0.5125", Y_high); check("Ybar low 0.2125", "0.2125", Y_low); check("spending gap 0.30", "0.30", Y_high - Y_low)
check("Ybar exec 0.475", "0.475", Y_exec); check("Ybar analyst 0.25", "0.25", Y_an); check("type gap 0.225", "0.225", Y_exec - Y_an)
check("D gap 0.125", "0.125", Y1 - Y0); check("root Ybar 0.3625", "0.3625", (Y_high + Y_low) / 2)
check("CART score spending 0.0225", "0.0225", F(1, 4) * (Y_high - Y_low) ** 2)
check("CART score type 0.0127", "0.0127", F(1, 4) * (Y_exec - Y_an) ** 2)
assert F(1, 4) * (Y1 - Y0) ** 2 < F(1, 4) * (Y_exec - Y_an) ** 2 < F(1, 4) * (Y_high - Y_low) ** 2
tau_high = (tau[('E', 'H')] + tau[('A', 'H')]) / 2; tau_low = (tau[('E', 'L')] + tau[('A', 'L')]) / 2
tau_E, tau_A = tau[('E', 'H')], tau[('A', 'H')]; ate = sum(tau.values()) / 4
check("tau gap spending 0", "0", tau_high - tau_low); check("tau gap type 0.15", "0.15", tau_A - tau_E)
# causal Delta in both forms
D_type = F(1, 2) * (tau_E - ate) ** 2 + F(1, 2) * (tau_A - ate) ** 2
check("causal Delta type 0.0056", "0.0056", D_type); check("second form equals first", "0", D_type - F(1, 4) * (tau_A - tau_E) ** 2)
check("causal Delta spending 0", "0", F(1, 2) * (tau_high - ate) ** 2 + F(1, 2) * (tau_low - ate) ** 2)

# ── Result 1.1 on Region 2: outcome gap = baseline gap + tau gap / 2 ──
mu0_high = (cells[('E', 'H')][1] + cells[('A', 'H')][1]) / 2; mu0_low = (cells[('E', 'L')][1] + cells[('A', 'L')][1]) / 2
mu0_E = (cells[('E', 'H')][1] + cells[('E', 'L')][1]) / 2; mu0_A = (cells[('A', 'H')][1] + cells[('A', 'L')][1]) / 2
check("mu0 high 0.45", "0.45", mu0_high); check("mu0 low 0.15", "0.15", mu0_low)
check("mu0 exec 0.45", "0.45", mu0_E); check("mu0 analyst 0.15", "0.15", mu0_A)
check("half effect gap type -0.075", "-0.075", F(1, 2) * (tau_E - tau_A))
check("Result 1.1 spending: 0.30", "0.30", (mu0_high - mu0_low) + F(1, 2) * (tau_high - tau_low))
check("Result 1.1 type: 0.225", "0.225", (mu0_E - mu0_A) + F(1, 2) * (tau_E - tau_A))
assert (mu0_E - mu0_A) + F(1, 2) * (tau_E - tau_A) == Y_exec - Y_an  # decomposition reproduces the pooled gap

# ── Three trees ──
# S-learner depth 2, within each spending group: type gap vs D gap
for sp in 'HL':
    tg = EY[('E', sp)] - EY[('A', sp)]; dg = (cells[('E', sp)][0] + cells[('A', sp)][0]) / 2 - (cells[('E', sp)][1] + cells[('A', sp)][1]) / 2
    check(f"S depth 2 type gap ({sp}) 0.225", "0.225", tg); check(f"S depth 2 D gap ({sp}) 0.125", "0.125", dg)
# T-learner
m1H = (cells[('E', 'H')][0] + cells[('A', 'H')][0]) / 2; m1L = (cells[('E', 'L')][0] + cells[('A', 'L')][0]) / 2
m0H, m0L = mu0_high, mu0_low
check("mu1 high 0.575", "0.575", m1H); check("mu1 low 0.275", "0.275", m1L); check("mu0 high 0.45", "0.45", m0H); check("mu0 low 0.15", "0.15", m0L)
check("coupon arm spending gap 0.30", "0.30", m1H - m1L)
check("coupon arm type gap 0.15", "0.15", (cells[('E', 'H')][0] + cells[('E', 'L')][0]) / 2 - (cells[('A', 'H')][0] + cells[('A', 'L')][0]) / 2)
check("control arm type gap 0.30 (ties)", "0.30", mu0_E - mu0_A); check("control spending gap 0.30", "0.30", m0H - m0L)
check("T tau high 0.125", "0.125", m1H - m0H); check("T tau low 0.125", "0.125", m1L - m0L)
check("causal tree root 0.125", "0.125", ate)

# ── Lena's tree on half A (counts behind the printed lifts; 250 per arm per analyst leaf, executives 200 app / 300 no app) ──
halfA = {'AL': (58, 250, 0, 250), 'AH': (130, 250, 77, 250), 'Eapp': (108, 200, 70, 200), 'Eno': (141, 300, 138, 300)}
for k, lab in [('AL', "0.23"), ('AH', "0.21"), ('Eapp', "0.19"), ('Eno', "0.01")]:
    a, n1, b, n0 = halfA[k]; check(f"half-A lift {k}", lab, F(a, n1) - F(b, n0))
check("half A: 2,000 members", "2000", 2 * sum(v[1] for v in halfA.values()))
check("app-use gap on half A 0.18", "0.18", F(19, 100) - F(1, 100))
thr = {'AL': F(20, 100) / 3, 'AH': F(50, 100) / 3, 'Eapp': p1E / 3, 'Eno': p1E / 3}
for k, lab in [('AL', "0.067"), ('AH', "0.167"), ('Eapp', "0.167"), ('Eno', "0.167")]: check(f"H1 tau* {k}", lab, thr[k])
assert [F(23, 100) > thr['AL'], F(21, 100) > thr['AH'], F(19, 100) > thr['Eapp'], F(1, 100) > thr['Eno']] == [True, True, True, False]
check("at least 42 candidate splits: 14 fields x 3 nodes", "42", 14 * 3)

# ── Two noisy splits ──
check("Delta A 0.0064", "0.0064", 0.5 * (0.02 - 0.10) ** 2 + 0.5 * (0.18 - 0.10) ** 2)
check("Delta B 0.0001", "0.0001", 0.5 * (0.09 - 0.10) ** 2 + 0.5 * (0.11 - 0.10) ** 2)
check("discovery gap 0.16", "0.16", 0.18 - 0.02); check("fresh gap 0.04", "0.04", 0.12 - 0.08)
check("fresh split A averages the overall 0.10", "0.10", (0.08 + 0.12) / 2)

# ── Winner's curse ──
for k, lab in [(2, "0.56"), (5, "1.16"), (20, "1.87"), (100, "2.51")]: check(f"E[max Z] k={k}", lab, emax(k))
check("by hand 0.125 + 1.87 x 0.04", "0.20", 0.125 + 1.87 * 0.04); check("(with exact E max)", "0.20", 0.125 + emax(20) * 0.04)
assert 0.125 + emax(20) * 0.04 > 0.5 / 3

# ── What honesty costs ──
check("bias^2 > s^2 from four candidates", "1", float(emax(4) > 1 and emax(3) < 1))
check("1.87^2 = 3.50", "3.50", 1.87 ** 2)
pH1, pH0 = 0.50, 0.30
check("0.50 x 0.50 = 0.25", "0.25", pH1 * (1 - pH1)); check("0.30 x 0.70 = 0.21", "0.21", pH0 * (1 - pH0))
s_full = se(pH1, 500, pH0, 500); s_half = se(pH1, 250, pH0, 250); s_quarter = se(pH1, 125, pH0, 125)
check("500 per arm = 25% of 4,000 / 2", "500", 4000 * 0.25 / 2)
check("SE 500 per arm 0.030", "0.030", s_full); check("SE 250 per arm 0.043", "0.043", s_half); check("SE 125 per arm 0.061", "0.061", s_quarter)
check("half = sqrt(2) s", "0", s_half - sqrt(2) * s_full, tol=1e-12); check("quarter = 2 s", "0", s_quarter - 2 * s_full, tol=1e-12)

# ── Protocol: Bonferroni ──
check("1 - 0.05/4 = 98.75%", "98.75", 100 * (1 - 0.05 / 4))
zB = stats.norm.ppf(1 - 0.05 / 8); check("Bonferroni z 2.50", "2.50", zB); check("95% z 1.96", "1.96", stats.norm.ppf(0.975))

# ── H2: half B ──
halfB = {'AL': (50, 250, 0, 250), 'AH': (125, 250, 80, 250), 'Eapp': (100, 200, 92, 200), 'Eno': (150, 300, 132, 300)}
check("half B: 2,000 members", "2000", 2 * sum(v[1] for v in halfB.values()))
assert all(halfA[k][1] == halfB[k][1] and halfA[k][3] == halfB[k][3] for k in halfA)
assert halfB['AL'][1] + halfB['AH'][1] == 500 and halfB['Eapp'][1] + halfB['Eno'][1] == 500  # 25% / 50% of 1,000 per arm
B = {}
for k, lift, sel, be, lo95, hi95, loB, hiB in [
        ('AL', "0.20", "0.025", "0.067", "0.15", "0.25", "0.14", "0.26"),
        ('AH', "0.18", "0.043", "0.167", "0.10", "0.26", "0.07", "0.29"),
        ('Eapp', "0.04", "0.050", "0.167", "-0.06", "0.14", "-0.08", "0.16"),
        ('Eno', "0.06", "0.041", "0.167", "-0.02", "0.14", "-0.04", "0.16")]:
    a, n1, b, n0 = halfB[k]; p1, p0 = a / n1, b / n0; t = p1 - p0; s = se(p1, n1, p0, n0)
    check(f"half-B lift {k}", lift, t); check(f"half-B SE {k}", sel, s); check(f"half-B tau* = p1/3 {k}", be, p1 / 3)
    check(f"95% low {k}", lo95, t - 1.96 * s); check(f"95% high {k}", hi95, t + 1.96 * s)
    check(f"98.75% low {k}", loB, t - zB * s); check(f"98.75% high {k}", hiB, t + zB * s)
    B[k] = (t, s, p1 / 3)
check("p0 x (1 - p0) for 80/250: 0.2176", "0.2176", 0.32 * 0.68)
check("half-B p1 reproduces four-cell tau* (AL)", "0", B['AL'][2] - float(cells[('A', 'L')][0] / 3), tol=1e-12)
check("half-B p1 reproduces four-cell tau* (AH)", "0", B['AH'][2] - float(cells[('A', 'H')][0] / 3), tol=1e-12)
check("half-B p1 reproduces executive tau* (app)", "0", B['Eapp'][2] - float(p1E / 3), tol=1e-12)
check("half-B p1 reproduces executive tau* (no app)", "0", B['Eno'][2] - float(p1E / 3), tol=1e-12)
# directions: liked leaves fell, disliked leaf rose
assert all(float(F(*halfA[k][:2]) - F(*halfA[k][2:])) > B[k][0] for k in ('AL', 'AH', 'Eapp'))
assert float(F(*halfA['Eno'][:2]) - F(*halfA['Eno'][2:])) < B['Eno'][0]
# H3 card: interval vs own tau*
def card(lo, hi, be): return 'coupon' if lo > be else ('no coupon' if hi < be else 'undecided')
for z in (1.96, zB):
    got = [card(B[k][0] - z * B[k][1], B[k][0] + z * B[k][1], B[k][2]) for k in ('AL', 'AH', 'Eapp', 'Eno')]
    assert got == ['coupon', 'undecided', 'no coupon', 'no coupon'], (z, got)
assert B['AH'][0] - zB * B['AH'][1] > 0  # A-High: real effect
check("Bonferroni: chance any line wrong <= 0.05", "0.05", 4 * (0.05 / 4))

# ── Forest weights: four trees, x's leaves {1,2,3,5}, {1,2,4,6}, {1,2,3,7}, {1,2,4,8} ──
leaves = [{1, 2, 3, 5}, {1, 2, 4, 6}, {1, 2, 3, 7}, {1, 2, 4, 8}]
alpha = {i: sum(F(1, len(L)) for L in leaves if i in L) / len(leaves) for i in range(1, 9)}
check("alpha units 1,2: 0.25", "0.25", alpha[1]); check("alpha units 3,4: 0.125", "0.125", alpha[3]); check("alpha units 5-8: 0.0625", "0.0625", alpha[5])
check("total 1,2: 0.50", "0.50", alpha[1] + alpha[2]); check("total 3,4: 0.25", "0.25", alpha[3] + alpha[4])
check("total 5-8: 0.25", "0.25", sum(alpha[i] for i in (5, 6, 7, 8))); check("weights sum to 1", "1", sum(alpha.values()))
assert alpha[1] == alpha[2] and alpha[3] == alpha[4] and len({alpha[i] for i in (5, 6, 7, 8)}) == 1

# ── Local centering on Region 2 (e = 0.5) ──
ell = {k: v[1] + F(1, 2) * tau[k] for k, v in cells.items()}
for k, lab in [(('E', 'H'), "0.625"), (('E', 'L'), "0.325"), (('A', 'H'), "0.40"), (('A', 'L'), "0.10")]:
    check(f"ell {k}", lab, ell[k]); check(f"half tau {k}", "0.025" if k[0] == 'E' else "0.10", F(1, 2) * tau[k])
    check(f"coupon residual {k}", "0.025" if k[0] == 'E' else "0.10", cells[k][0] - ell[k])
    check(f"control residual {k}", "-0.025" if k[0] == 'E' else "-0.10", cells[k][1] - ell[k])

# ── Centering inside a neighbourhood: 8 analysts, alpha = 1/8 ──
units = [(1, 'H')] * 3 + [(1, 'L')] + [(0, 'H')] + [(0, 'L')] * 3
Yn = [cells[('A', sp)][1 - d] for d, sp in units]; ln = [ell[('A', sp)] for d, sp in units]; Dn = [d for d, sp in units]
mt = sum(y for y, d in zip(Yn, Dn) if d) / 4; mc = sum(y for y, d in zip(Yn, Dn) if not d) / 4
check("coupon mean 0.425", "0.425", mt); check("no-coupon mean 0.075", "0.075", mc); check("raw 0.35", "0.35", mt - mc)
check("leak 0.20 + 0.30 x (3/4 - 1/4)", "0.35", F(20, 100) + F(30, 100) * (F(3, 4) - F(1, 4)))
check("centred residual coupon +0.10", "0.10", sum(y - l for y, l, d in zip(Yn, ln, Dn) if d) / 4)
check("centred residual control -0.10", "-0.10", sum(y - l for y, l, d in zip(Yn, ln, Dn) if not d) / 4)
num = sum(F(1, 8) * (y - l) * (d - F(1, 2)) for y, l, d in zip(Yn, ln, Dn)); den = sum(F(1, 8) * (d - F(1, 2)) ** 2 for d in Dn)
check("numerator 0.05", "0.05", num); check("denominator 0.25", "0.25", den); check("centred estimate 0.20", "0.20", num / den)
num0 = sum(F(1, 8) * y * (d - F(1, 2)) for y, d in zip(Yn, Dn)); check("uncentred Result 1.4 estimate = raw 0.35", "0.35", num0 / den)

# ── Three cautions ──
check("interval width 2 x 1.96 x 0.10 = 0.39", "0.39", 2 * 1.96 * 0.10)
sd_tau = float(abs(tau_A - tau_E) / 2); check("true SD 0.075", "0.075", sd_tau)
check("Var tau-hat 0.015625", "0.015625", sd_tau ** 2 + 0.10 ** 2); check("= 0.125^2", "0.125", sqrt(sd_tau ** 2 + 0.10 ** 2))
check("Region 2 types gap 0.15", "0.15", tau_A - tau_E)

# ── More trees, same uncertainty ──
sig, rho = 0.10, 0.3
for Bt, lab in [(1, "0.100"), (10, "0.061"), (100, "0.055")]: check(f"forest SD B={Bt}", lab, sig * sqrt(rho + (1 - rho) / Bt))
check("floor sigma sqrt(rho) 0.055", "0.055", sig * sqrt(rho))

# ── Result 1.5 on Region 2: BLP by enumeration of the DR score phi (true mu, e = 0.5) ──
check("ATE 0.125", "0.125", ate); check("Var tau 0.005625", "0.005625", sd_tau ** 2); check("= 0.075^2", "0.075", sd_tau)
def blp(score):
    """score(type, spend, z) -> tau-hat; z is an extra independent draw (noise sign or app use) with probs pz."""
    rows = []
    for (t, sp), (p1, p0) in cells.items():
        for z, pz in score['z']:
            th = score['f'](t, sp, z)
            for d in (0, 1):
                mu1, mu0 = float(p1), float(p0); py = mu1 if d else mu0
                for y, pyy in [(1, py), (0, 1 - py)]:
                    phi = mu1 - mu0 + d * (y - mu1) / 0.5 - (1 - d) * (y - mu0) / 0.5
                    rows.append((phi, th, 0.25 * pz * 0.5 * pyy))
    phi, th, w = (np.array(v, float) for v in zip(*rows))
    thc = th - (w * th).sum()
    X = np.column_stack([np.ones_like(thc), thc]); W = np.diag(w)
    return np.linalg.solve(X.T @ W @ X, X.T @ W @ phi) if (w * thc ** 2).sum() > 1e-15 else np.array([(w * phi).sum(), 0.0])
tt = lambda t: float(tau_A if t == 'A' else tau_E)
b_true = blp({'z': [(0, 1.0)], 'f': lambda t, sp, z: tt(t)})
b_noise = blp({'z': [(+1, 0.5), (-1, 0.5)], 'f': lambda t, sp, z: tt(t) + 0.10 * z})  # noise with SD 0.10
b_app = blp({'z': [(1, 0.4), (0, 0.6)], 'f': lambda t, sp, z: 0.05 + 0.10 * z})      # app use independent of type
for lab, b, b2 in [("tau-hat = tau", b_true, "1"), ("tau + noise", b_noise, "0.36"), ("app-use score", b_app, "0")]:
    check(f"beta1 {lab}", "0.125", b[0]); check(f"beta2 {lab}", b2, b[1])
check("0.005625/0.015625 = 0.36", "0.36", 0.005625 / 0.015625)

# ── GATES on half B: quartiles of 250 per arm ──
Q = [("Bottom", 0.10, 121, 106, "0.060", "0.044"), ("2", 0.40, 110, 84, "0.104", "0.043"),
     ("3", 0.60, 103, 68, "0.140", "0.042"), ("Top", 0.90, 91, 46, "0.180", "0.039")]
g, sQ = [], []
for name, sh, a, b, gl, sl in Q:
    gg = a / 250 - b / 250; ss = se(a / 250, 250, b / 250, 250); g.append(gg); sQ.append(ss)
    check(f"GATE {name}", gl, gg); check(f"GATE SE {name}", sl, ss)
assert g == sorted(g)
check("top minus bottom 0.12", "0.12", g[3] - g[0]); check("gap SE 0.059", "0.059", sqrt(sQ[0] ** 2 + sQ[3] ** 2))
check("gap SE from printed SEs 0.059", "0.059", sqrt(0.044 ** 2 + 0.039 ** 2)); check("z 2.03", "2.03", (g[3] - g[0]) / sqrt(sQ[0] ** 2 + sQ[3] ** 2))
check("GATES average 0.121", "0.121", sum(g) / 4); check("half-B overall lift 425/1000 - 304/1000", "0.121", 425 / 1000 - 304 / 1000)
check("quartile coupon buyers = half-B leaf buyers 425", "425", sum(q[2] for q in Q)); check("leaf coupon buyers", "425", sum(v[0] for v in halfB.values()))
check("quartile control buyers = half-B leaf buyers 304", "304", sum(q[3] for q in Q)); check("leaf control buyers", "304", sum(v[2] for v in halfB.values()))
check("analysts per arm across quartiles = 500", "500", sum(250 * q[1] for q in Q))
# one split of each quartile's buyers into analysts and executives that matches the leaf totals exactly
anC, exC, anN, exN = [9, 35, 52, 79], [112, 75, 51, 12], [4, 16, 24, 36], [102, 68, 44, 10]
assert sum(anC) == halfB['AL'][0] + halfB['AH'][0] and sum(exC) == halfB['Eapp'][0] + halfB['Eno'][0]
assert sum(anN) == halfB['AL'][2] + halfB['AH'][2] and sum(exN) == halfB['Eapp'][2] + halfB['Eno'][2]
for i, q in enumerate(Q):
    na = round(250 * q[1]); assert anC[i] + exC[i] == q[2] and anN[i] + exN[i] == q[3]
    assert anC[i] <= na and anN[i] <= na and exC[i] <= 250 - na and exN[i] <= 250 - na
check("top quartile 90% analysts", "90", 100 * Q[3][1])

print(f"\n{len(FAIL)} mismatches: {FAIL}")
