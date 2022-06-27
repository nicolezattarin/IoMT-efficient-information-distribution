for s in {1..5}
do
    for r in {1..4}
    do
        echo "Running clustering for s=$s, r=$r"
        python3.8 WalkingLying_cluster.py --subject $s --run $r --sensor_type triaxial_acc
        python3.8 WalkingLying_cluster.py --subject $s --run $r --sensor_type IMU_acc
        python3.8 WalkingLying_cluster.py --subject $s --run $r --sensor_type IMU_gyro
        python3.8 WalkingLying_cluster.py --subject $s --run $r --sensor_type IMU_mag
        python3.8 WalkingLying_cluster.py --subject $s --run $r --sensor_type all
    done
done
