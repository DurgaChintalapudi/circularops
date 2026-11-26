import csv
import unittest
from pathlib import Path
from circularops_model import solve

class ModelTests(unittest.TestCase):
    def test_reproduce_reference(self):
        path = Path(__file__).resolve().parents[1] / "CircularOps_3_results.csv"
        with path.open(newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 25)
        for row in rows:
            expected = [row["scenario"], row["policy"]] + [
                int(row[k]) for k in ("requests", "reused", "transfers", "direct_cost_usd")
            ]
            self.assertEqual(solve(scenario=row["scenario"], policy=row["policy"]), expected)

    def test_cost_and_count_invariants(self):
        for s in ("open", "constrained", "reserve", "deadline", "heterogeneous"):
            optimum = solve(scenario=s, policy="optimal")
            for p in ("new", "local", "greedy", "critical_first", "optimal"):
                _, _, n, reused, transfers, cost = solve(scenario=s, policy=p)
                self.assertTrue(0 <= transfers <= reused <= n)
                self.assertEqual(cost, (n-reused)*397 + reused*239 + transfers*30)
                self.assertLessEqual(optimum[-1], cost)

if __name__ == "__main__":
    unittest.main()
