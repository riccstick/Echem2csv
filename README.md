# Echem2csv
- python3 script to combine csv data
## Required modules
- argparse, textwrap, pandas

## Description
- This program reads .csv files containing two columns.
- Column A -> Potential (V); Column B -> Current (A)

- The Potential is converted into mV and can be converted to SHE values.
- The Current is converted into µA or nA, however a random factor can also be choosen.

- Finally a file is created and all Currents are combined and saved.
- Column A -> Potential (mV); Column B -> Current (µA); Column nth...
