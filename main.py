"""Entry point for the BustAMoveGGEditor application."""
from app.data_structures.game_structures import Struct_Game
from app.file_io.offset import UniversalOffset,PaletteTableOffset
from app.editor_app import EditorApp

CONST_ROM_PATH = 'E:\\EMU\\GENESIS\\aspectedit\\bustamoveGGeditor\\Bust-A-Move (USA).gg'

def main():
    #app = EditorApp()
    #app.mainloop()
    #current_level = LevelParse(CONST_ROM_PATH, lvlIdx=2)
    #print(current_level.getBubblesAsAsciiDiagram())
    #pp = PaletteParse(rompath='E:\\EMU\\GENESIS\\aspectedit\\bustamoveGGeditor\\Bust-A-Move (USA).gg')
    game = Struct_Game(CONST_ROM_PATH)
    print(game)
    for i in range(1,5):
        print(game.getLevelByIndex(i))


if __name__ == "__main__":
    main()
