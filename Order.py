class Order:
    def __init__(self, id: int, price: float, shares: int, buy: bool):
        self.trader = id
        self.price = price
        self.shares = shares
        self.buy = buy
        self.executed = False
        self.life = 100

    def partial_fill(self, shares, price, trader):
        self.shares -= shares
        trader.partial_fill(shares, price, self.buy)

        if self.shares == 0:
            self.executed = True

