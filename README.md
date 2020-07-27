

# What is this?

This is a no-frills command-line utlity that takes a time series and prints an
ASCII chart to standard output.

# Use Case

If you're working with stock market data, you can use this in your log files
to provide a quick visual reference.

# Usage:

WARNING: You will need to make sure your terminal is able to display extended ASCII. In the future, possibly UTF-8 as well.

See `test.py` for usage examples. 

There are two functions, `single()` and `ohlc()'.  
single() takes a list of datetimes and values, the prints a simple line chart.  
ohlc() is the same except for each datetime it takes four values (open high low close)  
and prints candlesticks.

# Example output

Example single-value line chart (labels haven't been added yet)

    .......░░░░░░....................................                                                                                                                                                                                         
    ......░......░░.................................░                                                                                                                                                                                         
    .....░.........░...............................░.                                                                                                                                                                                         
    ....░...........░.............................░..                                                                                                                                                                                         
    ...░.........................................░...                                                                                                                                                                                         
    .................░...............................                                                                                                                                                                                         
    ..░...............░.........................░....                                                                                                                                                                                         
    .░.................░.......................░.....                                                                                                                                                                                         
    .................................................                                                                                                                                                                                         
    ░...................░.....................░......                                                                                                                                                                                         
    .....................░...................░.......                                                                                                                                                                                         
    .................................................                                                                                                                                                                                         
    ......................░.................░........                                                                                                                                                                                         
    .......................░...............░.........                                                                                                                                                                                         
    ......................................░..........                                                                                                                                                                                         
    ........................░........................                                                                                                                                                                                         
    .........................░...........░...........                                                                                                                                                                                         
    ..........................░.........░............                                                                                                                                                                                         
    ...........................░......░░.............                                                                                                                                                                                         
    ............................░░░░░░...............   

Example candlestick OHLC chart:


    27░░...|.............................................
    ░░░░...|.............................................
    ░░░░..├┤.............................................
    ░░░░.|||.............................................
    ░░░░├┼┤├┤.|........................................├┼
    ░░░░||||├┼┤|..|...................................├┤.
    ░░░░┤...|.├┤|├┤............|......................|..
    ░░░░|...|.||├┤|.........|..||.....................|..
    ░░░░|...|..├┤.├┤.....├┤┼┼┤|├┤..|.|.|..|.........├┼┤..
    ░░░░.......||.|||.├┤├|├||├┤||.|├┤|||..|........||....
    ░░░░........|.|||.||||||||├┤||||├┼┼┤..|........||....
    ░░░░........|..|||||||||||||├┼┼┤|||├┤.├┤|.....├┼┤....
    ░░░░...........├┼┼┤├┤┤.|...|.|.||||||├┤|||....|.|....
    ░░░░............|||.|..|.........|.|├┤|├┼┤....|.|....
    ░░░░..............|.................||.||||..├┤......
    ░░░░..............|......................||..|.......
    ░░░░..............|......................├┤|||.......
    ░░░░.....................................|├┼┼┤.......
    ░░░░......................................|..........
    -27░......................................|..........
    ░░░░2020-12-06 00:00:00░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░2020-12-08 01:00:00




