# Simulated Pujiang Delivery zone-hour panel for the Meeting 8 worked example.
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LassoCV
from sklearn.model_selection import KFold
rng=np.random.default_rng(42)
n=40000
hour=rng.integers(0,24,n); rain=rng.binomial(1,0.2,n); weekend=rng.binomial(1,2/7,n)
zone=rng.normal(0,1,n); supply=rng.normal(0,1,n)
dinner=((hour>=17)&(hour<=20)).astype(float); lunch=((hour>=11)&(hour<=13)).astype(float)
demand=0.9*dinner+0.5*lunch+0.4*rain+0.2*weekend+0.3*zone+0.15*np.sin(hour/24*2*np.pi)
X=np.c_[hour,rain,weekend,zone,supply,dinner,lunch]
# fee set by system: responds to demand and supply plus experiments/rounding noise
logfee=np.log(4)+0.25*demand-0.10*supply+0.05*demand**2+rng.normal(0,0.10,n)
theta=-0.6
logq=2.0+1.0*demand+0.3*demand**2+theta*(logfee-np.log(4))+0.1*supply+rng.normal(0,0.30,n)
# naive
b=np.polyfit(logfee,logq,1)[0]
def dml(learner):
    kf=KFold(5,shuffle=True,random_state=0); rY=np.zeros(n); rD=np.zeros(n)
    for tr,te in kf.split(X):
        mY=learner().fit(X[tr],logq[tr]); mD=learner().fit(X[tr],logfee[tr])
        rY[te]=logq[te]-mY.predict(X[te]); rD[te]=logfee[te]-mD.predict(X[te])
    th=(rD*rY).sum()/(rD*rD).sum(); eps=rY-th*rD
    se=np.sqrt((rD**2*eps**2).sum())/(rD**2).sum()
    r2D=1-rD.var()/logfee.var()
    return th,se,r2D,rY,rD
gb=lambda: HistGradientBoostingRegressor(max_iter=300,learning_rate=0.05)
th,se,r2,rY,rD=dml(gb)
# lasso with polynomial-ish features
from sklearn.preprocessing import OneHotEncoder
H=np.eye(24)[hour]
Xl=np.c_[H,rain,weekend,zone,supply,zone*rain,rain*dinner,weekend*dinner,zone**2,supply**2]
def dml_l():
    kf=KFold(5,shuffle=True,random_state=0); rY2=np.zeros(n); rD2=np.zeros(n)
    for tr,te in kf.split(Xl):
        mY=LassoCV(cv=3).fit(Xl[tr],logq[tr]); mD=LassoCV(cv=3).fit(Xl[tr],logfee[tr])
        rY2[te]=logq[te]-mY.predict(Xl[te]); rD2[te]=logfee[te]-mD.predict(Xl[te])
    t=(rD2*rY2).sum()/(rD2*rD2).sum(); e=rY2-t*rD2; return t,np.sqrt((rD2**2*e**2).sum())/(rD2**2).sum()
thl,sel=dml_l()
print(f"naive {b:.3f}")
print(f"DML-GB {th:.3f} se {se:.3f} R2D {r2:.3f} sdY {(rY-th*rD).std():.3f} sdD {rD.std():.3f}")
print(f"DML-lasso {thl:.3f} se {sel:.3f}")
# figure data now written by m08_fig.py
# np.savetxt('m08_resid_sample.csv',np.c_[rD[:300],rY[:300]],delimiter=',',fmt='%.4f')
# benchmark: partial R2 of rain (column 1) with residualised fee and outcome
Xn=np.delete(X,1,axis=1)
def resid(Xm,y):
    kf=KFold(5,shuffle=True,random_state=0); r=np.zeros(n)
    for tr,te in kf.split(Xm):
        r[te]=y[te]-gb().fit(Xm[tr],y[tr]).predict(Xm[te])
    return r
rD_n=resid(Xn,logfee); 
yt=logq-th*logfee
rY_full=resid(X,yt); rY_n=resid(Xn,yt)
r2D=1-rD.var()/rD_n.var(); r2Y=1-rY_full.var()/rY_n.var()
print(f"rain partial R2: D {r2D:.3f} Y {r2Y:.3f}")
from scipy.optimize import brentq
ratio=(rY-th*rD).std()/rD.std()
f=lambda r: np.sqrt(r*r/(1-r))*ratio-(th-(-0.4))*-1
print('ratio',ratio,'flip r',brentq(lambda r: np.sqrt(r*r/(1-r))*ratio-abs(th+0.4),1e-5,0.9))
print('bound at .05', np.sqrt(.05*.05/.95)*ratio)
