from Agent import Agent
from OrderBook import OrderBook
from Order import Order


class Market:
    def __init__(self,
                 num_traders: int,
                 initial_price: float,
                 starting_cash: int,
                 initial_supply: int,
                 order_difference_tolerance: float,
                 trading_fee: float):
        self.initial_price = initial_price
        self.starting_shares = int(initial_supply / num_traders)
        self.traders = [Agent(trading_fee, self.starting_shares, starting_cash, i) for i in range(num_traders)]
        self.supply = initial_supply
        self.order_book = OrderBook(initial_price, order_difference_tolerance)
        self.price_history = []
        self.starting_cash = starting_cash

    def open_market(self, total_turns: int):
        for i in range(total_turns):
            # close previous rounds trades
            prices = self.order_book.match_trades(self.traders)
            self.price_history.append(prices)

            # open new trades for every trader
            for trader in self.traders:
                order = trader.trade(self.supply, self.order_book, self.price_history)
                if order:
                    self.order_book.add_order(order)
                    trader.account_values.append((self.order_book.price * trader.shares) + trader.cash)

            # purge dead traders
            self.traders = [trader for trader in self.traders if trader.trading]

            # quit if there are no more players
            if len(self.traders) == 0:
                return

    def close_market(self):
        for trader in self.traders:
            begin = trader.account_values[0]
            end = int(trader.account_values[len(trader.account_values) - 1])
            print(f"trader: {trader.id}"
                  f"\tstarting cash: ${self.starting_cash}"
                  f"\tstarting shares: {self.starting_shares}"
                  f"\t\tending cash: ${int(trader.cash)}"
                  f"\t\tending shares: {int(trader.shares)}")

