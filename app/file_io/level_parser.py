"""Level Parser"""
from app.file_io.offset import LevelTableOffset
from app.file_io.file_io import parse_rom

CONST_LEVEL_END_SYMBOL = "FF"
CONST_LEVEL_WIDTH  = 8
CONST_LEVEL_HEIGHT = 9
CONST_LEVEL_LENGTH = 35

class LevelParse:
    def __init__(self,rompath:str=None,lvlIdx:int=1,offset:LevelTableOffset=None,width:int=CONST_LEVEL_WIDTH,height:int=CONST_LEVEL_HEIGHT):
        self.rom_path     = rompath
        if self.rom_path == None:
            print(f"LevelParse:rompath is None! Set again")
        self.level_index  = lvlIdx
        self.width        = width
        self.height       = height
        self.offset       = offset 
        if self.offset == None:  
            self.setOffset(lvlIdx=lvlIdx)
        self.bubbles = []
        self.setBubbles(parse_rom(self.rom_path,start=self.offset.getHex(),distance=CONST_LEVEL_LENGTH))

    def __str__(self):
        return f"LevelParse: index={self.level_index}, offset={self.offset}, width={self.width}, height={self.height}, bubbles={self.bubbles} bubble_count={len(self.bubbles)}"

    def setOffset(self,lvlIdx:int=None):
        useIdx = lvlIdx if lvlIdx != None else self.level_index
        self.offset = LevelTableOffset(index=useIdx)

    def getOffsetInt(self):
        return self.offset.getInt()

    def getOffsetHex(self):
        return self.offset.getHex()

    def setBubbles(self,bubbles:list=None):
        self.bubbles = []
        if bubbles != None:
            for bubble in bubbles:
                if len(bubble) != 2:
                    print(f"Error: Bubble {bubble} is not a valid bubble. Must be a list of length 2.")
                    return
                else:
                    self.bubbles.append(bubble[0])
                    self.bubbles.append(bubble[1])

    def getBubblesAsAsciiDiagram(self):
        result  = "    1 2 3 4 5 6 7 8 \r\n"
        result += "   ----------------\r\n"
        bubIdx = 0
        for y in range(self.height+1):
            row = f"{y+1} | "
            rowlen = self.width
            if y % 2 == 1:
                row += " "
                spacer = " "
                rowlen = self.width - 1
            else:
                row += ""
                spacer = " "
                rowlen = self.width

            for x in range(rowlen):
                if bubIdx <= len(self.bubbles):
                    row += f"{self.bubbles[bubIdx]}{spacer}"
                    bubIdx += 1
                else:
                    row += f"?{spacer}"
            result += row + "\r\n"
        result += "   ----------------"
        return result