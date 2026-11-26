# CircularOps
Evidence-Gated Allocation of Recovered Server Power Supplies Across Enterprise Data Centers

A research prototype for comparing five allocation policies across five deterministic synthetic scenarios. This is not production dispatch software, a field trial, or a complete lifecycle assessment.

## Reproduce
Tested locally with Python 3.13.5, NumPy 2.3.5 and SciPy 1.17.0.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python circularops_model.py
python -m unittest discover -s tests -v
```

The script regenerates CircularOps_3_results.csv with 25 scenario-policy rows (60 requests each).

## Method
The model minimizes direct procurement and transfer costs with a linear assignment solver. Each recovered part can satisfy at most one request. Eligibility is a synthetic binary graph encoding qualification, route and deadline constraints; reserves are excluded from available inventory. Each request has a new-purchase fallback. The 20 repeated blocks are independent, not a fully pooled dynamic fleet.

New and recovered purchase inputs ($397 and $239) were based on public asking prices for Dell G6W6K, not enterprise quotations. The $30 transfer charge is hypothetical. See https://www.radwell.com/Buy/DELL/DELL/G6W6K . Prices and compatibility require rechecking before procurement.

## Findings and limits
The optimizer ties criticality-first allocation in four scenarios and saves $1,960 in the constructed heterogeneous scenario ($16,140 vs $18,100). This demonstrates a conditional benefit, not universal superiority. The model does not establish field failure probabilities, carbon savings, net lifecycle costs or exact OEM compatibility. A scarcity-aware heuristic could match the optimizer; additional validation is needed. Qualification is assumed, not measured.

No proprietary enterprise data is included. The coursework report is not distributed here.
