#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
	agregar el Encoding, porque habia un caracter no reconocido T____T   
	Read beacon satellite TLEs from NORAD and search for satellites.
   output a beacon.tle format. 
	TLE = A two-line element set (TLE) is a data format encoding a list of orbital elements of an Earth-orbiting object for a given 	point in time.NORAD es el acrónimo de North American Aerospace Defense Command (Mando Norteamericano de Defensa Aeroespacial). 		NORAD provee comunicación global, detección, validación y alerta de posibles ataques de misiles balísticos hacia Norteamérica, abarcando 	detección continental; también provee alerta temprana en tiempo de paz en caso de que el espacio aéreo esté comprometido

   Usage: ./get_beacontle.py /data/beacon/data/2011.06.28/

   (c) 2010 Juha Vierinen
"""
import urllib, re
import os, errno, sys
#The urllib module provides a simple interface for network resource access. Although urllib can be used with gopher and ftp.
#Searching within and changing text using formal pattern
#The errno module defines a number of symbolic error codes
#proxies = {'http': 'http://wwwproxy.fmi.fi:8080'}
proxies = None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def goto_dir(startd):
    # the start date in pyephem format: 
    dtuple = startd.tuple() # tupla = lista ordenada de elementos
    dirname = "%04d.%02d.%02d" % (dtuple[0],dtuple[1],dtuple[2])
    mkdir_p(dirname)
    os.chdir(dirname) #The method chdir() changes the current working directory to the given path.It returns None in all the cases. 

# list of beacon satellites and their frequencies.
class satellitelist:
    def __init__(self, fname):
        self.satnames = []
        self.offsets = []
        
        f = open(fname, 'r')
        data = f.readlines()
        f.close()
        
        for i in range(0,len(data)):
            (sn,of) = data[i].split(",") # lee los datos separados por comas d cada satelite
            self.satnames.append(sn.strip())
            self.offsets.append(float(of))


def writeBeaconsTLE(fname,sl):
    f = open(fname, 'w')
    #
    # Read all relevant files fron celestrak
    #
    a = None
    try:
        a = urllib.urlopen('http://celestrak.com/NORAD/elements/musson.txt',proxies=proxies).readlines()
        a = a + urllib.urlopen('http://celestrak.com/NORAD/elements/science.txt',proxies=proxies).readlines()
        a = a + urllib.urlopen('http://celestrak.com/NORAD/elements/military.txt',proxies=proxies).readlines()
        a = a + urllib.urlopen('http://celestrak.com/NORAD/elements/nnss.txt',proxies=proxies).readlines()
        a = a + urllib.urlopen('http://celestrak.com/NORAD/elements/tdrss.txt',proxies=proxies).readlines()
# broken
#        a = a + urllib.urlopen('http://www.wpusa.dynip.com/files/SPACE/CLASSFD.TLE',proxies=proxies).readlines()
        a = a + urllib.urlopen('http://www.tle.info/data/military.txt',proxies=proxies).readlines()
        a = a + urllib.urlopen('http://www.haystack.mit.edu/~j/sats.tle',proxies=proxies).readlines()
    except IOError:
        print("Could not retrieve ephemeris from celestrak, reverting to cached file. Check internet connection!")
        f.close()
        os.system("cp beacon.tle.cache %s"%(fname))
        return(False)

    print "Read ",len(a)/3," satellites"
    for i in range(0,len(a)/3):
        name = a[i*3].strip()
	
        for j in range(0,len(sl.satnames)):
            tmpname = name[0:len(sl.satnames[j])]
            if tmpname == sl.satnames[j]:
	        uname = re.sub(" ","_",tmpname)
                print "Found ",tmpname
                f.write("%s\n" % (uname))
                f.write("%s\n" % (a[i*3+1].strip()))
                f.write("%s\n" % (a[i*3+2].strip()))
                f.write("%d\n" % (int(sl.offsets[j])))
    f.close()
    os.system("cp %s beacon.tle.cache"%(fname))
    return(True)

def download_tle_files(download_dir):
    sl = satellitelist("satellites.txt")
    return(writeBeaconsTLE("%s/beacon.tle"%(download_dir),sl))

# By doing the main check, you can have that code only execute when you want to run the module as a program and not have it execute when someone just wants to import your module and call your functions themselves.

if __name__ == "__main__":                
    sl = satellitelist("satellites.txt")
    ddir = sys.argv[1]

    writeBeaconsTLE("%s/beacon.tle"%(ddir),sl)
