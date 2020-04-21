import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# define pins
Trigger = 17
Echo = 18
Buzzer = 2

# set up pins
GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)
GPIO.setup(Buzzer, GPIO.OUT)

# initalise the buzzer
pwm = GPIO.PWM(Buzzer, 1000)
pwm.start(0)

# define functions
    
def getDistance():
    
    # trigger the SRO4 
    GPIO.output(Trigger, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trigger, GPIO.LOW)
    
    # get the start time
    while GPIO.input(Echo) == False:
        startTime = time.time()
        
    # get the finishing time
    while GPIO.input(Echo) == True:
        finishTime = time.time()

    # calculate the distance
    totalTime = finishTime - startTime
    distance = (totalTime * 34300) / 2
    
    return distance

try:
    while True:
        # get the distance and print it to the terminal
        distance = getDistance()
        print(distance)
        
        # Limit the distance which will affect the buzzer to 30 cm
        if distance > 30:
            distance = 30
            
        if distance < 0:
            distance = 0
            
        # get a ratio from the distance and update the duty cycle using this ratio
        distance = (distance / 30) * 100
        pwm.ChangeDutyCycle(distance)
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    