# Crestron Signal and Parameter Report

by Stephen Genusa, May 2017

Whenever I replace a symbol in a Crestron program and get the warning "Note: some programming may be lost", I get an uneasy feeling about what is occurring and whether I'll be regretting the action when a client calls to say something isn't working. 

I've always wanted a way to quickly compare the signals on a symbol with the signals for the symbol on an updated version of the program. This Python program is a good start. You can pipe the output to a text file for both versions of an SMW and do a compare, or do a quick visual compare. In a future version, I may take two SMW file name parameters and do a compare of all symbols against one another.

The program can
 
- List the symbols found in the SMW file with the -l parameter
- List the symbols and associated comments as arguments to be fed back into the  program using the -la parameter
- Search for a specific symbol with the -sc (symbol comment) and -sn (symbol name) parameters.

You end up with output showing you the symbol name, all connected input signal names, output signal names and parameters w/values

- Video Source Select : Symbol Analog Initialize found
- I1=[TP01]_SourceSelect_BluRay
- I2=[TP01]_SourceSelect_Satellite
- I3=[TP01]_SourceSelect_SecurityCam1_IL
- I4=[TP01]_SourceSelect_SecurityCam2_IL
- O1=[VideoSource]_Selected
- P1='1d'
- P2='2d'
- P3='3d'
- P4='4d'

I adapted some SMW parsing code from Philip Lawall's [https://github.com/fueller/Crestron-Python-Graph](https://github.com/fueller/Crestron-Python-Graph "Crestron Python Graph") code.
