# -*- encoding: utf-8 -*-
#!/usr/bin/env python
# Beacon satellite receiver 
#
# (c) 2014 Juha Vierinen
#  primero instalar pip \pip install pyephem
# Este es el cmd para conectar al USRP
#LC_ALL="C"; ./beacon -d 100 -e 100000000 -g 0 -G 30 -a addr=192.168.10.2,recv_buff_size=100000000 -r "A:RX1 A:RX2" -o /home/usrp/Documents/ExampleBeacon/beacon20 -s 0.70710994574392038725 -t 24.32312035473312405998 -u 0 > /home/usrp/Documents/ExampleBeacon/beacon20/rout.log 2> /home/usrp/Documents/ExampleBeacon/beacon20/rerr.log

import optparse, os, time, thread, datetime
import subprocess, math
import beacon_conf as c

import beacon_fetchtle
import beacon_predict

#import beacon_phasecurve

def deg2degminsec(x):
    deg = math.floor(x)
    minutes = math.floor(60.0*(x-deg))
    sec = math.floor(3600.0*(x-deg-minutes/60.0))
    coord = "%d:%d:%d"%(int(deg),int(minutes),int(sec))
    print(coord)
    return(coord)

def fetch_ephemeris(state):
    times_to_check = [datetime.datetime.utcfromtimestamp(time.time()),
                      datetime.datetime.utcfromtimestamp(time.time()+3600.0)] #tiempo para revizar 1hora.
    state["last_tle_fetch"]=True
   # for x in range[] , sentencia
    for tnow in times_to_check:
        #   datetime.datetime(2014, 5, 9, 17, 32, 53, 818594)
        date_string = "%04d.%02d.%02d"%(tnow.year,tnow.month,tnow.day) # saca el dia actual, para usarlos en las direcciones
	#2015.09.28
        # fetch new tle files if needed
        if not os.path.exists("%s/%s/beacon.tle"%(c.datadir,date_string)): #revisa las direcciones, con el dia actual
            print("Fetching files")
            os.system("mkdir -p %s/%s"%(c.datadir, date_string))	    # Linea para generar la carpeta
            success = beacon_fetchtle.download_tle_files("%s/%s"%(c.datadir, date_string)) # Linea llama a la funcion para bajar los tle.
            state["last_tle_fetch"]=success 

        if not os.path.exists("%s/%s/passes.txt"%(c.datadir,date_string)):
            print("Predicting passes for %s"%(date_string))		 	#Reviza si existen las predicciones "pasos"
            os.system("mkdir -p %s/%s"%(c.datadir, date_string))		#pasos tiene start_time end_time freq1 (MHz) freq2 (MHz) bw1 (kHz) bw2 (kHz) peak_elevation name
            beacon_predict.write_pass_files(datestr="%04d/%02d/%02d 00:00:00"%(tnow.year,tnow.month,tnow.day),
                                            data_dir="%s/%s"%(c.datadir,date_string),
                                            latitude=deg2degminsec(c.station_latitude),
                                            longitude=deg2degminsec(c.station_longitude),
                                            altitude=c.station_elevation,
                                            sat_elev_cutoff=c.station_threshold_elevation,
                                            year=tnow.year, month=tnow.month, day=tnow.day)# la libreria de ephem requiere estos datos.


def is_recorder_alive(): #Recorder debe ser el USRP
    #cmd = "ps ax |grep \"./beacon -d\"|grep -v grep|awk '{print $1}'"
    cmd = "uhd_find_devices --args addr=192.168.10.2"
    p = os.popen(cmd)
    lines = p.readlines()
    p.close()
    if len(lines) < 1:
        return(False)
    else:
        return(True)



def do_housekeeping(state):
    fetch_ephemeris(state)
    rec_alive = is_recorder_alive()
    # raw_input("Press Enter to cancel...")
    state["rec_alive"]=rec_alive
    p = os.popen("tail -1 %s/rout.log"%(c.datadir))
    last_lines = p.readlines()
    p.close()

    last_an = ""			# check the last analysis 
    if os.path.exists("%s/last_an.txt"%(c.datadir)):
        p = os.popen("cat %s/last_an.txt"%(c.datadir))
        an_lines = p.readlines()
        if len(an_lines) > 0:
            last_an = an_lines[0].strip()
        p.close()

    status_string=""
    if len(last_lines) < 1:
        status_string="not alive"
    else:
        status_string = "%s tle %d recorder alive %d last analyzed %s %s"%(c.station, state["last_tle_fetch"],state["rec_alive"], last_an, last_lines[0].strip())
    print(status_string)
    status_file = file("%s/status.log"%(c.datadir),"w") #write to log, the last status of recorder
    status_file.write(status_string)
    status_file.close()














if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option('-x', '--stop_all', dest='stop_all', action='store_true', help='Stop receiver')
    (op, args) = parser.parse_args()

    state = {}
    do_housekeeping(state)
   # thread.start_new_thread(run_beacon_receiver, ())
   # thread.start_new_thread(run_beacon_calc, ())
   # thread.start_new_thread(cleanup, ())

  #  while True:
  #     do_housekeeping(state)
  #      time.sleep(5)


