python2 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/lora_dyn_node.py $* > ./phy_node.log 2>&1 &
sleep 5
python3 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/advanced_test/udp_node_less_param.py > ./up_node.log 2>&1
