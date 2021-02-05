from Order import Order
from copy import deepcopy


class OrderBook:
    def __init__(self, initial_price, order_difference_tolerance: float):
        self.orders = []
        self.price = initial_price
        self.tolerance = order_difference_tolerance

    def add_order(self, order):
        self.orders.append(order)

    def match_trades(self, traders: list):
        def match_order(order, trader):
            for matched_order in self.orders:
                if not matched_order.executed \
                        and (abs(order.price - matched_order.price) < self.tolerance * self.price) \
                        and order.buy != matched_order.buy:
                    # if the order prices are within tolerance, execute trade
                    for matched_trader in traders:
                        if matched_trader.id == matched_order.trader:
                            shares = min(order.shares, matched_order.shares)
                            price = order.price + matched_order.price / 2

                            # mark orders partially filled
                            order.partial_fill(shares, price, trader)
                            matched_order.partial_fill(shares, price, matched_trader)

                            self.price = order.price
                            print(f"price: ${self.price}")

                            return price

        trades = []
        for order in self.orders:
            for trader in traders:
                if trader.id == order.trader:
                    price = match_order(order, trader)
                    if price:
                        trades.append(price)

            order.life -= 1
            if order.life == 0:
                # release funds
                for trader in traders:
                    if trader.id == order.trader:
                        trader.order_expired(order.shares, order.price, order.buy)
                print("order expired.", order.shares, "shares at $" + str(order.price))

            # clean up orders where life == 0 or executed
            self.orders = [order for order in self.orders if not order.executed and order.life > 0]

        return trades
