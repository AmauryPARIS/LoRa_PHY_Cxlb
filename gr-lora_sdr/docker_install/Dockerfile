FROM m1mbert/cxlb-gnuradio-3.7:1.0 

WORKDIR /root

# lora_phy_cxlb.git
RUN git clone https://github.com/AmauryPARIS/LoRa_PHY_Cxlb.git LoRa_PHY_Cxlb.git ;
RUN cd /root/LoRa_PHY_Cxlb.git ; git pull ; git checkout stable


# build module
RUN chmod +x  /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/docker_install/build.sh ; /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/docker_install/build.sh 

# the container's default executable: ssh daemon
CMD [ "/usr/sbin/sshd", "-p", "2222", "-D" ]


