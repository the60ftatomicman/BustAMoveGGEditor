"""Main application window for the pixel grid editor."""
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

from app.data_structures.game_structures import Struct_Game
from app.file_io.palette_parser import PaletteParse
from app.controls.background_selector import background_selector
from app.controls.level_selector import level_selector
from app.controls.rom_selector import rom_selector
from app.controls.gridsize_selector import gridsize_selector,CONST_DEFAULT_CELL_SIZE
from .canvas_grid import PixelGridCanvas
from .color_palette import ColorPalette

DEFAULT_GRID_ROWS    = 9
DEFAULT_GRID_COLUMNS = 8
DIMENSION_OPTIONS    = [8, 10, 16, 24, 32, 40, 48, 56, 64]

ROM_PATH = '.\\roms\\Bust-A-Move (USA).gg'

class EditorApp(tk.Tk):
    """Top-level tkinter application window."""

    def __init__(self):
        super().__init__()
        # Properties
        self.rom_path = ROM_PATH
        self.game = None

        # Build self
        self.title("BustAMove GG Editor")
        self.resizable(True, False)

        # Define the different frames that will hold different controls.
        self.frame_toolbar      = None
        self.frame_canvas       = None
        self.frame_statusbar    = None

        # Define the controls
        self.rom_select_control = None
        self.cellsize_control   = None
        self.background_control = None
        self.level_control      = None

        self._build_toolbar()
        #self._build_canvas()
        #self._build_statusbar()
        self.geometry('900x300')
        self.grid_propagate(False)

    def _build_toolbar(self):
        toolbar = tk.Frame(self, padx=8, pady=8,width=900)
        toolbar.grid(row=0,column=0)

        ## Converted over controls
        self.rom_select_control = rom_selector(toolbar)
        self.rom_select_control.element_input.bind("<<RomChanged>>",self._on_rom_changed)

        self.level_control = level_selector(parentFrame=toolbar,r=1,c=0,rompath=ROM_PATH)
        self.level_control.element.bind("<<ComboboxSelected>>", lambda event: self.level_control.on_changed(event, "Hackapoo"))

        self.background_control = background_selector(parentFrame=toolbar,r=1,c=1)
        self.background_control.element.bind("<<ComboboxSelected>>", lambda event: self.background_control.on_changed(event, "Hackapoo"))

        self.cellsize_control   = gridsize_selector(toolbar,r=2,c=0)
        self.cellsize_control.element.bind("<<ComboboxSelected>>", self._on_cell_size_changed)

        ## TBD
        #palette_frame = tk.Frame(self, padx=8)
        #palette_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 8))
        #self.palette_colors = PaletteParse(rompath=ROM_PATH)
        #self.palette = ColorPalette(palette_frame, on_color_selected=self._on_color_selected,colors=self.palette_colors.getPalettesAsRGBHex())
        #self.palette.pack(side=tk.LEFT)

        #clear_button = tk.Button(toolbar, text="Clear", command=self._on_clear)
        #clear_button.pack(side=tk.LEFT)

        #outline_button = tk.Button(toolbar, text="Outline color...", command=self._on_pick_outline_color)
        #outline_button.pack(side=tk.LEFT, padx=(8, 0))

        #canvas_bg_button = tk.Button(toolbar, text="Canvas background...", command=self._on_pick_canvas_bg_color)
        #canvas_bg_button.pack(side=tk.LEFT, padx=(8, 0))

    def _build_canvas(self):
        canvas_frame = tk.Frame(self, padx=8, pady=8)
        canvas_frame.pack(side=tk.TOP)
        self.grid_canvas = PixelGridCanvas(
            canvas_frame,
            rows=DEFAULT_GRID_ROWS,
            columns=DEFAULT_GRID_COLUMNS,
            cell_size=CONST_DEFAULT_CELL_SIZE,
        )
        self.grid_canvas.pack()
        #self.grid_canvas.set_current_color(self.palette.current_color)

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value=f"Grid: {DEFAULT_GRID_ROWS}x{DEFAULT_GRID_COLUMNS}")
        status = tk.Label(self, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_color_selected(self, color):
        self.grid_canvas.set_current_color(color)

    def _on_dimensions_changed(self, _event):
        #rows = self.rows_var.get()
        #columns = self.columns_var.get()
        self.grid_canvas.resize_grid(rows, columns)
        self.status_var.set(f"Grid: {rows}x{columns}")
        self._refresh_window_size()

    def _on_cell_size_changed(self, _event):
        cell_size = self.cellsize_control.value.get()
        self.grid_canvas.resize_grid(DEFAULT_GRID_ROWS, DEFAULT_GRID_COLUMNS, cell_size=cell_size)
        self.status_var.set(f"Cell size: {cell_size}px")
        self._refresh_window_size()

    def _on_rom_changed(self,_event):
        rp = self.rom_select_control.getRomPath()
        print(f"ROM file was changed to [{rp}]")
        self.game = Struct_Game(rp)
        print(self.game)

    def _on_clear(self):
        self.grid_canvas.clear()

    def _on_pick_outline_color(self):
        _rgb, hex_color = colorchooser.askcolor(
            color=self.grid_canvas.outline_color, title="Choose outline color"
        )
        if hex_color:
            self.grid_canvas.set_outline_color(hex_color)
            self.status_var.set(f"Outline color: {hex_color}")

    def _on_pick_canvas_bg_color(self):
        _rgb, hex_color = colorchooser.askcolor(
            color=self.grid_canvas["bg"], title="Choose canvas background color"
        )
        if hex_color:
            self.grid_canvas.set_canvas_bg_color(hex_color)
            self.status_var.set(f"Canvas background: {hex_color}")
