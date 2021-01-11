from gooey import Gooey, GooeyParser
import textwrap
import pandas as pd

@Gooey(program_name="Echem2csv", 
    program_description="Settings", 
    default_size=(650, 1000),
    progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
    progress_expr="current / total * 100",
    required_cols=1,
    menu=[{
        'name': 'Help',
        'items': [{
                'type': 'AboutDialog',
                'menuTitle': 'About',
                'name': 'Echem2csv',
                'description': '''\
 
Echem2csv reads .csv files containing two columns.

Input Sample with 2 header rows:
Column1         Column2
Title: Title
Label: i vs E (AUT50246)
Potential (V)   Current (A)
 
The Potential is converted into a unit specified and can be converted to SHE (Standard Hydrogen Electrode) values. The Current is converted into a unit specified, or a random factor can also be applied.
 
Finally a file is created and all Current columns are combined and saved. The columns header is chosen from the filename. The xAxis or first column with the Potential (mV) is chosen from the first file processed!

Output Sample:
Column 1                                             Column2     Column*
 Potential (mV) / Current (µA)   filename1   filename*
''',
                'version': '1.4',
                'copyright': 'Erik Breslmayr, 2020',
                'license': 'MIT'
         },{
        'type': 'Link',
        'menuTitle': 'Help',
        'menuTitle': 'Documentation',
        'url': 'https://github.com/riccstick/Echem2csv'
        }]
    }]
)

def main():
   
    parser = GooeyParser()
    parser.add_argument("Inputfiles", nargs='+', help='Choose input files in CSV format!', widget="MultiFileChooser")
    parser.add_argument("Outputfile", help='Choose where to save the output file.', default='Echem2Output.csv', widget="FileSaver")
    
    parser.add_argument("-she", "--SHE_convert", metavar='Potential Unit (SHE)', default="200", help='Factor converting to Standard Hydrogen Electrode Potential. Use 0 for skipping.')
    
    parser.add_argument("potential_convert", metavar='Potential Unit', default="mV", help='Choose Unit', choices=['V', 'mV', 'µV', 'nV','pV', 'Random factor'])

    parser.add_argument("current_convert", metavar='Current Unit', default="µA", help='Choose Unit', choices=['A', 'mA', 'µA', 'nA','pA', 'Random factor'])

    parser.add_argument("-head", "--headerlines", metavar='Headerrows', default="2", help='Select header rows to skip')
    
    parser.add_argument("-isep", "--inputseperator", metavar='Seperator for Inputfiles', default="space", choices=['tab', 'space', 'comma', 'dot','minus'])
    
    parser.add_argument("-osep", "--outputseperator", metavar='Seperator for Outputfile', default="comma", choices=['tab', 'space', 'comma', 'dot','minus'])

    parser.add_argument("-potValue", "--potential_convert_value", metavar='Potential random convert factor',help='Random factor e.g. 123')
    
    parser.add_argument("-curValue", "--current_convert_value", metavar='Current random convert factor',help='Random factor e.g. 123')
    
    args = parser.parse_args()
    
    if args.inputseperator == "tab":
        args.inputseperator = "\t"
    elif args.inputseperator == "space":
        args.inputseperator = " "
    elif args.inputseperator == "comma":
        args.inputseperator = ","
    elif args.inputseperator == "dot":
        args.inputseperator = "."
    elif args.inputseperator == "minus":
        args.inputseperator = "-"
    
    if args.outputseperator == "tab":
        args.outputseperator = "\t"
    elif args.outputseperator == "space":
        args.outputseperator = " "
    elif args.outputseperator == "comma":
        args.outputseperator = ","
    elif args.outputseperator == "dot":
        args.outputseperator = "."
    elif args.outputseperator == "minus":
        args.outputseperator = "-"
    
    headerlines = int(args.headerlines)
    
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
        elif args.potential_convert == "Random factor":
            xcolFactor = args.potential_convert_value
            xcolName = 'Potential (custom) / '
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
        elif args.potential_convert == "Random factor":
            ycolFactor = args.current_convert_value
            ycolName = 'Current (custom)'
        return ycolFactor, ycolName

    def xcolumn():
        with open(args.Inputfiles[0], 'r') as f:     
            data = pd.read_csv(f, sep=args.inputseperator, skiprows=headerlines, names = ['Potential', 'Current'])
            xcolNameNew = xpot[1] + ycur[1]
            data[xcolNameNew] = data['Potential'] * float(xpot[0]) + float(args.SHE_convert)
            x = data[xcolNameNew]
            return x
    
    def ycolumns(f):
        with open(f, 'r') as f:     
            data = pd.read_csv(f, sep=args.inputseperator, skiprows=headerlines, names = ['Potential','Current'])
            data[ycur[1]] = data['Current'] * float(ycur[0])
            y = data[ycur[1]]
            return y
    
    xpot = potCalc()
    ycur = curCalc()
    xycombo = xcolumn()

    for i in enumerate(args.Inputfiles):
        y = ycolumns(i[1])
        nameori = i[1].split('.')
        name = nameori[0].split('/')
        y = pd.concat([y], keys=[name[-1]], axis=1)
        num = i[0] + 1
        xycombo = pd.concat([xycombo, y], axis=1)
    
    xycombo.to_csv(args.Outputfile, sep=args.outputseperator, index=False)

    print("   Processed and combined " + str(num) + " files.")
    print("   Output file saved -> " + args.Outputfile)
    print("\n")

    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
