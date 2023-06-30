from machine import Pin  
import time,utime
from pico_i2c_lcd import I2cLcd
from machine import I2C
from buzzer_music import music

### Indiana Jones and the Golden Bison smart cache

place = 0
lift = 0
state = -1
last_state = 0
delta = -1
gameOn = -1 #Game not running or finished
minTime = 500
gameStartEvent = 0

def reset():
    global lift, place
    global state
    global delta
    
    place = 0
    lift = 0
    state = -1
    delta = -1

#led = Pin(25, Pin.OUT)

def setupPins():
    global button
    global i2c
    global lcd
    global he
    global buzzer

    #Pin for start game
    button = Pin(16, Pin.IN, Pin.PULL_DOWN)
    
    buzzer = Pin(15)

    # Define pins and setup i2c for display
    sda=machine.Pin(0)
    scl=machine.Pin(1)
    i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
     
    I2C_ADDR = i2c.scan()[0]
    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

    # Pin for Hall Effect magnetic field sensor
    he = Pin(4,Pin.IN)
    
# Handler for Button pressed. Be sure bison is back in place
def startGameHandler(p):
    global gameStartEvent
    
    gameStartEvent = 1
    return

# Process Game Start button press
def gameStart():
    global gameOn
    global lcd
    global gameStartEvent
    
    if (gameOn == -1 and he.value() == 0):
        lcd.clear()
        lcd.putstr("Put Bison back  & Press start")
        return
    
    lcd.clear()
    lcd.putstr('Game ON')
    gameOn = 1
    
# Main loop - handles events for game play    
def gameLoop():
    global gameOn
    global lift, place
    global state
    global last_state
    global delta
    global buzzer
    global gameStartEvent
    # Make it easier after each fail
    retryDelay = [250, 500, 750, 2000]
    failnum = 0
    
    #print ("Game Loop", gameOn,state,delta)
    while True:
        # Check for Start button press and handle 
        if (gameStartEvent != 0):
            gameStartEvent = 0
            gameStart()
            minTime = retryDelay[failnum]
    
        # state has changed
        if (state != last_state):
            #print("last_state=", last_state, " state=", state, "minTime=", minTime, "delta=", delta)
            last_state = state
            # lifted and restored too slow
            if (delta > minTime):
                #print("Play sad", delta)
                lcd.clear()
                lcd.putstr('Put Bison back, push Start&retry')
                song = '0 C5 1 14;2 G4 1 14;4 G#4 1 14;6 G4 1 14;8 F#4 3 14;0 C6 1 4;2 G5 1 4;4 G#5 1 4;6 G5 1 4;8 F#5 4 4'
                mySong = music(song, pins=[buzzer])
                songlen = len(song)
                for i in range(len(song)):
                    mySong.tick()
                    time.sleep(0.04)
                mySong.stop()
                buzzer.off()
                if failnum < len(retryDelay) - 1:
                    failnum = failnum + 1
                reset()
                gameOn = -1
                
            if (delta > 0 and delta < minTime):
                #print("Play happy", delta)
                # Theme Notes from https://onlinesequencer.net/
                lcd.clear()
                lcd.putstr('WORD IS INDY')
                song = '0 E5 3 14;3 F5 1 14;4 G5 2 14;6 C6 7 14;16 D5 3 14;19 E5 1 14;20 F5 9 14;32 G5 3 14;35 A5 1 14;36 B5 2 14;38 F6 8 14;48 A5 3 14;51 B5 1 14;52 C6 4 14;56 D6 4 14;60 E6 2 14'
                mySong = music(song, pins=[Pin(15)],duty=4512)
                songlen = len(song)
                for i in range(len(song)):
                    mySong.tick()
                    time.sleep(0.04)
                #print("#Play song ",delta)
                mySong.stop()
                buzzer.off()
                time.sleep(1.0)
                lcd.clear()
                lcd.putstr('Put Bison Back  Now')
                time.sleep(4.0)
                lcd.clear()
                lcd.putstr('New Game.       Press Start')
                reset()
                failnum = 0
                gameOn = -1

# Callback function for Hall effect interrupt, compute ms from lift to replace into delta
def callback(p):
    global place, lift
    global lcd
    global messaging
    global state
    global delta 
    global gameOn
    
    if(gameOn == -1):
        #print ("#139 callback game not on")
        return
      
    if (p.value() == 1):
        place = time.ticks_ms()
        delta = time.ticks_diff(place, lift)
        #print("#148 vvvvPlace at ", delta)
        state = 1
        return
        
    if (p.value() == 0):
        lift = time.ticks_ms()
        delta = -1
        state = 0

reset()
setupPins()
button.irq(trigger=button.IRQ_RISING, handler=startGameHandler)
# he=0 if bison up, he=1 if down
he.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)
lcd.clear()
lcd.putstr('Press Start')
# Wait for initial game start press after power on
while gameStartEvent != 1:
    time.sleep(.5)
    
# Game LOOP ON
print("Enter game loop")
while True:
    gameLoop()
