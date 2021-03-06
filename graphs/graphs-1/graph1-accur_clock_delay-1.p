set encoding iso_8859_1 
set terminal postscript eps enhanced color butt "Times-Roman" 36
set output 'graph1-accur_clock_delay-1.eps'

set style data histogram
#set xlabel '# de Execucoes' font "Times-Roman,42" 
set ylabel 'Acuracia' font ",42"
set size 1.2, 1.0
set grid ytics
set style histogram cluster gap 1
set style fill pattern border -1
set key right top
#set key outside
unset key
unset xtics
set xtics rotate by -45 scale 0.5 nomirror norangelimit \
('s1d-controlador' -0.25, 's2d-controlador' 0.0, 's3d-controlador' 0.25)

set style line 10 lw 3 ps 2.5 lc rgb "#000000"
set style line 9 lw 3 ps 2.5 lc rgb "#000000"
set style line 8 lw 3 ps 2.5 lc rgb "#000000"
set style line 7 lw 3 ps 2.5 lc rgb "#000000"
set style line 6 lw 3 ps 2.5 lc rgb "#000000" 
set style line 5 lw 3 ps 2.5 lc rgb "#000000" 
set style line 4 lw 3 ps 2.5 lc rgb "#000000" 
set style line 3 lw 3 ps 2.5 lc rgb "#000000" 
set style line 2 lw 3 ps 2.5 lc rgb "#000000" 
set style line 16 lw 3 ps 2.5 lc rgb "#000000" 


plot 'CLOCK_SYNC-1.out' u 27 fs pattern 4 lt -1, \
''                      u 28 fs pattern 2 lt -1, \
''                      u 29 fs pattern 7 lt -1