# Conways Game of life

Implemented in python 3.11, using pygame to draw.
able to start from either a random generation or from a preset.

gosper glider (shown below) preset adapted from here:
https://github.com/matheusgomes28/pygame-life/blob/main/example_grids.py

this implementation includes a born (light green cells) an dying (dark red cells) state,
which i've found helps visualise the rules in action.

simulation starts paused, you can pause/unpause by hitting spacebar
clicking on a cell will set it to ALIVE, holding control while clicking sets it to DEAD
if you want to generate a preset you can set the preset field to in the main() World instance to EMPTY, draw out your shapes and hit return
the preset will print to the terminal and you can copy it you the presets file to use again later

![](media/conways3.GIF)