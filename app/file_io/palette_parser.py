"""Palette Parser"""
from app.file_io.offset import UniversalOffset
from app.file_io.file_io import parse_rom
from app.data_structures.color_engine import Colors

CONST_PALETTE_LENGTH    = 28
CONST_PALETTE_ADDRESS   = UniversalOffset(offsetHex="0x3E3A5")

class Palette:
    def __init__(self,offset:UniversalOffset=None,color:Colors=None):
        self.offset = offset
        self.color = color

class PaletteParse:
    def __init__(self,rompath:str=None):
        self.rom_path     = rompath
        if self.rom_path == None:
            print(f"PaletteParse:rompath is None! Set again")
        self.palettes = []
        self.setPalettes()

    def __str__(self):
        return f"PaletteParse: offset={CONST_PALETTE_ADDRESS.getHex()},palettes={self.palettes} palette_count={len(self.palettes)}"

    def getOffsetInt(self):
        return self.offset.getInt()

    def getOffsetHex(self):
        return self.offset.getHex()
#bytes 1-0 (0F:A3A6-0F:A3A5)   = white for scoreboard and orb accent    
#bytes 3-2 (0F:A3A8-0F:A3A7)   = BLUE for our orb
#bytes 5-4 (0F:A3AA-0F:A3A9)   = GREEN for our orb and bub
#bytes 7-6 (0F:A3AC-0F:A3AB)   = RED for our orb
#bytes 1-0 (0F:A3A6-0F:A3A5)   = white for scoreboard and orb accent
#bytes 9-8 (0F:A3AE-0F:A3AD)   = Yellow for our orb
#bytes 11-10 (0F:A3B0-0F:A3AF) = Bronze for machine
#bytes 13-12 (0F:A3B2-0F:A3B1) = Light Grey Orb
#bytes 15-14 (0F:A3B4-0F:A3B3) = Dark Grey Orb
#bytes 17-16 (0F:A3B4-0F:A3B3) = Purple Orb

    def setPalettes(self):
        self.palettes = []
        raw_bytes = parse_rom(self.rom_path,
                  start=CONST_PALETTE_ADDRESS.getHex(),
                  distance=CONST_PALETTE_LENGTH)
        for p in range(0, CONST_PALETTE_LENGTH,2):
            color = Colors()
            color.fromGameGearBytes(raw_bytes[p+1],raw_bytes[p])
            palette = Palette(offset=UniversalOffset(offsetHex=hex(CONST_PALETTE_ADDRESS.getInt()+(p*2))),color=color)
            self.palettes.append(palette)
            #print(color)

    def getPalettesAsRGBHex(self):
        rgbhex_list = []
        for p in self.palettes:
            rgbhex_list.append(p.color.toRGBHEX())
        return rgbhex_list