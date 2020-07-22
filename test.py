import  cli_chart as cc
from    copy import deepcopy
from    datetime import (
    datetime
    ,timedelta
)

time_series = []
point = [datetime.strptime('2020-01-01 13:00', '%Y-%m-%d %H:%M'), 100]
for i in range(0,50):
    time_series.append(deepcopy(point))
    point[0] += timedelta(minutes=1)
    point[1] += 1

cc.show(time_series)


