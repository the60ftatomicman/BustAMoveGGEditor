"""File import/export helpers built on PIL."""
from tkinter import filedialog
import binascii

def load_rom():
    """Prompt the user for a path and save `image`, optionally scaled up.

    Returns the chosen path, or None if the user cancelled.
    """
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("zip", "*.png"), ("All files", "*.*")],
    )
    if not path:
        return None
    return path

def parse_rom(fp:str,start:str="0x00000",distance:int=None):
    # Replace with the path to your actual .gg file
    try:
        with open(fp, "rb") as file:
            # Read the raw binary content
            raw_bytes = file.read()

            # Print the first 100 hex characters to peek inside
            start_idx    = int(start, 16)
            #print(start)
            distance = distance if distance != None and distance >= 1 else 1
            end_idx      = start_idx+distance
            #print(f"Reading hexes FROM:[{start} or {start_idx}] TO: [{distance} bytes or {end_idx}] ")
            raw_subbytes = raw_bytes[start_idx:end_idx]
            result = binascii.hexlify(raw_subbytes).decode('ANSI').upper()
            result_array = [result[i:i+2] for i in range(0, len(result), 2)]
            #print(result_array)
            return result_array
    except FileNotFoundError:
        print(f"Error: The file '{fp}' was not found.")

#parse_rom('E:\\EMU\\GENESIS\\aspectedit\\bustamoveGGeditor\\Bust-A-Move (USA).gg',start="0x3D59B",distance=35)