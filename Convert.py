"""
This module contains a single class, Convert. The class is used in the unit converter app to carry out the 
calculation to convert units. The Decimal class is imported to calculate using decimal objects instead of
the default float objects. Decimal objects can be better at producing results more true to what would be
expected to be shown to the user. This class sets the decimal precision to 12, and initialises a dictionary
that holds each unit type as the key, and a nested dictionary containing the units and a conversion factor
are the values. The keys for the nested dictionaries are the names of the units, and the units are assigned
a conversion factor, using a 'base' unit which will have a value of 1. The rest of the units are assigned
values that are pre-calculated so that they all satisfy the conversion equation:
        [value of unit from] * ( [conversion factor of unit from] / [conversion factor of unit to] )
The values should be accessed with dict[unit_type_name][unit_name].

A conversion function is created in the class. This should be used to carry out the conversion of all of the
units except for Temperature. The parameters it takes are the name of the type of units being converted, the
name of the unit that is being converted, the name of the unit that is being converted to, and the value of
the unit that is being converted. It accesses the initialised dictionary, and converts the values of the
conversion factors and the unit value to Decimal form, and makes the calculation.
"""
from decimal import Decimal, getcontext

class Convert:
    def __init__(self):
        getcontext().prec = 12# set decimal precision to 12
        self.types = {
            # factors based on square meter
            "Area": {"Square Kilometre": 1e06, "Square Metre": 1, "Square Centimetre": 1e-04,
                "Square Millimetre": 1e-06,"Square Mile": 2589988, "Square Yard": 1/1.19599, 
                "Square Foot": 9.290304e-02,"Square Inch": 6.4516e-04, "Hectare": 1e04, "Acre": 4840/1.19599},
            # factors based on megabits per second
            "Data Transfer Rate": {"Bit per Second": 1e-06, "Byte per Second": 8e-06,"Kilobit per Second": 1e-03, 
                "Kilobyte per Second": 8e-03, "Kibibit per Second": 1.024e-03,"Megabit per Second": 1, 
                "Megabyte per Second": 8, "Mebibit per Second": 1.048576,"Gigabit pe Second": 1e03, 
                "Gigabyte per Second": 8e03, "Gibibit per Second": 1073.741824,"Terabit per Second": 1e06, 
                "Terabyte per Second": 8e06, "Tebibit per Second": 1.0995116e06},
            # factors based on terabit
            "Digital Storage": {"Bit": 1e-12, "Kilobit": 1e-09, "Kibibit": 1.024e-09, "Megabit": 1e-06, 
                "Mebibit": 1.048576e-06,"Gigabit": 1e-03, "Gibibit": 1.07374e-03, "Terabit": 1, 
                "Tebibit":1.099511627776, "Petabit": 1e03, "Pebibit": 1125.9, "Exabit": 1e06, "Exbibit": 1152921.6, 
                "Zettabit": 1e09, "Yottabit": 1e12,"Byte": 8e-12, "Kilobyte": 8e-09, "Kibibyte": 8.192e-09, 
                "Megabyte": 8e-06, "Mebibyte": 8.388608e-06,"Gigabyte": 8e-03, "Gibibyte": 8.589934592e-03, 
                "Terabyte": 8, "Tebibyte": 8.796093, "Petabyte": 8e03, "Pebibyte": 9007.19925474, 
                "Exabyte": 8e06, "Exbibyte": 9.223372e06,"Zettabyte": 8e09, "Yottabyte": 8e12,},
            # factors based on joule
            "Energy": {"Joule": 1, "Kilojoule": 1000, "Gram Calorie": 4.184, "Kilocalorie": 4184, 
                "Watt Hour": 3600, "Kilowatt Hour": 3.6e06, "Electronvolt": 1.602176565e-19, 
                "British Thermal Unit": 1055.05585262, "US Therm": 1.054804e08, "Foot-Pound": 1.355817948},
            # factors based on hertz
            "Frequency": {"Hertz": 1, "Kilohertz": 1e03, "Megahertz": 1e06, "Gigahertz": 1e09},
            # factors based on kilometres per litre
            "Fuel Economy": {"Miles per Gallon": 0.425143707, "Miles per Gallon (Imperial)": 0.35400618997, 
                "Kilometres per Litre": 1, "Litre per 100 Kilometres": 100},
            # factors based on metre
            "Length": {"Kilometre": 1000, "Metre": 1, "Centimetre": 1e-02, "Millimetre": 1e-03, 
                "Micrometre": 1e-06, "Nanometre": 1e-09, "Mile": 1609.344, "Yard": 9.144e-01, 
                "Foot": 3.048e-01, "Inch": 2.54e-02, "Nautical Mile": 1852},
            # factors based on kilogram
            "Mass": {"Tonne": 1000, "Kilogram": 1, "Gram": 0.001, "Milligram": 1e-06, 
                "Microgram": 1e-09, "Imperial Ton": 1016.0469088, "US Ton": 907.18474, 
                "Stone": 6.35029318,"Pound": 0.45359237, "Ounce": 0.028349523125},
            # factors based on degree
            "Plane Angle": {"Arcsecond": 1/3600, "Degree": 1, "Gradian": 0.9, "Milliradian": 0.05729577951, 
                "Minute of Arc": 1/60, "Radian": 57.29577951},
            # factors based on pascal
            "Pressure": {"Atmosphere": 101325, "Bar": 1e05, "Newton per Square Millimeter": 1e-06, 
                "Pascal": 1,"Pound per Square Inch": 6894.757293, "Torr": 133.3223684},
            # factors based on metres per second
            "Speed": {"Kilometres per Hour": 1/3.6, "Metres per Second": 1,"Miles per Hour": 0.44704, 
                "Feet per Second":0.3048, "Knots": 0.514444444},
            # units do not use factors, see temperature function
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            # factors based on second
            "Time": {"Nanosecond": 1e-09, "Microsecond": 1e-06, "Millisecond": 1e-03, "Second": 1, "Minute": 60, 
                "Hour": 3600, "Day": 86400, "Week": 6.048e05, "Calendar Year": 3.1536e07, 
                "Decade": 3.1536e08, "Century": 3.1536e09},
            # factors based on litre
            "Volume": {"Cubic Metre": 1000, "Litre": 1, "Centilitre": 1e-02, "Millilitre": 1e-03, 
                "Cubic Foot": 28.31684659, "Cubic Inch": 0.016387064,"Imperial Gallon": 4.54609, 
                "Imperial Quart": 1.1365225, "Imperial Pint": 0.56826125,"Imperial Cup": 0.284130625, 
                "Imperial Fluid Ounce": 0.0284130625,"Imperial Tablespoon": 0.0177581714, 
                "Imperial Teaspoon": 0.00591939,"US Liquid Gallon": 3.785411784, "US Liquid Quart": 0.946353946, 
                "US Liquid Pint": 0.473176473, "US Cup": 0.25, "US Fluid Ounce": 0.0295735295625, 
                "US Tablespoon": 0.0147867478125, "US Teapoon": 0.00492892}
            }

    # function that carries out the conversion equation
    def conversion(self, unittype, fromunit, tounit, value):
        units = self.types[unittype]
        return Decimal(value) * (Decimal(units[fromunit]) / Decimal(units[tounit]))

    # function to convert temperature units
    def temperature(self, unittype, fromunit, tounit, value):
        if fromunit == "Celsius":
            if tounit == "Fahrenheit":
                return (Decimal(value) * Decimal(9/5)) + Decimal(32)
            elif tounit == "Kelvin":
                return Decimal(value) + Decimal(273.15)
            else: return Decimal(value)
        elif fromunit == "Fahrenheit":
            if tounit == "Celsius":
                return (Decimal(value) - Decimal(32)) * Decimal(5/9)
            elif tounit == "Kelvin":
                return ((Decimal(value) - Decimal(32)) * Decimal(5/9)) + Decimal(273.15)
            else: return Decimal(value)
        else:
            if tounit == "Celsius":
                return Decimal(value) - Decimal(273.15)
            elif tounit == "Fahrenheit":
                return ((Decimal(value) - Decimal(273.15)) * Decimal(9/5)) + Decimal(32)
            else: return Decimal(value)
