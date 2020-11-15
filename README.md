# LOw Cost CO2 data logger (LOCCO2)
Low Cost CO2 data logger

## Description
This project aims to deploy a LOW COST data logger to get CO2 concentration, which indicates the air quality and prevents from poor ventilation. This also may help to control the ventilation in order to prevent COVID-19 infections.

## Components & Prices
- Raspberry Pi 2-3-4 [<a href="https://es.aliexpress.com/item/32838484861.html">~30€</a>]
- MHZ-19 CO2 sensor (infrarred) [<a href="https://es.aliexpress.com/item/4000212024923.html">~14€</a>]
- RGB 4-pin LED [<a href="https://es.aliexpress.com/item/32950269694.html">~0.20€</a>]
- Micro SD [<a href="https://es.aliexpress.com/item/32855791603.html">~5€</a>]

TOTAL = ~ 50 €

## Circuit design
<img src="https://i.ibb.co/71qdGsc/Sin-nombre.png" alt="Raspberry Pi 2 circuit" style="margin-right: 25px" height=600>











## Requirements
You need to config also co2.service and locate it in the proper place (Example, in ubuntu, /etc/systemd/system/co2.service) and initiate it with journalctl.
ExecStart=/path/to/check_co2.py - Need to point to the path where check_co2.py file is.

This data logger has been created to store the data both local and remotelly (if you have an external server). Locally, the records are stored in co2.db. Remotely, you can configure your MySQL server (or any other, but some code need to be changed). 

```bash
apt-get install python3 sqlite3
pip install requirements.txt
systemctl enable co2.service
```

Feel free to contribute!!

## Color code
The concentration of CO2 should not be higher than ~ 750 ppm - 850 ppm (but it depends on the reference). To check if the concentration is OK, colors of the LED should be BLUE, CYAN or GREEN. YELLOW, MAGENTA and RED indicate poor air quality. This is the defined palette:

- co2 < 400: BLUE
- co2 >= 400 and co2 < 700: CYAN
- co2 >= 700 and co2 < 850: GREEN
- co2 >= 850 and co2 < 1500: YELLOW
- co2 >= 1500 and co2 < 1750: MAGENTA
- co2 >= 1750 and co2 < 5500: RED

## References

- https://pypi.org/project/mh-z19/
- https://www.instructables.com/Using-a-RPi-to-Control-an-RGB-LED/

## Cite
DOI: 10.5281/zenodo.4274924

