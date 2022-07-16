cd ns-allinone-3.36.1/ns-3.36.1
for nodes in {4..20}
do
    echo "Running simulation for nodes=$nodes"
    ./ns3 run "scratch/lena-simple-epc.cc --numNodePairs=$nodes"
done
cd ../../
