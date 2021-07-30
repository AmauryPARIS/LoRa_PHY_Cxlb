sleep 5
ARG1="$1"
shift
python2 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/lora_dyn_node.py "$@" | tee ./phy_node.log 2>&1 &
sleep 7
python3 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/advanced_test/automate/udp_node_less_param.py "$ARG1" | tee ./up_node.log 2>&1
