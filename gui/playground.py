"""Used to play with the code in order to learn the basics of Tkinter.

"""

# Import the library tkinter
import tkinter as tk
# Import the ttk widgets of tkinter
from tkinter import ttk
# Import the function configure_style
from gui_config import configure_style


###################### You'll copy here the code to play with ######################

radio_buttons = {}
buttons = {}

def click_ok_handler():
    print("The user clicked OK")

def rb_selected(*args):
    current_value = radio_buttons["enable_disable"][2].get()
    if current_value == 'E':
        ok_enabled_state()
    elif current_value == 'D':
        ok_disabled_state()

def ok_enabled_state():
    buttons["OK"].configure(state=["!disabled"])
    print("The button is now enabled")

def ok_disabled_state():
    buttons["OK"].configure(state=["disabled"])
    print("The button is now disabled")

window = tk.Tk()
window.title("Playground")
configure_style()
first_frm = ttk.Frame(window, style="Tab.TFrame")

rb_value = tk.StringVar(value="")
rb_value.trace("w", rb_selected)
enable_rb = ttk.Radiobutton(first_frm, text='Enable', value='E', variable=rb_value)
disable_rb = ttk.Radiobutton(first_frm, text='Disable', value='D', variable=rb_value)
radio_buttons["enable_disable"] = (enable_rb, disable_rb, rb_value)
enable_rb.pack()
disable_rb.pack()

button = ttk.Button(first_frm, state="disabled", text="OK", command=click_ok_handler)
buttons["OK"] = button
button.pack()
first_frm.pack()
window.mainloop()

#####################################################################################
