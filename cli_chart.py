# -*- coding: utf-8 -*-


#from copy import deepcopy
from datetime import(
    datetime
)
import math

# config
min_chart_width = 10
min_chart_height = 10
chart_width     = 50
chart_height    = 20
chart_bg        = '.'
label_bg        = ''
candle_body     = '─'
border_top      = '-'
border_sides    = '|'
draw_border     = False


def show(ts_unsorted):
    """
    time series (ts) formats
        1-datum   [ [dt, int],  ]
        OHLC      [ [dt, [int, int, int, int] ]
    1. sort time series by date
    2. determine date span per ascii column (end-start)/(num cols)
    3. for each col, avg points in that span --> this is price for that col
       NOTE: 
             for open,  do first
             for high,  do max
             for low,   do min 
             for close, do last
             for mid,   do avg
       determine y range from column data, not source points
       if no data in a span --> copy left col
    """
    # validation
    if len(ts_unsorted) < 1:
        print('empty time series')
        return
    # determine format of time series
    if len(ts_unsorted[0][1] == 4:
        show_ohlc(ts_unsorted)
        return
    # sort
    ts = sorted(ts_unsorted, key=lambda p: p[0])
    # range
    start = None
    end = None
    y_min = None
    y_max = None
    for p in ts:
        if start is None or p[0] < start:   start = p[0]
        if end   is None or p[0] > end:     end   = p[0]
        if y_min is None or p[1] < y_min:   y_min = p[1]
        if y_max is None or p[1] > y_max:   y_max = p[1]
    assert start==ts[0][0], end==ts[len(ts)-1][0]
    # plot
    col_i           = 0   # current ascii chart column index
    ts_i            = 0
    col_span        = (end-start)/chart_width
    chart           = []
    avg             = float(0)
    num_vals_in_avg = 0
    print()
    #while ts_i < len(ts):
    for point in ts:
        # if cur date < next threshold
        if point[0] <= ts[0][0] + ((col_i+1) * col_span):
            avg += point[1]
            num_vals_in_avg += 1
        else:
            # filled one ascii col; append to chart
            avg /= num_vals_in_avg
            candle = [chart_bg]*chart_height            
            if avg == y_min:
                row_i = int(0); 
            elif avg == y_max:
                row_i = int(chart_height - 1)
            else:
                row_i = float( (avg - y_min) / (y_max - y_min) )  # percent: 0 to 100
                row_i *= chart_height  # scale: 0 to chart_height
                row_i = int(row_i)
            candle[row_i] = candle_body
            chart.append(candle)
            avg = point[1]
            num_vals_in_avg = 1
            col_i += 1
    #print
    for y in range(len(chart[0])-1, -1, -1):
        for x in range(0, len(chart)):
            print(chart[x][y], end='')
        print()
    print()
    return

    # y axis labels - one candle at the left
    y_labels = [label_bg]*chart_height
    y_labels[0] = str(max_price) + label_bg
    y_labels[chart_height-1] = str(min_price) + label_bg
    y_labels_width = max( len(y_labels[0]), len(y_labels[chart_height-1]) )
    y_labels_width = min(y_labels_width, 10) # hard-coded max
    for z in range(0, chart_height): # justify labels
        y_labels[z] = y_labels[z].ljust(y_labels_width)
        y_labels[z] = y_labels[z][:y_labels_width-1] # trim
        y_labels[z] += label_bg
    chart = [y_labels] + chart # append to left of chart

    # print main chart
    for y in range(0, len(chart[0])):
        for x in range(0, len(chart)):
            print(chart[x][y], end='')
        print()
    # x axis labels - make one row for each label,
    x_labels = []

    total_width = y_labels_width + len(chart)

    row = [label_bg]*y_labels_width + list(str(start))
    while len(row) < total_width - 1: row += label_bg
    x_labels.append(row[:total_width-1])

    row = str(end).rjust( total_width-1 )
    x_labels.append( row )

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



def show_ohlc(ts_unsorted):
    """
        OHLC      [ [dt, [int, int, int, int] ]
    """
    # sort
    ts = sorted(ts_unsorted, key=lambda p: p[0])
    # range
    start = ts[0][0]
    end   = ts[0][len(ts)-1]
    y_min = ts[0][1][0] # initialize to first value
    y_max = ts[0][1][0] # initialize to first value
    for p in ts:
        y_min = min( p[1][2], y_min ) # min low
        y_max = max( p[1][1], y_max ) # max high
    # plot
    col_i     = 0   # current ascii chart column index
    ts_i      = 0
    col_span  = (end-start)/chart_width
    chart     = []
    avg       = [float(0)]*4
    num_vals_in_avg = 0
    for point in ts:
        # if cur date < next threshold
        if point[0] <= ts[0][0] + ((col_i+1) * col_span):
            avg_o += point[1][0]
            avg_h += point[1][1]
            avg_l += point[1][2]
            avg_c += point[1][3]
            num_vals_in_avg += 1
        else:
            # filled one ascii col; append to chart
            avg /= num_vals_in_avg
            candle = [chart_bg]*chart_height            
            if avg == y_min:
                row_i = int(0); 
            elif avg == y_max:
                row_i = int(chart_height - 1)
            else:
                row_i = float( (avg - y_min) / (y_max - y_min) )  # percent: 0 to 100
                row_i *= chart_height  # scale: 0 to chart_height
                row_i = int(row_i)
            candle[row_i] = candle_body
            chart.append(candle)
            avg = point[1]
            num_vals_in_avg = 1
            col_i += 1
    #print
    for y in range(len(chart[0])-1, -1, -1):
        for x in range(0, len(chart)):
            print(chart[x][y], end='')
        print()
    print()
    return

    # y axis labels - one candle at the left
    y_labels = [label_bg]*chart_height
    y_labels[0] = str(max_price) + label_bg
    y_labels[chart_height-1] = str(min_price) + label_bg
    y_labels_width = max( len(y_labels[0]), len(y_labels[chart_height-1]) )
    y_labels_width = min(y_labels_width, 10) # hard-coded max
    for z in range(0, chart_height): # justify labels
        y_labels[z] = y_labels[z].ljust(y_labels_width)
        y_labels[z] = y_labels[z][:y_labels_width-1] # trim
        y_labels[z] += label_bg
    chart = [y_labels] + chart # append to left of chart

    # print main chart
    for y in range(0, len(chart[0])):
        for x in range(0, len(chart)):
            print(chart[x][y], end='')
        print()
    # x axis labels - make one row for each label,
    x_labels = []

    total_width = y_labels_width + len(chart)

    row = [label_bg]*y_labels_width + list(str(start))
    while len(row) < total_width - 1: row += label_bg
    x_labels.append(row[:total_width-1])

    row = str(end).rjust( total_width-1 )
    x_labels.append( row )

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
