#!/usr/bin/env python

#######################################################################
# By Stephen Genusa
# May 2017
#
# Displays a list of inputs, outputs and parameters from a symbol
#
# Some parsing code adapted from 
# https://github.com/fueller/Crestron-Python-Graph/blob/master/test.py
#######################################################################

import argparse
from pprint import pprint
import re
import sys

class Signal:
    """docstring for Signal"""
    def __init__(self, signalStr):
        self.type = signalStr.get('SgTp', '1') # analog:2 , serial:4
        self.id = int(signalStr.get('H'))
        self.name = signalStr.get('Nm')

class Symbol:
    """docstring for Symbol"""
    def __init__(self, symbolStr):
        self.name = symbolStr.get('Nm')
        self.data = symbolStr
        

class CrestronSMWReport:
    
    
    def __init__(self, inputfilename, outputfilename, findsymbolname, listsymbols):
        self.SMWFilename = inputfilename
        self.outputfilename = outputfilename
        self.findsymbolname = findsymbolname
        self.listsymbols = listsymbols
    

    def parseSMW(self):
        with open(self.SMWFilename, 'r') as textfile:
            smwText = textfile.read()
        # Split the program into units [ ]
        regexresults = re.findall(r"\[\n(.*?)\n\]", smwText, re.DOTALL)
        progdata = []
        # Split the units into value=attribute
        for t in regexresults:
            obj1 = t.split('\n')
            obj = {}
            for o in obj1:
                if o == '':
                    continue
                else:
                    obj2 = o.split('=')
                    obj[obj2[0]] = obj2[1]
            progdata.append(obj)      
            
        # Split out by Object Type
        self.symbols = []
        self.signals = []
        for item in progdata:
            if 'ObjTp' not in item:
                continue
            if item['ObjTp'] == 'Sm':
                s = Symbol(item)
                self.symbols.append(s)
                #pprint(s)
            if item['ObjTp'] == 'Sg':
                s = Signal(item)
                self.signals.append(s)
        if self.listsymbols:
            print ("Symbol names found:")
            for symbol in self.symbols:
                print(symbol.name)
            sys.exit()
        #for signal in self.signals:
        #    pprint([signal.id, signal.name])
            
    def showReport(self):
        self.parseSMW()
        print()
        symbolfound = False
        for symbol in self.symbols:
            if symbol.name == self.findsymbolname:
                symbolfound = True
                print ("Symbol", self.findsymbolname, "found")
                if 'mI' in symbol.data:
                    maxinputs = int(symbol.data['mI'])
                else:
                    maxinputs = 0
                if 'mO' in symbol.data:
                    maxoutputs = int(symbol.data['mO'])
                else:
                    maxoutputs = 0
                if 'mP' in symbol.data:
                    maxparams = int(symbol.data['mP'])
                else:
                    maxparams = 0
                print ("Max Inputs", maxinputs)
                print ("Max Outputs", maxoutputs)
                print ("Max Parameters", maxparams)
                print ("=" * 50)
                for i in range(1, maxinputs + 1):
                    inputname = 'I' + str(i)
                    if inputname in symbol.data:
                        inputnumber = int(symbol.data[inputname])
                        match = next((l for l in self.signals if l.id == inputnumber), None)
                        if match:
                            print(inputname, "=", match.name)
                for i in range(1, maxoutputs + 1):
                    outputname = 'O' + str(i)
                    if outputname in symbol.data:
                        outputnumber = int(symbol.data[outputname])
                        match = next((l for l in self.signals if l.id == outputnumber), None)
                        if match:
                            print(outputname, "=", match.name)
                for i in range(1, maxparams + 1):
                    parametername = 'P' + str(i)
                    if parametername in symbol.data:
                        print(parametername, "='" + symbol.data[parametername] + "'")
        if not symbolfound:
            print ("Symbol name", self.findsymbolname, "was not found. Please check name and try again.")
        
        
def main():
    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='Report Signals on Symbol from SMW by Stephen Genusa - v0.70')
    parser.add_argument("-i", "--input", dest="inputfilename", default = "", help="Input filename", required=True)
    parser.add_argument("-l", "--list", dest="listsymbols", default = False, help="List symbol names", required=False, action='store_true')
    parser.add_argument("-s", "--symbol", dest="findsymbolname", default = "", help="Symbol name to report", required=False)   
    parser.add_argument("-o", "--output", dest="outputfilename", default = "", help="Output file. Currently this parameter ignored.", required=False)
    args = parser.parse_args()
    
    # Parse SMW and display signal report for symbol
    reporter = CrestronSMWReport(args.inputfilename, args.outputfilename, args.findsymbolname, args.listsymbols)
    reporter.showReport()

if __name__ == "__main__":
    main()