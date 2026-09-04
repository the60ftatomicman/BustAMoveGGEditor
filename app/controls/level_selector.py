from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
from app.file_io.level_parser import LevelParse
from app.file_io.offset import BackgroundTableOffset
from app.data_structures.game_structures import LEVEL_MIN,LEVEL_MAX

## TODO -- do we want the level to be a levelParse or LevelOffset?
@dataclass
class Level:
    index: int
    level: LevelParse
    bgOffset: BackgroundTableOffset

DEFAULT_LEVEL = 1
class level_selector():
    def __init__(self,parentFrame:tk.Frame=None,rompath:str=None):
        self.options    = None
        self.selection  = None
        self.value      = None
        self.frame      = None
        self.name_label = None
        self.element       = None
        
        if parentFrame is None:
            print("No parent frame provided for level selector. Skipping level selector creation.")
        else:
            self.frame = tk.Frame(parentFrame)
            self.frame.pack(side=tk.LEFT, padx=(0, 16))
            self.options   = [Level(index=i, level=LevelParse(rompath,i), bgOffset=BackgroundTableOffset(index=i-1)) for i in range(LEVEL_MIN, LEVEL_MAX + 1)]
            self.selection = tk.IntVar(value=DEFAULT_LEVEL)
            self.value     = self.options[self.selection.get() - 1].level
            tk.Label(self.frame, text="Levels:").grid(row=0, column=0, sticky="w")
            self.element = ttk.Combobox(
                self.frame,
                textvariable=self.selection,
                values=[i for i in range(LEVEL_MIN, LEVEL_MAX + 1)],
                width=4,
                state="readonly",
            )
            self.element.grid(row=0, column=1, sticky="w", padx=(4, 0))

            self.name_label = tk.Label(self.frame, textvariable=self.selection, anchor="w")
            self.name_label.grid(row=1, column=0, columnspan=2, sticky="w")

    def on_changed(self, event, p:str):
        print(f"Level selection changed: {self.selection.get()} (triggered by {p})")
        self._setValue()

    def _setValue(self, level_index:int=None):
        selection = level_index if level_index is not None else self.selection.get()
        self.value = self.options[selection-1].level
        bg = self.options[selection-1].bgOffset
        self.selection.set(selection)
        print(f"Level {self.selection.get()}")
        print(f"Level Offsets: [{self.value.getOffsetHex()}, {self.value.getOffsetInt()}]")
        print(f"Level BG Offsets [{bg.getHex()}, {bg.getInt()}]")
        print(self.value.getBubblesAsAsciiDiagram())
