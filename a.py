#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time
import sys
import Adafruit_CharLCD as LCD
import getch
from spacebrew import Spacebrew

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
lcd_backlight = 4
lcd_message = ""

# BeagleBone Black configuration:
# lcd_rs        = 'P8_8'
# lcd_en        = 'P8_10'
# lcd_d4        = 'P8_18'
# lcd_d5        = 'P8_16'
# lcd_d6        = 'P8_14'
# lcd_d7        = 'P8_12'
# lcd_backlight = 'P8_7'

showingSongInfo = False
currentSongTitle = ""
currentSongArtist = ""

def setSongTitle(title):
    print "new title "
    currentSongTitle = title
    lcd.clear()
    lcd.message(title+'\n'+currentSongArtist)
    showingSongInfo = True
def setSongArtist(artist):
    currentSongArtist = artist
    #lcd.message(artist)

def submitQuery(query):
    #do stuff
    print "Published "+query+"!"
    brew.publish("ttl_keyboard",query)

class jagLCD(LCD.Adafruit_CharLCD):
    pass
    def Adafruit_CharLCD(self,lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7,lcd_columns,lcd_rows,lcd_backlight):
        LCD.__init(self);
        self.Adafruit_CharLCD(lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7,lcd_columns,lcd_rows,lcd_backlight)
        self._currentMessage = ""

    @property
    def currentMessage(self):
        return self._currentMessage

    @currentMessage.setter
    def currentMessage(self,value):
        self._currentMessage=value
        self.clear()
        self.message(value)
 
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = jagLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Print a two line message
lcd.currentMessage = "Search Spotify:\n"

#init spacebrew
brew = Spacebrew("ttl_keyboard",description="A simple IO device",server="192.168.1.96",port=9000)
brew.addPublisher("ttl_keyboard","string")
brew.addSubscriber("songTitle","string")
brew.addSubscriber("songArtist","string")

brew.subscribe("songTitle",setSongTitle)
brew.subscribe("songArtist",setSongArtist)
brew.start()

searchString=""
#get the user's input to search on spotify
while 1:
    c = getch.getche()
    print "char is " + str(ord(c))
    if c:
        if showingSongInfo == True:
            lcd.clear()
            lcd.message("Search Spotify:\n")
            showingSongInfo = False
        lcd.message(c)
        searchString+=c
    #esc key (clear)
    if ord(c) == 27:
        lcd.clear()
        lcd.message("Search Spotify:\n")
        searchString=""
    #backspace
    if ord(c) == '\b' or ord(c) == 127:
        searchString=searchString[:-2]
        lcd.clear()
        lcd.message("Search Spotify:\n"+searchString)
        if len(searchString) > 16:
            for i in range(len(searchString)%16):
                lcd.move_left()
    if len(searchString) > 16:
        lcd.move_left()
    lcd.show_cursor(True)
    if c == '\n':
        #lcd.clear()
        #remove \n from query
        searchString=searchString[:-1]
        submitQuery(searchString)
        lcd.clear()
        lcd.message("Search Spotify:\n")
        
        searchString=""
        #lcd.message("Transmitting\nData...")
        # with this var set, once the sogn name changes, it'll display it properly
        #lcd.show_cursor(False)
#time.sleep(5.0)
#lcd.blink(True)
# Stop blinking and showing cursor.
#lcd.show_cursor(False)

