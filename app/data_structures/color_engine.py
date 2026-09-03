from enum import Enum
from math import floor

GG_BYTES  = 4
RGB_BYTES = 24
COLOR_BYTE_DELTA = 17

class ColorType(Enum):
    GameGear = 1
    RGB      = 2
    HEXRGB   = 3

class Colors:
    def __init__(self):
        self.red = {
            ColorType.GameGear: None,
            ColorType.RGB:      None,
            ColorType.HEXRGB:   None
        }
        self.green = {
            ColorType.GameGear: None,
            ColorType.RGB:      None,
            ColorType.HEXRGB:   None
        }
        self.blue = {
            ColorType.GameGear: None,
            ColorType.RGB:      None,
            ColorType.HEXRGB:   None
        }

    def __str__(self):
        """
        Debugging override
        """
        ggTpl  = self.toGGTuple()
        ggStr  = ",".join(ggTpl)
        rgbTpl = self.toRGBTuple()
        rgbStr = ",".join(rgbTpl)
        return f"GG: [{ggStr}]\r\n RGB: [{rgbStr}] HEXRGB:[{self.toRGBHEX()}]"

    def fromGameGearBytes(self,b1:str,b2:str):
        """
        Converts two individual Game Gear bytes into an RGB tuple.
        byte1 contains Blue (0x0B). byte2 contains Green and Red (0xGR).
        """
        b1_int = int(b1, 16)
        b2_int = int(b2, 16)
        blue_4bit  = b1_int & 0x0F       # Ignore the top nibble of byte 1
        green_4bit = (b2_int & 0xF0) >> 4 # High nibble of byte 2
        red_4bit   = b2_int & 0x0F       # Low nibble of byte 2
        red_int   = red_4bit * COLOR_BYTE_DELTA
        green_int = green_4bit * COLOR_BYTE_DELTA
        blue_int  = blue_4bit * COLOR_BYTE_DELTA
        self.red = {
            ColorType.GameGear: red_4bit,
            ColorType.RGB:      red_int,
            ColorType.HEXRGB:   f"{red_int:02X}"
        }
        self.green = {
            ColorType.GameGear: green_4bit,
            ColorType.RGB:      green_int,
            ColorType.HEXRGB:   f"{green_int:02X}"
        }
        self.blue = {
            ColorType.GameGear: blue_int,
            ColorType.RGB:      blue_int,
            ColorType.HEXRGB:   f"{blue_int:02X}"
        }

    def fromRGBStr(self,r:str,g:str,b:str):
        """
        Converts RGB tuple 24 bytes to gg 4 bytes
        """
        red_int   = int(r)
        green_int = int(g)
        blue_int  = int(b)
        self.fromRGBInt(red_int,green_int,blue_int)

    def fromRGBInt(self,r:int,g:int,b:int):
        """
        Converts RGB tuple 24 bytes to gg 4 bytes
        """
        self.red = {
            ColorType.GameGear: floor(r / COLOR_BYTE_DELTA) if r != 0 else 0,
            ColorType.RGB:      r,
            ColorType.HEXRGB:   f"{r:02X}"
        }
        self.green = {
            ColorType.GameGear: floor(g / COLOR_BYTE_DELTA) if g != 0 else 0,
            ColorType.RGB:      g,
            ColorType.HEXRGB:   f"{g:02X}"
        }
        self.blue = {
            ColorType.GameGear: floor(b / COLOR_BYTE_DELTA) if b != 0 else 0,
            ColorType.RGB:      b,
            ColorType.HEXRGB:   f"{b:02X}"
        }

    def fromRGBHex(self,rgb:str):
        """
        Converts RGB tuple 24 bytes to gg 4 bytes
        """
        r = int(rgb[1:3], 16)
        g = int(rgb[3:5], 16)
        b = int(rgb[5:7], 16)
        self.red = {
            ColorType.GameGear: floor(r / COLOR_BYTE_DELTA) if r != 0 else 0,
            ColorType.RGB:      r,
            ColorType.HEXRGB:   f"{r:02X}"
        }
        self.green = {
            ColorType.GameGear: floor(g / COLOR_BYTE_DELTA) if g != 0 else 0,
            ColorType.RGB:      g,
            ColorType.HEXRGB:   f"{g:02X}"
        }
        self.blue = {
            ColorType.GameGear: floor(b / COLOR_BYTE_DELTA) if b != 0 else 0,
            ColorType.RGB:      b,
            ColorType.HEXRGB:   f"{b:02X}"
        }


    def toGGTuple(self) -> tuple:
        """
        despite being read in as 0bgr, we want to output as GR0B
        f"{num:X}"
        """
        red = self.red[ColorType.GameGear]
        red = red if red != None else 0
        red = f"{red:X}"

        green = self.green[ColorType.GameGear]
        green = green if green != None else 0
        green = f"{green:X}"

        blue = self.blue[ColorType.GameGear]
        blue = blue if blue != None else 0
        blue = f"{blue:X}"

        byte1 = f"{green}{red}"
        byte2 = f"0{blue}"
        return [byte1,byte2]

    def toRGBTuple(self) -> tuple:
        """
        a tuple with rgb
        """
        red = self.red[ColorType.RGB]
        red = red if red != None else "0"

        green = self.green[ColorType.RGB]
        green = green if green != None else "0"

        blue = self.blue[ColorType.RGB]
        blue = blue if blue != None else "0"

        return [str(red),str(green),str(blue)]
    
    def toRGBHEX(self) -> str:
        """
        a str with rgb
        """
        return f"#{self.red[ColorType.HEXRGB]}{self.green[ColorType.HEXRGB]}{self.blue[ColorType.HEXRGB]}"
##
## Test
##

#colorTest = colors()
#colorTest.fromRGBInt(255,23,55)
#print(colorTest)