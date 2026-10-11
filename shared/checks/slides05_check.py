"""Arithmetic checks for meetings/m05/slides.tex (lecture case: Lena's coupon programme, Houtan Coffee, M5 releases).
The slides use their own numbers, not the notes' worked example. Run: python3 slides05_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from itertools import product
from math import sqrt
import statistics
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)

m, c = 30, 10                                   # margin per purchase, coupon paid on every purchase made while holding it
R = lambda d, y: (m - c * d) * y                # reward R(d) = (30 - 10d) Y(d)
check("coupon-arm buyer's reward 20", "20", R(1, 1)); check("control-arm buyer's reward 30", "30", R(0, 1))

# ── Segment economics (Meeting 1 rates) ──
seg = {'A': (F(75, 100), F(80, 100)), 'L': (F(10, 100), F(30, 100))}   # (mu0, mu1)
v_seg = {k: m * (mu1 - mu0) - c * mu1 for k, (mu0, mu1) in seg.items()}
check("v active -6.50", "-6.50", v_seg['A']); check("v lapsed 3.00", "3.00", v_seg['L'])
base = 10000
G_every = (v_seg['A'] + v_seg['L']) / 2; G_seg = v_seg['L'] / 2
check("coupon everyone -1.75", "-1.75", G_every); check("everyone total -17,500", "-17500", base * G_every)
check("segment rule 1.50", "1.50", G_seg); check("segment total 15,000", "15000", base * G_seg)
check("random half of lapsed 0.75", "0.75", F(1, 4) * v_seg['L']); check("its total 7,500", "7500", base * F(1, 4) * v_seg['L'])

# ── Row contributions (Result 1.2) ──
g = lambda pi, d, y, e: pi * (d * R(1, y) / e - (1 - d) * R(0, y) / (1 - e))
check("e=0.5 coupon buyer +40", "40", g(1, 1, 1, F(1, 2))); check("e=0.5 control buyer -60", "-60", g(1, 0, 1, F(1, 2)))
check("e=0.25 coupon buyer +80", "80", g(1, 1, 1, F(1, 4))); check("e=0.25 control buyer -40", "-40", g(1, 0, 1, F(1, 4)))
check("1/0.25 = 4 times", "4", 1 / F(1, 4))

# ── The 80-row fold ──
cells = {('L', 1): (20, 6), ('L', 0): (20, 2), ('A', 1): (20, 16), ('A', 0): (20, 15)}
check("fold size 80", "80", sum(n for n, _ in cells.values()))
for (sg, d), (n, b) in cells.items():
    check(f"fold rate {sg} D={d} equals segment rate", str(float(seg[sg][d])), F(b, n))
def rows(policy):
    out = []
    for (sg, d), (n, b) in cells.items():
        pi = policy[sg]
        out += [g(pi, d, 1, F(1, 2))] * b + [g(pi, d, 0, F(1, 2))] * (n - b)
    return out
pol = {'seg': {'L': 1, 'A': 0}, 'every': {'L': 1, 'A': 1}, 'active': {'L': 0, 'A': 1}}
gr = {k: rows(p) for k, p in pol.items()}
check("lapsed rows sum 120", "120", 6 * 40 - 2 * 60); check("active rows sum -260", "-260", 16 * 40 - 15 * 60)
check("everyone sum -140", "-140", sum(gr['every']))
check("G-hat segment 1.50", "1.50", F(sum(gr['seg']), 80)); check("G-hat everyone -1.75", "-1.75", F(sum(gr['every']), 80))
check("G-hat active only -3.25", "-3.25", F(sum(gr['active']), 80))
assert F(sum(gr['seg']), 80) == G_seg and F(sum(gr['every']), 80) == G_every   # equal the hand values
check("six 40s", "6", gr['seg'].count(40)); check("two -60s", "2", gr['seg'].count(-60)); check("72 zeros", "72", gr['seg'].count(0))
sd_seg80 = statistics.stdev([float(x) for x in gr['seg']]); se_seg80 = sd_seg80 / sqrt(80)
check("80-row sd 14.50", "14.50", sd_seg80); check("80-row SE 1.62", "1.62", se_seg80)
check("1.96 x SE = 3.2", "3.2", 1.96 * se_seg80)
assert 1.0 < 2 * 1.96 * se_seg80                 # lists 1 apart cannot be told apart

# ── Result 1.3, exact moments by enumeration over (X, D, Y) ──
def moments(groups, policy, e=F(1, 2)):
    """groups: {name: (weight, mu0, mu1)}; policy: {name: 0/1}. Exact E[g], Var(g) by enumeration."""
    Eg = Eg2 = F(0)
    for k, (w, mu0, mu1) in groups.items():
        for d, pd in [(1, e), (0, 1 - e)]:
            py = mu1 if d else mu0
            for y, pyy in [(1, py), (0, 1 - py)]:
                x = g(policy[k], d, y, e); Eg += w * pd * pyy * x; Eg2 += w * pd * pyy * x * x
    return Eg, Eg2 - Eg ** 2
def result13(groups, policy, e=F(1, 2)):
    G = sum(w * policy[k] * (m * (mu1 - mu0) - c * mu1) for k, (w, mu0, mu1) in groups.items())
    return sum(w * policy[k] * (R(1, 1) ** 2 * mu1 / e + R(0, 1) ** 2 * mu0 / (1 - e)) for k, (w, mu0, mu1) in groups.items()) - G ** 2
segs = {k: (F(1, 2), mu0, mu1) for k, (mu0, mu1) in seg.items()}
check("E[R(1)^2] lapsed 120", "120", R(1, 1) ** 2 * seg['L'][1]); check("E[R(0)^2] lapsed 90", "90", R(0, 1) ** 2 * seg['L'][0])
Gs, Vs = moments(segs, pol['seg']); assert Vs == result13(segs, pol['seg'])
check("Var(g) segment 207.75", "207.75", Vs); check("sd 14.41", "14.41", sqrt(Vs))
check("SE on 5,000 0.20", "0.20", sqrt(Vs / 5000))
check("active rows add 995", "995", F(1, 2) * (R(1, 1) ** 2 * seg['A'][1] / F(1, 2) + R(0, 1) ** 2 * seg['A'][0] / F(1, 2)))
Ge, Ve = moments(segs, pol['every']); assert Ve == result13(segs, pol['every'])
check("sd coupon everyone 34.67", "34.67", sqrt(Ve))

# ── The four groups (2,500 each) ──
grp = {'L1': (F(5, 100), F(40, 100)), 'L2': (F(15, 100), F(20, 100)),
       'A1': (F(75, 100), F(95, 100)), 'A2': (F(75, 100), F(65, 100))}
tau = {k: mu1 - mu0 for k, (mu0, mu1) in grp.items()}; mu1 = {k: v[1] for k, v in grp.items()}
v = {k: m * tau[k] - c * mu1[k] for k in grp}
for k, t, vv in [('L1', "0.35", "6.50"), ('L2', "0.05", "-0.50"), ('A1', "0.20", "-3.50"), ('A2', "-0.10", "-9.50")]:
    check(f"tau {k}", t, tau[k]); check(f"v {k}", vv, v[k])
for sg, (a, b) in {'L': ('L1', 'L2'), 'A': ('A1', 'A2')}.items():   # each segment keeps its Meeting 1 averages
    assert (grp[a][0] + grp[b][0]) / 2 == seg[sg][0] and (grp[a][1] + grp[b][1]) / 2 == seg[sg][1]
ATE = sum(tau.values()) / 4; check("ATE 0.125", "0.125", ATE)
by_tau = sorted(grp, key=lambda k: -tau[k]); by_v = sorted(grp, key=lambda k: -v[k])
assert by_tau == ['L1', 'A1', 'L2', 'A2'] and by_v == ['L1', 'L2', 'A1', 'A2']
def curve(order, f):
    out, acc = [], F(0)
    for k in order: acc += f[k] / 4; out.append(acc)
    return out
Q = curve(by_tau, tau)
for q, s in zip(Q, ["0.0875", "0.1375", "0.150", "0.125"]): check(f"forest gain curve {s}", s, q)
assert Q[-1] == ATE and Q[3] < Q[2]                     # ends at the ATE; falls at A2
lap_first = [F(1, 4) * (tau['L1'] + tau['L2']) / 2, F(1, 2) * (tau['L1'] + tau['L2']) / 2]
lap_first += [lap_first[1] + F(1, 4) * (tau['A1'] + tau['A2']) / 2, ATE]
assert lap_first == [F(5, 100), F(10, 100), F(1125, 10000), F(125, 1000)]   # plotted segment-rule curve
check("Qini: top half adds 1,375", "1375", Q[1] * base)
# profit curves (Result 1.5)
Pv, Pt = curve(by_v, v), curve(by_tau, v)
for p, s in zip(Pv, ["1.625", "1.50", "0.625", "-1.75"]): check(f"P by v {s}", s, p)
for p, s in zip(Pt, ["1.625", "0.75", "0.625", "-1.75"]): check(f"P forest {s}", s, p)
slopes = [v[k] for k in by_v]; assert slopes == sorted(slopes, reverse=True)         # concave
for sl, s in zip(slopes, ["6.50", "-0.50", "-3.50", "-9.50"]): check(f"slope {s}", s, sl)
assert max(Pv) == Pv[0]                                  # peak at phi = 1/4, where v turns negative
assert Pt[1] < Pt[0] and Q[1] > Q[0]                     # gain rises while profit falls
check("forest top 5,000 = 0.75 per member", "0.75", Pt[1]); check("A1 coupon loses 3.50", "-3.50", v['A1'])

# ── Denominators (Result 1.4) ──
check("1,000 = top 20% of 5,000", "1000", F(20, 100) * 5000); check("540 + 460", "1000", 540 + 460)
check("216 = 540 x 0.40", "216", 540 * F(40, 100)); check("138 = 460 x 0.30", "138", 460 * F(30, 100))
check("rates then scale 100", "100", (F(216, 540) - F(138, 460)) * 1000); check("count difference 78", "78", 216 - 138)
check("equal arms 50", "50", 500 * F(40, 100) - 500 * F(30, 100)); check("arm-size part 28", "28", 78 - 50)
check("lift per member targeted 0.10", "0.10", F(216, 540) - F(138, 460)); check("Q(0.2) 0.02", "0.02", F(100, 5000))
check("Q(0.2) = 0.2 x 0.10", "0.02", F(2, 10) * F(1, 10)); check("per coupon -1.00", "-1.00", m * F(1, 10) - c * F(40, 100))

# ── RATE on the grid q = 1/4, 1/2, 3/4, 1 ──
qs = [F(1, 4), F(1, 2), F(3, 4), F(1)]
toc_f = [sum(tau[k] for k in by_tau[:j]) / j - ATE for j in range(1, 5)]
lap, act = (tau['L1'] + tau['L2']) / 2, (tau['A1'] + tau['A2']) / 2
toc_s = [lap - ATE, lap - ATE, (2 * lap + act) / 3 - ATE, F(0)]
for t, s in zip(toc_f, ["0.225", "0.150", "0.075", "0"]): check(f"TOC forest {s}", s, t)
for t, s in zip(toc_s, ["0.075", "0.075", "0.025", "0"]): check(f"TOC segment {s}", s, t)
autoc = lambda t: sum(t) / 4; qini = lambda t: sum(q * x for q, x in zip(qs, t)) / 4
check("AUTOC forest 0.113", "0.113", autoc(toc_f)); check("Qini forest 0.047", "0.047", qini(toc_f))
check("AUTOC segment 0.044", "0.044", autoc(toc_s)); check("Qini segment 0.019", "0.019", qini(toc_s))
assert all(q * t == Qv - q * ATE for q, t, Qv in zip(qs, toc_f, Q))   # q TOC(q) = Q(q) - q ATE

# ── Result 1.6: scores twice the effects ──
bar = {k: mu1[k] / 3 for k in grp}
for k, s in [('L1', "0.133"), ('L2', "0.067"), ('A1', "0.317"), ('A2', "0.217")]: check(f"bar {k}", s, bar[k])
for k, s in [('L1', "0.70"), ('L2', "0.10"), ('A1', "0.40"), ('A2', "-0.20")]: check(f"2 tau {k}", s, 2 * tau[k])
list_true = [k for k in grp if tau[k] > bar[k]]; list_dbl = [k for k in grp if 2 * tau[k] > bar[k]]
assert list_true == ['L1'] and list_dbl == ['L1', 'L2', 'A1']
assert list_true == [k for k in grp if v[k] > 0]          # the rule picks exactly the positive-v groups
gain = lambda ks: 2500 * sum(v[k] for k in ks)
check("rule with tau 16,250", "16250", gain(list_true)); check("rule with 2 tau 6,250", "6250", gain(list_dbl))
check("adds 5,000 coupons", "5000", 2500 * (len(list_dbl) - len(list_true))); check("which lose 10,000", "-10000", gain(['L2', 'A1']))
assert sorted(grp, key=lambda k: -2 * tau[k])[:1] == sorted(grp, key=lambda k: -tau[k])[:1] == ['L1']   # top 2,500 either way

# ── Result 1.7: isotonic calibration of six bins by pool-adjacent-violators ──
score = [-0.04, 0.06, 0.12, 0.24, 0.36, 0.48]; psi = [-0.12, 0.08, 0.02, 0.18, 0.36, 0.32]
mu1b = [0.66, 0.24, 0.21, 0.93, 0.42, 0.39]
def pav(y):
    blocks = [[yi, 1] for yi in y]                     # equal-sized bins: (mean, count)
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][0] > blocks[i + 1][0]:
            (a, na), (b, nb) = blocks[i], blocks[i + 1]
            blocks[i:i + 2] = [[(a * na + b * nb) / (na + nb), na + nb]]; i = max(i - 1, 0)
        else: i += 1
    return [mean for mean, n in blocks for _ in range(n)]
h = pav(psi)
for k, s in enumerate(["-0.12", "0.05", "0.05", "0.18", "0.34", "0.34"]): check(f"PAV bin {k+1}", s, h[k])
assert all(h[i] <= h[i + 1] for i in range(5)) and score == sorted(score)    # order never reversed
for k, s in enumerate(["0.22", "0.08", "0.07", "0.31", "0.14", "0.13"]): check(f"bar bin {k+1}", s, mu1b[k] / 3)
raw = [score[k] > mu1b[k] / 3 for k in range(6)]; cal = [h[k] > mu1b[k] / 3 for k in range(6)]
assert raw == [False, False, True, False, True, True] and cal == [False, False, False, False, True, True]
check("bin 3 raw per coupon +1.50", "1.50", m * 0.12 - c * 0.21); check("bin 3 calibrated -0.60", "-0.60", m * h[2] - c * 0.21)

# ── Result 1.8: K equally good candidates, estimates 1.50 +/- 0.50, by enumeration ──
for K, s in [(1, "1.50"), (2, "1.75"), (3, "1.88"), (10, "2.00")]:
    outs = [max(F(3, 2) + F(1, 2) * e for e in signs) for signs in product([1, -1], repeat=K)]
    em = sum(outs) / len(outs); check(f"winner's selection value, K={K}", s, em)
    assert em == F(3, 2) + F(1, 2) * (1 - F(2) ** (1 - K))                # the printed formula
    assert sum(1 for o in outs if o < 2) == 1                             # 2.00 unless all drew -0.50

# ── Result 1.9 on the 80 rows: segment rule minus coupon everyone ──
d = [a - b for a, b in zip(gr['seg'], gr['every'])]
assert sum(1 for (sg, _), (n, _) in cells.items() if sg == 'L' for _ in range(n)) == 40
assert all(x == 0 for x, (sg, dd) in zip(d, [(sg, dd) for (sg, dd), (n, b) in cells.items() for _ in range(n)]) if sg == 'L')
check("d-bar 3.25", "3.25", F(sum(d), 80)); check("= 1.50 - (-1.75)", "3.25", G_seg - G_every)
check("d-bar by hand", "3.25", F(-16 * 40 + 15 * 60, 80))
sd_d = statistics.stdev([float(x) for x in d]); check("sd(d) 31.57", "31.57", sd_d); check("paired SE 3.53", "3.53", sd_d / sqrt(80))
se_ev80 = statistics.stdev([float(x) for x in gr['every']]) / sqrt(80)
check("everyone SE on 80 rows 3.90", "3.90", se_ev80); check("unpaired 4.22", "4.22", sqrt(se_seg80 ** 2 + se_ev80 ** 2))
check("unpaired from printed SEs", "4.22", sqrt(1.62 ** 2 + 3.90 ** 2))

# ── The fold is unlocked: four-group base, evaluation fold of 5,000 ──
G4 = {k: (F(1, 4), mu0, mu1_) for k, (mu0, mu1_) in grp.items()}
lists = {'seg': ['L1', 'L2'], 'top5000': ['L1', 'A1'], 'cut': ['L1']}
P = {n: {k: int(k in ks) for k in grp} for n, ks in lists.items()}
mom = {n: moments(G4, P[n]) for n in lists}
for n, gs, ses in [('seg', "1.50", "0.20"), ('top5000', "0.75", "0.35"), ('cut', "1.625", "0.14")]:
    check(f"{n} gain", gs, mom[n][0]); check(f"{n} SE on 5,000", ses, sqrt(mom[n][1] / 5000))
    assert mom[n][1] == result13(G4, P[n])
assert mom['seg'][1] == Vs                                    # same variance as the two-segment base
def paired(a, b):
    """Exact Var(d_i) for d_i = g_i(a) - g_i(b), by enumeration."""
    Ed = Ed2 = F(0)
    for k, (w, mu0, mu1_) in G4.items():
        for dd, pd in [(1, F(1, 2)), (0, F(1, 2))]:
            py = mu1_ if dd else mu0
            for y, pyy in [(1, py), (0, 1 - py)]:
                x = g(P[a][k], dd, y, F(1, 2)) - g(P[b][k], dd, y, F(1, 2)); Ed += w * pd * pyy * x; Ed2 += w * pd * pyy * x * x
    return Ed, Ed2 - Ed ** 2
for a, gs, ps, us, zs in [('top5000', "-0.75", "0.36", "0.41", "-2.1"), ('cut', "0.125", "0.15", "0.25", "0.85")]:
    Ed, Vd = paired(a, 'seg'); se_p = sqrt(Vd / 5000); se_u = sqrt((mom[a][1] + mom['seg'][1]) / 5000)
    check(f"{a} minus segment", gs, Ed); check(f"{a} paired SE", ps, se_p); check(f"{a} unpaired SE", us, se_u)
    check(f"{a} z", zs, float(Ed) / se_p)
Ed, Vd = paired('cut', 'seg')
check("edge 1,250 on the base", "1250", Ed * base); check("cut-off list = 2,500 coupons", "2500", base // 4)
check("about 26,000 members to confirm", "26000", (1.96 * sqrt(Vd) / float(Ed)) ** 2, tol=1000)
assert (1.96 * sqrt(Vd) / float(Ed)) ** 2 > base and float(Ed) < sqrt(Vd / 5000)   # more than the base; under one SE
assert set(lists['seg']) ^ set(lists['cut']) == {'L2'}           # differ only on L2, a quarter of the rows
assert set(lists['seg']) ^ set(lists['top5000']) == {'L2', 'A1'}  # swaps L2 for A1
# the engine's cut-off: the best prefix of the lift ranking in truth is 2,500
assert max(range(1, 5), key=lambda j: Pt[j - 1]) == 1

print(f"\n{len(FAIL)} mismatches: {FAIL}")
