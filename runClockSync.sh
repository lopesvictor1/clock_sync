#!/bin/bash

outFile="CLOCK_SYNC.out"
rm -rf CLOCK_SYNC.out

N=30
ACURACIA=20 #alfa
PRECISAO=20 #pi

echo "#exec s1_clock_on s1_clock_off s1_delay s2_clock_on s2_clock_off s2_delay s3_clock_on s3_clock_off s3_delay \
controller (s1c-s2c)_prec (s1c-s3c)_prec (s2c-s3c)_prec (s1nc-s2nc)_prec (s1nc-s3nc)_prec (s2nc-s3nc)_prec (s1d-s2d)_prec (s1d-s3d)_prec \
(s2d-s3d)_prec (s1c-s2c)_accur (s1c-s3c)_accur (s2c-s3c)_accur (s1nc-s2nc)_accur (s1nc-s3nc)_accur (s2nc-s3nc)_accur \
(s1d-s2d)_accur (s1d-s3d)_accur (s2d-s3d)_accur" >> $outFile

for((i = 0; i < $N; i++)); do
	#execute
	sudo python3 orquestrador.py -m clock_on
	sudo python3 orquestrador.py -m clock_off
	sudo python3 orquestrador.py -m delay #delay ainda nao funciona, como disse

	#get output
	s1c=$(tail -n 1 switch1_clock_on.txt | grep -Po "(?<=Local time:\s)\d+")
	s1nc=$(tail -n 1 switch1_clock_off.txt | grep -Po "(?<=Local time:\s)\d+")
	s1d=$(tail -n 1 switch1_delay.txt | grep -Po "(?<=Local time:\s)\d+") 

	s2c=$(tail -n 1 switch2_clock_on.txt | grep -Po "(?<=Local time:\s)\d+")
	s2nc=$(tail -n 1 switch2_clock_off.txt | grep -Po "(?<=Local time:\s)\d+")
	s2d=$(tail -n 1 switch2_delay.txt | grep -Po "(?<=Local time:\s)\d+") 

	s3c=$(tail -n 1 switch3_clock_on.txt | grep -Po "(?<=Local time:\s)\d+")
	s3nc=$(tail -n 1 switch3_clock_off.txt | grep -Po "(?<=Local time:\s)\d+")
	s3d=$(tail -n 1 switch3_delay.txt | grep -Po "(?<=Local time:\s)\d+") 

	controller=$(tail -n 1 controlador.txt | grep -Po "(?<=Local time:\s)\d+")
	echo $(($i+1)) $s1c $s1nc $s1d $s2c $s2nc $s2d $s3c $s3nc $s3d $controller
	echo $(($i+1)) $s1c $s1nc $s1d $s2c $s2nc $s2d $s3c $s3nc $s3d $controller >> $outFile
done

avg=$(awk -v s1c=0 -v s1nc=0 -v s1d=0 -v s2c=0 -v s2nc=0 -v s2d=0 -v s3c=0 -v s3nc=0 -v s3d=0 -v controlador=0 -v prec=$PRECISAO -v accur=$ACURACIA -v exec=$N \
'function abs(x){return ((x < 0.0) ? -x : x)} {s1c+=$2; s1nc+=$3; s1d+=$4; s2c+=$5; s2nc+=$6; s2d+=$7; s3c+=$8; \
s3nc+=$9; s3d+=$10; controlador+=$11; count+=1} END {print exec,s1c/count,s1nc/count,s1d/count,s2c/count,s2nc/count,\
s2d/count,s3c/count,s3nc/count,s3d/count,controlador/count,abs(s1c/count-s2c/count),abs(s1c/count-s3c/count),abs(s2c/count-s3c/count),abs(s1nc/count-s2nc/count),\
abs(s1nc/count-s3nc/count),abs(s2nc/count-s3nc/count),abs(s1d/count-s2d/count),abs(s1d/count-s3d/count),abs(s2d/count-s3d/count),abs(s1c/count-controlador/count),abs(s2c/count-controlador/count),abs(s3c/count-controlador/count),\
abs(s1nc/count-controlador/count),abs(s2nc/count-controlador/count),abs(s3nc/count-controlador/count),abs(s1d/count-controlador/count),abs(s2d/count-controlador/count),abs(s3d/count-controlador/count),
prec,accur}' CLOCK\_SYNC\.out)

echo $avg >> $outFile