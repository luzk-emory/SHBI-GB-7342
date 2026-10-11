"""Arithmetic checks for meetings/m06/slides.tex (lecture case: Lena's coupon programme, Houtan Coffee, the Q4 push in
Region 2, M6 releases). The slides use their own numbers, not the notes' worked example. Run: python3 slides06_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from itertools import product
from math import sqrt, ceil
from scipy.stats import beta, norm
from scipy.integrate import quad
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)

# ── The case: the push test's cell rates (M6-R1, R2) ──
m, k, a = 30, F(3, 2), 5                     # margin per purchase; opt-out cost per push; coupon face, paid on redemption
N = 2500                                     # members per cell; Region 2 has 4 cells
cells = ['AL', 'AH', 'EL', 'EH']
mu0 = {'AL': F(0), 'AH': F(30, 100), 'EL': F(30, 100), 'EH': F(60, 100)}
mu1 = {'AL': F(20, 100), 'AH': F(50, 100), 'EL': F(35, 100), 'EH': F(65, 100)}
tau = {x: mu1[x] - mu0[x] for x in cells}
check("Region 2 members 10,000", "10000", 4 * N); check("share 25%", "25", 100 * N / (4 * N))
check("lift analyst 0.20", "0.20", tau['AL']); check("lift analyst-high 0.20", "0.20", tau['AH'])
check("lift executive 0.05", "0.05", tau['EL']); check("lift executive-high 0.05", "0.05", tau['EH'])

# ── Result 1.1: free push, then the opt-out cost ──
assert all(tau[x] > 0 for x in cells)                           # free push: everyone
check("opt-out cost 150 x 0.01 = 1.50", "1.50", 150 * F(1, 100)); assert 150 * F(1, 100) == k
check("threshold c/m = 0.05", "0.05", k / m)
check("v analyst uniform cost 4.50", "4.50", m * tau['AL'] - k); check("v executive uniform cost 0.00", "0.00", m * tau['EL'] - k)
assert not (m * tau['EL'] - k > 0)                              # exactly at the threshold: not pushed (strict rule)
check("analysts pushed 5,000", "5000", 2 * N)

# ── Costs paid on redemption; Result 1.2 ──
c = {x: k + a * mu1[x] for x in cells}; v = {x: m * tau[x] - c[x] for x in cells}
for x, cs, vs in [('AL', "2.50", "3.50"), ('AH', "4.00", "2.00"), ('EL', "3.25", "-1.75"), ('EH', "4.75", "-3.25")]:
    check(f"c({x})", cs, c[x]); check(f"v({x})", vs, v[x])
for x, t1, t2 in [('AL', "5.00", "0.00"), ('AH', "5.00", "-1.50"), ('EL', "1.25", "-1.50"), ('EH', "1.25", "-3.00")]:
    check(f"25 tau({x})", t1, (m - a) * tau[x]); check(f"-5 mu0({x})", t2, -a * mu0[x])
    assert (m - a) * tau[x] - a * mu0[x] - k == v[x]                # Result 1.2 holds cell by cell
check("k = 1.50", "1.50", k); check("m - a = 25", "25", m - a)

# ── Result 1.3: the cap, with the forest's split of analyst-low ──
cap = 1000
check("any 1,000 analyst-low earn 3,500", "3500", cap * v['AL'])
grp = [(500, F(30, 100)), (1000, F(20, 100)), (1000, F(15, 100))]
check("forest groups sum to 2,500", "2500", sum(n for n, _ in grp))
check("forest groups average 0.20", "0.20", sum(n * t for n, t in grp) / N)
vg = [(n, (m - a) * t - k) for n, t in grp]                     # mu0 = 0 in analyst-low, so mu1 = tau and v = 25 tau - 1.50
for (n, vv), s in zip(vg, ["6.00", "3.50", "2.25"]): check(f"forest v {s}", s, vv)
assert all(m * t - (k + a * t) == (m - a) * t - k for _, t in grp)
# rank all positive-v members (forest groups and analyst-high) and fill the cap
pool = sorted([vv for n, vv in vg for _ in range(n)] + [v['AH']] * N, reverse=True)
check("forest list earns 4,750", "4750", sum(pool[:cap])); check("on the 1,000 from the middle group: 500", "500", cap - 500)
assert pool[cap - 1] == F(7, 2) and pool[cap] == F(7, 2)        # the cap cuts inside the middle group
check("gain from within-segment ranking 1,250", "1250", sum(pool[:cap]) - cap * v['AL'])

# ── Result 1.4: the budget ──
b = {x: m * tau[x] for x in cells}; r = {x: b[x] / c[x] for x in cells}
for x, s in [('AL', "6.00"), ('AH', "6.00"), ('EL', "1.50"), ('EH', "1.50")]: check(f"b({x})", s, b[x])
for x, s in [('AL', "2.40"), ('AH', "1.50"), ('EL', "0.46"), ('EH', "0.32")]: check(f"ratio {x}", s, r[x])
assert r['EL'] < 1 and r['EH'] < 1
C = 8000
order = sorted(cells, key=lambda x: -r[x]); assert order[:2] == ['AL', 'AH']
spent_AL = N * c['AL']; check("all analyst-low 6,250", "6250", spent_AL); check("remaining 1,750", "1750", C - spent_AL)
frac = (C - spent_AL) / c['AH']; check("1,750/4.00 = 437.5", "437.5", frac); check("437 whole members", "437", int(frac))
check("left over 2", "2", C - spent_AL - int(frac) * c['AH'])
lam = r['AH'] - 1; check("lambda* = 0.50", "0.50", lam); check("marginal ratio 1.50", "1.50", r['AH'])
def V_budget(Cb):                                              # value of the relaxation by greedy, for the slope check
    val, left = F(0), F(Cb)
    for x in order:
        if r[x] <= 1: break
        n = min(F(N), left / c[x]); val += n * v[x]; left -= n * c[x]
    return val
check("slope of V(C) at 8,000 is 0.50", "0.50", V_budget(8001) - V_budget(8000))
check("analyst-high runs out at 16,250", "16250", N * c['AL'] + N * c['AH'])
check("slope beyond 16,250 is 0", "0", V_budget(16252) - V_budget(16251))
check("price rule analyst-low 2.25", "2.25", b['AL'] - (1 + lam) * c['AL']); check("price rule analyst-high 0", "0", b['AH'] - (1 + lam) * c['AH'])
check("charge at 1.5", "1.5", 1 + lam)

# ── Several coupon depths (a hypothetical ¥10 arm on analyst-low) ──
mu1_10 = F(28, 100); b10 = m * mu1_10; c10 = k + 10 * mu1_10   # mu0 = 0 in analyst-low, so tau = mu1
check("b ¥10 8.40", "8.40", b10); check("c ¥10 4.30", "4.30", c10); check("b - c ¥10 4.10", "4.10", b10 - c10)
check("b - 1.5c ¥10 1.95", "1.95", b10 - (1 + lam) * c10); check("b - 1.5c ¥5 2.25", "2.25", b['AL'] - (1 + lam) * c['AL'])
check("upgrade b 2.40", "2.40", b10 - b['AL']); check("upgrade c 1.80", "1.80", c10 - c['AL'])
check("upgrade b - c 0.60", "0.60", (b10 - c10) - v['AL']); check("upgrade b - 1.5c -0.30", "-0.30", (b10 - b['AL']) - (1 + lam) * (c10 - c['AL']))
check("upgrade ratio 1.33", "1.33", (b10 - b['AL']) / (c10 - c['AL'])); assert (b10 - b['AL']) / (c10 - c['AL']) < r['AH']
check("upgrade pays when lambda < 0.33", "0.33", (b10 - b['AL']) / (c10 - c['AL']) - 1)
assert b10 - c10 > v['AL']                                     # no budget: ¥10 nets more

# ── Result 1.5: the price of fairness, North (a) and South (b) ──
Na, Nb, g = 6000, 4000, F(5, 4); check("districts sum to 10,000", "10000", Na + Nb)
hi, lo = F(5), F(5, 2); na5, nb5, nb25 = 840, 160, 1000
check("unconstrained top 1,000 at 5.00", "1000", na5 + nb5)
check("rate North 14%", "14", 100 * F(na5, Na)); check("rate South 4%", "4", 100 * F(nb5, Nb)); check("value 5,000", "5000", cap * hi)
nb = F(cap) / (1 + g * F(Na, Nb)); na = cap - nb
check("n_b 347.8", "347.8", nb); check("n_a 652.2", "652.2", na)
NA, NB = 652, 348; assert NA + NB == cap
assert F(NA, Na) <= g * F(NB, Nb) and F(NA + 1, Na) > g * F(NB - 1, Nb)   # whole members: 652/348 feasible, 653/347 not
check("rate North 10.9%", "10.9", 100 * F(NA, Na)); check("rate South 8.7%", "8.7", 100 * F(NB, Nb))
swap = na5 - NA; check("swapped 188", "188", swap); assert NB - nb5 == swap and NB - nb5 <= nb25
check("constrained value 4,530", "4530", NA * hi + nb5 * hi + swap * lo)
check("price of fairness 470", "470", cap * hi - (NA * hi + nb5 * hi + swap * lo))
eta = (hi - lo) / (F(1, Na) + g / Nb); lam_cap = hi - eta / Na
check("eta* about 5,217", "5217", eta); check("lambda* about 4.13", "4.13", lam_cap)
check("South threshold 2.50", "2.50", lam_cap - g * eta / Nb)
check("rate_b 0.087", "0.087", F(NB, Nb))
check("tightening to 1.20 costs about 23", "23", F(5, 100) * eta * F(NB, Nb))
check("0.05 x 5,217 x 0.087", "23", 0.05 * 5217 * 0.087)
def V_fair(gg):                                                 # relaxation value with the cap and the rate constraint both binding
    nbb = F(cap) / (1 + gg * F(Na, Nb)); return (cap - nbb) * hi + nb5 * hi + (nbb - nb5) * lo
check("exact change 1.25 -> 1.20 near 23", "23", V_fair(F(5, 4)) - V_fair(F(6, 5)), tol=1)

# ── Result 1.6: spending risk ──
z95 = norm.ppf(0.95); check("z 1.645", "1.645", z95)
EK = N * c['AH'] + N * c['AL']; check("E[K] all analysts 16,250", "16250", EK)
sdK = sqrt(a ** 2 * (N * float(mu1['AH'] * (1 - mu1['AH'])) + N * float(mu1['AL'] * (1 - mu1['AL']))))
check("0.5 x 0.5 = 0.25", "0.25", mu1['AH'] * (1 - mu1['AH'])); check("0.2 x 0.8 = 0.16", "0.16", mu1['AL'] * (1 - mu1['AL']))
check("sd(K) 160", "160", sdK); check("z 10.9", "10.9", (18000 - EK) / sdK); check("95th percentile 16,513", "16513", float(EK) + 1.645 * sdK)
check("redeem costs 6.50", "6.50", k + a); check("no redemption 1.50", "1.50", k)
check("25 = a^2", "25", a ** 2)

# ── The Q4 list ──
def ok_n(n): return float(N * c['AL'] + n * c['AH']) + 1.645 * sqrt(25 * (N * 0.16 + n * 0.25)) <= C
n_star = max(n for n in range(0, N + 1) if ok_n(n)); check("analyst-high kept 391", "391", n_star)
sd391 = sqrt(N * 25 * 0.16 + 391 * 25 * 0.25); check("sd 111.6", "111.6", sd391); check("reserve 184", "184", 1.645 * sd391)
check("(8,000 - 184 - 6,250)/4.00 = 391", "391", int((C - 184 - 6250) / 4.00))
check("A-High expected cost 1,564", "1564", 391 * c['AH']); check("A-High expected net 782", "782", 391 * v['AH'])
check("A-Low expected net 8,750", "8750", N * v['AL']); check("pushes 2,891", "2891", N + 391)
check("total cost 7,814", "7814", N * c['AL'] + 391 * c['AH']); check("total net 9,532", "9532", N * v['AL'] + 391 * v['AH'])
check("guarantee costs 46 pushes", "46", 437 - 391); check("guarantee costs 92", "92", 46 * v['AH'])
check("three days under the cap of 1,000", "3", ceil((N + 391) / cap))

# ── Result 1.7: lower bounds on the money ──
assert all((m - a) * mu1[x] - m * mu0[x] - k == v[x] for x in cells)   # v = 25 mu1 - 30 mu0 - 1.50
w = sqrt((m - a) ** 2 + m ** 2)
for lab, se_lift, vv, s_arm, s_se, s_lb in [("AL", 0.05, 3.50, "0.035", "1.38", "1.23"),
                                             ("AH", 0.03, 2.00, "0.021", "0.83", "0.64"),
                                             ("AH SE 6%", 0.06, 2.00, "0.042", "1.66", "-0.73")]:
    arm = se_lift / sqrt(2); check(f"{lab} arm SE", s_arm, arm); check(f"{lab} SE(v)", s_se, w * arm); check(f"{lab} bound", s_lb, vv - 1.645 * w * arm)
check("625 = 25^2", "625", 25 ** 2); check("900 = 30^2", "900", 30 ** 2)

# ── Results 1.8 and 1.9: a store's capacity ──
p, gv, q, cpush = 30, 20, 400, 500
pi = lambda y: p * min(y, q) - gv * max(y - q, 0)
check("pi(360) 10,800", "10800", pi(360)); check("pi(420) 11,600", "11600", pi(420)); check("pi(480) 10,400", "10400", pi(480))
check("12,000 = p q", "12000", p * q); check("400 = g x 20", "400", gv * 20); check("1,600 = g x 80", "1600", gv * 80)
YP1 = [(420, 1)]; YQ1 = [(480, F(1, 2)), (360, F(1, 2))]; Y0 = 360
tP = sum(y * pr for y, pr in YP1) - Y0; tQ = sum(y * pr for y, pr in YQ1) - Y0
check("tau store P 60", "60", tP); check("tau store Q 60", "60", tQ)
check("linear rule 1,300", "1300", p * tP - cpush)
vP = sum(pi(y) * pr for y, pr in YP1) - pi(Y0) - cpush; vQ = sum(pi(y) * pr for y, pr in YQ1) - pi(Y0) - cpush
check("store P v 300", "300", vP); check("store Q v -700", "-700", vQ); check("store Q half difference -200", "-200", F(1, 2) * (pi(480) - pi(360)))
cu, co = p + gv, 10; check("c_u 50", "50", cu); kappa = F(cu, cu + co); check("kappa 0.83", "0.83", kappa); check("60 = c_u + c_o", "60", cu + co)
F1 = lambda y: sum(pr for yy, pr in YQ1 if yy <= y); check("F1(360) 0.5", "0.5", F1(360)); check("F1(480) 1", "1", F1(480))
qstar = min(y for y, _ in YQ1 if F1(y) >= kappa); check("plan for 480", "480", qstar)
loss = lambda qq: sum(pr * (cu * max(y - qq, 0) + co * max(qq - y, 0)) for y, pr in YQ1)
check("loss at 420 1,800", "1800", loss(420)); check("loss at 480 600", "600", loss(480))
assert min(range(300, 601), key=loss) == 480                   # brute force agrees with the fractile
check("420 = baseline plus the CATE", "420", Y0 + tQ)

# ── Block B: same accuracy, different losses ──
check("model 1: 4.50 - 4.75", "-0.25", m * F(15, 100) - c['EH']); check("30 x 0.15 = 4.50", "4.50", m * F(15, 100))
check("model 2: 3.00 - 4.00", "-1.00", m * F(10, 100) - c['AH']); check("30 x 0.10 = 3.00", "3.00", m * F(10, 100))
check("model 1 error 0.10", "0.10", F(15, 100) - tau['EH']); check("model 2 error 0.10", "0.10", tau['AH'] - F(10, 100))
check("MSE 0.0025", "0.0025", F(1, 4) * F(1, 100)); check("bar 0.158", "0.158", c['EH'] / m)
check("model 2 loses 5,000", "5000", N * v['AH'])

# ── Result 1.10: DR scores (e = 0.5, outcome models at the cell rates) ──
e = F(1, 2)
def phi(x, d, y): return mu1[x] - mu0[x] + d * (y - mu1[x]) / e - (1 - d) * (y - mu0[x]) / (1 - e)
def Gam(x, d, y): return m * phi(x, d, y) - c[x]
pats = [(1, 1), (1, 0), (0, 1), (0, 0)]
prob = lambda x, d, y: e * (mu1[x] if d else mu0[x]) if y else e * (1 - (mu1[x] if d else mu0[x]))
for (d, y), sp, sphi, sg in zip(pats, ["0.25", "0.25", "0.15", "0.35"], ["1.20", "-0.80", "-1.20", "0.80"], ["32.00", "-28.00", "-40.00", "20.00"]):
    check(f"AH ({d},{y}) prob", sp, prob('AH', d, y)); check(f"AH ({d},{y}) phi", sphi, phi('AH', d, y)); check(f"AH ({d},{y}) Gamma", sg, Gam('AH', d, y))
check("E[Gamma | AH] = v = 2.00", "2.00", sum(prob('AH', d, y) * Gam('AH', d, y) for d, y in pats))
for x in cells: assert sum(prob(x, d, y) * Gam(x, d, y) for d, y in pats) == v[x]   # unbiased in every cell

# ── Eight members ──
rows = [('AL', 1, 1, "1.80", "51.50"), ('AL', 0, 0, "0.20", "3.50"), ('AH', 1, 1, "1.20", "32.00"), ('AH', 0, 1, "-1.20", "-40.00"),
        ('EL', 1, 0, "-0.65", "-22.75"), ('EL', 0, 0, "0.65", "16.25"), ('EH', 1, 1, "0.75", "17.75"), ('EH', 0, 1, "-0.75", "-27.25")]
G = []
for i, (x, d, y, sphi, sg) in enumerate(rows, 1):
    check(f"member {i} phi", sphi, phi(x, d, y)); check(f"member {i} Gamma", sg, Gam(x, d, y)); G.append((x, Gam(x, d, y)))
pol = {'everyone': set(cells), 'analysts': {'AL', 'AH'}, 'low spenders': {'AL', 'EL'}, 'analyst-low only': {'AL'}}
S = {nm: sum(gm for x, gm in G if x in st) for nm, st in pol.items()}
for nm, s1, s2 in [('everyone', "31.00", "3.88"), ('analysts', "47.00", "5.88"), ('low spenders', "48.50", "6.06"), ('analyst-low only', "55.00", "6.88")]:
    check(f"sum {nm}", s1, S[nm]); check(f"per member {nm}", s2, S[nm] / 8)

# ── Result 1.11: weighted classification ──
absG = sum(abs(gm) for _, gm in G); negG = sum(max(-gm, 0) for _, gm in G)
check("sum |Gamma| 211", "211", absG); check("sum Gamma^- 90", "90", negG); check("121", "121", absG - negG)
check("positive labels 1,2,3,6,7", "5", sum(1 for _, gm in G if gm > 0))
for nm, members, sw in [('everyone', "4, 5, 8", "90.00"), ('analysts', "4, 6, 7", "74.00"), ('analyst-low only', "3, 6, 7", "66.00")]:
    mis = [i for i, (x, gm) in enumerate(G, 1) if (x in pol[nm]) != (gm > 0)]
    check(f"misclassified {nm}: {members}", members.replace(', ', ''), int(''.join(map(str, mis))))
    wgt = sum(abs(G[i - 1][1]) for i in mis); check(f"weight {nm}", sw, wgt); check(f"121 - weight {nm}", f"{S[nm]:.2f}", absG - negG - wgt)
check("member 3 under the budget 30.00", "30.00", Gam('AH', 1, 1) - lam * c['AH'])

# ── Policy trees: exhaustive search over depth-1 and depth-2 trees on (type, spending) ──
cellsum = {x: sum(gm for xx, gm in G if xx == x) for x in cells}
for x, s in [('AL', "55.00"), ('AH', "-8.00"), ('EL', "-6.50"), ('EH', "-9.50")]: check(f"leaf sum {x}", s, cellsum[x])
depth1 = {}
for feat, groups in [('type', [{'AL', 'AH'}, {'EL', 'EH'}]), ('spend', [{'AL', 'EL'}, {'AH', 'EH'}])]:
    for lab in product([0, 1], repeat=2):
        st = set().union(*[gr for gr, l in zip(groups, lab) if l]); depth1[(feat, lab)] = (sum(cellsum[x] for x in st), frozenset(st))
best1 = max(depth1.values(), key=lambda t: t[0]); check("best depth-one tree 48.50", "48.50", best1[0]); assert best1[1] == {'AL', 'EL'}
check("depth one, analysts 47.00", "47.00", depth1[('type', (1, 0))][0])
subsets = [frozenset(x for x, l in zip(cells, lab) if l) for lab in product([0, 1], repeat=4)]
best2 = max(subsets, key=lambda st: sum(cellsum[x] for x in st)); assert best2 == {'AL'}
check("best depth-two tree 55.00", "55.00", sum(cellsum[x] for x in best2))

# ── Regret ──
Gtrue = lambda st: sum(F(1, 4) * v[x] for x in st)
best_true = max(subsets, key=Gtrue); assert best_true == {'AL', 'AH'}
check("G analysts 1.38", "1.38", Gtrue({'AL', 'AH'})); check("G analyst-low 0.88", "0.88", Gtrue({'AL'})); check("G low spenders 0.44", "0.44", Gtrue({'AL', 'EL'}))
check("regret 0.50", "0.50", Gtrue({'AL', 'AH'}) - Gtrue({'AL'})); check("regret on 10,000 is 5,000", "5000", 4 * N * (Gtrue({'AL', 'AH'}) - Gtrue({'AL'})))
check("sqrt(10,000/8) about 35", "35", sqrt(10000 / 8))

# ── Deployment ──
hAL, hAH = round(F(N, 10)), round(F(391, 10)); check("holdout analyst-low 250", "250", hAL); check("holdout analyst-high 39", "39", hAH)
check("holdout 289", "289", hAL + hAH); check("forgone net 953", "953", hAL * v['AL'] + hAH * v['AH'])
check("about a tenth of 9,532", "0.1", (hAL * v['AL'] + hAH * v['AH']) / 9532)
check("pushed buyer weight 1.11", "1.11", 1 / 0.9); check("held-out buyer weight 10", "10", 1 / 0.1)

# ── Bandit ──
s1, n1, s2, n2 = 50, 200, 40, 200
check("posterior 1: Beta(51, ...)", "51", s1 + 1); check("posterior 1: Beta(..., 151)", "151", n1 - s1 + 1)
check("posterior 2: Beta(41, ...)", "41", s2 + 1); check("posterior 2: Beta(..., 161)", "161", n2 - s2 + 1)
B1, B2 = beta(s1 + 1, n1 - s1 + 1), beta(s2 + 1, n2 - s2 + 1)
pbest = quad(lambda t: B1.pdf(t) * B2.cdf(t), 0, 1)[0]
check("Pr(text 1 better) 0.88", "0.88", pbest); check("text 2 share 0.12", "0.12", 1 - pbest)

# ── Recaps (End of Block A, pitfalls, summary) repeat numbers checked above ──
check("recap: same lift, 3.50 vs 2.00", "1.50", v['AL'] - v['AH']); check("recap: model gap 0 vs 5,000", "5000", N * v['AH'] - 0)
check("recap: tree claims 6.88, earns 0.88", "6.00", F(55, 8) - Gtrue({'AL'}))

print(f"\n{len(FAIL)} mismatches: {FAIL}")
