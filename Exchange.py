from Market import Market

num_traders = 6
starting_price = 1
num_turns = 150
starting_cash = 5000
initial_supply = 10000
order_difference_tolerance = .2  # allow 10% difference between orders
trading_fee = 0.0025  # .25%

market = Market(num_traders, starting_price, starting_cash, initial_supply, order_difference_tolerance, trading_fee)
market.open_market(num_turns)
market.close_market()

ending_price = market.order_book.price
print(f"initial market cap: ${initial_supply * starting_price}"
      f"\tending market cap: ${int(initial_supply * ending_price)}"
      f"\tcurrent market price: ${ending_price}")
