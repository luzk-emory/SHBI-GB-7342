# Independent arithmetic check of handoutH6.tex (Staggered adoption), Yangsi Fitness waves example and exercise.
import sys
import numpy as np
R = []
def check(label, claimed, computed, tol=1e-9, sev="error"):
    ok = abs(claimed - computed) <= tol; R.append((ok, sev))
    print(f"[{'ok  ' if ok else ('FAIL' if sev=='error' else 'WARN')}] {label}: text={claimed} computed={computed:.6g}")

# Table rebuilt from the stated DGP: common trend +1/month, effect 6 in adoption month, 3 in the next.
Y = {'E': [40, 47, 45], 'L': [50, 51, 58], 'N': [60, 61, 62]}
G = {'E': 2, 'L': 3, 'N': np.inf}
eff = {0: 6, 1: 3, 2: 3}   # e=2 value 3 is the exercise's month-4 assumption
for g in Y:
    for t in (1, 2, 3):
        y0 = Y[g][0] + (t-1)
        e = t - G[g]
        gen = y0 + (eff[int(e)] if e >= 0 else 0)
        check(f"Table cell {g}, month {t} matches stated trend+effects", Y[g][t-1], gen)
y = lambda g, t: Y[g][t-1]
att_E2 = (y('E',2)-y('E',1)) - (y('N',2)-y('N',1))
att_E3 = (y('E',3)-y('E',1)) - (y('N',3)-y('N',1))
att_L3 = (y('L',3)-y('L',2)) - (y('N',3)-y('N',2))
check("'ATT(E,2) = (47 - 40) - (61 - 60) = 6'", 6, att_E2)
check("'ATT(E,3) = (45 - 40) - (62 - 60) = 3'", 3, att_E3)
check("'ATT(L,3) = (58 - 51) - (62 - 61) = 6'", 6, att_L3)
check("'(ATT(0), ATT(1)) = (6, 3)': ATT(0)", 6, (att_E2+att_L3)/2)
check("'(ATT(0), ATT(1)) = (6, 3)': ATT(1)", 3, att_E3)
check("'overall average 5' (cell-weighted, equal cohort sizes)", 5, np.mean([att_E2, att_E3, att_L3]))
contam = (y('L',3)-y('L',2)) - (y('E',3)-y('E',2))
check("'L against E, months 2->3: (58 - 51) - (45 - 47) = 9'", 9, contam)
check("'ATT(L,3) - [ATT(E,3) - ATT(E,2)] = 6 - (3 - 6) = 9'", 9, att_L3-(att_E3-att_E2))

# Goodman-Bacon 2x2s
m = lambda g, ts: np.mean([y(g,t) for t in ts])
EvN = (m('E',[2,3])-m('E',[1])) - (m('N',[2,3])-m('N',[1]))
LvN = (m('L',[3])-m('L',[1,2])) - (m('N',[3])-m('N',[1,2]))
EvL = (m('E',[2])-m('E',[1])) - (m('L',[2])-m('L',[1]))
LvE = (m('L',[3])-m('L',[2])) - (m('E',[3])-m('E',[2]))
for lab, c, v in [("E vs N 4.5",4.5,EvN),("L vs N 6",6,LvN),("E vs L before 6",6,EvL),("L vs E after 9",9,LvE)]:
    check(f"Bacon 2x2 {lab}", c, v)
# Goodman-Bacon (2021) weights, equal group shares
n = {'E':1/3,'L':1/3,'N':1/3}; Db = {'E':2/3,'L':1/3}
s_EU = (n['E']+n['N'])**2 * 0.25 * Db['E']*(1-Db['E'])
s_LU = (n['L']+n['N'])**2 * 0.25 * Db['L']*(1-Db['L'])
nkl = 0.5
s_kl_k = ((n['E']+n['L'])*(1-Db['L']))**2 * nkl*(1-nkl) * (Db['E']-Db['L'])/(1-Db['L']) * (1-Db['E'])/(1-Db['L'])
s_kl_l = ((n['E']+n['L'])*Db['E'])**2 * nkl*(1-nkl) * Db['L']/Db['E'] * (Db['E']-Db['L'])/Db['E']
S = s_EU+s_LU+s_kl_k+s_kl_l
for lab, c, v in [("1/3 (E vs N)",1/3,s_EU/S),("1/3 (L vs N)",1/3,s_LU/S),("1/6 (E vs L before)",1/6,s_kl_k/S),("1/6 (L vs E after)",1/6,s_kl_l/S)]:
    check(f"Bacon weight {lab}", c, v, tol=1e-12)
bw = (s_EU*EvN+s_LU*LvN+s_kl_k*EvL+s_kl_l*LvE)/S
check("'1/3(4.5) + 1/3(6) + 1/6(6) + 1/6(9) = 6'", 6, 4.5/3+6/3+6/6+9/6)
check("Bacon-weighted average = 6", 6, bw)
# TWFE on the nine cells
rows, yy = [], []
units = ['E','L','N']
for i,g in enumerate(units):
    for t in (1,2,3):
        x = np.zeros(6); x[0]=1
        if i>0: x[i]=1
        if t>1: x[1+t]=1
        x[5] = float(t >= G[g]); rows.append(x); yy.append(y(g,t))
b = np.linalg.lstsq(np.array(rows), np.array(yy), rcond=None)[0][5]
check("'least squares on the nine cells confirms' 6", 6, b, tol=1e-9)
check("'TWFE overstates the overall average of 5'", 1, float(b > 5))
check("Decision: TWFE 6 >= 5.5 but e=1 effect 3 < 5.5", 1, float(b >= 5.5 and att_E3 < 5.5))

# Exercise: month 4 E:46, L:56, N:63
Y4 = {'E':46,'L':56,'N':63}
check("Exercise month-4 E=46 consistent with trend + effect 3", 46, Y['E'][0]+3+3)
check("Exercise month-4 L=56 consistent with trend + effect 3", 56, Y['L'][0]+3+3)
check("Exercise month-4 N=63 consistent with trend", 63, Y['N'][0]+3)
a = (Y4['L']-y('L',2)) - (Y4['N']-y('N',2))
bb = (Y4['L']-y('L',2)) - (Y4['E']-y('E',2))
check("Answer (a) '(56 - 51) - (63 - 61) = 3'", 3, a)
check("Answer (b) '(56 - 51) - (46 - 47) = 5 + 1 = 6'", 6, bb)
att_E4 = (Y4['E']-y('E',1)) - (Y4['N']-y('N',1))
check("Answer (c) ATT(E,4) = 3", 3, att_E4)
check("Answer (c) '3 - (3 - 6) = 6'", 6, a-(att_E4-att_E2))
check("Answer (c) contamination formula equals (b)", bb, a-(att_E4-att_E2))

nbad = [s for ok,s in R if not ok]
print(f"\n{len(R)} checks; {len(R)-len(nbad)} ok; {nbad.count('error')} FAIL; {nbad.count('minor')} WARN")
sys.exit(1 if 'error' in nbad else 0)
