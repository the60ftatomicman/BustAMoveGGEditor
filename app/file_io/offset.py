from enum import Enum
##
## Core
##
## Enum to determine the display / calc type
class OffsetType(Enum):
    Hex = 1
    Int = 2
## Universal base class for offsets. Can be used for any offset type, including level table offsets, background table offsets, etc.
class UniversalOffset:
    def __init__(self,offsetInt:int=None,offsetHex:str=None):
        if offsetInt == None and offsetHex == None:
            print(f"UniversalOffset:set the offsetInt or offsetHex")
        self.int = offsetInt
        self.hex = offsetHex
        if offsetInt == None and offsetHex != None:
            self.int = int(offsetHex, 16)
        if offsetHex == None and offsetInt != None:
            self.hex = f"{offsetInt:#X}"
    def __str__(self):
        return f"UniversalOffset: int={self.int}, hex={self.hex}"
    def getHex(self):
        return self.hex
    def getInt(self):
        return self.int
##
##
## Implementation classes for specific offsets, such as level table offsets and background table offsets.
## These are defined so that if we want to easily crawl through a data table, we can just define the index
## (usually the level number) and get the offset for that index. The starting offsets are defined in the constants below.
##
##

# This is used to find the bubble layout data, or "level" data.
class LevelTableOffset(UniversalOffset):
    CONST_LEVEL_LENGTH       = 35
    CONST_OFFSET_LEVEL_START = "0x3D59B"
    def __init__(self,index:int=None):
        if index == None:
            print(f"LevelTableOffset:set the index")
        offInt = int(self.CONST_OFFSET_LEVEL_START, 16) + (index * self.CONST_LEVEL_LENGTH)
        super().__init__(offsetInt=offInt, offsetHex=None)

# This is used to find the index of the background we use for a level
class BackgroundTableOffset(UniversalOffset):
    CONST_OFFSET_BG_LENGTH = 1
    CONST_OFFSET_BG_START = "0x0392B"
    def __init__(self,index:int=None):
        if index == None:
            print(f"BackgroundTableOffset:set the index")
        offInt = int(self.CONST_OFFSET_BG_START, 16) + (index * self.CONST_OFFSET_BG_LENGTH)
        super().__init__(offsetInt=offInt, offsetHex=None)
