"""Запуск: python3 -m mp demo"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

from mp import agent
from mp.modules import ads, logistics, pricing

ROOT = Path(__file__).resolve().parent.parent

CFG = {  # те же значения, что в config.example.yaml
    "logistics": {"sales_window_days": 14, "lead_time_days": 7, "cover_days": 30,
                  "min_stock_days": 14, "max_stock_days": 60},
    "ads": {"max_drr": 0.12, "min_ctr": 0.02, "min_cart_to_order": 0.25},
    "pricing": {"target_margin": 0.20, "ads_share": 0.08},
}


def load(name):
    with open(ROOT / "demo" / name, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k, v in r.items():
            if k != "sku":
                r[k] = v == "1" if k == "ads_on" else float(v)
    return rows


def demo():
    stocks = load("stocks.csv")
    days = logistics.stock_days(stocks, CFG["logistics"])
    blocks = {
        "Логистика": logistics.check(stocks, CFG["logistics"]),
        "Продвижение": ads.check(load("ads.csv"), CFG["ads"]),
        "Цены": pricing.check(load("prices.csv"), CFG["pricing"], days),
    }
    lines = ["# Ежедневный отчёт (демо-данные)", ""]
    for title, signals in blocks.items():
        lines += [f"## {title}", ""]
        by_sku = defaultdict(list)
        for sku, kind, text in signals:
            by_sku[sku].append((kind, text))
        lines += [f"- {agent.explain(sku, s)}" for sku, s in by_sku.items()] or ["- без отклонений"]
        lines.append("")
    report = "\n".join(lines)
    (ROOT / "demo" / "report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    {"demo": demo}.get(sys.argv[1] if len(sys.argv) > 1 else "demo", demo)()
