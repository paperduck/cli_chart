#from copy import deepcopy
from datetime import(
    datetime
)
import math

# config
min_chart_width = 10
min_chart_height = 10
chart_width     = 24
chart_height    = 15
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
    """
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
    # validation
    if not min_price: print('failed to find  min price'); return
    if not max_price: print('failed to find  min price'); return
    if not start:     print('failed to find  start');     return
    if not end:       print('failed to find  end');       return
    # aggregate data into candles and add to chart
    chart = []
    datum_i = 0
    for c in range(0, chart_width):
        # (cols > data): Rather than trying to streth candles evenly, just keep the chart small
        # (data > cols): add points to a col until ppc met (compress data)
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
        #print('datum_i:{}     avg:{}      val_i:{}'.format(datum_i, avg, val_i))
        col = [chart_bg]*chart_height
        col[val_i] = candle_body 
        chart.append(col)
    """
    for i in range(0,len(ts)): # for each entry in time series
        avg = float(0) # avg of points in current candle
        points_added = 0
        while points_added < ppc:
            avg += ts[i][1]
            points_added += 1
        avg   /= ppc # average
        candle  = [chart_bg]*chart_height
        if   avg == min_price:   price_i = chart_height - 1
        elif avg == max_price: price_i = 0
        else:
            price_i = (avg - min_price)/(max_price - min_price) # 0 to 1 percentage
            price_i *= chart_height # scale
            price_i = int(chart_height - price_i)  # flip
        candle[price_i] = candle_body
        for r in range(0,candle_width):
            chart.append(candle)
            #TODO: didn't I need to shrink points from last candle or something?
    """

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



