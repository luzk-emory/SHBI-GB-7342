"""Arithmetic checks for meetings/m10/slides.tex (lecture case: Dana's AI assistant rollout, Sanlin Home,
Case C Meeting 10 parts). The slides use their own numbers, not the notes' worked example. Run: python3 slides10_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import sqrt
import numpy as np
from scipy.stats import t as tdist, norm
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)
z = norm.ppf(0.975)
check("z 1.96", "1.96", z)

# ── The case: costs and the break-even (R1) ──
cost = 1700 + 300 + 500; margin = F(1, 4)
check("cost per store-week 2,500", "2500", cost)
check("break-even 10,000", "10000", cost / margin)
check("dashboard 38,000 / 2,500 = 15.2", "15.2", F(38000, cost))
check("0.25 x 38,000 = 9,500", "9500", margin * 38000); check("9,500 / 2,500 = 3.8", "3.8", margin * 38000 / cost)
check("120 stores = 30 + 89 + flagship", "120", 30 + 89 + 1)
check("comparison 89 = cohort 2 + never scheduled", "89", 30 + 59)

# ── The four cells (R2) ──
n1, n0 = 30, 89
Y = {(1, 0): 181, (1, 1): 196, (0, 0): 151, (0, 1): 155}     # (cohort 1?, after?)
ba = Y[1, 1] - Y[1, 0]; ac = Y[1, 1] - Y[0, 1]; gap0 = Y[1, 0] - Y[0, 0]; trend = Y[0, 1] - Y[0, 0]
did = ba - trend
check("before-after 15", "15", ba); check("across 41", "41", ac); check("level gap before 30", "30", gap0)
check("comparison change +4", "4", trend); check("DiD 11", "11", did)
check("15 = 11 + 4", "15", did + trend); check("41 = 11 + 30", "41", did + gap0)
check("DiD - break-even = 1,000 (yuan)", "1000", (did - 10) * 1000)

# ── Regression to the mean, by enumeration of Result 1.1's model (ATT = 0) ──
lam_step, shocks = 2, (-4, 4)
def mean_change(q4_shock):            # E[(lambda5 + u5) - (lambda4 + u4) | u4], u5 independent of u4
    return lam_step + np.mean(shocks) - q4_shock
pilot, good = mean_change(-4), mean_change(4)
check("pilot change 6", "6", pilot); check("good-Q4 change -2", "-2", good)
check("DiD vs good-Q4 stores 8", "8", pilot - good); check("DiD vs same-selected 0", "0", pilot - mean_change(-4))
check("Result 1.1 decomposition: 0 + 2 + 4", "6", 0 + lam_step - (-4))

# ── Result 1.2 on the four cells: double-demeaning a two-unit panel ──
Ym = np.array([[181, 196], [151, 155]], float); Dm = np.array([[0, 1], [0, 0]], float)
dd = lambda W: W - W.mean(1, keepdims=True) - W.mean(0, keepdims=True) + W.mean()
Yd, Dd = dd(Ym), dd(Dm)
check("Ydd cohort1 before -2.75", "-2.75", Yd[0, 0]); check("Ydd cohort1 after 2.75", "2.75", Yd[0, 1])
check("Ydd comparison before 2.75", "2.75", Yd[1, 0]); check("Ydd comparison after -2.75", "-2.75", Yd[1, 1])
check("Ddd cohort1 before -0.25", "-0.25", Dd[0, 0]); check("Ddd cohort1 after 0.25", "0.25", Dd[0, 1])
check("Ddd comparison before 0.25", "0.25", Dd[1, 0]); check("Ddd comparison after -0.25", "-0.25", Dd[1, 1])
check("sum Ddd Y 2.75", "2.75", (Dd * Ym).sum()); check("0.25 x (-181+196+151-155)", "2.75", 0.25 * (-181 + 196 + 151 - 155))
check("sum Ddd^2 = 4 x 0.0625", "0.25", (Dd ** 2).sum()); check("0.25^2 0.0625", "0.0625", 0.25 ** 2)
check("within beta 11", "11", (Dd * Ym).sum() / (Dd ** 2).sum())
# unit effects only: regress on unit dummies and D, by least squares
X1 = np.column_stack([[1, 1, 0, 0], [0, 0, 1, 1], Dm.ravel()]); b1 = np.linalg.lstsq(X1, Ym.ravel(), rcond=None)[0]
check("store effects only: 15", "15", b1[2])
check("15 - 4 = 11", "11", 15 - 4)

# ── Six quarters (R3); a balanced store-level panel with 30 and 89 stores at the group means ──
q1 = [176, 178, 180, 182, 192, 200]; q0 = [146, 148, 150, 152, 154, 156]
check("78 weeks / 6 quarters = 13", "13", 78 / 6); check("Q7 starts in week 79", "79", 6 * 13 + 1)
check("Q3-Q4 mean cohort 1 = 181", "181", np.mean(q1[2:4])); check("Q5-Q6 mean cohort 1 = 196", "196", np.mean(q1[4:]))
check("Q3-Q4 mean comparison = 151", "151", np.mean(q0[2:4])); check("Q5-Q6 mean comparison = 155", "155", np.mean(q0[4:]))
gaps = [a - b for a, b in zip(q1, q0)]
for k in range(4): check(f"pre gap Q{k+1} 30", "30", gaps[k])
check("counterfactual Q5 184", "184", q0[4] + 30); check("counterfactual Q6 186", "186", q0[5] + 30)
check("arrow Q5 8", "8", q1[4] - (q0[4] + 30)); check("arrow Q6 14", "14", q1[5] - (q0[5] + 30))

units = [1] * n1 + [0] * n0
rows = [(i, t, (q1 if g else q0)[t], g, g * (t >= 4)) for i, g in enumerate(units) for t in range(6)]
idx_i = np.array([r[0] for r in rows]); idx_t = np.array([r[1] for r in rows])
y = np.array([r[2] for r in rows], float); D = np.array([r[4] for r in rows], float); G = np.array([r[3] for r in rows], float)
N = len(units)
UI = np.eye(N)[idx_i]; TT = np.eye(6)[idx_t][:, 1:]
def ols(cols): return np.linalg.lstsq(np.column_stack([UI, TT] + cols), y, rcond=None)[0][N + 5:]
beta_twfe = ols([D])[0]
check("TWFE on six quarters, 119 stores: 11", "11", beta_twfe)
check("pre mean Q1-Q4 cohort 1 179", "179", np.mean(q1[:4])); check("pre mean Q1-Q4 comparison 149", "149", np.mean(q0[:4]))
check("Delta-bar cohort 1 17", "17", np.mean(q1[4:]) - np.mean(q1[:4])); check("Delta-bar comparison 6", "6", np.mean(q0[4:]) - np.mean(q0[:4]))
# event study: k = t - 4 (Q5 is k = 0), base k = -1 (Q4)
ks = [-4, -3, -2, 0, 1]
ev = ols([G * (idx_t - 4 == k) for k in ks])
for k, s in zip(ks, ["0", "0", "0", "8", "14"]): check(f"event-study beta_{k}", s, ev[ks.index(k)])
check("DiD 11 = mean of 8 and 14", "11", (ev[3] + ev[4]) / 2)

# ── Result 1.6: levels or logs ──
check("4/181 = 2.2%", "2.2", 100 * 4 / 181); check("4/151 = 2.6%", "2.6", 100 * 4 / 151)
check("yuan counterfactual 185", "185", 181 + 4); check("yuan effect 11.0", "11.0", 196 - 185)
pc = 181 * 155 / 151
check("percent counterfactual 185.8", "185.8", pc); check("percent effect 10.2", "10.2", 196 - pc)
check("the choice moves about 800 yuan (11.0 - 10.2 as printed)", "800", 1000 * (11.0 - 10.2)); check("unrounded, about 800", "800", 1000 * (11 - (196 - pc)), tol=10)
check("percent gap Q1 20.5%", "20.5", 100 * (176 / 146 - 1)); check("percent gap Q4 19.7%", "19.7", 100 * (182 / 152 - 1))

# ── Result 1.9: one change per store; event-study bars use the same SE ──
se_store = sqrt(6 ** 2 / n1 + 5 ** 2 / n0)
check("36/30 = 1.20", "1.20", 36 / 30); check("25/89 = 0.28", "0.28", 25 / 89); check("SE store 1.22", "1.22", se_store)
lo, hi = did - z * se_store, did + z * se_store
check("store CI low 8.6", "8.6", lo); check("store CI high 13.4", "13.4", hi)
check("plot half-width 2.385", "2.385", z * se_store)
check("margin low -350 (from 8.6)", "-350", 1000 * (0.25 * 8.6 - 2.5)); check("margin high 850 (from 13.4)", "850", 1000 * (0.25 * 13.4 - 2.5))
check("margin low, unrounded, about -350", "-350", 1000 * (0.25 * lo - 2.5), tol=5)
check("margin high, unrounded, about 850", "850", 1000 * (0.25 * hi - 2.5), tol=5)

# ── Store-weeks are not independent: AR(1) with autocorrelation 0.8, 26 weeks before and 26 after ──
check("store-weeks 119 x 78 = 9,282", "9282", 119 * 78); check("weeks 27-52 = 26", "26", 52 - 27 + 1)
rho, T = 0.8, 52
S = rho ** np.abs(np.subtract.outer(np.arange(T), np.arange(T)))
w = np.r_[-np.ones(26) / 26, np.ones(26) / 26]
k = (w @ S @ w) / (1 / 26 + 1 / 26)
check("variance factor 6.70", "6.70", k); check("SE factor 2.59", "2.59", sqrt(k))
se_naive = se_store / sqrt(k)
check("naive SE 0.47", "0.47", se_naive)
check("naive CI low 10.1", "10.1", did - z * se_naive); check("naive CI high 11.9", "11.9", did + z * se_naive)
assert did - z * se_naive > 10 and lo < 10 < hi       # naive interval clears break-even; the honest one does not
# the iid formula for TWFE equals the collapse formula with Var(Delta_i) = sigma^2 (1/26 + 1/26)
sumDdd2 = (n1 * n0 / (n1 + n0)) * (26 * 26 / 52)
assert abs(1 / sumDdd2 - (1 / n1 + 1 / n0) * (2 / 26)) < 1e-12

# ── Region clustering ──
se_reg = sqrt(3 ** 2 / 3 + 2.5 ** 2 / 9); df = 3 + 9 - 2; tc = tdist.ppf(0.975, df)
check("9/3 = 3.00", "3.00", 9 / 3); check("6.25/9 = 0.69", "0.69", 6.25 / 9); check("SE region 1.92", "1.92", se_reg)
check("df 10", "10", df); check("t critical 2.23", "2.23", tc)
check("region CI low 6.7", "6.7", did - tc * se_reg); check("region CI high 15.3", "15.3", did + tc * se_reg)
check("region margin low -825 (from 6.7)", "-825", 1000 * (0.25 * 6.7 - 2.5)); check("region margin high 1,325 (from 15.3)", "1325", 1000 * (0.25 * 15.3 - 2.5))
check("region margin low, unrounded, about -825", "-825", 1000 * (0.25 * (did - tc * se_reg) - 2.5), tol=5)
check("region margin high, unrounded, about 1,325", "1325", 1000 * (0.25 * (did + tc * se_reg) - 2.5), tol=5)
check("twelve clusters", "12", 3 + 9)

# ── Pre-trends and Result 1.8 ──
m = np.array([1, 2, 3]); pre = np.array([ev[2], ev[1], ev[0]])          # beta_{-2}, beta_{-3}, beta_{-4}
check("sum m^2 = 1 + 4 + 9 = 14", "14", (m ** 2).sum())
dhat = -(m * pre).sum() / (m ** 2).sum(); sed = se_store / sqrt(14)
check("delta-hat 0", "0", dhat); check("SE(delta-hat) 0.33", "0.33", sed)
check("drift bound 0.64", "0.64", z * sed); check("drift bound in yuan 640", "640", 1000 * 0.64)
# breakdown drifts; quarters indexed 1..6
tb = lambda qs: np.mean(qs)
check("tbar post 5.5", "5.5", tb([5, 6])); check("tbar Q3-Q4 3.5", "3.5", tb([3, 4])); check("tbar Q1-Q4 2.5", "2.5", tb([1, 2, 3, 4]))
check("four cells distance 2", "2", tb([5, 6]) - tb([3, 4])); check("six quarters distance 3", "3", tb([5, 6]) - tb([1, 2, 3, 4]))
check("Q6 vs Q4 distance 2", "2", 6 - 4)
dstar4 = (did - 10) / 2; dstar6 = (beta_twfe - 10) / 3; dstarQ6 = (ev[4] - 10) / 2
check("delta* four cells 0.5", "0.5", dstar4); check("delta* six quarters 0.33", "0.33", dstar6); check("delta* Q6 2.0", "2.0", dstarQ6)
# Result 1.8 confirmed by adding a linear drift to the comparison-relative gap and recomputing each estimate
def with_drift(delta):
    q1d = [v - delta * (t + 1) for t, v in enumerate(q1)]   # remove a drift that would otherwise inflate the estimates
    return (np.mean(q1d[4:]) - np.mean(q1d[2:4])) - (np.mean(q0[4:]) - np.mean(q0[2:4])), \
           (q1d[5] - q0[5]) - (q1d[3] - q0[3])
check("four-cell DiD at delta* is 10", "10", with_drift(dstar4)[0]); check("Q6 coefficient at delta* is 10", "10", with_drift(dstarQ6)[1])
check("drift 0.5 moves Q1-Q4 gap by 1.5", "1.5", 0.5 * 3)
check("2.0 is about three times 0.64", "3", 2.0 / 0.64, tol=0.2)
assert dstar4 < z * sed < dstarQ6

# ── Staggered warning ──
check("cohort 2 vs cohort 1, Q6 to Q7: 8 - (18 - 14) = 4", "4", 8 - (18 - 14))

# ── Pitfalls frame ──
check("pilot +6 from nothing", "6", pilot)

# ── Dana's decision ──
mg = lambda lift: 1000 * (0.25 * lift - 2.5)
check("margin Q5 -500", "-500", mg(ev[3])); check("margin Q6 +1,000", "1000", mg(ev[4])); check("margin average +250", "250", mg(did))
check("Q6 CI low 11.6", "11.6", ev[4] - z * se_store); check("Q6 CI high 16.4", "16.4", ev[4] + z * se_store)

print(f"\n{len(FAIL)} mismatches: {FAIL}")
