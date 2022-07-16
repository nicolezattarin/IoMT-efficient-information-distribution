echo insert distance
read dist
for nodes in {4..20}
do
    echo "parsing simulation for nodes=$nodes"
    python3.8 flowmon-parse-results.py results/lena_${nodes}nodes_${dist}dist.xml
done
