"""Arithmetic checks for meetings/m09/slides.tex (lecture case: Wendy's rate decisions at Qiantan Hotels, Case B,
Meeting 9 releases R1 to R7). The slides use the case's numbers, not the notes' worked example (Pujiang Delivery).
Simulation outputs (testbed means and coverage, regrets, backtest reproductions, embedding-DML estimates) are the
case's inputs, checked in case_check.py; here every quantity derived from them, and every exact example, is recomputed.
Run: python3 slides09_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import sqrt, log
import numpy as np
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)

# ── Block A. The decision (Meeting 8 Left One Doubt) ──
rate, cost, rise = 800, 200, F(8, 100)
check("contribution now 600", "600", rate - cost)
check("contribution after 8% rise 664", "664", rate * (1 + rise) - cost)
check("higher rate 864", "864", rate * (1 + rise))
be = log(600 / 664) / log(1.08)
check("break-even elasticity -1.32", "-1.32", be)
check("hotel-nights 87,600 = 80 x 1,095", "87600", 80 * 1095)
m8 = -1.56
assert m8 < be                                          # M8's estimate is past the break-even: do not raise
pays = lambda eta: 664 * 1.08 ** eta > 600               # does the 8% rise pay at elasticity eta?
assert not pays(m8) and pays(-0.9)                       # synthetic guests' -0.9 would say raise

# ── Realistic Is Not Causal: Meeting 8's six nights ──
cat = np.array([0, 0, 0, 1, 1, 1]); P = np.array([30, 40, 50, 70, 80, 90.]); Q = np.array([110, 100, 90, 210, 200, 190.])
pooled = np.polyfit(P, Q, 1)[0]
check("pooled slope +2.0", "2.0", pooled)
Pt = P - np.array([P[cat == k].mean() for k in cat]); Qt = Q - np.array([Q[cat == k].mean() for k in cat])
within = (Pt @ Qt) / (Pt @ Pt)
check("within-category slope -1.0", "-1.0", within)
check("price +10, Simulator 1: demand +20", "20", 10 * pooled); check("price +10, Simulator 2: demand -10", "-10", 10 * within)
assert np.corrcoef(P, Q)[0, 1] > 0                     # 'the same positive association'

# ── Planting the truth ──
check("8% rise multiplies bookings by 1.08^-1.50 = 0.891", "0.891", 1.08 ** -1.50)

# ── Estimator testbed (case inputs: means and coverage); bias = mean - (-1.50) ──
truth = -1.50
rows = [("OLS none", 0.42, "1.92", 0.00), ("OLS bands", -1.18, "0.32", 0.02), ("DML boost", -1.49, "0.01", 0.94),
        ("DML lasso", -1.41, "0.09", 0.71), ("DML boost, overrides", -1.37, "0.13", 0.38)]
for lab, est, bias, cov in rows:
    check(f"bias {lab}", bias, est - truth)
assert min(rows, key=lambda r: abs(r[1] - truth))[0] == "DML boost"
check("override-adjusted M8: -1.56 - 0.13", "-1.69", m8 - 0.13)
assert m8 - 0.13 < be                                   # further past the break-even: decision unchanged

# ── Result 1.2 illustration: four equally common nights ──
v = np.array([800, 100, -100, -1000.])
vP = np.array([350, -350, 350, -550.]); vQ = np.array([-50, 150, -150, -950.])
w = np.full(4, 0.25)
oracle = (v > 0).astype(int); piP = (vP > 0).astype(int); piQ = (vQ > 0).astype(int)
assert list(oracle) == [1, 1, 0, 0] and list(piP) == [1, 0, 1, 0] and list(piQ) == [0, 1, 0, 0]
val = lambda pi: float(w @ (pi * v))
check("oracle value 225", "225", val(oracle)); check("P value 175", "175", val(piP)); check("Q value 25", "25", val(piQ))
reg = lambda pi: float(w @ (np.abs(v) * (pi != oracle)))   # Result 1.2's formula
check("P regret 50 (formula)", "50", reg(piP)); check("Q regret 200 (formula)", "200", reg(piQ))
check("P regret = V* - V(P)", "50", val(oracle) - val(piP)); check("Q regret = V* - V(Q)", "200", val(oracle) - val(piQ))
check("oracle 1/4(800 + 100)", "225", (800 + 100) / 4); check("P 1/4(100 + 100)", "50", (100 + 100) / 4)
check("Q 1/4(800)", "200", 800 / 4)
check("RMSE P 450", "450", sqrt(w @ (vP - v) ** 2)); check("RMSE Q 427", "427", sqrt(w @ (vQ - v) ** 2))
assert sqrt(w @ (vP - v) ** 2) > sqrt(w @ (vQ - v) ** 2)  # P less accurate
check("P regret a quarter of Q's", "0.25", reg(piP) / reg(piQ))
check("P's mistakes 100 from break-even", "100", np.abs(v[piP != oracle]).max())
assert np.all(np.abs((vQ - v)[1:]) == 50)               # Q gets three nights nearly right

# ── Pipeline testbed (case inputs: regrets, shares above 1,920) ──
regret = {"RM": (1450, 1520), "vendor": (380, 2240), "DML": (690, 760)}
above = {"RM": 5, "vendor": 14, "DML": 3}
assert sorted(regret, key=lambda k: regret[k][0]) == ["vendor", "DML", "RM"]
assert sorted(regret, key=lambda k: regret[k][1]) == ["DML", "RM", "vendor"]
worst = {k: max(r) for k, r in regret.items()}
check("worst case RM 1,520", "1520", worst["RM"]); check("worst case vendor 2,240", "2240", worst["vendor"])
check("worst case DML 760 (smallest)", "760", min(worst.values())); assert min(worst, key=worst.get) == "DML"
assert regret["DML"][0] < regret["RM"][0] and regret["DML"][1] < regret["RM"][1]   # DML beats RM on both
assert max(regret["vendor"]) == max(max(r) for r in regret.values())                 # vendor worst on neural
check("1,920 is the 95th percentile: 5% of logged nights above", "5", 100 - 95)
assert above["DML"] < above["RM"] < above["vendor"]

# ── Backtest ──
itt, se_bt = 4.8, 1.3
check("backtest SE 20 sqrt(2/500)", "1.3", 20 * sqrt(2 / 500))
check("gap boosted 0.2", "0.2", itt - 4.6); check("gap neural 1.4", "1.4", itt - 3.4)
check("gap boosted in SEs 0.2", "0.2", (itt - 4.6) / se_bt); check("gap neural in SEs 1.1", "1.1", (itt - 3.4) / se_bt)
assert (itt - 3.4) / se_bt < 1.96                       # neither rejected

# ── Block B. The Q3 test and the review labels ──
N, nG = 5000, 200
check("reviews 10,000 = 2 x 5,000", "10000", 2 * N)
llm = {"hi": F(22, 100), "cur": F(15, 100)}
check("model-label effect 0.07", "0.07", llm["hi"] - llm["cur"]); check("7 points", "7", 100 * (llm["hi"] - llm["cur"]))
assert 100 * (llm["hi"] - llm["cur"]) > 5               # trips the 5-point guardrail on model labels
conf = {"hi": dict(tp=34, fn=2, fp=12, tn=152), "cur": dict(tp=26, fn=2, fp=4, tn=168)}
p, al, be_, mg, var_r = {}, {}, {}, {}, {}
for a, k in conf.items():
    assert sum(k.values()) == nG
    p[a] = F(k["tp"] + k["fn"], nG); al[a] = F(k["fp"], k["fp"] + k["tn"]); be_[a] = F(k["fn"], k["tp"] + k["fn"])
    mg[a] = F(k["tp"] + k["fp"], nG)
    r = [-1] * k["fp"] + [1] * k["fn"] + [0] * (k["tp"] + k["tn"])
    mu = sum(r) / nG; var_r[a] = sum((x - mu) ** 2 for x in r) / nG
check("gold complaints higher 36", "36", 34 + 2); check("gold complaints current 28", "28", 26 + 2)
check("gold non-complaints higher 164", "164", 12 + 152); check("gold non-complaints current 172", "172", 4 + 168)
check("p1 36/200 = 0.18", "0.18", p["hi"]); check("p0 28/200 = 0.14", "0.14", p["cur"])
check("catches higher 0.944", "0.944", 1 - be_["hi"]); check("catches current 0.929", "0.929", 1 - be_["cur"])
check("flags higher 0.073", "0.073", al["hi"]); check("flags current 0.023", "0.023", al["cur"])
check("true effect 0.04", "0.04", p["hi"] - p["cur"])
check("three times as many false positives", "3", al["hi"] / al["cur"], tol=0.2)

# ── Differential error, decomposed (Result 1.3 on the gold reviews) ──
check("model on gold, higher 46/200 = 0.23", "0.23", mg["hi"]); check("model on gold, current 30/200 = 0.15", "0.15", mg["cur"])
check("gap on gold 0.08", "0.08", mg["hi"] - mg["cur"]); check("twice the true 0.04", "2", (mg["hi"] - mg["cur"]) / (p["hi"] - p["cur"]))
check("beta higher 0.056", "0.056", be_["hi"]); check("beta current 0.071", "0.071", be_["cur"])
scaled = (1 - al["hi"] - be_["hi"]) * p["hi"] - (1 - al["cur"] - be_["cur"]) * p["cur"]
check("scaled true rates 0.030", "0.030", scaled); check("alpha gap 0.050", "0.050", al["hi"] - al["cur"])
check("Result 1.3 sum = 0.08 exactly", "0.08", scaled + al["hi"] - al["cur"]); assert scaled + al["hi"] - al["cur"] == mg["hi"] - mg["cur"]
check("printed rounded terms give 0.030", "0.030", (1 - 0.073 - 0.056) * 0.18 - (1 - 0.023 - 0.071) * 0.14)
fac = F(26, 28) - F(4, 172)
check("1 - alpha0 - beta0 = 26/28 - 4/172 = 0.905", "0.905", fac); assert 1 - al["cur"] - be_["cur"] == fac
check("non-differential effect 0.036", "0.036", fac * (p["hi"] - p["cur"]))
check("manufactured about 0.03", "0.03", (llm["hi"] - llm["cur"]) - fac * (p["hi"] - p["cur"]), tol=0.005)

# ── Result 1.4 illustration: business vs leisure hotels ──
q = F(1, 10); tb, tl = F(-1), F(-2)
check("hotels 40 = 20 + 20", "40", 20 + 20)
cb = (1 - q) * tb + q * tl; cl = q * tb + (1 - q) * tl
check("coded business -1.1", "-1.1", cb); check("coded leisure -1.9", "-1.9", cl)
check("true gap 1.0", "1.0", tb - tl); check("coded gap 0.8", "0.8", cb - cl)
check("(1 - 2q) x 1.0 = 0.8", "0.8", (1 - 2 * q) * (tb - tl)); assert cb - cl == (1 - 2 * q) * (tb - tl)
check("1 - 2 x 0.10 = 0.8", "0.8", 1 - 2 * F(10, 100))

# ── PPI on the Q3 reviews (Result 1.5) ──
ppi = {a: llm[a] + p[a] - mg[a] for a in llm}
check("rectifier higher -0.05", "-0.05", p["hi"] - mg["hi"]); check("rectifier current -0.01", "-0.01", p["cur"] - mg["cur"])
check("PPI higher 0.17", "0.17", ppi["hi"]); check("PPI current 0.14", "0.14", ppi["cur"])
check("PPI effect 0.03", "0.03", ppi["hi"] - ppi["cur"]); check("3 points", "3", 100 * (ppi["hi"] - ppi["cur"]))
check("Var(Y - f) higher 0.0675", "0.0675", var_r["hi"]); check("Var(Y - f) current 0.0299", "0.0299", var_r["cur"])
check("Var(f) higher 0.22 x 0.78", "0.78", 1 - llm["hi"]); check("Var(f) current 0.15 x 0.85", "0.85", 1 - llm["cur"])
se_hi = sqrt(float(llm["hi"] * (1 - llm["hi"])) / N + var_r["hi"] / nG)
se_cu = sqrt(float(llm["cur"] * (1 - llm["cur"])) / N + var_r["cur"] / nG)
check("SE higher 0.019", "0.019", se_hi); check("SE current 0.013", "0.013", se_cu)
check("SE effect from printed 0.019, 0.013", "0.023", sqrt(0.019 ** 2 + 0.013 ** 2))
check("SE effect unrounded", "0.023", sqrt(se_hi ** 2 + se_cu ** 2))
check("CI lower -0.015", "-0.015", 0.03 - 1.96 * 0.023); check("CI upper 0.075", "0.075", 0.03 + 1.96 * 0.023)
check("interval reaches 7.5 points", "7.5", 100 * (0.03 + 1.96 * 0.023))
assert 0.03 < 0.05 < 0.03 + 1.96 * 0.023               # not tripped, not cleared
check("gold-only SE 0.037", "0.037", sqrt(0.18 * 0.82 / nG + 0.14 * 0.86 / nG))
check("outcome variance higher 0.15", "0.15", 0.18 * 0.82); check("outcome variance current 0.12", "0.12", 0.14 * 0.86)
assert var_r["hi"] < 0.18 * 0.82 and var_r["cur"] < 0.14 * 0.86
one_arm = (llm["hi"] + p["cur"] - mg["cur"]) - (llm["cur"] + p["cur"] - mg["cur"])
check("rectifier from current arm alone leaves 0.07", "0.07", one_arm)

# ── Embeddings as controls (case inputs: shares left and estimates) ──
check("reviews move the estimate by 0.59", "0.59", -0.97 - m8)
check("listing pages move it by 0.02 (barely)", "0.02", abs(-1.58 - m8))
assert -0.97 > be                                        # past the break-even, on the wrong side
check("SE factor 9% -> 6%: 1.22", "1.22", sqrt(9 / 6)); check("SE factor 9% -> 1%: 3", "3", sqrt(9 / 1))
check("SE at 6%: 0.03 x 1.22", "0.04", 0.03 * 1.22); check("SE at 1%: 0.03 x 3", "0.09", 0.03 * 3)
check("SE at 6% unrounded factor", "0.04", 0.03 * sqrt(9 / 6))

# ── What Wendy decides: the Q3 elasticity ──
el = lambda x: log(1 + x) / log(1.08)
check("Q3 elasticity -1.72", "-1.72", el(-0.124))
check("Q3 CI lower -2.07", "-2.07", el(-0.124 - 1.96 * 0.012)); check("Q3 CI upper -1.38", "-1.38", el(-0.124 + 1.96 * 0.012))
assert el(-0.124 + 1.96 * 0.012) < be                    # excludes the break-even, narrowly
check("margin to break-even (narrowly)", "0.06", be - el(-0.124 + 1.96 * 0.012), tol=0.01)

print(f"\n{len(FAIL)} mismatches: {FAIL}")
