# LOw Cost CO2 data logger (LOCCO2)
Low Cost CO2 data logger

## Description
This project 

## Components
- Raspberry Pi 2
- MHZ-19 CO2 sensor (infrarred)
- RGB 4-pin LED
- Micro SD
- USB WiFi card (optional)

## Circuit design
<img src="https://i.ibb.co/71qdGsc/Sin-nombre.png" alt="Raspberry Pi 2 circuit" style="margin-right: 25px" height=600>











## Requirements
You need to config also co2.service and locate it in the proper place (Example, in ubuntu, /etc/systemd/system/co2.service) and initiate it with journalctl.


## References
https://pypi.org/project/mh-z19/
https://www.instructables.com/Using-a-RPi-to-Control-an-RGB-LED/
