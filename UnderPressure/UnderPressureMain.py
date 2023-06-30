from machine import ADC
from machine import Pin  
import time,utime
from pico_i2c_lcd import I2cLcd
from machine import I2C
from buzzer_music import music

def setupPins():
#    global i2c
#    global lcd
    global buzzer
    global adc
    
    adc = machine.ADC(2)
    buzzer = Pin(15)
#    buzzer.off()
    
    # Define pins and setup i2c for display
#    sda=machine.Pin(0)
#    scl=machine.Pin(1)
#    i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
     
#    I2C_ADDR = i2c.scan()[0]
#    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Main loop - handles events for game play    
def gameLoop():
    global buzzer
    global adc
    
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
      print(val1,val2,val3,val4,val5,val6)
      if (val1 == val2 & val2 == val3 & val3 == val4 & val4 == val5 & val5 == val6 ):
        print("Use your finger, not object")
        sadSong = '6 D3 6 14;12 A2 11 14;0 G#3 6 14'
        sadlen = len(sadSong)
        sadTune = music(sadSong, pins=[buzzer], duty=100)
        for i in range(sadlen):
            if(sadTune.tick()):
                time.sleep(0.04)
        sadTune.stop()
        return

      print ("2 times",avg1, avg2)
      if (avg1 == 0 & avg2 == 0):
          return
      # success if averages of two times are the same. Finger was steady force.
      if (avg1 == avg2):
        song = '16.5 C5 0.5 14;15.5 C5 0.5 14;0 A5 0.5 14;4 F5 0.5 14;7 F5 0.5 14;8 D5 0.5 14;10 F5 0.5 14;12 C5 0.5 14;19 C5 0.5 14;20 D5 0.5 14;21 E5 0.5 14;23 A5 0.5 14;25 A5 0.5 14;27 G5 0.5 14;29 G5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A5 0.5 14;32 A5 0.5 14;32 A#5 0.5 14;32 D#3 0.5 14;32 D#3 0.5 14;34 A5 0.5 14;36 F5 0.5 14;39 F5 0.5 14;40 D5 0.5 14;42 F5 0.5 14;44 C5 0.5 14;47.5 C5 0.5 14;48.5 C5 0.5 14;51 C5 0.5 14;52 E5 0.5 14;53 A5 0.5 14;55 G5 0.5 14;57 F5 0.5 14;16.5 C5 0.5 14;15.5 C5 0.5 14;0 A5 0.5 14;4 F5 0.5 14;7 F5 0.5 14;8 D5 0.5 14;10 F5 0.5 14;12 C5 0.5 14;19 C5 0.5 14;20 D5 0.5 14;21 E5 0.5 14;23 A5 0.5 14;25 A5 0.5 14;27 G5 0.5 14;29 G5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A#5 0.5 14;32 A5 0.5 14;32 A5 0.5 14;32 A#5 0.5 14;34 A5 0.5 14;36 F5 0.5 14;39 F5 0.5 14;40 D5 0.5 14;42 F5 0.5 14;44 C5 0.5 14;47.5 C5 0.5 14;48.5 C5 0.5 14;51 C5 0.5 14;52 E5 0.5 14;53 A5 0.5 14;55 G5 0.5 14;57 F5 0.5 14;0 A6 0.5 14;4 F6 0.5 14;7 F6 0.5 14;8 D6 0.5 14;10 F6 0.5 14;12 C6 0.5 14;15.5 C6 0.5 14;16.5 C6 0.5 14;19 C6 0.5 14;20 D6 0.5 14;21 E6 0.5 14;23 A6 0.5 14;25 A6 0.5 14;27 G6 0.5 14;29 G6 0.5 14;34 A6 0.5 14;36 F6 0.5 14;39 F6 0.5 14;40 D6 0.5 14;42 F6 0.5 14;44 C6 0.5 14;47.5 C6 0.5 14;48.5 C6 0.5 14;51 C6 0.5 14;52 E6 0.5 14;53 A6 0.5 14;55 G6 0.5 14;57 F6 0.5 14;0 C7 0.5 14'
        print('STEADY HAND. Answer is XXXX')
        songlen = len(song)
        songTune = music(song, pins=[buzzer], duty=100)
        for i in range(songlen):
            if(songTune.tick()):
                time.sleep(0.04)
        songTune.stop()
        utime.sleep(3)
        print('New Game')

setupPins()
#lcd.clear()
    
# Game LOOP ON
print("Enter game loop")
while True:
    gameLoop()
  
