"""Ozon: забор данных. OZON_CLIENT_ID и OZON_API_KEY для Seller API, отдельный ключ для Performance API."""
import os

SELLER = "https://api-seller.ozon.ru"           # товары, остатки, цены, аналитика
PERFORMANCE = "https://api-performance.ozon.ru"  # реклама


def headers():
    return {"Client-Id": os.environ["OZON_CLIENT_ID"], "Api-Key": os.environ["OZON_API_KEY"]}


def fetch_stocks():
    raise NotImplementedError("остатки FBO/FBS по складам")


def fetch_analytics(date_from, date_to):
    raise NotImplementedError("показы, переходы, корзина, заказы по товару")


def fetch_ads_stats(date_from, date_to):
    raise NotImplementedError("статистика кампаний Performance API")
