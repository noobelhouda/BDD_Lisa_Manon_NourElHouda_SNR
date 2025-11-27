"""Used to play with the code in order to learn the basics of Tkinter.

"""

# Import the library tkinter
import tkinter as tk
# Import the ttk widgets of tkinter
from tkinter import ttk
# Import the function configure_style
from gui_config import configure_style


###################### You'll copy here the code to play with ######################
window = tk.Tk()
window.title("Playground")


configure_style()


first_frame = ttk.Frame(window, style="Sample.TFrame")
first_label = ttk.Label(first_frame, text="First label", style="Sample.TLabel")
first_ent_var = tk.StringVar(value="")
first_text_field = ttk.Entry(first_frame, textvariable=first_ent_var)
first_button = ttk.Button(first_frame, text="First button")
first_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

first_text_field.pack()
first_button.pack()
first_frame.pack(expand=True, fill=tk.BOTH)
window.mainloop()


#####################################################################################
