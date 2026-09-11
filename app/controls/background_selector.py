from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
from app.controls.section import section

@dataclass
class Background:
    code: str
    description: str

DEFAULT_BACKGROUND = "Granite blocks"
BACKGROUND_TOTAL = [
    Background(code="00", description="Granite blocks"),
    Background(code="01", description="Starry sky"),
    Background(code="02", description="Bubbles"),
    Background(code="03", description="Cave"),
    Background(code="04", description="Trees / Forest"),
    Background(code="05", description="Stained Glass / Cathedral"),
    Background(code="06", description="Purple planet / cityscape?"),
    Background(code="07", description="Ocean"),
    Background(code="08", description="Egyptian ruins"),
    Background(code="09", description="Between two trees"),
    Background(code="0A", description="Flower field"),
    Background(code="0B", description="Inside barn with candles"),
    Background(code="0C", description="Palatial steps"),
    Background(code="0D", description="Clocks"),
    Background(code="0E", description="Gears and Chains"),
    Background(code="0F", description="Roses")
]
BACKGROUND_LOOKUP = {bg.description: bg.code for bg in BACKGROUND_TOTAL}
BACKGROUND_OPTIONS= [bg.description for bg in BACKGROUND_TOTAL]

class background_selector(section):
    def __init__(self,parentFrame:tk.Frame=None,r:int=0,c:int=0):
        super().__init__(name=self.__class__.__name__,parentFrame=parentFrame,r=r,c=c)

        self.selection = tk.StringVar(value=DEFAULT_BACKGROUND)
        self.value     = tk.StringVar(value=BACKGROUND_LOOKUP[DEFAULT_BACKGROUND])
        

        tk.Label(self.frame, text="Backgrounds:").grid(row=0, column=0)
        self.element = ttk.Combobox(
            self.frame,
            textvariable=self.selection,
            values=BACKGROUND_OPTIONS,
            width=max(len(opts) for opts in BACKGROUND_OPTIONS),
            state="readonly"
        )
        self.element.grid(row=0, column=1)
        background_name_label = tk.Label(self.frame, textvariable=self.value)
        background_name_label.grid(row=0, column=2)

    def on_changed(self, event,p:str):
        print(f"Background selection changed: {self.selection.get()} (triggered by {p})")
        selected_description = self.selection.get()
        selected_code = BACKGROUND_LOOKUP[selected_description]
        self.value.set(selected_code)
        self.selection.set(selected_description)
        