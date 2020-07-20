#from copy import deepcopy
from datetime import(
    datetime
)
import math

# config
chart_width     = 39
chart_height    = 10
chart_bg        = '.'
label_bg        = ' '
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
    # aggregate data into candles and add to chart
    chart = [[]] # one for the y-labels
    for i in range(0,len(ts)): # for each entry in time series
        price = float(0) # avg of points in current candle
        points_added = 0
        while points_added < ppc:
            price += ts[i][1]
            points_added += 1
        price   /= ppc # average
        candle  = [chart_bg]*chart_height
        if   price == min_price:   price_i = chart_height - 1
        elif price == max_price: price_i = 0
        else:
            price_i = (price - min_price)/(max_price - min_price) # 0 to 1 percentage
            price_i *= chart_height # scale
            price_i = int(chart_height - price_i)  # flip
        candle[price_i] = candle_body
        for r in range(0,candle_width):
            chart.append(candle)
            #TODO: didn't I need to shrink points from last candle or something?
    # y axis labels - one candle at the left
    y_labels = [label_bg]*chart_height
    y_labels[0] = str(max_price) + label_bg
    y_labels[chart_height-1] = str(min_price) + label_bg
    y_labels_width = max( len(y_labels[0]), len(y_labels[chart_height-1]) )
    y_labels_width = min(y_labels_width, 10) # hard-coded max
    for z in range(0, chart_height): # justify labels
        y_labels[z] = y_labels[z].ljust(y_labels_width)
        #y_labels[z] = y_labels[z][:y_labels_width-1] # trim
    chart[0] = y_labels
    # print main chart
    for y in range(0, len(chart[0])):
        for x in range(0, len(chart)):
            print(chart[x][y], end='')
        print()
    # x axis labels - make one row for each label,
    x_labels = []

    row = [label_bg]*y_labels_width + list(str(start))
    while len(row) < len(chart) + y_labels_width - 1: row += label_bg
    x_labels.append(row)

    row = str(end).rjust( y_labels_width + len(chart) )
    x_labels.append(row)

    for row in range(0, len(x_labels)):
        for col in range(0, len(x_labels[0])):
            print( x_labels[row][col], end='')
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



