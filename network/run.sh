#!/bin/bash
echo "##### Simulation Start #####"

if [ ! -d TestResult/ ]
	then
	mkdir TestResult/
fi

if [ ! -d TestResult/test1/ ]
	then
	mkdir TestResult/test1/
fi

if [ ! -d TestResult/test1/traffic-0.1/ ]
	then
	mkdir TestResult/test1/traffic-0.1/
fi

touch ./TestResult/test1/traffic-0.1/result-STAs.dat
file1="./TestResult/test1/traffic-0.1/result-STAs.dat"
echo "#numSta, Throughput(Kbps), ProbSucc(%), ProbLoss(%), avgDelay(Seconds)" > ./TestResult/test1/traffic-0.1/result-STAs.dat 
    
touch ./TestResult/test1/traffic-0.1/mac-STAs-GW-1.txt
file2="./TestResult/test1/traffic-0.1/mac-STAs-GW-1.txt"

for numSta in 4 6 8 10 12 14 16 18 20
do
        echo "trial:1-numSTA:$numSta #"

        if [ ! -d TestResult/test1/traffic-0.1/pcap-sta-$numSta/ ]
        then
            mkdir TestResult/test1/traffic-0.1/pcap-sta-$numSta/
        fi

        touch TestResult/test1/time-record$numSta.txt

        echo "Time: $(date) 0.1 $numSta" >> TestResult/test1/time-record$numSta.txt

    for numSeed in 1 2 3 4 
    do
        echo -ne "$numSeed \r"
        ./waf --run "lorawan-network-sim --nSeed=$numSeed --nDevices=$numSta --nGateways=1 --radius=100 --gatewayRadius=1 --simulationTime=15 --appPeriod=0.1 --file1=$file1 --file2=$file2 --printEDs=true --trial=1"  > ./TestResult/test1/traffic-0.1/pcap-sta-$numSta/record-$numSta.txt 2>&1
    done
done


#done
echo "##### Simulation finish #####"
echo "seinding email..."
echo simulation finish | mail -s Simulator helderhdw@gmail.com

