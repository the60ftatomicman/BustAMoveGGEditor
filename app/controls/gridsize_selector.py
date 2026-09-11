import tkinter as tk
from tkinter import ttk
from app.controls.section import section

CONST_DEFAULT_CELL_SIZE = 24
GRID_SIZE_OPTIONS = [8, 16, 24, 32, 64]
CONST_GRIDSIZE_LABEL = "Grid size:"

class gridsize_selector(section):
    def __init__(self,parentFrame:tk.Frame=None,r:int=0,c:int=0):
        super().__init__(name=self.__class__.__name__,parentFrame=parentFrame,r=r,c=c)
        self.value   = None
        self.element = None

        self.value = tk.IntVar(value=CONST_DEFAULT_CELL_SIZE)
        tk.Label(self.frame, text=CONST_GRIDSIZE_LABEL).grid(row=0,column=0)
        
        self.element = ttk.Combobox(
            self.frame,
            textvariable=self.value,
            values=GRID_SIZE_OPTIONS,
            width=4,
            state="readonly",
        )
        self.element.grid(row=0,column=1)
    