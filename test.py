import  cli_chart as cc
from    copy import deepcopy
from    datetime import (
    datetime
    ,timedelta
)
from    math    import (sin)
from random import(randrange)


def single():
    time_series = []
    step  = 0.05
    i = 0
    n = 150
    curval = 0
    point = [datetime.strptime('2020-01-01 13:00', '%Y-%m-%d %H:%M'), [curval]]
    while i < n:
        time_series.append(deepcopy(point))
        point[0]    += timedelta(minutes=1)
        curval      += step
        point[1]    = [sin(curval)]
        i           += 1
    cc.show(time_series)

def ohlc():
    time_series = []
    i = 1
    n = 50
    curval = [10,10,10,10]
    point = [datetime.strptime('2020-12-06 00:00', '%Y-%m-%d %H:%M'), curval]
    while i <= n:
        time_series.append(deepcopy(point))
        point[0] += timedelta(hours=1)
        op = point[1][3] # prev close
        rand_1 = randrange( op, op+11, 1  )   # fluctuate by max of x
        rand_2 = randrange( op, op-11, -1 )   # fluctuate by max of x
        high = max(rand_1, rand_2)
        low  = min(rand_1, rand_2)
        close = randrange(low, high+1)
        point[1] = [op, high, low, close]
        i+=1
        #print(point)
    cc.show(time_series)


ohlc()
#single()
