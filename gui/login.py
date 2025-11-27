"""The login window.

Follow the instructions in the comments in order to create the login window.

READ THE CODE FROM TOP TO BOTTOM in order to read all the comments and understand the instructions.

"""

# Import the tkinter widgets.
import tkinter as tk
from tkinter import ttk

# Import the configuration of the SkisatiResa GUI.
import gui.gui_config as config

# Import the function open_main_window. This will be called if the login succeeds.
from gui.mainwindow import open_main_window

# Import the authentication module. This is used to check whether the username and the password
# are correct. For now, login and password are considered as correct if they're both "admin".
# We'll implement a more sophisticated version of the authorization module later.
import authentication as auth

# Import the utility functions.
import utils



"""
INSTRUCTION: The definition of global variables goes here. 
You can add as many as you need for the realization of the window.
"""

# The messages bundle.
messages_bundle = {}

# The language of the interface.
lang = None

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

# The root window.
window = None

# The entries in the login window.
entries = {}

# The control labels in the login window.
control_labels = {}

# The buttons in the login window.
buttons = {}

def open_login_window(_cursor, _conn, _messages_bundle, _lang):
    """Opens a new login window.

    This is the function that is called from file skisati.py to open the login window.
    THIS FUNCTION IS ALREADY IMPLEMENTED, BUT READ THE CODE AND THE COMMENTS TO UNDERSTAND WHAT IT DOES

    Parameters
    ----------
    _cursor : 
        The object used to query the database.
    _conn : 
        The object used to connect to the database.
    _messages_bundle : dictionary
        The messages bundle.
    _lang : string
        The language of the interface.
    """
    global messages_bundle
    global cursor
    global conn
    global window
    global lang
    
    # We assign the passed arguments to the global variables.
    messages_bundle = _messages_bundle
    cursor = _cursor
    conn = _conn
    lang = _lang

    # Creates the login window.
    window = tk.Tk()
    
    # Assigns a title to the window
    # NOTE: we don't hard-code the title, but instead we refer to it by using its key in the messages
    # bundle.
    window.title(messages_bundle["authentication_title"])
    
    # Load the icon image of the application. 
    # This function is already implemented in the file ./gui/gui_config.py
    icon = config.load_icon_image()
    
    # Assigns the icon to the window.
    # If you're on Windows, the icon will appear next to the title in the title bar. 
    # If you're on MacOS, the icon  will appear in the dock (the bar at the bottom of the 
    # screen showing the application icons). 
    # The same instruction is interpreted in two different ways by the underlying windows managers. 
    # This is a good example of how complicated is to provide a cross-platform widget toolkit!
    window.iconphoto(False, icon)
    
    # Set the window as non-resizable.
    window.resizable(False, False)

    # We configure the style of the window.
    config.configure_style()

    # We create a frame inside the window. This frame will contain all the widgets of the window.
    root_frame = ttk.Frame(window, style="Tab.TFrame")
    
    # We add a frame, called the credentials frame, that will contain:
    # 
    # * The label "Username".
    # * The text field to enter the username.
    # * The label "Password".
    # * The text field to enter the password.
    # The parent of this frame is the root frame.
    credentials_frm = ttk.Frame(root_frame, style="Tab.TFrame")

    # Call the function that creates the widgets in the credentials frame. 
    # This function is defined below in this file and you'll have to implement it.
    _credentials_frm_widgets(credentials_frm)
    
    # Create the message frame that will contain the label displaying messages 
    # to the user (in the figure, that's the label with the text "Enter the username (at least 5 characters)").
    message_frm = ttk.Frame(root_frame, style="Tab.TFrame")

    # Call the function that creates the widgets in the message frame.
    # This function is defined below in this file and you'll have to implement it.
    _message_frm_widgets(message_frm)

    # Creates the buttons frame. This frame will contain the buttons at the bottom of the 
    # window.
    buttons_frm = ttk.Frame(root_frame, style="Tab.TFrame")

    # Call the function that creates the widgets in the buttons frame.
    # This function is defined below in this file and you'll have to implement it.
    _buttons_frm_widgets(buttons_frm)
    
    # Adds the credentials, message and buttons frames to the root frame.
    # We add some extra space between them, so as to make the interface prettier. 
    credentials_frm.pack(fill="both", expand=True, padx=20, pady=10)
    message_frm.pack(fill="both", expand=True, padx=20, pady=10)
    buttons_frm.pack(fill="both", expand=True, padx=20, pady=10)

    # Adds the root frame to the window.
    root_frame.pack()

    # The login window is initially in the state INIT
    init_state()

    # Starts the event loop.
    window.mainloop()

def _credentials_frm_widgets(credentials_frm):
    """Creates the widgets in the credentials frame.

    The credentials frame will have to contain:

     * The label "Username".
     * The text field to enter the username.
     * The label "Password".
     * The text field to enter the password.

    Parameters
    ----------
    credentials_frm : ttk.Frame
        The credentials frame.
    """
    
    # The text of the label "Username".
    username_lbl_text = messages_bundle["username"]

    # The text of the label "password".
    password_lbl_text = messages_bundle["password"]

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    # TIP: when you create the text field to enter the password, you can use the argument 
    # show='*' of ttk.Entry() in order to hide the password while the user types it.
    
    username_lbl_text = messages_bundle["username"]
    password_lbl_text = messages_bundle["password"]

    #Tkinter Variable
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    # Label + Entry Username
    username_lbl = ttk.Label(credentials_frm, text=username_lbl_text)
    username_entry = ttk.Entry(credentials_frm, textvariable=username_var)

    # on fait un label + entry Password
    password_lbl = ttk.Label(credentials_frm, text=password_lbl_text)
    password_entry = ttk.Entry(credentials_frm, textvariable=password_var, show="*")

    # On stocke dans entries
    entries["username"] = (username_lbl, username_var)
    entries["password"] = (password_lbl, password_var)

    # on les place
    username_lbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    password_lbl.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    ####################################################################################
    

def _message_frm_widgets(message_frm):
    """Creates the widgets in the message frame.

    This frame will contain the label used to display messages to the user.

    Parameters
    ----------
    message_frm : ttk.Frame
        The message frame.
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    message_lbl = ttk.Label(message_frm, text=messages_bundle["enter_username"])
    control_labels["message"] = message_lbl
    message_lbl.pack()

    ####################################################################################

def _buttons_frm_widgets(buttons_frm):
    """Creates the widgets in the buttons frame.

    This frame will contain the buttons at the bottom of the window.

    Parameters
    ----------
    buttons_frm : ttk.Frame
        The buttons frame.
    """
    
    # Text in the button "Login".
    login_btn_text = messages_bundle["login"]

    # Text in the button clear.
    clear_btn_text = messages_bundle["clear_button"]

    # Text in the button cancel.
    cancel_btn_text = messages_bundle["cancel_button"]

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    # Boutons avec callbacks
    login_btn = ttk.Button(buttons_frm, text=login_btn_text, command=login)
    clear_btn = ttk.Button(buttons_frm, text=clear_btn_text, command=clear)
    cancel_btn = ttk.Button(buttons_frm, text=cancel_btn_text, command=cancel)

    # Enregistrer les boutons
    buttons["login"] = login_btn
    buttons["clear"] = clear_btn
    buttons["cancel"] = cancel_btn

    # Placement
    login_btn.pack(side="left", padx=10)
    clear_btn.pack(side="left", padx=10)
    cancel_btn.pack(side="right", padx=10)

    ####################################################################################

def init_state():
    """Sets the state of the widgets in the INIT_STATE.

    The password text field and the login button are disabled.
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    """INIT state : only username enabled, message: enter_username"""
    
    # username
    entries["username"][1].config(state="normal")
    
    # psw
    entries["password"][1].config(state="disabled")
    
    # boutton login
    buttons["login"].config(state="disabled")
    
    # message pour entrer le username
    control_labels["msg"].config(text=messages_bundle["enter_username"])
    
    ####################################################################################

def username_entered_state():
    """Sets the state of the widgets in the USERNAME_ENTERED_STATE.

    The login button is disabled.
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    pass

    ####################################################################################

def credentials_entered_state(message):
    """Sets the state of the widgets in the CREDENTIALS_ENTERED_STATE

    All widgets are enabled and the given message is written in the control label.

    Parameters
    ----------
    message: string
    The message to show in the control label.

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    pass

    ####################################################################################

def username_updated(*args):
    """Invoked when the user is typing the username.

    This function checks whether the current value in the username text field meets the validity
    constraints. Depeding on the result of the validity check and the current state, the window will
    transition to the appropriate state.

    Parameters
    ----------
    args :
        Arguments passed to the function by Tkinter when it is invoked as a callback.
        You can ignore them.

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    pass

    ####################################################################################

        
def password_updated(*args):
    """Invoked when the user is typing the password.

    This function checks whether the current value in the password text field meets the validity
    constraints. Depeding on the result of the validity check and the current state, the window will
    transition to the appropriate state.

    Parameters
    ----------
    args :
        Arguments passed to the function by Tkinter when it is invoked as a callback.
        You can ignore them.

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    pass

    ####################################################################################

def login():
    """Invoked when the user clicks on the button Login.

    The function calls auth.login_correct() to check whether the username and password typed by the user are correct.
    The function auth.login_correct() takes in as arguments:
    * The username
    * The password
    * The cursor (not used in the current implementation of the function, it will be used when we implement 
    the authentication module).

    The function returns a tuple:
    * (True, None, None) if the username and the password are correct (in the current implementation, the only correct
    combinatio is ("admin", "Adm1n!") ).

    * (False, USERNAME_NOT_FOUND, username) if the username doesn't exist.

    * (False, INCORRECT_PASSWORD, password) if the password is not correct.

    Use the return value of this function to take the proper action.
    """
    res = auth.login_correct(get_username(), get_password(), cursor)

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
# res est un tuple (ok, error_code, offending_value)
    ok, error_code, value = res

    if ok:
        # Identifiants corrects : on ouvre la fenêtre principale
        # puis on ferme la fenêtre de login
        control_labels["message"].config(text=messages_bundle["login_authorized"])
        # ouvrir la fenêtre principale
        open_main_window(cursor, conn, messages_bundle, lang)
        # fermer la fenêtre de login
        window.destroy()
    else:
        # Erreur : username inexistant ou mot de passe incorrect
        if error_code == auth.USERNAME_NOT_FOUND:
            control_labels["message"].config(text=messages_bundle["username_not_found"])
        elif error_code == auth.INCORRECT_PASSWORD:
            control_labels["message"].config(text=messages_bundle["incorrect_password"])
        else:
            # erreur inattendue (par sécurité)
            control_labels["message"].config(text=messages_bundle["unexpected_error"])
    ####################################################################################

def clear():
    """Invoked when the user clicks on the button Clear.

    This function needs to clear the text fields and return to the state INIT
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    #Vider les champs
    entries["username"][1].set("")
    entries["password"][1].set("")

    #Remettre le message initial
    control_labels["message"].config(text=messages_bundle["enter_username"])

    #Revenir à l'état INIT (désactiver widgets si implémenté dans init_state)
    init_state()


    ####################################################################################

def cancel():
    """Invoked when the user clicks on the button Cancel.
    
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    window.destroy()

    ####################################################################################
    
def get_username():
    """Returns the current value of the username.

    Returns
    -------
    string
        The current value of the username text field.
    """
    return entries["username"][1].get().strip()

def get_password():
    """Returns the current value of the password.

    Returns
    -------
    string
        The current value of the password text field.
    """
    return entries["password"][1].get().strip()