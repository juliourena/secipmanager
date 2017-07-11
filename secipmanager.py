#!/usr/bin/python
import netifaces as ni
import os
import getopt
import sys

ip = ""
netmask = ""
nic = ""
delete = False
IPRange = ""

def usage():
    print "Secondary IP Manager Tool by ~EnGeLs~"
    print "it works only for /24 networks"
    print "Usage: secipmanager.py -r numberFrom-To -i eth0" #-p port"
    
    print "-r --range - expect a range between 1 and 254 for ip address configuration"
    print "-i --interface - interface to configure IP Addresses"
    print "-d --delete - to delete the IP Address range from the computer"
    
    print
    print
    print "Examples: "
    print "secipmanager.py -r 30-60 -i eth0"
    print "secipmanager.py -r 30-60 -i eth0 -d"
    sys.exit(0)

def getIPfromInterface(interface):
    global ip 
    
    ni.ifaddresses(interface)

    ip = ni.ifaddresses(interface)[2][0]['addr']
    ip = ".".join(ip.split('.')[0:-1])
    
    mask = ni.ifaddresses(interface)[2][0]['netmask']
    netmaskConvert(mask)

def netmaskConvert(mask):
    global netmask
    
    if mask == '255.255.255.0':
        netmask = '/24'

def asignRangeIP(start,end): 
    
    for num in range(start,end):
        iptoAdd = ip + '.' + str(num)
        
        if not delete:
            os.system("ip address add "+ iptoAdd + netmask + ' dev '+ nic)
        else:
            os.system("ip address del "+ iptoAdd + netmask + ' dev '+ nic)    
        
    print (os.system("ip address"))

def main():
    global nic
    global delete 
    global IPRange
    
    if not len(sys.argv[1:]):
        usage()    
    
    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hr:i:d", ["help","range","interface","delete"])
    except getopt.GetoptError as err:
        print str(err)
        usage() 
    
    for o,a in opts:
        if o in ("-h","--help"):
            usage()    
        elif o in ("-r","--range"):
            IPRange = a   
        elif o in ("-i","--interface"):
            nic = a
        elif o in ("-d","--delete"):
            delete = True
    
    if not IPRange:
        sys.exit(0)
    
    start = int(IPRange.split('-')[0])
    end = int(IPRange.split('-')[1]) + 1 
    
    getIPfromInterface(nic)
    
    asignRangeIP(start, end)
                 
if __name__ == '__main__':
    main()
