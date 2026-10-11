"""Arithmetic checks for meetings/m08/slides.tex (lecture case: Wendy's rate decision at Qiantan Hotels, Case B, M8
releases). The slides use their own numbers, not the notes' worked example (Pujiang Delivery). Quoted case numbers are
checked against the case files (cases/caseB-qiantan) or, for the few that only the v2 deck carried, against that deck
at commit 5522695; everything derived from them is recomputed here. Run: python3 slides08_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import log, sqrt
from pathlib import Path
import subprocess
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)
def truth(label, cond):
    print(f"{'OK ' if cond else 'MISMATCH'} | {label}")
    if not cond: FAIL.append(label)

ROOT = Path(__file__).resolve().parents[2]
CASE = ''.join((ROOT / 'cases/caseB-qiantan' / f).read_text() for f in ('student.md', 'instructor.md')).replace('−', '-')
try:
    V2 = subprocess.run(['git', '-C', str(ROOT), 'show', '5522695:meetings/m08/slides.tex'],
                        capture_output=True, text=True, check=True).stdout
except Exception:
    V2 = None
def sourced(label, text, where='case'):
    """A quoted input: must appear verbatim in the case files (or the v2 deck)."""
    if where == 'v2' and V2 is None:
        print(f"NOTE | {label}: v2 deck not available, provenance not checked"); return
    src = CASE if where == 'case' else V2
    truth(f"source ({where}) {label}: '{text}'", text in src)

# ── The proposal and the break-even ──
P0, c, rise = 800, 200, F(8, 100)
sourced("rate 800", "**¥800**"); sourced("cost 200", "**¥200**"); sourced("8% rise", "**8%**")
sourced("logs", "80 hotels × 1,095 nights"); sourced("47 signals", "47 recorded signals")
check("87,600 hotel-nights", "87600", 80 * 1095); sourced("87,600", "87,600")
m0, m1 = P0 - c, P0 * (1 + rise) - c
check("contribution 600", "600", m0); check("new rate 864", "864", P0 * (1 + rise)); check("contribution 664", "664", m1)
check("up 10.7%", "10.7", 100 * (m1 / m0 - 1)); check("bookings may fall 9.6%", "9.6", 100 * (1 - F(600, 664)))
be = log(600 / 664) / log(1.08); check("break-even -1.32", "-1.32", be)
truth("rise pays iff theta > break-even (1.08^theta x 664 > 600)",
      all((1.08 ** t * 664 > 600) == (t > be) for t in [-2.0, -1.56, -1.33, -1.31, -1.0, -0.5]))

# ── Six nights ──
D = [30, 40, 50, 70, 80, 90]; Y = [110, 100, 90, 210, 200, 190]; cat = [0, 0, 0, 1, 1, 1]
sourced("six nights", "| 4 | Premium | 70 | 210 |")
Db, Yb = F(sum(D), 6), F(sum(Y), 6); check("mean D 60", "60", Db); check("mean Y 150", "150", Yb)
sxy = sum((d - Db) * (y - Yb) for d, y in zip(D, Y)); sxx = sum((d - Db) ** 2 for d in D)
check("pooled numerator 5,600", "5600", sxy); check("pooled denominator 2,800", "2800", sxx)
check("pooled slope +2.0", "2.0", sxy / sxx); check("10 yuan -> 20 bookings", "20", 10 * sxy / sxx)
check("pooled line intercept 30 (plot)", "30", Yb - (sxy / sxx) * Db)
cm = {k: (F(sum(d for d, g in zip(D, cat) if g == k), 3), F(sum(y for y, g in zip(Y, cat) if g == k), 3)) for k in (0, 1)}
check("standard means 40", "40", cm[0][0]); check("standard means 100", "100", cm[0][1])
check("premium means 80", "80", cm[1][0]); check("premium means 200", "200", cm[1][1])
Dt = [d - cm[g][0] for d, g in zip(D, cat)]; Yt = [y - cm[g][1] for y, g in zip(Y, cat)]
truth("residuals D: -10 0 10 -10 0 10", Dt == [-10, 0, 10, -10, 0, 10])
truth("residuals Y: 10 0 -10 10 0 -10", Yt == [10, 0, -10, 10, 0, -10])
num, den = sum(a * b for a, b in zip(Dt, Yt)), sum(a * a for a in Dt)
check("within numerator -400", "-400", num); check("within denominator 400", "400", den); check("within slope -1.0", "-1.0", num / den)
# why both sides
nraw = sum((d - Db) * yt for d, yt in zip(D, Yt))
check("outcome-only numerator -400", "-400", nraw); check("outcome-only slope -0.14", "-0.14", nraw / sxx)
check("between-category part 6 x 20^2 = 2,400", "2400", 6 * 20 ** 2); assert 6 * 20 ** 2 == sum((cm[g][0] - Db) ** 2 for g in cat)
check("within-category part 400", "400", sxx - 2400); check("diluted seven-fold", "7", (num / den) / (nraw / sxx))

# ── Result 1.4: airport and resort nights ──
th = {'air': -2.0, 'res': -0.8}; sd = {'air': 0.20, 'res': 0.10}; v = {k: sd[k] ** 2 for k in sd}
check("Var airport 0.04", "0.04", v['air']); check("Var resort 0.01", "0.01", v['res'])
check("weights' denominator 0.04 + 0.01 = 0.05 (equal shares cancel)", "0.05", v['air'] + v['res'])
check("weight airport 0.8", "0.8", v['air'] / (v['air'] + v['res'])); check("weight resort 0.2", "0.2", v['res'] / (v['air'] + v['res']))
tw = (0.5 * th['air'] * v['air'] + 0.5 * th['res'] * v['res']) / (0.5 * v['air'] + 0.5 * v['res'])
check("variance-weighted theta -1.76", "-1.76", tw); check("simple average -1.40", "-1.40", (th['air'] + th['res']) / 2)
truth("both below break-even; resort alone above", tw < be and (th['air'] + th['res']) / 2 < be and th['res'] > be)

# ── The real logs (case R3) ──
for s in ["¥803", "¥439", "¥1,920", "| Median premium rooms booked | 61 |", "six forecast-occupancy bands"]: sourced("R3", s)

# ── The ladder and the plug-in attempts (case key; three figures only in the v2 deck) ──
ladder = {'+0.40': 0.40, '+0.49': 0.49, '-0.07': -0.07, '-0.54': -0.54, '-1.03': -1.03, '-0.95': -0.95}
for s in ["pooled +0.40", "within hotel +0.49", "band -0.07", "controls: -0.54", "feature: -1.03", "in-sample: -0.95",
          "4.2% to 0.9%", "in-sample $R^2$ is 0.97", "Well-regularized in-sample gives -1.57 and cross-fitted -1.56"]:
    sourced("key", s)
for s in ["0.951", "0.970", "17.6\\%"]: sourced("boosted-model table", s, 'v2')
truth("every ladder and plug-in estimate says raise (> -1.32)", all(x > be for x in ladder.values()))
truth("-1.57 and -1.56 say do not raise", -1.57 < be and -1.56 < be)
truth("R^2 with log rate (0.970) > without (0.951)", 0.970 > 0.951)
check("competitor share falls 78.6% (> three-quarters)", "78.6", 100 * (4.2 - 0.9) / 4.2); assert (4.2 - 0.9) / 4.2 > 0.75

# ── Cross-fitting on six nights: folds {1,4}, {2,5}, {3,6} ──
folds = [{0, 3}, {1, 4}, {2, 5}]
rhat, lhat = [None] * 6, [None] * 6
for f in folds:
    for i in f:
        others = [j for j in range(6) if j not in f and cat[j] == cat[i]]
        rhat[i] = F(sum(D[j] for j in others), len(others)); lhat[i] = F(sum(Y[j] for j in others), len(others))
truth("r-hat 45 40 35 85 80 75", rhat == [45, 40, 35, 85, 80, 75])
truth("l-hat 95 100 105 195 200 205", lhat == [95, 100, 105, 195, 200, 205])
Do = [d - r for d, r in zip(D, rhat)]; Yo = [y - l for y, l in zip(Y, lhat)]
truth("out-of-fold D: -15 0 15 -15 0 15", Do == [-15, 0, 15, -15, 0, 15]); truth("out-of-fold Y: 15 0 -15 15 0 -15", Yo == [15, 0, -15, 15, 0, -15])
n2, d2 = sum(a * b for a, b in zip(Do, Yo)), sum(a * a for a in Do)
check("cross-fit numerator -900", "-900", n2); check("cross-fit denominator 900", "900", d2); check("cross-fit slope -1.0", "-1.0", n2 / d2)
check("out-of-fold residual size 15", "15", max(abs(x) for x in Do)); check("in-sample residual size 10", "10", max(abs(x) for x in Dt))

# ── The product of errors: bias = (rho m_r m_l - theta m_r^2)/(E nu^2 + m_r^2) ──
theta, Enu2, rho = -1.56, 0.10 ** 2, 0.5
check("E[nu^2] = 0.01", "0.01", Enu2)
bias = lambda mr, ml: (rho * mr * ml - theta * mr ** 2) / (Enu2 + mr ** 2)
for mr, ml, s in [(0.04, 0.04, "0.28"), (0.02, 0.02, "0.08"), (0.01, 0.01, "0.02"), (0.01, 0.08, "0.06"), (0.08, 0.01, "0.63")]:
    check(f"bias rmse_r {mr} rmse_l {ml}", s, bias(mr, ml))
check("halving both cuts bias about four-fold (0.04 -> 0.02)", "4", bias(0.04, 0.04) / bias(0.02, 0.02), tol=0.5)
check("halving both cuts bias about four-fold (0.02 -> 0.01)", "4", bias(0.02, 0.02) / bias(0.01, 0.01), tol=0.5)

# ── The elasticity at Qiantan Hotels and the decision table ──
th_hat = -1.56; sourced("DML -1.56", "-1.56")
check("gap to break-even 0.24", "0.24", round(be, 2) - th_hat); sourced("gap 0.24", "sits 0.24 from the break-even")
for g, rate, bk, ct in [(-0.08, "736", "13.9", "1.7"), (-0.04, "768", "6.6", "0.9"), (0.0, "800", "0.0", "0.0"),
                        (0.04, "832", "-5.9", "-0.9"), (0.08, "864", "-11.3", "-1.9")]:
    P = P0 * (1 + g); q = (1 + g) ** th_hat
    check(f"rate {rate}", rate, P); check(f"bookings at {rate}", bk, 100 * (q - 1)); check(f"contribution at {rate}", ct, 100 * (q * (P - c) / m0 - 1))
check("rise costs about 2% of contribution", "2", -100 * ((1.08) ** th_hat * 664 / 600 - 1), tol=0.5)
for s in ["bookings -11.3%, contribution -1.9%", "-8%: +1.7%", "-4%: +0.9%"]: sourced("key decision table", s)

# ── Inference ──
se_cl = 0.03; sourced("clustered SE 0.03", "-1.56 (0.03)")
se_ind = se_cl / 3
check("row-independent SE 0.01 (three times too small)", "0.01", se_ind)
for se, lo, hi in [(se_ind, "-1.58", "-1.54"), (se_cl, "-1.62", "-1.50")]:
    check(f"CI low SE {se:.2f}", lo, th_hat - 1.96 * se); check(f"CI high SE {se:.2f}", hi, th_hat + 1.96 * se)
truth("clustered interval excludes -1.32", th_hat + 1.96 * se_cl < be)

# ── Overlap ──
sourced("12% pinned", "on 12% of nights the rate is pinned"); sourced("9% left", "| 47 signals | 9% |")
check("out-of-fold R^2 0.91", "0.91", 1 - 0.09); check("91%", "91", 100 * (1 - 0.09))
check("SD one-fifth = 0.2", "0.2", 1 / 5)
check("pinned nights' share of sum D-tilde^2 0.5%", "0.5", 100 * 0.12 * 0.2 ** 2 / (0.12 * 0.2 ** 2 + 0.88 * 1))
check("0.88 = 1 - 0.12", "0.88", 1 - 0.12)

# ── A local slope ──
Pstar = lambda k: c * k / (k - 1)
check("P* 557", "557", c * th_hat / (1 + th_hat)); check("-0.56 = 1 + theta", "-0.56", 1 + th_hat)
check("cut of about 30%", "30", 100 * (1 - c * th_hat / (1 + th_hat) / P0), tol=1)
sourced("support 703-910", "¥703–910")
lo_k, hi_k = -(th_hat + 1.96 * se_cl), -(th_hat - 1.96 * se_cl)
check("kappa low 1.50", "1.50", lo_k); check("kappa high 1.62", "1.62", hi_k)
check("P* at kappa 1.62 -> 523", "523", Pstar(1.62)); check("P* at kappa 1.50 -> 600", "600", Pstar(1.50))
truth("whole P* range below the support's 703", Pstar(1.50) < 703)

# ── The last-minute discount: two kinds of night, equally common ──
w = {'air': F(1, 2), 'res': F(1, 2)}; e = {'air': F(1, 2), 'res': F(9, 10)}
mu0 = {'air': 50, 'res': 60}; mu1 = {'air': 54, 'res': 72}; tau = {k: mu1[k] - mu0[k] for k in w}
check("tau airport 4", "4", tau['air']); check("tau resort 12", "12", tau['res'])
pt = {k: w[k] * e[k] for k in w}; pc = {k: w[k] * (1 - e[k]) for k in w}
check("treated airport share 0.25", "0.25", pt['air']); check("treated resort share 0.45", "0.45", pt['res'])
check("treated share 0.70", "0.70", sum(pt.values())); check("untreated airport 0.25", "0.25", pc['air'])
check("untreated resort 0.05", "0.05", pc['res']); check("untreated share 0.30", "0.30", sum(pc.values()))
mt = sum(pt[k] * mu1[k] for k in w) / sum(pt.values()); mc = sum(pc[k] * mu0[k] for k in w) / sum(pc.values())
check("treated mean 65.6", "65.6", mt); check("untreated mean 51.7", "51.7", mc); check("naive difference 13.9", "13.9", mt - mc)
check("65.6 - 51.7 printed = 13.9", "13.9", 65.6 - 51.7)
vD = {k: e[k] * (1 - e[k]) for k in w}
check("e(1-e) airport 0.25", "0.25", vD['air']); check("e(1-e) resort 0.09", "0.09", vD['res'])
plm = sum(w[k] * vD[k] * tau[k] for k in w) / sum(w[k] * vD[k] for k in w)
check("partially linear theta 6.1", "6.1", plm)
check("ATE 8.0", "8.0", sum(w[k] * tau[k] for k in w)); check("ATT 9.1", "9.1", sum(pt[k] * tau[k] for k in w) / sum(pt.values()))

# AIPW at resorts with mu1-hat = 74, e-hat = 0.8
m1h, eh = 74, F(8, 10)
check("regression alone 74", "74", m1h); check("regression error +2.0", "2.0", m1h - mu1['res'])
ipw = e['res'] * mu1['res'] / eh; check("weighting alone 81", "81", ipw); check("weighting error +9.0", "9.0", ipw - mu1['res'])
aipw = m1h + e['res'] * (mu1['res'] - m1h) / eh
check("AIPW limit 71.75", "71.75", aipw); check("AIPW error -0.25", "-0.25", aipw - mu1['res'])
check("1 - e/e-hat = -0.125", "-0.125", 1 - e['res'] / eh); assert aipw - mu1['res'] == (m1h - mu1['res']) * (1 - e['res'] / eh)

# CATE: E[phi | X] with correct nuisances, by enumeration of D (Y given D enters through its mean)
def Ephi(k):
    return (mu1[k] - mu0[k] + e[k] * (mu1[k] - mu1[k]) / e[k] - (1 - e[k]) * (mu0[k] - mu0[k]) / (1 - e[k]))
check("BLP intercept 4", "4", Ephi('air')); check("BLP resort coefficient 8", "8", Ephi('res') - Ephi('air'))
phi1 = tau['res'] + F(75 - 72) / e['res']; phi0 = tau['res'] - F(57 - 60) / (1 - e['res'])
check("phi treated resort night 15.3", "15.3", phi1); check("phi untreated resort night 42.0", "42.0", phi0)
check("weight 1/0.1 = 10", "10", 1 / (1 - e['res'])); check("three-room surprise moves phi by 30", "30", phi0 - tau['res'])
check("0.9 x 0.1 = 0.09", "0.09", e['res'] * (1 - e['res']))

# ── Sensitivity ──
sourced("8% of nights", "**8% of nights**")
B = lambda r2y, r2d, S: sqrt(r2y * r2d / (1 - r2d)) * S
# the case key's table (1%, 2%, 5%, 10% -> 0.03, 0.06, 0.15, 0.32) pins the residual-SD ratio; the slide prints 3.0
for s in ["1% → bias 0.03", "2% → 0.06", "5% → 0.15", "**10% → 0.32**"]: sourced("key sensitivity table", s)
S = 3.0
for q, s in [(0.01, "0.03"), (0.02, "0.06"), (0.05, "0.15"), (0.10, "0.32")]:
    check(f"key table at S = 3.0, R^2 {q}", s, B(q, q, S))
for q, s, lo, hi in [(0.01, "0.03", "-1.59", "-1.53"), (0.02, "0.06", "-1.62", "-1.50"), (0.05, "0.15", "-1.71", "-1.41"), (0.10, "0.32", "-1.88", "-1.24")]:
    b = B(q, q, S); check(f"bias at {q}", s, b); check(f"range low at {q}", lo, th_hat - b); check(f"range high at {q}", hi, th_hat + b)
    truth(f"crosses -1.32 at {q} only if 10%", (th_hat + b > be) == (q == 0.10))
# robustness value: q / sqrt(1 - q) * S = 0.24
gap = 0.24; k2 = (gap / S) ** 2; rv = (-k2 + sqrt(k2 ** 2 + 4 * k2)) / 2
check("robustness value 7.7%", "7.7", 100 * rv); check("robustness value solves the bound", "0.24", B(rv, rv, S))
truth("robustness value between 5% and 10%", 0.05 < rv < 0.10)
# benchmark: the event flag explains R2_D = 0.04, R2_Y = 0.06 (new case data, flagged in the report)
print("GIVEN | event-flag benchmark R2_D = 0.04, R2_Y = 0.06 (new input; not yet in the case files)")
r2d, r2y = 0.04, 0.06
for k, sd_, sy, s, lo, hi in [(1, "0.04", "0.06", "0.15", "-1.71", "-1.41"), (2, "0.08", "0.12", "0.31", "-1.87", "-1.25")]:
    check(f"k={k} R2_D", sd_, k * r2d); check(f"k={k} R2_Y", sy, k * r2y)
    b = B(k * r2y, k * r2d, S); check(f"k={k} bias", s, b); check(f"k={k} range low", lo, th_hat - b); check(f"k={k} range high", hi, th_hat + b)
check("k=1 radicand exactly 0.0025", "0.0025", r2y * r2d / (1 - r2d))
truth("k=1 survives, k=2 crosses", th_hat + B(r2y, r2d, S) < be and th_hat + B(2 * r2y, 2 * r2d, S) > be)
lo_, hi_ = 1.0, 2.0
for _ in range(60):
    mid = (lo_ + hi_) / 2
    lo_, hi_ = (mid, hi_) if B(mid * r2y, mid * r2d, S) < gap else (lo_, mid)
check("overturned at about 1.6 times the event flag", "1.6", lo_)

print(f"\n{len(FAIL)} mismatches: {FAIL}")
