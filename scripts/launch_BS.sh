python2 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/lora_dyn_node.py $* > ./phy_BS.log 2>&1 &
sleep 5
python3 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/advanced_test/udp_BS_less_param.py > ./up_BS.log 2>&1
