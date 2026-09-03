RAM:C105 = level index (confirmed)

_DATA_392B_ == background table.
00 == Granite blocks
01 == Starry sky
02 == Bubbles
03 == Cave
04 == Trees / Forest
05 == Stained Glass / Cathedral
06 ==  purple planet / cityscape?
07 == Ocean
08 == Egyptian ruins
09 == between two trees
0A == Flower field
0B == Inside barn with candles
0C == palatial steps
0D == Clocks
OE == Gears and Chains
OF == roses (Challenge Mode)
10 or greater == broken

# How graphics and ball data are stored #
everything from $A9 - $FF in the VDP are where we store the actual live layout of the map. These are dynamically created

_LABEL_31A_  - clears level

RAM D040 --- here is where we point the HL to outi and load our ball data

Who writes to d040?
a ton! but _LABEL_4C02 looks like it loads it with the data we WANT
TWIST! C400 == our true UNFILTERED ram location for the level layout. C4xx byte rows use the 15 bytes of the row to represent a level row. the 16th byte is skipped.
The index of the balls below do NOT map to the palette colors directly. but rather the tiles in the sprite index.
00 = empty
01 = black
02 = red
03 = yellow
04 = green
05 = purple
06 = orange
07 = blue
08 = light grey
09 = green again
0A = fire
0B = water
OC = lightening
OD = pop animation 1
0E = pop animation 2
OF = some gem looking one that never pops


_LABEL_43D2_ == we write the spheres out to c400 here.
we do so on the line under the call to _LABEL_44D2_.

We move the DE pointer to _RAM_C400_ under _LABEL_43AC_ so presummably this is important.


SHAZAM!
the _LABEL_43D2_ label is the importabt one. above all of the RRCA calls, we load the balls 2 at a time. High and low nibble == first than second ball.

9598 --- first ball I see loaded. is it 22? can I adjust it to say... 33?

YES!!!! AT 0F:959B (3D59B) we we see level one. it will load until it sees...FF!
All levels defined this way. 
THIS IS THE ANSWER!!!

$22 $33 $77 $44 $22 
$33 $77 $47 $74 $42
$23 $37 $44 $22 $33 
$00 $00 $00 $00 $00 
$00 $00 $00 $00 $00 
$00 $00 $00 $00 $00 
$00 $00 $00 $00 $FF



_LABEL_427_ = we dynamically set the VDP tile
    -> _LABEL_81B_  = label before 427
    -> _LABEL_4CCF_ = label before 81B
    -> _LABEL_47C9_ = label before 4ccF
        -> here we have a ton of aRAM checks
        -> the _RAM_D40_ spot doesn't control ball type


----------- Palette hunt -------
memory address 23,24 make our blue ball.
under _LABEL_3D5_ this is done
starting at 0F:A3A0 ---
we read furthest bit than closest. it's backwards.
it's 28 bytes, so lets map it out.
bytes 1-0 (0F:A3A6-0F:A3A5)   = white for scoreboard and orb accent
bytes 3-2 (0F:A3A8-0F:A3A7)   = BLUE for our orb
bytes 5-4 (0F:A3AA-0F:A3A9)   = GREEN for our orb and bub
bytes 7-6 (0F:A3AC-0F:A3AB)   = RED for our orb
bytes 9-8 (0F:A3AE-0F:A3AD)   = Yellow for our orb
bytes 11-10 (0F:A3B0-0F:A3AF) = Bronze for machine
bytes 13-12 (0F:A3B2-0F:A3B1) = Light Grey Orb
bytes 15-14 (0F:A3B4-0F:A3B3) = Dark Grey Orb
bytes 17-16 (0F:A3B4-0F:A3B3) = Purple Orb

RGB mapping
B1 B2
00 00
GR ?B

 1   2  
        bgr
$FF $0F FFF = WHITE
$00 $0F F00 = BLUE
$E0 $00 0E0 = GREEN
$0F $00 00F = RED
$EF $00 0EF = YELLOW
$BF $03 3BF 
$BB $0B BBB 
$55 $05 555 
$0A $0F F0A 
$90 $0F F90 
$7F $00 07F 
$59 $01 159 
$A0 $00 0A0 
$5D $00 05D = PURPLE