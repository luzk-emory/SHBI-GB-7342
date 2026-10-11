"""Arithmetic checks for meetings/m01/slides.tex (lecture case: Lena's coupon programme, Houtan Coffee).
The slides use their own numbers, not the notes' worked example. Run: python3 slides01_check.py"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
FAIL = []
def check(label, claimed, computed, tol=None):
    """claimed: string as printed in the .tex; computed rounded half-up to the same decimals."""
    s = str(claimed); d = len(s.split('.')[1]) if '.' in s else 0
    c = Decimal(repr(round(float(computed), 12))).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    ok = abs(float(c) - float(s)) < 1e-12 if tol is None else abs(float(computed) - float(s)) <= tol
    print(f"{'OK ' if ok else 'MISMATCH'} | {label}: text {s}, computed {float(computed):.6g}")
    if not ok: FAIL.append(label)

m, c = 30, 10                                   # margin per purchase, coupon cost per redemption
N_BASE, N_REGION = 10_000, 1_000
be = lambda p1: F(c) * F(p1) / m                 # Result 1.4: tau* = c p1 / m
net = lambda tau, p1: m * F(tau) - c * F(p1)     # V = m tau - c p1

# --- R1: marketing's pilot
p1_pilot, p0_pilot = F(68, 100), F(24, 100)
check("pilot naive 0.68 - 0.24 = 0.44", "0.44", p1_pilot - p0_pilot)
check("pilot break-even p1/3", "0.227", be(p1_pilot))
check("c x p1 = 6.80", "6.80", c * p1_pilot)
check("pilot net per coupon +6.40", "6.40", net(F(44, 100), p1_pilot))
check("pilot forecast across base 64,000", "64000", N_BASE * net(F(44, 100), p1_pilot))

# --- R2: types in the pilot region (thought experiment) and the confounded split
types = {'LC': (0, 0), 'ST': (1, 1), 'P': (0, 1), 'DND': (1, 0)}
total = {'LC': 400, 'ST': 300, 'P': 200, 'DND': 100}
cpn = {'LC': 100, 'ST': 220, 'P': 120, 'DND': 60}
non = {k: total[k] - cpn[k] for k in total}
check("non-coupon arm counts", "300", non['LC']); check("non ST 80", "80", non['ST'])
check("non P 80", "80", non['P']); check("non DND 40", "40", non['DND'])
check("region size 1,000", "1000", sum(total.values()))
check("coupon arm 500", "500", sum(cpn.values())); check("no-coupon arm 500", "500", sum(non.values()))
for k, sh in zip(total, ("40", "30", "20", "10")): check(f"share {k}", sh, 100 * F(total[k], 1000))
ATE = F(total['P'] - total['DND'], 1000)
check("ATE = 0.20 - 0.10 = 0.10", "0.10", ATE)
check("30% - 20% gives the same 0.10", "0.10", F(30, 100) - F(20, 100))
rate = lambda arm, d: F(sum(n for k, n in arm.items() if types[k][d] == 1), sum(arm.values()))
check("pilot coupon arm rate (220+120)/500", "0.68", rate(cpn, 1))
check("pilot no-coupon arm rate (80+40)/500", "0.24", rate(non, 0))
check("4.4 times the true effect", "4.4", (rate(cpn, 1) - rate(non, 0)) / ATE)
# type cost table
for k, (y0, y1) in types.items():
    un, tr = m * y0, (m - c) * y1
    print(f"OK  | type {k}: without {un}, with {tr}, change {tr - un}")
assert [(m - c) * 1 - 0, (m - c) - m, 0, 0 - m] == [20, -10, 0, -30]

# --- Results 1.6 and 1.7 on the pilot
ATT = F(cpn['P'] - cpn['DND'], 500); ATU = F(non['P'] - non['DND'], 500)
Y0_T = F(cpn['ST'] + cpn['DND'], 500); Y0_U = F(non['ST'] + non['DND'], 500)
check("would buy without, coupon arm 280", "280", cpn['ST'] + cpn['DND'])
check("would buy without, no-coupon arm 120", "120", non['ST'] + non['DND'])
check("E[Y(0)|D=1] 0.56", "0.56", Y0_T); check("E[Y(0)|D=0] 0.24", "0.24", Y0_U)
check("ATT (120-60)/500 = 0.12", "0.12", ATT); check("selection bias 0.32", "0.32", Y0_T - Y0_U)
check("naive = 0.12 + 0.32 = 0.44", "0.44", ATT + Y0_T - Y0_U)
share = (Y0_T - Y0_U) / F(44, 100)
print(f"OK  | 'nearly three quarters' of the lift is selection: {float(share):.3f}"); assert F(7, 10) < share < F(3, 4)
check("recipients' net 0.12x30 - 6.80 = -3.20", "-3.20", net(ATT, p1_pilot))
check("ATU (80-40)/500 = 0.08", "0.08", ATU)
check("0.5x0.12 + 0.5x0.08 = 0.10", "0.10", F(1, 2) * ATT + F(1, 2) * ATU)
check("selection on gains 0.5x(0.12-0.08) = 0.02", "0.02", F(1, 2) * (ATT - ATU))
check("total bias 0.44 - 0.10 = 0.34", "0.34", (Y0_T - Y0_U) + F(1, 2) * (ATT - ATU))

# --- R3: segments of the base (5,000 each)
seg = {'active': (F(80, 100), F(75, 100)), 'lapsed': (F(30, 100), F(10, 100))}
eff = {k: y1 - y0 for k, (y1, y0) in seg.items()}
check("active effect 0.05", "0.05", eff['active']); check("lapsed effect 0.20", "0.20", eff['lapsed'])
check("base ATE 0.125", "0.125", (eff['active'] + eff['lapsed']) / 2)
check("four times better", "4", eff['lapsed'] / eff['active'])
# (a) coupon to the active; (b) coupon to the lapsed
check("(a) naive 0.80 - 0.10", "0.70", seg['active'][0] - seg['lapsed'][1])
check("(a) bias 0.75 - 0.10", "0.65", seg['active'][1] - seg['lapsed'][1])
check("(a) 14-fold", "14", (seg['active'][0] - seg['lapsed'][1]) / eff['active'])
check("(b) naive 0.30 - 0.75", "-0.45", seg['lapsed'][0] - seg['active'][1])
check("(b) bias 0.10 - 0.75", "-0.65", seg['lapsed'][1] - seg['active'][1])
check("(b) ATT + bias = naive", "-0.45", eff['lapsed'] + seg['lapsed'][1] - seg['active'][1])

# --- R4: the Q2 test, expected split and one possible draw
half = {k: v // 2 for k, v in total.items()}
check("Q2 expected coupon rate (150+100)/500", "0.50", rate(half, 1))
check("Q2 expected control rate (150+50)/500", "0.40", rate(half, 0))
check("Q2 difference 0.10", "0.10", rate(half, 1) - rate(half, 0))
draw = {'LC': 195, 'ST': 155, 'P': 105, 'DND': 45}; rest = {k: total[k] - draw[k] for k in total}
check("draw coupon arm 500", "500", sum(draw.values()))
check("draw control LC 205", "205", rest['LC']); check("draw control ST 145", "145", rest['ST'])
check("draw control P 95", "95", rest['P']); check("draw control DND 55", "55", rest['DND'])
check("draw coupon rate 0.52", "0.52", rate(draw, 1)); check("draw control rate 0.40", "0.40", rate(rest, 0))
check("draw estimate 0.12", "0.12", rate(draw, 1) - rate(rest, 0))
check("2,000 fixed potential outcomes", "2000", 2 * N_REGION)
p1_q2 = F(1, 2)
check("Q2 break-even 0.50/3", "0.167", be(p1_q2))
check("c x p1 = 5", "5", c * p1_q2)
check("Q2 net per coupon -2.00", "-2.00", net(F(1, 10), p1_q2))
check("Q2 forecast across base -20,000", "-20000", N_BASE * net(F(1, 10), p1_q2))

# --- R5: segment economics
for k, (y1, _) in seg.items():
    check(f"{k} revenue", {"active": "1.50", "lapsed": "6.00"}[k], m * eff[k])
    check(f"{k} break-even", {"active": "0.267", "lapsed": "0.100"}[k], be(y1))
    check(f"{k} net", {"active": "-6.50", "lapsed": "3.00"}[k], net(eff[k], y1))
check("coupon everyone -17,500", "-17500", 5000 * net(eff['active'], seg['active'][0]) + 5000 * net(eff['lapsed'], seg['lapsed'][0]))
check("lapsed only +15,000", "15000", 5000 * net(eff['lapsed'], seg['lapsed'][0]))

# --- Block B: Q3 win-back campaign (Simpson reversal), counts at the segment rates
wb = {('active', 1): 1000, ('active', 0): 4000, ('lapsed', 1): 4000, ('lapsed', 0): 1000}
bought = {(s, d): n * seg[s][0 if d == 1 else 1] for (s, d), n in wb.items()}
for key, cl in zip(wb, ("800", "3000", "1200", "100")): check(f"bought {key}", cl, bought[key])
pc = (bought[('active', 1)] + bought[('lapsed', 1)]) / 5000
pn = (bought[('active', 0)] + bought[('lapsed', 0)]) / 5000
check("pooled coupon bought 2,000", "2000", bought[('active', 1)] + bought[('lapsed', 1)])
check("pooled no-coupon bought 3,100", "3100", bought[('active', 0)] + bought[('lapsed', 0)])
check("pooled coupon rate 0.40", "0.40", pc); check("pooled no-coupon rate 0.62", "0.62", pn)
check("pooled difference -0.22", "-0.22", pc - pn)
check("standardised ATE 0.125", "0.125", (5000 * eff['active'] + 5000 * eff['lapsed']) / 10000)
ATT_wb = (1000 * eff['active'] + 4000 * eff['lapsed']) / 5000
check("standardised ATT 0.17", "0.17", ATT_wb)
Y0_T_wb = (1000 * seg['active'][1] + 4000 * seg['lapsed'][1]) / 5000
check("E[Y(0)|D=1] 0.23", "0.23", Y0_T_wb)
check("selection bias 0.23 - 0.62", "-0.39", Y0_T_wb - pn)
check("ATT + bias = -0.22", "-0.22", ATT_wb + Y0_T_wb - pn)

# --- Result 1.10 (collider), as stated on the slide
cells = [(d, u) for d in (0, 1) for u in (0, 1)]
cm = lambda dv: F(sum(u for d, u in cells if d == dv and max(d, u) == 1), sum(1 for d, u in cells if d == dv and max(d, u) == 1))
check("collider E[Y|D=1,C=1]", "0.5", cm(1)); check("collider E[Y|D=0,C=1]", "1", cm(0))
check("collider difference", "-0.5", cm(1) - cm(0))

print(f"\n{len(FAIL)} mismatches: {FAIL}")
