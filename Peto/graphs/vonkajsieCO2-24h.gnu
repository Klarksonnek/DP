# http://gnuplot.sourceforge.net/docs_4.2/node274.html
# https://www.techrepublic.com/blog/linux-and-open-source/how-to-handle-time-based-data-with-gnuplot/
# https://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# http://gnuplot.sourceforge.net/demo_4.4/key.html

stats 'vonkajsieCO2-24h.csv' using 1:2

set ylabel 'CO2 [ppm]'
set xlabel 'time [s]'

set xdata time
set timefmt "%s"
set xtics format "%d/%m\n%H:%M"
set xtics 1527847203, 14400, 1527933598
set grid


set key out vert
set key left top
set key center top

# set terminal png size 400, 300
# set output 'vonkajsieCO2-24h.png'

set term eps size 4.5,2 enhanced color linewidth 2
set output 'vonkajsieCO2-24h.eps'

plot [1527847203:1527933598][350:500]'vonkajsieCO2-24h.csv' using 1:2 title "Vonkajšia koncentrácia CO2" with lines, \
            'vonkajsieCO2-24h.csv' using 1:(434) title "Priemerná koncentrácia CO2" with lines
