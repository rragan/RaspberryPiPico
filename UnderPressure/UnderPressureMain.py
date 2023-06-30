from machine import ADC
from machine import Pin  
import time,utime
from buzzer_music import music
from pico_i2c_lcd import I2cLcd
from machine import I2C

def setupPins():
    global buzzer
    global adc
    global lcd
    
    # Define pins and setup i2c for display
    sda=machine.Pin(0)
    scl=machine.Pin(1)
    i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
    
    I2C_ADDR = i2c.scan()[0]
    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
    
    adc = machine.ADC(2)
    buzzer = Pin(15)
#    buzzer.off()
    

def formatTimes(line1, t1, t2):
    line2 = "T1: " + str(t1) + "         "
    line3 = "T2: " + str(t2) + "        "
    return line1 + line2[0:8] + line3[0:7]

# Main loop - handles events for game play    
def gameLoop():
    global buzzer
    global adc
    global lcd
    global avg1
    global avg2
    
    avg1 = 0
    avg2 = 0
    
    while True:
      # If nothing on sensor, wait
      value = round(adc.read_u16()/1000)
      if (value <= 5):
        continue
      # Get 3 readings 1 second apart and average them
      val1 = round(adc.read_u16()/1000)
      utime.sleep(1)  
      val2 = round(adc.read_u16()/1000)
      utime.sleep(1)
      val3 = round(adc.read_u16()/1000)
      utime.sleep(1)
      avg1 = int(sum([val1, val2, val3])/3)
      
      # Get 3 more readings 1 second apart and average them
      val4 = round(adc.read_u16()/1000)
      utime.sleep(1)  
      val5 = round(adc.read_u16()/1000)
      utime.sleep(1)
      val6 = round(adc.read_u16()/1000)
      avg2 = int(sum([val4, val5, val6])/3)
        
      # If all readings are identical, likely an object and not a finger
      #print(val1,val2,val3,val4,val5,val6)
      if (val1 == val2 & val2 == val3 & val3 == val4 & val4 == val5 & val5 == val6 ):
        lcd.clear()
        lcd.putstr("USE YOUR FINGER NOT AN OBJECT") 
        #print("Use your finger, not object")
        sadSong = '6 D3 6 14;12 A2 11 14;0 G#3 6 14'
        #sadSong = '0 C5 1 14;2 G4 1 14;4 G#4 1 14;6 G4 1 14;8 F#4 3 14;0 C6 1 4;2 G5 1 4;4 G#5 1 4;6 G5 1 4;8 F#5 4 4'
        sadlen = len(sadSong)
        sadTune = music(sadSong, pins=[buzzer], duty=4512)
        for i in range(sadlen):
            if(sadTune.tick()):
                time.sleep(0.04)
        sadTune.stop()
        utime.sleep(2)
        lcd.clear()
        lcd.putstr('NEW GAME        Measuring Force')
        utime.sleep(1)
        continue

      #print ("2 times",avg1, avg2)
      # noise or no data
      if (avg1 < 5 & avg2 < 5 ):
          continue
      # success if averages of two times are the same. Finger was steady force.
      if (avg1 != avg2):
          string = formatTimes("NOT SAME", avg1, avg2)
          lcd.clear()
          lcd.putstr('NOT THE SAME    T1='+ str(avg1) + "/T2=" + str(avg2)) 
      else:
        lcd.clear()
        lcd.putstr('YOU DID IT!     WORD IS FROG')
        song = '16.5 C5 0.5 14;15.5 C5 0.5 14;0 A5 0.5 14;4 F5 0.5 14;7 F5 0.5 14;8 D5 0.5 14;10 F5 0.5 14;12 C5 0.5 14;19 C5 0.5 14;20 D5 0.5 14;21 E5 0.5 14;23 A5 0.5 14;25 A5 0.5 14;27 G5 0.5 14;29 G5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A5 0.5 14;32 A5 0.5 14;32 A#5 0.5 14;32 D#3 0.5 14;32 D#3 0.5 14;34 A5 0.5 14;36 F5 0.5 14;39 F5 0.5 14;40 D5 0.5 14;42 F5 0.5 14;44 C5 0.5 14;47.5 C5 0.5 14;48.5 C5 0.5 14;51 C5 0.5 14;52 E5 0.5 14;53 A5 0.5 14;55 G5 0.5 14;57 F5 0.5 14;16.5 C5 0.5 14;15.5 C5 0.5 14;0 A5 0.5 14;4 F5 0.5 14;7 F5 0.5 14;8 D5 0.5 14;10 F5 0.5 14;12 C5 0.5 14;19 C5 0.5 14;20 D5 0.5 14;21 E5 0.5 14;23 A5 0.5 14;25 A5 0.5 14;27 G5 0.5 14;29 G5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A5 0.5 14;32 A5 0.5 14;32 A#5 0.5 14;34 A5 0.5 14;36 F5 0.5 14;39 F5 0.5 14;40 D5 0.5 14;42 F5 0.5 14;44 C5 0.5 14;47.5 C5 0.5 14;48.5 C5 0.5 14;51 C5 0.5 14;52 E5 0.5 14;53 A5 0.5 14;55 G5 0.5 14;57 F5 0.5 14;0 A6 0.5 14;4 F6 0.5 14;7 F6 0.5 14;8 D6 0.5 14;10 F6 0.5 14;12 C6 0.5 14;15.5 C6 0.5 14;16.5 C6 0.5 14;19 C6 0.5 14;20 D6 0.5 14;21 E6 0.5 14;23 A6 0.5 14;25 A6 0.5 14;27 G6 0.5 14;29 G6 0.5 14;34 A6 0.5 14;36 F6 0.5 14;39 F6 0.5 14;40 D6 0.5 14;42 F6 0.5 14;44 C6 0.5 14;47.5 C6 0.5 14;48.5 C6 0.5 14;51 C6 0.5 14;52 E6 0.5 14;53 A6 0.5 14;55 G6 0.5 14;57 F6 0.5 14;0 C7 0.5 14'
        #print('STEADY HAND. Answer is XXXX')
        songlen = len(song)
        songTune = music(song, pins=[buzzer], duty=4512)
        for i in range(songlen):
            if(songTune.tick()):
                time.sleep(0.04)
        songTune.stop()
        utime.sleep(3)
        lcd.clear()
        lcd.putstr('NEW GAME        Measuring Force')
        #print('New Game')

setupPins()
lcd.clear()
lcd.putstr('NEW GAME        Measuring Force')
#print ("Start Game Loop")
    
# Game LOOP ON
while True:
    gameLoop()
  
