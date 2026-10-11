# Figure data for Meeting 8: random 300 residual pairs and 20 binned means (full sample).
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
gb=lambda: HistGradientBoostingRegressor(max_iter=300,learning_rate=0.05,random_state=0)
th,se,r2,rY,rD=dml(gb)

print(f"DML-GB {th:.4f} se {se:.4f}")
import numpy as np
idx=np.random.default_rng(1).choice(n,300,replace=False)
np.savetxt('../../meetings/m08/m08_resid_sample.csv',np.c_[rD[idx],rY[idx]],delimiter=',',fmt='%.4f')
q=np.quantile(rD,np.linspace(0,1,21)); b=np.clip(np.searchsorted(q,rD,side='right')-1,0,19)
bm=np.array([[rD[b==k].mean(),rY[b==k].mean()] for k in range(20)])
np.savetxt('../../meetings/m08/m08_resid_bins.csv',bm,delimiter=',',fmt='%.4f')
s=np.polyfit(rD[idx],rY[idx],1)[0]; print('sample slope',s); print(bm)
