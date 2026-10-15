"""Entirely fictional accounting example: not Apex Pack business data."""
from collections import defaultdict

FICTIONAL_ROWS = [
    {"customer":"Example Client A","product":"Demo Film","revenue":1200.0,"cost":900.0,"collected":800.0},
    {"customer":"Example Client B","product":"Demo Clips","revenue":500.0,"cost":390.0,"collected":500.0},
    {"customer":"Example Client A","product":"Demo Film","revenue":700.0,"cost":520.0,"collected":500.0},
]

def analyze(rows):
    totals = {"revenue":0.0,"cost":0.0,"collections":0.0}
    due = defaultdict(float)
    products = defaultdict(lambda: {"revenue":0.0,"gross_profit":0.0})
    for row in rows:
        if row["cost"]>row["revenue"] or row["collected"]>row["revenue"]:
            raise ValueError("Illustrative record needs review")
        for field, key in [("revenue","revenue"),("cost","cost"),("collected","collections")]:
            totals[key]+=row[field]
        due[row["customer"]]+=row["revenue"]-row["collected"]
        products[row["product"]]["revenue"]+=row["revenue"]
        products[row["product"]]["gross_profit"]+=row["revenue"]-row["cost"]
    totals["gross_profit"]=totals["revenue"]-totals["cost"]
    totals["receivables"]=sum(due.values())
    return totals, dict(due), dict(products)

if __name__=="__main__":
    totals,due,products=analyze(FICTIONAL_ROWS)
    print("FICTIONAL DEMONSTRATION ONLY — no real company data")
    print("Synthetic totals:",totals)
    print("Illustrative account receivables:",due)
    print("Illustrative gross-profit by product:",products)
