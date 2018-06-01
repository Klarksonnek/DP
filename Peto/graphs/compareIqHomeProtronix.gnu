# http://gnuplot.sourceforge.net/docs_4.2/node274.html
# https://www.techrepublic.com/blog/linux-and-open-source/how-to-handle-time-based-data-with-gnuplot/
# https://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# http://gnuplot.sourceforge.net/demo_4.4/key.html

stats 'iqHome.csv' using 1:2
stats 'protronix.csv' using 1:2

set ylabel 'CO2 [ppm]'
set xlabel 'time [s]'

set xdata time
set timefmt "%s"
set xtics format "%H:%M"
set xtics 1525495804, 600, 1525499387
set grid


set key out vert
set key left top
set key center top

# set terminal png size 1000, 300
# set output 'compareIqHomeProtronix.png'

set term eps size 3.6,2 enhanced color linewidth 2
set output 'compareIqHomeProtronix.eps'

plot [1525495804:1525499387][400:2000]'iqHome.csv' using 1:2 title "IQHome CO2" with lines, \
            'protronix.csv' using 1:2 title "Protronix CO2" with lines
