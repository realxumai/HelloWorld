# -*- coding: utf-8 -*-
import datetime

from gmsdk.api import StrategyBase


class Mystrategy(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(Mystrategy, self).__init__(*args, **kwargs)
        #持仓记录
        self.myPositions = []
        #日线数据记录
        self.day_records = []
        #当日操作[日期,买次数，卖次数]
        self.oneDayOpt = [0, 0, 0]

    def checkMyPositions(self, last_price):
        '''检查仓位,若有盈利达标的则启动卖出'''
        if len(self.myPositions) > 0:
            for index in range(len(self.myPositions)):
                myPosition = self.myPositions[index]
                if (last_price - myPosition[1]) / myPosition[1] > 0.1:
                    Mystrategy.offerStock(self, tick, bid_quantity, t_day, index)

    def check_price(self, last_price):
        '''检查N日前价格.'''
        try:
            if self.day_records[-1]:
                day = self.day_records[-1]
                if (last_price - day[2]) / day[2] < -0.06:
                    return 5000
        except:
            return 0
        try:
            if self.day_records[-2]:
                day = self.day_records[-2]
                if (last_price - day[2]) / day[2] < -0.06:
                    return 5000
        except:
            return 0
        try:
            if self.day_records[-3]:
                day = self.day_records[-3]
                if (last_price - day[2]) / day[2] < -0.06:
                    return 5000
        except:
            return 0
        try:
            if self.day_records[-4]:
                day = self.day_records[-4]
                if (last_price - day[2]) / day[2] < -0.06:
                    return 5000
        except:
            return 0
        try:
            if self.day_records[-5]:
                day = self.day_records[-5]
                if (last_price - day[2]) / day[2] < -0.06:
                    return 5000
        except:
            return 0

    def offerStock(self, tick, bid_quantity, today, index):
        '''卖出，记录本日买入次数，更新持仓信息'''
        self.close_long(tick.exchange, tick.sec_id,
                        tick.last_price, offer_quantity)
        print("OpenLong: day %s, sec_id %s, price %s, quantity %s" %
              (today, tick.sec_id, tick.last_price, offer_quantity))
        self.oneDayOpt[2] = 1
        del self.myPositions[index]

    def bidStock(self, tick, bid_quantity, today):
        '''买入，记录本日买入次数，更新持仓信息'''
        self.open_long(tick.exchange, tick.sec_id,
                       tick.last_price, bid_quantity)
        print("OpenLong: day %s, sec_id %s, price %s, quantity %s" %
              (today, tick.sec_id, tick.last_price, bid_quantity))
        self.oneDayOpt[1] = 1
        self.myPositions.append([today, tick.last_price, bid_quantity])

    def on_bar(self, bar):
        day = [bar.strtime.split('T')[0], bar.open, bar.close]
        self.day_records.append(day)
        print('bar_date: %s open: %s close: %s' %
              (bar.strtime.split('T')[0], bar.open, bar.close))

    def on_tick(self, tick):
        t_day = tick.strtime.split('T')[0]
        #如果是新的一天，初始化买卖次数
        if self.oneDayOpt[0] != t_day:
            self.oneDayOpt[0] = t_day
            self.oneDayOpt[1] = 0
            self.oneDayOpt[2] = 0
        #还剩买入次数则去检查买入策略
        if self.oneDayOpt[1] == 0:
            bid_quantity = Mystrategy.check_price(self, tick.last_price)
            if bid_quantity > 0 and self.get_cash().nav > bid_quantity * tick.last_price:
                Mystrategy.bidStock(self, tick, bid_quantity, t_day)
        #还剩卖出次数则去检查卖出策略
        if self.oneDayOpt[2] == 0:
            last_price = tick.last_price
            Mystrategy.checkMyPositions(self, last_price)


if __name__ == '__main__':
    myStrategy = Mystrategy(
        username='18186948121',
        password='cciikk999',
        strategy_id='598a0230-f380-11e7-8131-bc5ff468ef2f',
        subscribe_symbols='SZSE.000895.tick,SZSE.000895.bar.daily',
        mode=4,
        td_addr=''
    )
    myStrategy.backtest_config(
        start_time='2017-11-21 08:00:00',
        end_time='2018-01-15 08:00:00',
        initial_cash=1000000,
        transaction_ratio=1,
        commission_ratio=0.00025,
        slippage_ratio=0.0,
        price_type=1)
    ret = myStrategy.run()
    print('exit code: ', ret)
