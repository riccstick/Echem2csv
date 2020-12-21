#!/usr/bin/python3

import argparse, textwrap
import pandas as pd

parser = argparse.ArgumentParser(
	prog='PROG',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent('''\
 +----------------+
 | Echem2csv_v1.3 |
 +----------------+
 by Erik Breslmayr, 2020
 
 Echem2csv reads .csv files containing two columns.

 Input Sample:
 Column1         Column2 
 Potential (V)   Current (A)
 
 The Potential is converted into a unit specified and can be converted to SHE (Standard Hydrogen Electrode) values. The Current is converted into a unit specified, or a random factor can also be applied.
 
 Finally a file is created and all Current columns are combined and saved. The columns header is chosen from the filename. The xAxis or first column with the Potential (mV) is chosen from the first file processed!

 Output Sample:
 Column 1                           Column2     Column*
 Potential (mV) / Current (µA)      filename1   filename*

 - Examples:
    Echem2csv.py -i file1.csv file2.csv 
    Echem2csv.py -i file?.csv -she 230 -cur nA 
    Echem2csv.py -i *.csv -cur 100000 -s tab
    
'''))

parser.add_argument("-i", "--Inputfiles", nargs='+', required=True, help='Specify input filenames in csv format!')
parser.add_argument("-o", "--Outputfile", default="Echem2Output.csv", help='Optional: Specify output filename')

parser.add_argument("-she", "--SHE_convert", default="200", help='Specify factor to convert to Standard Hydrogen Electrode potential; default = 200')

parser.add_argument("-pot", "--potential_convert", default="mV", help='Specify Unit (V, mV, µV, nV, pV; default = mV')

parser.add_argument("-cur", "--current_convert", default="µA", help='Choose if converted to µA or nA; default = µA')

parser.add_argument("-potValue", "--potential_convert_value", help='Random factor; e.g. 123')

parser.add_argument("-curValue", "--current_convert_value", help='Specify a factor to convert e.g. 123')

parser.add_argument("-head", "--headerlines", default="2", help='Optional: Choose how many header lines before measured data start; default is 2 lines')

parser.add_argument("-isep", "--inputseperator", default="\t", help='Optional: Choose seperator (e.g. tab); default is a comma tab')
parser.add_argument("-osep", "--outputseperator", default=",", help='Optional: Choose seperator (e.g. tab); default is a comma ,')

args = parser.parse_args()

if args.inputseperator == "tab":
	args.inputseperator = "\t"
if args.outputseperator == "tab":
        args.outputseperator = "\t"

headerlines = int(args.headerlines) - 1

def potCalc():
    if args.potential_convert == "V":
        xcolFactor = 1
        xcolName = 'Potential (V) / '        
    elif args.potential_convert == "mV":
        xcolFactor = 1000
        xcolName = 'Potential (mV) / '        
    elif args.potential_convert == "µV":
        xcolFactor = 1000000
        xcolName = 'Potential (µV) / '
    elif args.potential_convert == "nV":
        xcolFactor = 1000000000
        xcolName = 'Potential (nV) / '
    elif args.potential_convert == "pV":
        xcolFactor = 1000000000000
        xcolName = 'Potential (pV) / '
    else:
        xcolFactor = args.potential_convert_value
        xcolName = 'Potential (custom)'
    return xcolFactor, xcolName
        

def curCalc():
    if args.current_convert == "A":
        ycolFactor = 1
        ycolName = 'Current (A)'        
    elif args.current_convert == "mA":
        ycolFactor = 1000
        ycolName = 'Current (mA)'        
    elif args.current_convert == "µA":
        ycolFactor = 1000000
        ycolName = 'Current (µA)'
    elif args.current_convert == "nA":
        ycolFactor = 1000000000
        ycolName = 'Current (nA)'
    elif args.current_convert == "pA":
        ycolFactor = 1000000000000
        ycolName = 'Current (pA)'
    else:
        ycolFactor = args.current_convert_value
        ycolName = 'Current (custom)'
    return ycolFactor, ycolName

def xcolumn():
    with open(args.Inputfiles[0], 'r') as f:     
        data = pd.read_csv(f, sep=args.inputseperator, header=headerlines, names = ['Potential', 'Current'])
        xcolNameNew = xpot[1] + ycur[1]
        data[xcolNameNew] = data['Potential'] * float(xpot[0]) + float(args.SHE_convert)
        x = data[xcolNameNew]
        return x
    
def ycolumns(f):
    with open(f, 'r') as f:     
        data = pd.read_csv(f, sep=args.inputseperator, header=headerlines, names = ['Potential','Current'])
        data[ycur[1]] = data['Current'] * float(ycur[0])
        y = data[ycur[1]]
        return y
    
xpot = potCalc()
ycur = curCalc()
xycombo = xcolumn()

for i in enumerate(args.Inputfiles):
    y = ycolumns(i[1])
    name = i[1].split('.csv')
    y = pd.concat([y], keys=[name[0]], axis=1)
    num = i[0] + 1
    xycombo = pd.concat([xycombo, y], axis=1)
    
xycombo.to_csv(args.Outputfile, sep=args.outputseperator, index=False)

print("+-------------------------------------------+")
print("   Processed and combined " + str(num) + " files.")
print("   Output filename: " + args.Outputfile)
print("+-------------------------------------------+")

    
    
    
    
    
    
    
    
    
    
