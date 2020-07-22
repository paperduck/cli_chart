import  cli_chart as cc
from    copy import deepcopy
from    datetime import (
    datetime
    ,timedelta
)
from    math    import (sin)

time_series = []

step  = 0.04
i = 0
n = 100
curval = 0
point = [datetime.strptime('2020-01-01 13:00', '%Y-%m-%d %H:%M'), curval]
while i < n:
    time_series.append(deepcopy(point))
    point[0]    += timedelta(minutes=1)
    curval      += step
    point[1]    = sin(curval)
    i           += 1

cc.show(time_series)


