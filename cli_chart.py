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
label_bg        = '░'  #█
candle_default  = '─'
candle_bg       = '|'
candle_open     = '┤'
candle_high     = '|'
candle_low      = '|'
candle_close    = '├'
candle_open_close = '┼'
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
    elif len(ts_unsorted) < chart_width:
        print('insufficient ticks ({}) for chart width of ({})'.format(len(ts_unsorted), chart_width))
    # determine format of time series
    elif len( ts_unsorted[0][1] ) == 1:
        print ('SINGLE')
        show_single(ts_unsorted)
    elif len( ts_unsorted[0][1] ) == 4:
        print ('OHLC')
        show_ohlc(ts_unsorted)
    else:
        print ('UNKNOWN')

    
def show_single(ts_unsorted):
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
            candle[row_i] = candle_default
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
    # spans
    start = ts[0][0]
    end   = ts[len(ts)-1][0]
    y_max = ts[0][1][1] # initialize to first high
    y_min = ts[0][1][2] # initialize to first low
    for p in ts:
        y_max = max( p[1][1], y_max ) # max high
        y_min = min( p[1][2], y_min ) # min low
    # plot
    col_i     = 0   # current ascii chart column index
    ts_i      = 0
    col_span  = (end-start)/chart_width
    chart     = []
    avg       = [float(0)]*4
    num_vals_in_avg = 0
    first_open = None # first within candle
    highest = None
    lowest = None
    for tick in ts:
        print(tick[1])
        # if cur date < next threshold
        if tick[0] <= ts[0][0] + ((col_i+1) * col_span):
            if not first_open:  first_open = tick[1][0]
            if highest: highest = max(highest, tick[1][1])
            else:       highest = tick[1][1]
            if lowest:  lowest  = min(lowest, tick[1][2])
            else:       lowest  = tick[1][2]
        else:
            final_close         = tick[1][3] # final within candle
            # filled one ascii col; append to chart
            candle = [chart_bg]*chart_height            
            # calculate row index for each OHLC
            if   first_open == y_min:   open_i = int(0); 
            elif first_open == y_max:   open_i = int(chart_height - 1)
            else:
                open_i = float( (first_open - y_min) / (y_max - y_min) )  # percent: 0 to 100
                open_i *= chart_height  # scale: 0 to chart_height
                open_i = int(open_i)    # floor
            if   highest == y_min:       high_i = int(0)
            elif highest == y_max:       high_i = int(chart_height - 1)
            else:
                high_i  = float( (highest - y_min) / (y_max - y_min) )  # percent: 0 to 100
                high_i  *= chart_height  # scale: 0 to chart_height
                high_i  = int(high_i)    # floor
            if   lowest == y_min:        low_i = int(0)
            elif lowest == y_max:        low_i = int(chart_height - 1)
            else:
                low_i  = float( (lowest - y_min) / (y_max - y_min) )  # percent: 0 to 100
                low_i  *= chart_height  # scale: 0 to chart_height
                low_i  = int(low_i)    # floor
            if   final_close == y_min:   close_i = int(0); 
            elif final_close == y_max:   close_i = int(chart_height - 1)
            else:
                close_i = float( (final_close - y_min) / (y_max - y_min) )  # percent: 0 to 100
                close_i *= chart_height  # scale: 0 to chart_height
                close_i = int(close_i)    # floor
            # draw candle
            for row_i in range(low_i, high_i+1):
                candle[row_i] = candle_bg
            candle[high_i]  = candle_high
            candle[low_i]   = candle_low

            print('open/close: {:5d} --> {:5d}    row_i: {:5d} --> {:5d}'.format(
                first_open, final_close, open_i, close_i))
            #print(tick)

            if open_i == close_i:
                candle[open_i] = candle_open_close
            else:
                candle[open_i]  = candle_open
                candle[close_i] = candle_close
            # add to chart
            chart.append(candle)
            # increment + continue
            col_i     += 1
            first_open = None
            highest = None
            lowest = None

    # y axis labels - one candle at the left
    y_labels            = [label_bg]*chart_height
    y_labels[0]         = str(y_max) + label_bg
    y_labels[chart_height-1] = str(y_min) + label_bg
    y_labels_width      = max( len(y_labels[0]), len(y_labels[chart_height-1]) ) # get widest label
    y_labels_width      = min(y_labels_width, 10) # width threshold
    for z in range(0, chart_height): # justify labels
        y_labels[z]     = y_labels[z].ljust(y_labels_width, label_bg)
        y_labels[z]     = y_labels[z][:y_labels_width-1] # trim
        y_labels[z]     += label_bg
    chart = [y_labels] + chart # append to left of chart

    # print main chart
    for y in range(0, len(chart[0])):
        for x in range(0, len(chart)):
            print(chart[x][y], end='')
        print()

    # x axis labels - make one row for each label,
    x_labels = []

    total_width = y_labels_width + len(chart)
    # starting timestamp
    row = [label_bg]*y_labels_width + list(str(start))
    while len(row) < total_width - 1: row += label_bg
    x_labels.append(row[:total_width-1])
    # ending timestamp
    row = str(end).rjust( total_width-1, label_bg )
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
