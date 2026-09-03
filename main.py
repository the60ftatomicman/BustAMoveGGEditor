"""Entry point for the BustAMoveGGEditor application."""
from app.editor_app import EditorApp
from app.file_io.file_io import parse_rom
from app.file_io.level_parser import CONST_LEVEL_LENGTH
from app.file_io.level_parser import LevelParse
from app.file_io.palette_parser import PaletteParse

CONST_ROM_PATH = 'E:\\EMU\\GENESIS\\aspectedit\\bustamoveGGeditor\\Bust-A-Move (USA).gg'

def main():
    app = EditorApp()
    app.mainloop()
    #current_level = LevelParse(CONST_ROM_PATH, lvlIdx=2)
    #print(current_level.getBubblesAsAsciiDiagram())
    #pp = PaletteParse(rompath='E:\\EMU\\GENESIS\\aspectedit\\bustamoveGGeditor\\Bust-A-Move (USA).gg')


if __name__ == "__main__":
    main()
