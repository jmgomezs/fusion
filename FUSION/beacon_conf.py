## 
## Beacon local configuration file, python-only
## 
## Version 2.0
##

##
## The name of the station. It is recommended that each station has a unique name.
##
station="SVA"

##
## Directorio para guardar toda la data. 
##
datadir = "/home/jmgomezs/Documents/FUSION/data"
#
# UHD device arguments. 
#
uhd_device_address = "addr=192.168.10.2,recv_buff_size=100000000"
#
# UHD subdevice string.
# los 2 canales del USRP
uhd_subdev_string = "A:RX1 A:RX2"
 
#
# Receiver sample clock. 
# usrp2/n210 100Mhz
uhd_refclock = 100000000

#
# Integration and decimation window length. 
# Deberia ser la decimacion de la tvrx2
# This results in 1 MHz bandwidth on usrp2/n210
uhd_decimation = "100"

#
# Receiver gain on channel 1 (150 MHz)
#
uhd_gain0 = 0
# Receiver gain on channel 2 (400 MHz)
uhd_gain1 = 30 # 400Mhz se atenua mucho mas, 20log(400)

#
# Offset of the 150 MHz channel. 
#
# This should be 0 in an ideal world, but
# the tvrx2 has a tuning error and with a TVRX2 + USRP N200 combination, 
# it results in these offsets
uhd_rx_offset0 = 0.70710994574392038725

# offset of the 400 MHz channel 
# TVRX2 400 MHz offset
uhd_rx_offset1 = 24.32312035473312405998

#
# Station latitude and longitude
# Coordenadas de la Estacion Receptora
station_latitude = 78.148
station_longitude = 16.043

# Station altitude (meters from sea level)
station_elevation = 520.0

# lowest elevation to measure, elevacion minima en grados, apara jicarmarca podria ser 30
station_threshold_elevation = 10.0

# Delete 40 kHz raw baseband binary files after phase curve analysis. 
# This saves a lot of disk space, but on the other hand reanalysis 
# is impossible without the raw data files. 
#Podriamos activarlo para ver la rawdata
keep_raw_files = False
raw_file_max_age_days=20.0
 
# if you want to / need to use proxy for accessing web, modify this:
# proxies = {'http': 'http://wwwproxy.fmi.fi:8080'}
proxies = None

# minimum duration
min_duration = 60.0

# InterrupThrottle=0 fix for e1000e to reduce number of dropped packets.
intel_ethernet_fix = True

use_measured_freq_offset = True
