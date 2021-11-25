###############################################################################
# Fast furier transform
###############################################################################

# This example show how to use FFT class to make frequency spectrum analysis.
# This is done creating a fake input signal with noise and that doing FFT on that.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from math.fft import fft
from math import math

# Create a FFT object with 1024 inputs
nfft = 1024
furier = fft.FFT(nfft, is_real=True)

# Add dc component
dc = 0.6

# Create nfft inputs with two periodic signals and some noise
for num in range(nfft):
    r = math.sin(num/3) + math.cos(4*num) + dc + (random(-1000, 1000) / 1000)
    # Pass them to the FFT object
    furier[num]=r
# Compute the FFT
furier.fft()

# Get the amplitute array and print it
for i in range(furier.length):
    print(furier.amplitude(i)," ",sep="",end="")
print()

# Get the phases array and print it
for i in range(furier.length):
    print(furier.phase(i, 5)," ",sep="",end="")
print()

while True:
    sleep(1000)