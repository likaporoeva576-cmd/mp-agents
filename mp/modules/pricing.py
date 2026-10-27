"""Цены: пол цены от себестоимости, акции, конкуренты, связка с остатками."""


def floor_price(r, cfg):
    # цена, при которой после комиссии, логистики и рекламы остаётся целевая маржа
    share = 1 - r["commission"] - cfg["ads_share"] - cfg["target_margin"]
    return (r["cost"] + r["logistics"]) / share


def profit(price, r, cfg):
    return price * (1 - r["commission"] - cfg["ads_share"]) - r["cost"] - r["logistics"]


def check(rows, cfg, stock_days=None):
    stock_days = stock_days or {}
    out = []
    for r in rows:
        floor = floor_price(r, cfg)
        days = stock_days.get(r["sku"])
        low_stock = days is not None and 0 < days < 7

        if profit(r["price"], r, cfg) < 0:
            out.append((r["sku"], "убыток", f"минус {-profit(r['price'], r, cfg):.0f} ₽ с единицы, пол цены {floor:.0f} ₽"))
        elif r["price"] < floor:
            out.append((r["sku"], "маржа", f"цена {r['price']:.0f} ₽ ниже пола {floor:.0f} ₽"))

        # акция площадки: заходим, только если по цене акции остаёмся в плюсе
        if r["promo_price"]:
            p = profit(r["promo_price"], r, cfg)
            verdict = f"прибыль {p:.0f} ₽ с единицы → заходить" if p > 0 else f"убыток {-p:.0f} ₽ с единицы → не заходить"
            out.append((r["sku"], "акция", f"цена акции {r['promo_price']:.0f} ₽, {verdict}"))

        # конкурент дешевле: опускаемся не ниже пола, иначе держим цену и усиливаем карточку
        if r["competitor_price"] and r["competitor_price"] < r["price"] and not low_stock:
            target = max(r["competitor_price"], floor)
            if target < r["price"]:
                note = "" if target == r["competitor_price"] else ", ниже не даёт маржа"
                out.append((r["sku"], "конкурент", f"конкурент {r['competitor_price']:.0f} ₽, можно снизить до {target:.0f} ₽{note}"))
            else:
                out.append((r["sku"], "конкурент", f"конкурент {r['competitor_price']:.0f} ₽ ниже нашего пола, цену держим, работаем с карточкой"))

        # связка с логистикой: мало запаса — не распродавать хит в ноль и не гнаться за конкурентом,
        # много — ускорить продажи
        if low_stock:
            out.append((r["sku"], "запас", f"запаса {days:.0f} дн., поднять цену на 5–10% до прихода поставки"))
        elif days is not None and days > 90 and r["price"] * 0.9 >= floor:
            out.append((r["sku"], "запас", f"запаса {days:.0f} дн., снизить цену до {r['price'] * 0.9:.0f} ₽ вместо платного хранения"))
    return out
