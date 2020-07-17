from datetime import(
    datetime
)

# config
chart_bg_char       = '.'
chart_width         = 40
chart_height        = 40
candle_body_car     = 'O'
border_top_char     = '-'
border_sides_char   = '|'
draw_border         = False


def show(ts):
    """
    time series = [ [dt, int],  ]

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
    min_price   = None
    max_price   = None
    start       = ts[0][0]
    end         = ts[len(ts)-1][0]
    points_per_candle = int( len(ts)/chart_width )
    for p in ts:
        if not min_price or p[1] < min_price:   min_price = p[1]
        if not max_price or p[1] > max_price:   max_price = p[1]
    print('{}  to  {}'.format(min_price, max_price))
    print('{}  to  {}'.format(start, end))
    # points per candle (ppc) - shrink candles as needed to fit all data points
    rem = len(ts) % chart_width
    ppc = len(ts)/chart_width if rem == 0 else (len(ts)/chart_width)+1
    # aggregate each candle and add to chart
    chart       = []
    candle_i = 0
    avg_price       = 0
    num_price_in_avg = 1
    candle = [chart_bg_char]*chart_height # height of chart, top to bottom string
    for i,p in enumerate(ts):
        print('point {}  candle {}'.format(i, candle_i))
        if i%ppc == 0: # new candle
            candle[3] = avg_price/num_price_in_avg  # add price point to candle
            chart.append(candle)  # add previous candle to chart
            num_price_in_avg = 0
            candle = [chart_bg_char]*chart_height # height of chart, top to bottom string
            avg_price = ts[i][2]
        else: # still aggregating data into a candle
            avg_price += ts[i][2]
            num_price_in_avg += 1
    for candle in chart:
        for p in candle:
            print(p, end='')
        print()
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



