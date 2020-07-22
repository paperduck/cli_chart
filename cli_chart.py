#from copy import deepcopy
from datetime import(
    datetime
)
import math

# config
min_chart_width = 10
min_chart_height = 10
chart_width     = 50
chart_height    = 15
chart_bg        = '.'
label_bg        = ' '
candle_body     = 'o'
border_top      = '-'
border_sides    = '|'
draw_border     = False


def show(ts_unsorted):
    """
    ts (time series) = [ [dt, int],  ]
    1. sort time series by date
    2. determine date span per ascii column (end-start)/(num cols)
    3. for each col, avg points in that span --> this is price for that col
       NOTE: 
             for open,  do first
             for high,  do max
             for low,   do min 
             for close, do last
             for mid,   do avg
       determine y range from averages, not source points
       no data in a range --> copy left col
    """
    # sort
    ts = sorted(ts_unsorted, key=lambda p: p[0])
    # range
    start = None
    end = None
    y_min = None
    y_max = None
    for p in ts:
        if not start or p[0] < start:   start = p[0]
        if not end   or p[0] > end:     end   = p[0]
        if not y_min or p[1] < y_min:   y_min = p[1]
        if not y_max or p[1] > y_max:   y_max = p[1]
    assert start==ts[0][0], end==ts[len(ts)-1][0]
    # plot
    col_i = 0   # current ascii chart column index
    ts_i = 0
    col_span = (end-start)/chart_width
    print('col_span = {}'.format(col_span))
    chart = []
    avg = 0
    num_vals_in_avg = 0
    while ts_i < len(ts):
        # if cur date < next threshold
        if ts[ts_i][0] <= ts[0][0] + ((col_i+1) * col_span):
            avg += ts[ts_i][1]
            num_vals_in_avg += 1
        else:
            avg /= num_vals_in_avg
            candle = [chart_bg]*chart_height            
            row_i = float(0) # set type
            if   avg == y_min:  row_i = 0
            elif avg == y_max:  row_i = chart_height - 1
            else:
                row_i = (avg - y_min) / (y_max - y_min)  # percent: 0 to 100
                row_i *= chart_height  # scale: 0 to chart_height
                row_i = int(row_i)
                #row_i = int(chart_height - row_i)  # flip
            candle[row_i] = candle_body

            # debugging: center line
            #if row_i != 0:
                #print('row  {}   col  {}'.format(row_i, col_i))
                #print( '{} = abs({}  -  {})'.format(
                #float( (col_i+1)/(row_i+1) ) - float(chart_width/chart_height)
                #,float( (col_i+1)/(row_i+1) )
                #,float( chart_width/chart_height) 
            #) )
            if row_i==0 or abs(float((col_i+1)/(row_i+1)) - float(chart_width/chart_height)) < 0.13:
                pass#candle[row_i] = 'X'

            chart.append(candle)

            avg = ts[ts_i][1]
            num_vals_in_avg = 1
            col_i += 1
        ts_i += 1
    # last candle
    avg /= num_vals_in_avg
    candle = [chart_bg]*chart_height            
    row_i = float(0) # set type
    if   avg == y_min:  row_i = 0; print('S')
    elif avg == y_max:  row_i = chart_height - 1; print('A')
    else:
        row_i = (avg - y_min) / (y_max - y_min)  # percent: 0 to 100
        row_i *= chart_height  # scale: 0 to chart_height
        row_i = int(row_i)
    candle[row_i] = candle_body
    if row_i==0 or abs(float((col_i+1)/(row_i+1)) - float(chart_width/chart_height)) < 0.13:
        pass#candle[row_i] = 'X'
    chart.append(candle)
    #print
    for y in range(len(chart[0])-1, -1, -1):
        for x in range(0, len(chart)):
            print(chart[x][y], end='')
        print()
    return

    # validation
    if chart_width < min_chart_width:
        print('Chart width must be >= {}'.format(min_chart_width))
        return
    if chart_height < min_chart_height:
        print('Chart height must be >= {}'.format(min_chart_height))
        return
    # points per candle (ppc)
    ppc             = math.ceil(len(ts)/chart_width)
    print('ppc = {}'.format(ppc))
    # one sweep to determine range
    start     = None
    end       = None
    for point in ts:
        if not start     or point[0] < start:       start     = point[0]
        if not end       or point[0] > end:         end       = point[0]
    # aggregate data into candles and add to chart
    chart = []
    datum_i = 0
    for c in range(0, chart_width):
        # (cols > data): Rather than trying to streth candles evenly, just keep the chart small
        # (data > cols): add points to a col until ppc met (compress data)
        print(datum_i)
        if datum_i < len(ts):
            avg = float( 0 )
            avg += ts[datum_i][1]
            datum_i += 1
        else:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
            continue
        while datum_i < len(ts) and datum_i % ppc != 0:
            avg += ts[datum_i][1]
            datum_i += 1
        avg /= ppc
        if   avg == min_price: val_i = chart_height - 1
        elif avg == max_price: val_i = 0
        else:
            val_i = (avg - min_price) / (max_price - min_price)
            val_i *= chart_height
            val_i = int(chart_height - val_i)
        col = [chart_bg]*chart_height
        print('val_i = {}'.format(val_i))
        print('                  avg = {}'.format(avg))
        col[val_i] = candle_body 
        chart.append(col)

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



