import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from app.controls.section import section

DEFAULT_FILEPATH = ".\\"
ROM_FILETYPES = (
    ('ROM files', '*.gg'),
    ('All files', '*.*')
)
class rom_selector(section):
    def __init__(self,parentFrame:tk.Frame=None,r:int=0,c:int=0):
        self.options       = None
        self.value         = None
        self.frame         = None
        self.element_label = None
        self.element_input = None
        self.element_btn   = None
        if parentFrame is None:
            print("No parent frame provided for rom selector. Skipping rom selector creation.")
        else:
            self.value = tk.StringVar(value="")
            self.frame = tk.Frame(parentFrame)
            self.frame.grid(row=r, column=c,columnspan=3)
            
            self.element_label = tk.Label(self.frame, text="Rom File:")
            self.element_label.grid(row=0, column=0)

            self.element_input = ttk.Entry(self.frame,textvariable=self.value,state="readonly")
            self.element_input.grid(row=0, column=1)

            self.element_btn = ttk.Button(
                self.frame,
                text='Open a File',
                command=self.selectFile
            )
            self.element_btn.grid(row=0, column=2)
            
            
    def selectFile(self):
        fn = fd.askopenfilename(
            title='Open a ROM file',
            initialdir='/',
            filetypes=ROM_FILETYPES)
        self.value.set(fn)
        self.element_input.event_generate("<<RomChanged>>")
        
    def setRomPath(self,val:str=None):
        self.value.set(val)

    def getRomPath(self):
        return self.value.get()