#!/home/ricci/anaconda3/bin/python3

import argparse, textwrap
import pandas as pd

parser = argparse.ArgumentParser(
	prog='PROG',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent('''\
 +----------------+
 | Echem2csv_v1.0 |
 +----------------+
 by Erik Breslmayr, 2020
 
 - This program reads .csv files containing two columns.
 - Column A -> Potential (V); Column B -> Current (A)
 
 - The Potential is converted into mV and can be converted to SHE values.
 - The Current is converted into µA or nA, however a random factor can also be choosen.
 
 - Finally a file is created and all Currents are combined and saved.
 - Column A -> Potential (mV); Column B -> Current (µA); Column nth...

'''))

parser.add_argument("-i", "--infile", nargs='+', required=True, help='Specify input filename in csv format!')
parser.add_argument("-o", "--outfile", default="processedFile.csv", help='Optional: Specify output filename')

parser.add_argument("-she", "--SHE_convert", default="200", help='Specify factor to convert to Standard Hydrogen Electrode potential; default = 200')

parser.add_argument("-cur", "--current_convert", default="µA", help='Choose if converted to µA or nA; default = µA')

parser.add_argument("-curValue", "--current_convert_value", help='Specify a factor to convert e.g. 10')

parser.add_argument("-s", "--seperator", default=",", help='Optional: Choose seperator (e.g. tab); default is a comma ,')

args = parser.parse_args()

if args.seperator == "tab":
	args.seperator = "\t"

if args.current_convert == "µA":
    curFactor = 1000000
    colName = 'Current (µA)'
elif args.current_convert == "nA":
    curFactor = 1000000000
    colName = 'Current (nA)'
else:
    curFactor = args.curValue
    colName = 'Current (custom)'

def xcolumn():
    with open(args.infile[0], 'r') as f:     
        data = pd.read_csv(f, sep=',', header=1, names = ['Potential', 'Current'])
        data['Potential (mV)'] = data['Potential'] * 1000 + float(args.SHE_convert)
        x = data['Potential (mV)']
        return x
    
def ycolumns(f):
    with open(f, 'r') as f:     
        data = pd.read_csv(f, sep=',', header=1, names = ['Potential','Current'])
        data[colName] = data['Current'] * float(curFactor)
        y = data[colName]
        return y

xycombo = xcolumn()

for i in enumerate(args.infile):
    y = ycolumns(i[1])
    num = i[0] + 1
    xycombo = pd.concat([xycombo, y], axis=1)
    
xycombo.to_csv(args.outfile, sep=args.seperator, index=False)

print("+-------------------------------------------+")
print("   Processed and combined " + str(num) + " files.")
print("   Output filename: " + args.outfile)
print("+-------------------------------------------+")

    
    
    
    
    
    
    
    
    
    
