#!/bin/bash

cloud_name=$1
user=$2
pass=$3

echo "Compressing fit/evolutio/individuals folder"
tar -czvf fit_map_$cloud_name.tar.gz ./fit_map
tar -czvf evolution_$cloud_name.tar.gz ./evolution
tar -czvf individuals_$cloud_name.tar.gz ./individuals
tar -czvf results_$cloud_name.tar.gz ./results

echo "Making folders in the cloud"
megamkdir /Root/results/fit_map --username $user --password $pass
megamkdir /Root/results/evolution --username $user --password $pass
megamkdir /Root/results/individuals --username $user --password $pass
megamkdir /Root/results/results --username $user --password $pass

echo "Copying files to the cloud"
megaput --path /Root/results/fit_map fit_map_$cloud_name.tar.gz --username $user --password $pass
megaput --path /Root/results/evolution evolution_$cloud_name.tar.gz --username $user --password $pass
megaput --path /Root/results/individuals individuals_$cloud_name.tar.gz --username $user --password $pass
megaput --path /Root/results/results results_$cloud_name.tar.gz --username $user --password $pass
