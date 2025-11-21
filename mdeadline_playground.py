"""This file shows an example of how we implement a background task that is executed periodically.
It also shows how we send an email in Python.

#####################################################################

IMPORTANT: before you run this file, open a new terminal window and type the following command:

python -m smtpd -c DebuggingServer -n localhost:1025

This will start a simple SMTP server on your machine listening on port 1025

#####################################################################

When you execute this file as a Python script, the instructions in the main section of the file 
are run (see bottom of the file).
These instructions:

* Create a window and add a label to it.
* Start a background process (implemented in the function send_email) that connects to a SMTP server and 
sends an email.
* The background process is repeated every 5 seconds.

####################################################################################################
MAKE SURE YOU READ THE CODE AND THE COMMENTS TO LEARN HOW THESE OPERATIONS ARE IMPLEMENTED
####################################################################################################

"""

import tkinter as tk
from tkinter import ttk

# smtplib defines a SMTP client session object that is used to send 
# an email to a machine with a SMTP server.
import smtplib

# MIMEText is used to create MIME objects of type text. 
# MIME (Multipurpose Internet Mail Extensions) is an Internet standard that generalizes the format 
# of email messages to support non-ASCII characters.
from email.mime.text import MIMEText

# The main window of the application.
window = None

def send_email():
    """ This function sends an email to a specified recipient.
    This function is called every 5 seconds.
    """
    print("Sending an email....")
    
    # Connecting to the SMTP server. Here, the server runs on the local machine on 
    # port 1025.
    mail_server = smtplib.SMTP('localhost', 1025)

    # The text of the email.
    mail_text = '''Dear {}, 
This is just a test.
Sincerely, 
The Skisati Organizers'''

    # Creating the email in the MIME format.
    msg = MIMEText(mail_text.format("Clara"), 'plain')

    # Adding the sender, the subject and the recipient.
    msg['from'] = 'organization@skisati.fr'
    msg['Subject'] = 'Payment deadline reminder'
    msg['to'] = "clara.degas@etudiant.univ-rennes1.fr"

    # Sends the message to the SMTP server.
    mail_server.send_message(msg)

    # Call this function every 5 seconds (background process).
    window.after(5000, send_email)
    
    # Disconnect from the SMTP server
    mail_server.quit()


# Entry point of this module, executed when we execute this file as a Python script.
if __name__ == "__main__":

    # Create a window.
    window = tk.Tk()

    # Add a frame to the window.
    root_frm = ttk.Frame(window)

    label_text = '''This is a background process that sends automatic emails. 
Look at the terminal window where you launched the SMTP server
to verify that the email has been sent
'''
    # Adds a label
    ttk.Label(root_frm, text=label_text).pack()
    root_frm.pack()

    # Invoke the function send_email() when the application is launched.
    window.after(0, send_email)

    # Start the event loop
    window.mainloop()