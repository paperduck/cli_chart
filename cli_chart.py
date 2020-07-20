#from copy import deepcopy
from datetime import(
    datetime
)
import math

# config
chart_width     = 40
chart_height    = 10
chart_bg        = '.'
candle_body     = 'O'
border_top      = '-'
border_sides    = '|'
draw_border     = False


def show(ts):
    """
    ts (time series) = [ [dt, int],  ]
    Generate each candle as a vertical slice of the chart, then append them
    and print.

    case: points < chart_width
        candles become wide, without surpassing chart_width
        ex) 3 points, width=10
            ppc          = floor(3/10) = 0 -> 1
            candle_width = 
        ex) 6 points, width=10
            ppc         = floor(6/10) = 0 -> 1
            cand wid    = 

    case: points == chart_width
        ex) 4 points, chart_width = 4 
            ppc         = 2/4 = 0 -> 1
            cand wid    = 4/4 = 0 -> 1
        ex) 

    case: points > chart width
        ex) 10 points, width=5
            pts/cand    = floor(points/chart_width) (+1 if rem) = 2+0
            num_cand    = chrt_wid / ppc    = 
            cand wid    = chrt_wid / pts    = 5/10  = 0 (min 1) -> 1
        ex) 11 pts, chart width = 2
            pts/can     = pts/width = flr(11/2) (+1 if rem)  = 5+1 for all but last candle
            num cand    = 2/5       = 
            cand width  = 2/11      = 0     -> 1
    """
    # points per candle (ppc)
    ppc             = math.ceil(len(ts)/chart_width)
    candle_width    = math.floor(chart_width/len(ts))
    print('ppc = {}'.format(ppc)) # debugging
    print('candle width = {}'.format(candle_width)) # debugging
    # one sweep to determine min and maxes
    min_price = None
    max_price = None
    start     = None
    end       = None
    for point in ts:
        if not min_price or point[1] < min_price:   min_price = point[1]
        if not max_price or point[1] > max_price:   max_price = point[1]
        if not start     or point[0] < start:       start     = point[0]
        if not end       or point[0] > end:         end       = point[0]
    print('{} to {}'.format(min_price, max_price))# debugging
    print('{}    to    {}'.format(start,end))#debugging
    # aggregate data into candles and add to chart
    chart = []
    for i in range(0,len(ts)): # for each entry in time series
        price = float(0) # avg of points in current candle
        points_added = 0
        while points_added < ppc:
            price += ts[i][1]
            points_added += 1
        price   /= ppc # average
        candle  = [chart_bg]*chart_height
        if   price == min_price:   price_i = chart_height - 1; print(str(price_i))
        elif price == max_price: price_i = 0; print (0)
        else:
            price_i = (price - min_price)/(max_price - min_price) # 0 to 1 percentage
            price_i *= chart_height # scale
            print('float price_i = {}'.format(price_i)) # debugging
            price_i = int(chart_height - price_i)  # flip
            print('                     int price_i = {}'.format(price_i)) # debugging
        candle[price_i] = candle_body
        for r in range(0,candle_width):
            chart.append(candle)
    # print
    for y in range(0, chart_height):
        for x in range(0, chart_width):
            #print('{},{}'.format(x,y))# debugging
            print(chart[x][y], end='')
        print()
    """
    y axis = min price to max
    x axis = first time to last
    divide prices into chunks
    average price of each chunk
    list of candles (horizontal)
        from each candle, make a vertical list of chars
    for each row of candle:
        for each candle:
            print one char
        line break carriage return
    """



