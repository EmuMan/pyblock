from dataclasses import dataclass

from .item import Item
from .utils import request_endpoint

@dataclass
class OrderInformation:
    amount: int
    price_per_unit: float
    orders: int    

class BazaarItem:
    
    product_id: str
    sell_summary: list[OrderInformation]
    buy_summary: list[OrderInformation]
    sell_price: float
    sell_volume: int
    sell_moving_week: int
    sell_orders: int
    buy_price: float
    buy_volume: int
    buy_moving_week: int
    buy_orders: int

    def __init__(self, data: dict):
        self.product_id = data['product_id']
        self.sell_summary = [OrderInformation(order['amount'], order['pricePerUnit'], order['orders']) \
            for order in data['sell_summary']]
        self.buy_summary = [OrderInformation(order['amount'], order['pricePerUnit'], order['orders']) \
            for order in data['buy_summary']]
        quick_status = data['quick_status']
        self.sell_price = quick_status['sellPrice']
        self.sell_volume = quick_status['sellVolume']
        self.sell_moving_week = quick_status['sellMovingWeek']
        self.sell_orders = quick_status['sellOrders']
        self.buy_price = quick_status['buyPrice']
        self.buy_volume = quick_status['buyVolume']
        self.buy_moving_week = quick_status['buyMovingWeek']
        self.buy_orders = quick_status['buyOrders']

class BazaarSnapshot:

    products: dict[str, BazaarItem]

    def __init__(self, bazaar_data: dict):
        self.products = {}
        for key, value in bazaar_data.items():
            self.products[key] = BazaarItem(value)

    def product(self, product_id: str) -> BazaarItem | None:
        return self.products.get(product_id, None)

def get_bazaar_information() -> BazaarSnapshot:
    data = request_endpoint('skyblock/bazaar')
    return BazaarSnapshot(data['products'])
