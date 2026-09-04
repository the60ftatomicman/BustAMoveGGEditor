@dataclass
class JSONExport_Palette:
    color:any=[]
@dataclass
class JSONExport_Background:
    code:str="00"
    description:str="UnsetBackground"
@dataclass
class JSONExport_Level:
    index:int      = 0
    background:str = "00"
    bubbles:list   = []
@dataclass
class JSONExport_Game:
    timestamp:str    = ""
    rom_path:str     = ""
    palette:list     = []
    backgrounds:list = []
    levels:list      = []