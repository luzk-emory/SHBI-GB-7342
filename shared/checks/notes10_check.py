# Independent arithmetic check of notes10.tex (Panel data and DiD), Yangsi Fitness worked example and exercise.
import sys
from math import sqrt, log
import numpy as np
R = []
def check(label, claimed, computed, tol=0.005, sev="error"):
    ok = abs(claimed - computed) <= tol; R.append((ok, sev))
    print(f"[{'ok  ' if ok else ('FAIL' if sev=='error' else 'WARN')}] {label}: text={claimed} computed={computed:.6g}")

a_pre, a_post, o_pre, o_post = 8.0, 8.9, 7.5, 7.9
# Step 1 / Step 2 table
check("Step 1 'a change of 0.9'", 0.9, a_post-a_pre, tol=1e-9)
check("Table 'Other clubs ... +0.4'", 0.4, o_post-o_pre, tol=1e-9)
check("Table 'Difference 0.5' (Jan-Jun)", 0.5, a_pre-o_pre, tol=1e-9)
check("Table 'Difference 1.0' (Jul-Dec)", 1.0, a_post-o_post, tol=1e-9)
did = (a_post-a_pre)-(o_post-o_pre)
check("Table 'DiD = +0.5'", 0.5, did, tol=1e-9)
check("Table DiD by columns = by rows", (a_post-o_post)-(a_pre-o_pre), did, tol=1e-9)
cf = a_pre + (o_post-o_pre)
check("'the counterfactual 8.4'", 8.4, cf, tol=1e-9)
check("'about 6% of the counterfactual'", 0.06, did/cf, tol=0.005)
# Step 3 logs
dl = log(a_post/a_pre) - log(o_post/o_pre)
check("Step 3 'ln(8.9/8.0) - ln(7.9/7.5) = 0.055'", 0.055, dl, tol=0.0005)
cf_log = a_pre*o_post/o_pre
check("Step 3 '8.0 x 7.9/7.5 = 8.43'", 8.43, cf_log)
check("Step 3 'an effect of 0.47 visits'", 0.47, a_post-cf_log)
check("Step 3 log-scale effect still above 0.3 ('the decision is the same')", 1, float(a_post-cf_log > 0.3), tol=0)

# Step 4 figure
se_es = 0.06
check("Figure error-bar half-width 0.118 = 1.96 x SE 0.06", 0.118, 1.96*se_es, tol=0.0005)
coef = {-3:0.02, -2:-0.03, -1:0.0, 0:0.35, 1:0.52, 2:0.60}
# Step 5: linear drift through base -1: beta_k = delta*(k+1)
x = np.array([-2+1, -3+1], float)  # -1, -2  -> beta_-2 = -delta, beta_-3 = -2 delta
y = np.array([coef[-2], coef[-3]])
check("Step 5 'beta_-2 = -delta' coefficient", -1, x[0], tol=0)
check("Step 5 'beta_-3 = -2 delta' coefficient", -2, x[1], tol=0)
dhat = (x@y)/(x@x)
check("Step 5 'delta_hat = -(1x(-0.03) + 2x0.02)/5 = -0.002'", -0.002, dhat, tol=1e-9)
check("Step 5 'SE 0.06/sqrt5 = 0.027'", 0.027, se_es/sqrt(x@x), tol=0.0005)
half = 1.96*se_es/sqrt(5)
check("Step 5 drift CI lower -0.055", -0.055, dhat-half, tol=0.0005)
check("Step 5 drift CI upper 0.051", 0.051, dhat+half, tol=0.0005)
dstar = (coef[2]-0.30)/(2-(-1))
check("Step 5 'delta* = (0.60 - 0.30)/3 = 0.10'", 0.10, dstar, tol=1e-9)
check("Step 5 'nearly twice what the pre-period allows'", 2.0, dstar/0.055, tol=0.2)
check("Step 5 '0.60 - 3 x 0.055 = 0.435'", 0.435, 0.60-3*0.055, tol=1e-9)
check("Step 5 '0.435 > 0.3'", 1, float(0.60-3*0.055 > 0.3), tol=0)
check("'Pre-period coefficients (0.02 and -0.03) are small' within 1.96 SE", 1, float(max(abs(coef[-3]),abs(coef[-2])) < 1.96*se_es), tol=0)
# Exercise
s1, n1, s0, n0 = 0.20, 20, 0.18, 30
check("Answer '0.20^2/20 = 0.0020'", 0.0020, s1**2/n1, tol=0.00005)
check("Answer '0.18^2/30 = 0.0011'", 0.0011, s0**2/n0, tol=0.00005)
se = sqrt(s1**2/n1 + s0**2/n0)
check("Answer 'SE = ... = 0.055'", 0.055, se, tol=0.0005)
check("Answer interval lower 0.39", 0.39, did-1.96*se)
check("Answer interval upper 0.61", 0.61, did+1.96*se)
check("Answer 'clear of the break-even of 0.3'", 1, float(did-1.96*se > 0.3), tol=0)
check("Answer '6 clusters ... about 5 degrees of freedom'", 5, 6-1, tol=0)

# Prop twfedid numerically: TWFE on a random balanced panel equals the DiD of unit means
rng = np.random.default_rng(0); nU, Tn, t0 = 7, 6, 3
T = (np.arange(nU) < 3).astype(float); P = (np.arange(Tn) >= t0).astype(float)
Y = rng.normal(size=(nU, Tn)); D = np.outer(T, P)
dd = lambda W: W - W.mean(1, keepdims=True) - W.mean(0, keepdims=True) + W.mean()
b = (dd(D)*Y).sum()/(dd(D)**2).sum()
Dl = Y[:, t0:].mean(1) - Y[:, :t0].mean(1)
check("Prop twfedid: TWFE = mean Delta(T=1) - mean Delta(T=0)", Dl[T==1].mean()-Dl[T==0].mean(), b, tol=1e-10)

nbad = [s for ok,s in R if not ok]
print(f"\n{len(R)} checks; {len(R)-len(nbad)} ok; {nbad.count('error')} FAIL; {nbad.count('minor')} WARN")
sys.exit(1 if 'error' in nbad else 0)
