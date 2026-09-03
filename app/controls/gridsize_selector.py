import tkinter as tk
from tkinter import ttk

CONST_DEFAULT_CELL_SIZE = 24
GRID_SIZE_OPTIONS = [8, 16, 24, 32, 64]
CONST_GRIDSIZE_LABEL = "Grid size:"

class gridsize_selector():
    def __init__(self,parentFrame:tk.Frame=None):
        self.value = None
        self.element = None
        if parentFrame is None:
            print("gridsize_selector: No parent frame provided for grid size selector. Skipping grid size selector creation.")

        self.value = tk.IntVar(value=CONST_DEFAULT_CELL_SIZE)
        tk.Label(parentFrame, text=CONST_GRIDSIZE_LABEL).pack(side=tk.LEFT)
        
        self.element = ttk.Combobox(
            parentFrame,
            textvariable=self.value,
            values=GRID_SIZE_OPTIONS,
            width=4,
            state="readonly",
        )
        self.element.pack(side=tk.LEFT, padx=(4, 16))
    