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

first_frm = ttk.Frame(window, style="Sample.TFrame")
ttk.Label(first_frm, text="Grid (0, 0)", style="Sample.TLabel").grid(row=0, column=0, padx=10, pady=10)
ttk.Label(first_frm, text="Grid (0, 1)", style="Sample.TLabel").grid(row=0, column=1, padx=10, pady=10)
ttk.Label(first_frm, text="Grid (1, 0)", style="Sample.TLabel").grid(row=1, column=0, padx=10, pady=10)
ttk.Label(first_frm, text="Grid (1, 1)", style="Sample.TLabel").grid(row=1, column=1, padx=10, pady=10)
first_frm.pack(expand=True, fill="both")

second_frm = ttk.Frame(window, style="SampleBottom.TFrame")
ttk.Label(second_frm, text="Grid (0, 0)", style="Sample.TLabel").grid(row=0, column=0, padx=10, pady=10)
ttk.Label(second_frm, text="Grid (0, 1)", style="Sample.TLabel").grid(row=0, column=1, padx=10, pady=10)
ttk.Label(second_frm, text="Grid (0, 2)", style="Sample.TLabel").grid(row=0, column=2, padx=10, pady=10)
second_frm.pack()

window.mainloop()

#####################################################################################
