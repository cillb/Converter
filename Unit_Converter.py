"""
This program creates a unit conversion app using tkinter. The Convert module is imported and the Convert
class is assigned to a variable. The dictionary in the Convert class containing the unit conversion
information is also assigned to a variable. When the type of unit is selected in the app, a partial function
is created of the conversion or temperature function in Convert, where the type of unit is a set parameter.
A second partial function is created from the initial partial function. The units are set as parameters when
they are selected. This means that a full conversion function is prepared with only a value to convert from
needing to be ran in the function. This allows the value to be converted more efficiently as it is entered
in the app.
"""
# import tools
from tkinter import *
from Convert import *
from functools import partial
from tkinter import font

root = Tk()
root.geometry("650x250")
root.wm_title("Unit Converter")
root.configure(background="#e6e6e6")

# assign the Convert class to a variable
conversion = Convert()
types_dict = conversion.types

# declare variables which will have partial functions assigned to them
conv_equation_type = None
conv_equation = None

# the string displayed in the unit types drop down menu
typeselected = StringVar()
typeselected.set("--Select the Type of Units--")

# the string displayed in the units drop down menus
defaultmessage = "--Select Units--"# the default message
unitsfromselected = StringVar()
unitstoselected = StringVar()
unitsfromselected.set(defaultmessage)
unitstoselected.set(defaultmessage)

# font settings for the drop down widgets and menus
font_style_widgets = font.Font(family="Calibri", size=11)
font_style_menus = font.Font(family="Calibri", size=9)
font_style_values = font.Font(family="Calibri", size=14)

# the unit type drop down menu button
unit_type_menu = Menubutton(root, textvariable=typeselected, anchor="w", bg="#ffffff", activebackground="#4da6ff", height=2, width=70, font=font_style_widgets)
unit_type_menu.grid(row=0, column=0, columnspan=5, pady=10, padx=20)
unit_type_menu.menutype = Menu(unit_type_menu, tearoff=0)
unit_type_menu["menu"] = unit_type_menu.menutype

# the units from drop down menu button
unit_from_menu = Menubutton(root, textvariable=unitsfromselected, anchor="w", bg="#ffffff", activebackground="#4da6ff", pady=7, height=1, width=30, font=font_style_widgets)
unit_from_menu.grid(row=2, column=0, columnspan=2,padx=20, sticky=E)
unit_from_menu.menufrom = Menu(unit_from_menu, tearoff=0)
unit_from_menu["menu"] = unit_from_menu.menufrom

# the units to drop down menu button
unit_to_menu = Menubutton(root, textvariable=unitstoselected, anchor="w", bg="#ffffff", activebackground="#4da6ff", pady=7, height=1, width=30, font=font_style_widgets)
unit_to_menu.grid(row=2, column=3, columnspan=2, padx=20, sticky=W)
unit_to_menu.menuto = Menu(unit_to_menu, tearoff=0)
unit_to_menu["menu"] = unit_to_menu.menuto

# add unit types options to the menu
for unittype in types_dict:
    unit_type_menu.menutype.add_cascade(label=unittype, font=font_style_menus, command=lambda p=unittype: select_unit_type(p))
unit_type_menu.grid()

# function ran by selecting a unit type
def select_unit_type(unit):
    global conv_equation_type# access one of the variables to take a partial function
    typeselected.set(unit)# set the type of unit displayed to the user
    unitsfromselected.set(defaultmessage)# reset the selected units when a unit type is selected
    unitstoselected.set(defaultmessage)
    fill_select_units(unit)# run this function based on the selected type of unit
    if typeselected.get() == "Temperature":# if temperature is selected, a different conversion method is needed
        conv_equation_type = partial(conversion.temperature, unit)
    else: conv_equation_type = partial(conversion.conversion, unit)# the conversion function will be ran with the unit type added to it already

# add unit options to the menus
def fill_select_units(unit):
    unit_from_menu.menufrom.delete(0, "end")# delete any existing items before adding new ones
    unit_to_menu.menuto.delete(0, "end")
    value_unit_from.delete(0, "end")# clear the input and display fields
    value_converted.config(text="")
    for unit_selected in types_dict[unit]:
        unit_from_menu.menufrom.add_cascade(label=unit_selected, font=font_style_menus, command=lambda x=unit_selected: select_units_from(x))
        unit_to_menu.menuto.add_cascade(label=unit_selected, font=font_style_menus, command=lambda y=unit_selected: select_units_to(y))
    unit_from_menu.grid()
    unit_to_menu.grid()

# function ran by selecting a unit to convert from
def select_units_from(unit):
    unitsfromselected.set(unit)# set the unit displayed to the user
    check_selections()# run a check
    if value_unit_from.get():
        display_conversion()

# function ran by selecting a unit to convert to
def select_units_to(unit):
    unitstoselected.set(unit)
    check_selections()# run a check
    if value_unit_from.get():
        display_conversion()

# function to check if a unit has been selected to convert to and from
def check_selections():
    global conv_equation# access the second variable to take a partial function
    if unitsfromselected.get() != defaultmessage and unitstoselected.get() != defaultmessage:
        # assign a partial function of the first partial function, so that only the unit value needs to be entered into the function
        conv_equation = partial(conv_equation_type, unitsfromselected.get(), unitstoselected.get())

# function ran when values are typed into input field, validates the input, then runs the conversion and displays value to the user
def display_conversion(*args):
    try:
        value = float(value_unit_from.get())# convert the value entered to a float object, will fail if input is invalid
        converted = float(conv_equation(value))# run conversion equation on value decimal values, trim any trailing zeros
        if converted == int(converted):
            converted = int(converted)
        value_converted.config(text=converted)# set the text of the converted value field
    except ValueError:# display error message for invalid input
        value_converted.config(text="Invalid Entry")

# add the unit value input field
value_unit_from = Entry(root, justify="right", bg="#ffffff", width=15, border=2, font=font_style_values)
value_unit_from.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky=SE)
value_unit_from.bind("<KeyRelease>", display_conversion)# the value is converted as it is entered

# add the converted unit value field
value_converted = Label(root, anchor="e", bg="#ffffff", height=1, width=15, border=2, font=font_style_values)
value_converted.grid(row=5, column=3, columnspan=2, padx=20, sticky=E)

root.mainloop()