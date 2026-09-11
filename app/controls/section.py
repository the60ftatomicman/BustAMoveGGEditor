import tkinter as tk

class section():
    def __init__(self,name:str="UnnamedWidget",parentFrame:tk.Frame=None,r:int=0,c:int=0,rspan=1,cspan=1):
        self.frame = None
        if parentFrame is None:
            print(f"No parent frame provided for {name}. Skipping {name} creation.")
        else:
            print(f"Appending section [{name}] to grid at row[{r}] column[{c}] rowspan[{rspan}] colspan[{cspan}]")
            self.frame = tk.Frame(parentFrame,borderwidth=2, relief="ridge")
            self.frame.grid(row=r, column=c,rowspan=rspan,columnspan=cspan,sticky="w")
            self.frame.columnconfigure(index=[0,1, 2, 3], weight=0)
            self.frame.rowconfigure(index=0)