import tkinter as tk
from tkinter import ttk

CONST_DEFAULT_CELL_SIZE = 24
GRID_SIZE_OPTIONS = [8, 16, 24, 32, 64]
CONST_GRIDSIZE_LABEL = "Grid size:"

class gridsize_selector():
    def __init__(self,parentFrame:tk.Frame=None,r:int=0,c:int=0):
        self.value   = None
        self.frame   = None
        self.element = None
        if parentFrame is None:
            print("gridsize_selector: No parent frame provided for grid size selector. Skipping grid size selector creation.")

        self.frame = tk.Frame(parentFrame)
        self.frame.grid(row=r, column=c)
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
    