from dataclasses import dataclass,field

@dataclass
class JSONExport_Palette:
    color:any = field(default_factory=list)
@dataclass
class JSONExport_Background:
    code:str        ="00"
    description:str ="UnsetBackground"
@dataclass
class JSONExport_Level:
    index:int      = 0
    background:str = "00"
    bubbles:list   = field(default_factory=list)
@dataclass
class JSONExport_Game:
    timestamp:str    = ""
    rom_path:str     = ""
    palette:list     = field(default_factory=list)
    backgrounds:list = field(default_factory=list)
    levels:list      = field(default_factory=list)