"""Логистика: дни запаса, объём поставки, риск платного хранения."""


def stock_days(rows, cfg):
    """Дни запаса по артикулу — нужны модулю цен."""
    res = {}
    for r in rows:
        daily = r["sales_14d"] / cfg["sales_window_days"]
        res[r["sku"]] = r["stock"] / daily if daily else float("inf")
    return res


def check(rows, cfg):
    out = []
    for r in rows:
        daily = r["sales_14d"] / cfg["sales_window_days"]
        days = r["stock"] / daily if daily else float("inf")
        need = max(0, round(daily * (cfg["lead_time_days"] + cfg["cover_days"]) - r["stock"] - r["in_transit"]))
        if r["stock"] == 0 and r["ads_on"]:
            out.append((r["sku"], "стоп", "нет остатка, а реклама идёт — остановить кампанию"))
        elif days < cfg["min_stock_days"]:
            out.append((r["sku"], "поставка", f"запас {days:.0f} дн., везти {need} шт."))
        elif days > cfg["max_stock_days"]:
            out.append((r["sku"], "хранение", f"запас {days:.0f} дн., риск платного хранения"))
    return out
