from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
from app.controls.section import section

DEFAULT_LEVEL = 1
##
## What I want out of this is:
## 1) to set options based on what the game_structure returns with as it's length for it's levels parameter.
## 2) That when this has it's selection changed, we also fire an event to change the BACKGROUND selector
## 3) Eventually we will do that with the bubbles as well.

class level_selector(section):
    def __init__(self,parentFrame:tk.Frame=None,r:int=0,c:int=0):
        super().__init__(name=self.__class__.__name__,parentFrame=parentFrame,r=r,c=c)

        self.options      = []
        self.value        = tk.IntVar()
        self.element      = None

        tk.Label(self.frame, text="Levels:").grid(row=0, column=0)
        self.element = ttk.Combobox(
            self.frame,
            textvariable=self.value,
            values=self.options,
            width=3,
            state="readonly",
        )
        self.element.grid(row=0, column=1, sticky="w", padx=(4, 0))

    def set_options(self,options:list=None):
        opts = options if options is not None else self.options
        self.options = [i for i in range(1, len(opts) + 1)]
        self.element['values'] = self.options
        self.value.set(DEFAULT_LEVEL)

    def on_changed(self,level_index:int=None):
        print(f"Level selection changed. Current: {self.value.get()} Override: {level_index}")
        value  = level_index if level_index is not None else self.value.get()
        self.value.set(value)
