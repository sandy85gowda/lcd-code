import time
import RPi.GPIO as IO    #calling for header file which helps in using GPIOs of PI

string_of_characters = 0 

IO.setwarnings(False)    #do not show any warnings
IO.setmode (IO.BCM)      #programming the GPIO by BCM pin numbers. (like PIN29 as GPIO5)
IO.setup(6,IO.OUT)      #initialize GPIO17,27,24,23,18,26,5,6,13,19,21 as an output
IO.setup(22,IO.OUT)
IO.setup(21,IO.OUT)
IO.setup(20,IO.OUT)
IO.setup(16,IO.OUT)
IO.setup(12,IO.OUT)
IO.setup(25,IO.OUT)
IO.setup(24,IO.OUT)
IO.setup(23,IO.OUT)
IO.setup(18,IO.OUT)
IO.setup(2,IO.OUT)
IO.setup(3,IO.IN)      #initialize GPIO16 as an input

def send_a_command (command):  #steps for sending a command to 16x2 LCD
    pin=command
    PORT(pin);
    IO.output(6,0)
    #PORTD&= ~(1<<RS);
    IO.output(22,1)
    #PORTD|= (1<<E);
    time.sleep(0.001)
    #_delay_ms(50);
    IO.output(22,0)
    #PORTD&= ~(1<<E);
    pin=0
    PORT(pin); 

def send_a_character (character):  #steps for sending a character to 16x2 LCD
    pin=character
    PORT(pin);
    IO.output(6,1)
    #PORTD|= (1<<RS);
    IO.output(22,1)
    #PORTD|= (1<<E);
    time.sleep(0.001)
    #_delay_ms(50);
    IO.output(22,0)
    #PORTD&= ~(1<<E);
    pin=0
    PORT(pin);

def PORT(pin):                    #assigning level for PI GPIO for sending data to LCD through D0-D7
    if(pin&0x01 == 0x01):
        IO.output(21,1)
    else:
        IO.output(21,0)
    if(pin&0x02 == 0x02):
        IO.output(20,1)
    else:
        IO.output(20,0)
    if(pin&0x04 == 0x04):
        IO.output(16,1)
    else:
        IO.output(16,0)
    if(pin&0x08 == 0x08):
        IO.output(12,1)
    else:
        IO.output(12,0)    
    if(pin&0x10 == 0x10):
        IO.output(25,1)
    else:
        IO.output(25,0)
    if(pin&0x20 == 0x20):
        IO.output(24,1)
    else:
        IO.output(24,0)
    if(pin&0x40 == 0x40):
        IO.output(23,1)
    else:
        IO.output(23,0)
    if(pin&0x80 == 0x80):
        IO.output(18,1)
    else:
        IO.output(18,0)

def send_a_string(string_of_characters):
  string_of_characters = string_of_characters.ljust(16," ")
  for i in range(16):
    send_a_character(ord(string_of_characters[i]))  #send characters one by one through data port
    
while 1:
    send_a_command(0x38);  #16x2 line LCD
    send_a_command(0x0E);  #screen and cursor ON
    send_a_command(0x01);  #clear screen
    time.sleep(0.1)                #sleep for 100msec
    
    IO.setup(2,1)
    time.sleep(0.00001)
    IO.setup(2,0)           #sending trigger pulse for sensor to measure the distance
        
    while (IO.input(3)==0):
        start = time.time()  #store the start time of pulse output         
            
    while (IO.input(3)==1):
        stop = time.time()   #store the stop time 
      
            
    distance = ((stop - start)*17150)  #calculate distance from time
    distance = round(distance,2)       #round up the decimal values
    if(distance<400):                  #if distance is less than 400 cm, display the result on LCD 
        send_a_command(0x80 + 0);
        send_a_string ("Dist=%s cm"% (distance));
        time.sleep(0.15)
        
    if(distance>400):                  #If distance is more than 400cm, just print 400+ on LCD
        send_a_command(0x80 + 0);
        send_a_string ("Dist= 400+ cm");
        time.sleep(0.15)
