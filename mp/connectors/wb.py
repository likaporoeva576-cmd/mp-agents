"""Wildberries: забор данных. Ключ — WB_TOKEN в .env (создаётся в кабинете продавца)."""
import os

HOSTS = {
    "statistics": "https://statistics-api.wildberries.ru",      # остатки, заказы, продажи
    "analytics": "https://seller-analytics-api.wildberries.ru",  # воронка по карточкам
    "advert": "https://advert-api.wildberries.ru",              # рекламные кампании и статистика
    "prices": "https://discounts-prices-api.wildberries.ru",     # цены и скидки
    "feedbacks": "https://feedbacks-api.wildberries.ru",         # отзывы
}


def headers():
    return {"Authorization": os.environ["WB_TOKEN"]}


def fetch_stocks():
    raise NotImplementedError("остатки по складам → строки (sku, warehouse, qty)")


def fetch_funnel(date_from, date_to):
    raise NotImplementedError("показы, клики, корзина, заказы, выкупы по артикулу")


def fetch_ads_stats(date_from, date_to):
    raise NotImplementedError("расход и выручка по кампаниям и артикулам")
