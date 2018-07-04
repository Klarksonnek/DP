# http://gnuplot.sourceforge.net/docs_4.2/node274.html
# https://www.techrepublic.com/blog/linux-and-open-source/how-to-handle-time-based-data-with-gnuplot/
# https://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# http://gnuplot.sourceforge.net/demo_4.4/key.html

stats 'protronix.csv' using 1:2

set ylabel 'Koncentrácia CO2 [ppm]'
set xlabel 'Čas [s]'

set xdata time
set timefmt "%s"
set xtics format "%H:%M"
set xtics 1525518601, 1800, 1525531200
set grid

#set key out vert
#set key left top
#set key center top

set nokey

set term eps size 4.5,2.5 enhanced color linewidth 2
set output '2ludiaDennaAktivitaCO2.eps'

plot [1525518601:1525531200][400:1200] \
     '2ludiaDennaAktivitaCO2.csv' using 1:2 title "Koncentrácia CO2 (Protronix)" with lines
