"""Продвижение: ДРР и провал в воронке по артикулу."""


def check(rows, cfg):
    out = []
    for r in rows:
        drr = r["ad_spend"] / r["ad_revenue"] if r["ad_revenue"] else float("inf")
        ctr = r["clicks"] / r["views"] if r["views"] else 0
        c2o = r["orders"] / r["carts"] if r["carts"] else 0
        if r["rating"] < 4.6:
            out.append((r["sku"], "рейтинг", f"рейтинг {r['rating']}, не гнать рекламу, разобрать отзывы"))
        if drr > cfg["max_drr"]:
            out.append((r["sku"], "ДРР", f"ДРР {drr:.0%} при норме {cfg['max_drr']:.0%}, снизить ставку"))
        if ctr < cfg["min_ctr"]:
            out.append((r["sku"], "CTR", f"CTR {ctr:.1%}, проверить фото и цену на выдаче"))
        if c2o < cfg["min_cart_to_order"]:
            out.append((r["sku"], "корзина", f"из корзины в заказ {c2o:.0%}, смотреть цену и доставку"))
    return out
