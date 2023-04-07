# Unit Converter in Tkinter

A simple converter GUI is created. It allows the selection of the type of units, and the units to convert from and convert to.

A module, Convert.py, is imported into the main program, Unit_Converter.py. It holds a dictionary containing the units and the values used to carry out a conversion equation. This module imports the Decimal class to use in the calculations.

A seperate function for converting temperature values is also inside of this module. The main program evaluates the unit type selected and sets the appropriate function as the conversion function.