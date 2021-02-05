from NeuralNet import Network
from OrderBook import OrderBook
from Order import Order


class Agent:
    def __init__(self, trading_fee: float, shares: int, cash: int, id: int):
        self.brain = Network()
        self.id = id
        self.brain.add_layer(4)  # 1. self.cash, 2. current market price, 3. self.position 4. supply
        self.brain.add_layer(4)
        self.brain.add_layer(4)
        self.brain.add_layer(4)  # 1. how much to buy or sell as a percent of total cash, 2. buy, 3. sell, 4. price
        self.cash = cash
        self.shares = shares
        self.trading = True
        self.account_values = []
        self.trading_Fee = trading_fee

    def order_expired(self, shares, price, buy: bool):
        if buy:
            self.cash += shares * price
        else:
            self.shares += shares

        self.cash += self.trading_Fee * shares * price

    def partial_fill(self, shares, price, buy: bool):
        if buy:
            self.shares += shares
        else:
            self.cash += shares * price

    def trade(self, supply: int, order_book: OrderBook, price_history: list):
        trade = self.brain.fire_network([self.cash, order_book.price, self.shares, supply])
        buy = trade[1] > trade[2]
        price = order_book.price + .01 if trade[3] >= .5 else order_book.price - .01  # proportional to distance from .5
        shares = int((trade[0] * self.cash) / price) if buy else int(trade[0] * self.shares)
        if not buy:
            if shares > self.shares:
                shares = self.shares

        # subtract trading fee
        fee = self.trading_Fee * shares * price
        if fee < self.cash:
            if buy:
                self.cash -= shares * price
            else:

                self.shares -= shares

            self.cash -= fee
            return Order(self.id, price, shares, buy)


