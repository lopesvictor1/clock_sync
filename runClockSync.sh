#!/bin/bash

outFile="CLOCK_SYNC.out"

N=30
echo "#exec s1_normal s1_noclocksync.txt s1_delay s2_normal s2_noclocksync.txt s2_delay s3_normal s3_noclocksync.txt s3_delay controller" >> outFile

for((i = 0; i < $N; i++)); do
	#execute
	sudo python orquestrador.py -m clock_on
	sudo python orquestrador.py -m clock_off
	#sudo python3 orquestrador.py -m delay #delay ainda nao funciona, como disse

	#get output
	s1c=$(tail -n 1 switch1_normal.txt | grep -Po "(?<=Local time:\s)\d+")
	s1nc=$(tail -n 1 switch1_noclocksync.txt | grep -Po "(?<=Local time:\s)\d+")
	s1d="NaN" #s1d==$(tail -n 1 switch1_delay.txt | grep -Po "(?<=Local time:\s)\d+") #delay ainda nao funciona, como disse

	s2c=$(tail -n 1 switch2_normal.txt | grep -Po "(?<=Local time:\s)\d+")
	s2nc=$(tail -n 1 switch2_noclocksync.txt | grep -Po "(?<=Local time:\s)\d+")
	s2d="NaN" #s1d==$(tail -n 1 switch2_delay.txt | grep -Po "(?<=Local time:\s)\d+") #delay ainda nao funciona, como disse

	s3c=$(tail -n 1 switch3_normal.txt | grep -Po "(?<=Local time:\s)\d+")
	s3nc=$(tail -n 1 switch3_noclocksync.txt | grep -Po "(?<=Local time:\s)\d+")
	s3d="NaN" #s1d==$(tail -n 1 switch3_delay.txt | grep -Po "(?<=Local time:\s)\d+") #delay ainda nao funciona, como disse

	controller=$(tail -n 1 controlador.txt | grep -Po "(?<=Local time:\s)\d+")
		
	echo $(i+1) $s1c $s1nc $s1d $s2c $s2nc $s2d $s3c $s3nc $s3d $controller >> outFile
done


#------------------------------------------------------------------------------------------------
#OBS.:
	#1. Inserir numero para diferenciar switch_delay, isto é: switch1_delay, switch2_delay, ...
	#2. Mudar nome de 'normal' para 'clock_on', se possível.
	#3. Rodar o código com permissão de 'sudo'
#------------------------------------------------------------------------------------------------