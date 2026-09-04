
from app.file_io.offset import UniversalOffset,BackgroundTableOffset
from app.file_io.level_parser import LevelParse,CONST_LEVEL_HEIGHT,CONST_LEVEL_WIDTH
from app.file_io.export_formats import JSONExport_Game
from app.data_structures.trackable_data import TrackableData

class Struct_Background:
    def __init__(self,index:int=None,offset:UniversalOffset=None,bgIdx:int=0):
        self.index      = index
        self.offset     = offset
        self.bgIdx      = TrackableData()
        self.bgIdx.data = bgIdx

class Struct_Level():
    def __init__(self,index:int=None,offset:UniversalOffset=None,background:Struct_Background=None,bubbles=None):
        # Static Elements
        self.index       = index
        self.offset      = TrackableData() # TODO -- why would THIS be different?
        self.offset.data = offset
        #Configuraable Elements
        self.bubbles     = TrackableData()
        self.bubbles.data = bubbles
        self.background  = TrackableData()
        self.background.data = background

    def getBubblesAsAsciiDiagram(self):
        bubbles = self.bubbles.data
        result  = "    1 2 3 4 5 6 7 8 \r\n"
        result += "   ----------------\r\n"
        bubIdx = 0
        for y in range(CONST_LEVEL_HEIGHT):
            row = f"{y+1} | "
            rowlen = CONST_LEVEL_WIDTH
            if y % 2 == 1:
                row += " "
                spacer = " "
                rowlen = CONST_LEVEL_WIDTH - 1
            else:
                row += ""
                spacer = " "
                rowlen = CONST_LEVEL_WIDTH

            for x in range(rowlen):
                if bubIdx <= len(bubbles):
                    row += f"{bubbles[bubIdx]}{spacer}"
                    bubIdx += 1
                else:
                    row += f"?{spacer}"
            result += row + "\r\n"
        result += "   ----------------"
        return result
    def __str__(self):
        rt  = f"---- Level [{self.index}]"
        rt += f"\r\n   Offsets(Modified? {self.offset.modified}): [{self.offset.data}]"
        rt += f"\r\nBackground(Modified? {self.background.modified}): [{self.background.data}]"
        rt += f"\r\n   Bubbles(Modified? {self.bubbles.modified}): [{self.bubbles.data}]"
        return rt
    
LEVEL_MIN = 1
LEVEL_MAX = 99
BACKGROUND_MIN = 1
BACKGROUND_MAX = 16

class Struct_Game():
    def __init__(self,rom_path:str=None):
        self.rom_path    = rom_path
        self.levels      = []
        self.palette     = []
        self.backgrounds = [] 
        self._setLevels()

    def _setLevels(self):
        self.levels = []
        for lvlidx in range(LEVEL_MIN,LEVEL_MAX+1):
            parsedLevel = LevelParse(rompath=self.rom_path,lvlIdx=lvlidx)
            parsedBG    = BackgroundTableOffset(index=lvlidx)
            self.levels.append(Struct_Level(index=lvlidx,offset=parsedLevel.offset,background=parsedBG,bubbles=parsedLevel.bubbles))

    def getLevelByIndex(self,index:int=1)->Struct_Level:
        if index < 1:
            print(f"Struct_Game: to print a level, use {CONST_LEVEL_MIN} -> {(CONST_LEVEL_MAX-1)}")
            return None
        else:
            return self.levels[index-1]

    def __str__(self):
        rt  = f"ROM [{self.rom_path}]"
        rt += f"\r\nCounts: Levels [{len(self.levels)}] Backgrounds: [{len(self.backgrounds)}] "
        rt += f"\r\nBackgrounds: [{self.backgrounds}]"
        rt += f"\r\nPalette: [{self.palette}]"
        rt += f"\r\nLevels are TOO verbose to list!"
        return rt

    def toJSON(self):
        rt = JSONExport_Game()
        rt.rompath = self.rom_path
        return rt
        
