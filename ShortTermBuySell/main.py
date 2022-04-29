import backtrader as bt
import datetime  # For datetime objects, the timezone is always assumed to be UTC

DATA_PATH = './../data/orcl-1995-2014.txt'

# create a data feed
# yahoo sends data in descending order (newest first)
data = bt.feeds.YahooFinanceCSVData(
    dataname = DATA_PATH,
    # Do not pass values before this date
    fromdate = datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate = datetime.datetime(2000, 12, 31),
    # the data is not in descending order
    reverse = False
)

# create a trading strategy that buys if the price went down twice in a row
class TestStategy(bt.Strategy):
    def log(self, txt, dt = None):
        # dt is the current datetime
        # self.data[0] is the current days data
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            # current close less than previous close

            if self.dataclose[-1] < self.dataclose[-2]:
                # previous close less than the previous close

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()
        elif self.dataclose[0] > self.dataclose[-1]:
            # current close greater than previous close

            if self.dataclose[-1] > self.dataclose[-2]:
                # previous close greater than the previous close

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # check if we are holding a position
                self.sell()


def main():
    cerebro = bt.Cerebro() # creates a broker for the user

    cerebro.addstrategy(TestStategy) # add the strategy to the broker
    
    cerebro.broker.setcash(100000.0) # sets the cash to 100,000

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.adddata(data) # adds the data to the broker
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    main()