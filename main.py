"""Entry point for the BustAMoveGGEditor application."""
from app.data_structures.game_structures import Struct_Game
from app.file_io.offset import UniversalOffset,PaletteTableOffset
from app.editor_app import EditorApp

def main():
    app = EditorApp()
    app.mainloop()
    #game = Struct_Game(CONST_ROM_PATH)
    #print(game)
    #for i in range(1,5):
    #    print(game.getLevelByIndex(i))


if __name__ == "__main__":
    main()
