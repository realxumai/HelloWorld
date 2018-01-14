# -*- coding: utf-8 -*-
import datetime

from gmsdk.api import StrategyBase


class Mystrategy(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(Mystrategy, self).__init__(*args, **kwargs)
        #持仓记录
        self.myPosition = []
        #日线数据记录
        self.day_records = []
        #当日操作[日期,买，卖]
        self.oneDayOpt = [0, 0, 0]
        #1111

    def on_bar(self, bar):
        day = [bar.strtime.split('T')[0], bar.open, bar.close]
        self.day_records.append(day)
        print('bar_date: %s open: %s close: %s' % (bar.strtime.split('T')[0], bar.open, bar.close))            

    def on_tick(self, tick):
        t_day = tick.strtime.split('T')[0]
        if self.oneDayOpt != day[-2:]:
            self.oneDayOpt[0] = day[-2:]
            self.oneDayOpt[1] = 0
            self.oneDayOpt[2] = 0
        bid_quantity = Mystrategy.check_price(self, tick.last_price)
        if bid_quantity > 0:
            #bid *****
    def bidStock(self, tick, bid_quantity,today):
        self.open_long(tick.exchange, tick.sec_id, tick.last_price, bid_quantity)
        print("OpenLong: day %s, sec_id %s, price %s, quantity %s" %
                (today, tick.sec_id, tick.last_price, bid_quantity))

    def check_price(self, last_price):
        '''检查N日前价格.'''
        try:
            if self.day_records[-1]:
                day = self.day_records[-1]
                if (last_price - day[2]) / day[2] < -0.06 :
                    return 5000
        except: 
            return 0   
        try:
            if self.day_records[-2]:
                day = self.day_records[-2]
                if (last_price - day[2]) / day[2] < -0.06 :
                    return 5000
        except: 
            return 0 
        try:
            if self.day_records[-3]:
                day = self.day_records[-3]
                if (last_price - day[2]) / day[2] < -0.06 :
                    return 5000
        except: 
            return 0 
        try:
            if self.day_records[-4]:
                day = self.day_records[-4]
                if (last_price - day[2]) / day[2] < -0.06 :
                    return 5000
        except: 
            return 0 
        try:
            if self.day_records[-5]:
                day = self.day_records[-5]
                if (last_price - day[2]) / day[2] < -0.06 :
                    return 5000
        except: 
            return 0                                      
    

if __name__ == '__main__':
    myStrategy = Mystrategy(
        username='18186948121',
        password='cciikk999',
        strategy_id='598a0230-f380-11e7-8131-bc5ff468ef2f',
        subscribe_symbols='SZSE.002415.tick,SZSE.002415.bar.daily',
        mode=4,
        td_addr=''
    )
    myStrategy.backtest_config(
        start_time='2017-01-01 08:00:00',
        end_time='2018-01-01 08:00:00',
        initial_cash=1000000,
        transaction_ratio=1,
        commission_ratio=0.00025,
        slippage_ratio=0.0,
        price_type=1)
    ret = myStrategy.run()
    print('exit code: ', ret)
