"""Synthetic one-period dispatch experiment. Python 3 + scipy; no measured fleet data."""
import numpy as np
from scipy.optimize import linear_sum_assignment
import csv
from pathlib import Path
NEW=397; REUSE=239; TRANSFER=30 # transfer is a scenario input, not a quote
# Requests: A standard, B critical, C standard. Parts: A high, B standard,
# C standard. Eligibility is an assumed qualification/deadline graph.
# H can cover critical or standard; L only standard. A->B route allowed;
# B->A route allowed. Reserve case holds one H per four repeated blocks.
def solve(blocks=20, scenario='constrained', policy='optimal', reuse=REUSE):
    req=[]; parts=[]
    for b in range(blocks):
        req += [(b,'A',False),(b,'B',True),(b,'C',False)]
        parts += [(b,'A',True),(b,'B',False),(b,'C',False)]
    if scenario=='heterogeneous':
        req=[(b,s,True if s in ('A','B') else False) for b,s,_ in req]
        parts=[(b,s,True if s in ('A','C') else False) for b,s,_ in parts]
    if scenario=='reserve': parts=[p for p in parts if not(p[1]=='A' and p[0]%4==0)]
    n=len(req); m=len(parts); M=np.full((n,m+n),1e6); M[:,m:]=NEW
    for i,(b,s,critical) in enumerate(req):
        for j,(d,t,high) in enumerate(parts):
            if b!=d or (critical and not high): continue
            if scenario=='heterogeneous' and (s,t) not in [('A','A'),('A','C'),('B','A'),('C','B')]: continue
            if scenario not in ('open','heterogeneous') and s!=t and {s,t}!={'A','B'}: continue
            if scenario=='deadline' and s!=t: continue
            M[i,j]=reuse+(TRANSFER if s!=t else 0)
    if policy=='new': chosen=[(i,m+i) for i in range(n)]
    elif policy=='optimal': chosen=list(zip(*linear_sum_assignment(M)))
    else:
        order=sorted(range(n),key=lambda i:not req[i][2]) if policy=='critical_first' else list(range(n))
        free=set(range(m)); chosen=[]
        for i in order:
            elig=[j for j in free if M[i,j]<NEW and (policy!='local' or req[i][1]==parts[j][1])]
            j=min(elig,key=lambda j:(M[i,j],j)) if elig else m+i
            free.discard(j); chosen.append((i,j))
    return [scenario,policy,n,sum(j<m for i,j in chosen),sum(j<m and req[i][1]!=parts[j][1] for i,j in chosen),int(sum(M[i,j] for i,j in chosen))]
if __name__=='__main__':
    rows=[solve(scenario=s,policy=p) for s in ['open','constrained','reserve','deadline','heterogeneous'] for p in ['new','local','greedy','critical_first','optimal']]
    with open(Path(__file__).with_name('CircularOps_3_results.csv'),'w',newline='') as f:
        w=csv.writer(f); w.writerow(['scenario','policy','requests','reused','transfers','direct_cost_usd']); w.writerows(rows)
    for row in rows: print(*row)
