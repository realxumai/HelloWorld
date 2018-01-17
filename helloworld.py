﻿# -*- coding: utf-8 -*-
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
        #市值
        self.market_capitalization = 0

    def checkMyPositions(self, last_price, tick):
        '''检查仓位,若有盈利达标的则启动卖出'''
        #市值金额
        cum_trade = self.get_cash().cum_trade
        if len(self.myPositions) > 0:
            #if cum_trade < self.initial_cash * 0.5:
            #超过5成时
            if cum_trade > self.initial_cash * 0.5:   
                #大于5成小于8成   
                if cum_trade < self.initial_cash * 0.8:  
                    offer_quantity =int(((cum_trade-self.initial_cash * 0.5) / last_price) / 100)*100
                    if len(self.myPositions) < 1:
                        x='123'
                    for index in range(len(self.myPositions)):
                        myPosition = self.myPositions[index]
                        if (last_price - myPosition[1]) / myPosition[1] > 0.15:
                            Mystrategy.offerStock(self, tick, offer_quantity, index)
                #大于8成              
                else:   
                    offer_quantity =int(((cum_trade-self.initial_cash * 0.5) / last_price) / 100)*100           
                    for index in range(len(self.myPositions)):
                        myPosition = self.myPositions[index]
                        if (last_price - myPosition[1]) / myPosition[1] > 0.20:
                            Mystrategy.offerStock(self, tick, offer_quantity, index)                            

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
                    return 6000
        except:
            return 0
        try:
            if self.day_records[-4]:
                day = self.day_records[-4]
                if (last_price - day[2]) / day[2] < -0.06:
                    return 7000
        except:
            return 0
        try:
            if self.day_records[-5]:
                day = self.day_records[-5]
                if (last_price - day[2]) / day[2] < -0.06:
                    return 10000
        except:
            return 0
        return 0

    def offerStock(self, tick, offer_quantity, index):
        '''卖出，记录本日买入次数，更新持仓信息'''
        t_day = tick.strtime.split('T')[0]
        self.close_long(tick.exchange, tick.sec_id,
                        tick.last_price, offer_quantity)
        print("CloseLong: day %s, sec_id %s, price %s, quantity %s" %
              (t_day, tick.sec_id, tick.last_price, offer_quantity))
        self.oneDayOpt[2] = 1
        del self.myPositions[index]
        self.market_capitalization = self.market_capitalization - offer_quantity

    def bidStock(self, tick, bid_quantity, today):
        '''买入，记录本日买入次数，更新持仓信息'''
        self.open_long(tick.exchange, tick.sec_id,
                       tick.last_price, bid_quantity)
        print("OpenLong: day %s, sec_id %s, price %s, quantity %s" %
              (today, tick.sec_id, tick.last_price, bid_quantity))
        self.oneDayOpt[1] = 1
        self.myPositions.append([today, tick.last_price, bid_quantity])
        self.market_capitalization = self.market_capitalization + bid_quantity

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
        if  tick.last_price >0:
            #还剩买入次数则去检查买入策略
            if self.oneDayOpt[1] == 0:
                bid_quantity = Mystrategy.check_price(self, tick.last_price)
                x= self.get_cash()
                if bid_quantity > 0 and self.get_cash().available > (bid_quantity * tick.last_price):
                    Mystrategy.bidStock(self, tick, bid_quantity, t_day)
            #还剩卖出次数则去检查卖出策略
            if self.oneDayOpt[2] == 0:
                last_price = tick.last_price
                Mystrategy.checkMyPositions(self, last_price, tick)

if __name__ == '__main__':
    myStrategy = Mystrategy(
        username='18186948121',
        password='cciikk999',
        strategy_id='9bf656aa-fa6b-11e7-b943-00ff0665d720',
        subscribe_symbols='SZSE.000895.tick,SZSE.000895.bar.daily',
        mode=4,
        td_addr=''
    )
    myStrategy.backtest_config(
        start_time='2017-04-25 08:00:00',
        end_time='2018-01-01 08:00:00',
        initial_cash=1000000,
        transaction_ratio=1,
        commission_ratio=0.00025,
        slippage_ratio=0.0,
        price_type=1)
    ret = myStrategy.run()
    print('exit code: ', ret)
