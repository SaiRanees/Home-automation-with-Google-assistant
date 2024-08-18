from gpiozero import MCP3208
from time import sleep
import time
import urllib.request
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
rly1=2
rly2=3
fr=19
buz=26

GPIO.setup(rly1,GPIO.OUT)
GPIO.setup(rly2,GPIO.OUT)
GPIO.setup(fr,GPIO.IN)
GPIO.setup(buz,GPIO.OUT)

GPIO.output(rly1,0)
GPIO.output(rly2,0)

hm1 = MCP3208(channel=0, device=0)
hm2 = MCP3208(channel=1, device=0)


mVperAmp = 180
Voltage = 0
VRMS = 0
AmpsRMS = 0
prv=0

def getVPP(adc):
  i=0
  ac=0
  while(i<2):
    i=i+1
    result=0
    readValue=0
    maxValue = 0
    minValue = 5000
    start_time = time.time()
    while((time.time()-start_time) < 1):
         readValue = (adc.value * 5) * 1000
         if (readValue > maxValue): 
             maxValue = readValue
         if (readValue < minValue): 
             minValue = readValue
    
    result = ((maxValue - minValue) * 5.0)/5000.0

    VRMS = (result/2.0) *0.707
    AmpsRMS = (VRMS * 1000)/mVperAmp
    ac=ac+AmpsRMS

    
  if(ac/2<0.15):
    ac=0
  return ac/2
print('Initializing')
c1=getVPP(hm1)
c2=getVPP(hm2)

print('Reading Sensor Info')
while True:
    c1=getVPP(hm1)*1.6
    c2=getVPP(hm2)*1.6
    Watt1 = (c1*230)
    Watt2 = (c2*230)
    fval=1-GPIO.input(fr)
    if(fval==1):
      GPIO.output(buz,1)
      time.sleep(1)
      GPIO.output(buz,0)
      
    
    print("LOAD1:" +str(round(Watt1,2)) + " Watts")
    print("LOAD2:" +str(round(Watt2,2)) + " Watts")
    bill=(Watt1+Watt2)*0.0015
    print(bill)

    wp = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=P51O0F0FJHC9JXPY&field1=" + str(round(Watt1,2)) + "&field2=" + str(round(Watt2,2)) + "&field3=" + str(round(bill,2))+ "&field4=" + str(fval))


    r_link='https://api.thingspeak.com/channels/403900/fields/1/last?api_key=N0392W61F64BVJAQ'
    f=urllib.request.urlopen(r_link)
    rcv = (f.readline()).decode()
    if(prv != rcv):
        prv=rcv
        if(rcv[0]=='A'):
          print('D1 ON ')
          GPIO.output(rly1,0)
          
        if(rcv[0]=='B'):
        
          print('D2 ON')
          GPIO.output(rly2,0)
         
        if(rcv[0]=='C'):
          print('D1 OFF')
          GPIO.output(rly1,1)
        
        if(rcv[0]=='D'):
          print('D2 OFF')
          GPIO.output(rly2,1)


    if(Watt1>150):
       print('Over load-1')
       GPIO.output(rly1,1)

    if(Watt2>150):
       print('Over load-2')
       GPIO.output(rly2,1)
