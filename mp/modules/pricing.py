"""Цены: пол цены от себестоимости и юнит-экономика."""


def floor_price(r, cfg):
    # цена, при которой после комиссии, логистики и рекламы остаётся целевая маржа
    share = 1 - r["commission"] - cfg["ads_share"] - cfg["target_margin"]
    return (r["cost"] + r["logistics"]) / share


def check(rows, cfg):
    out = []
    for r in rows:
        floor = floor_price(r, cfg)
        profit = r["price"] * (1 - r["commission"] - cfg["ads_share"]) - r["cost"] - r["logistics"]
        if profit < 0:
            out.append((r["sku"], "убыток", f"минус {-profit:.0f} ₽ с единицы, пол цены {floor:.0f} ₽"))
        elif r["price"] < floor:
            out.append((r["sku"], "маржа", f"цена {r['price']:.0f} ₽ ниже пола {floor:.0f} ₽"))
    return out
