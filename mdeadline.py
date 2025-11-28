"""The deadline module.
"""

import datetime
import sqlite3
import mregistration as mreg
import mstudent as mstud
import utils

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# The main window of the SkisatiResa application.
skisati_window = None

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

# Code indicating an unexpected database error.
UNEXPECTED_ERROR = 0

def deadline(registration_date):
    """Returns the payment deadline given the registration date.

    Parameters
    ----------
        registration_date : datetime
            The registration date.
    
    Returns
    -------
        datetime
            The deadline computed on the given registration date.
    """
    return (registration_date + datetime.timedelta(days=5)).date()


def deadline_expired(_registration_date):
    """Returns whether the payment deadline has expired for a given registration.

    Parameters
    ----------
    _registration_date : string
        The registration date (dd/mm/yyyy).
    
    Returns
    -------
    bool
        True if the deadline has expired, False otherwise.
    """
    registration_date = utils.get_date(_registration_date)
    if registration_date is not None:
        return (datetime.date.today() - deadline(registration_date)).days > 0
    
    return False

def deadline_aproaching(_registration_date):
    """Returns whether the deadline for the given registration is approaching (2 days before the deadline).

    Parameters:
    ----------
        _registration_date : string
            The registration date.
    
    Returns:
    --------
        bool
            True if today is 2 days before the deadline.

    """
    registration_date = utils.get_date(_registration_date)
    if registration_date is not None:
        return (deadline(registration_date) - datetime.date.today()).days == 2
    
    return False

def deadline_management_init(_skisati_window, _cursor, _conn):
    """Initializes the deadline management module.

    Parameters
    ----------
        _skisati_window : tk.Tk
            The main window of the application.
        _cursor : 
            The object used to query the database.
        _conn : 
            The object used to connect to the database.
    """
    global skisati_window
    global cursor
    global conn

    skisati_window = _skisati_window
    cursor = _cursor
    conn = _conn

def _unpaid_registrations():
    """Returns all the unpaid registrations.

    Returns
    -------
    list.
        The list of unpaid registrations. 
        Each item of the list is a tuple (stud_number, year, registration_date).
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    # 
    sql_query = "SELECT stud_number, year, registration_date FROM Registration WHERE payment_date IS NULL"
    try:
        # exécute la requête dans la base de données
        cursor.execute(sql_query)
        # récupère toutes les lignes de résultat
        return cursor.fetchall()
    except sqlite3.Error as e:
        # si il y a une erreur de base de données on l'affiche
        print(f"erreur de base de données pendant la recherche des non payés: {e}")
        # retourne une liste vide en cas d'erreur
        return []

    ####################################################################################

def _expired_registrations(unpaid_registrations):
    """Returns all the registrations that haven't met the payment deadline.

    Parameters
    ----------
    unpaid_registrations : list
        List of all the unpaid registrations. 
        This list is the one returned by the function _unpaid_registrations().

    Returns
    -------
    list
        The list of all the registrations that haven't met the payment deadline.
        Each item of the list is a tuple (stud_number, year, registration_date).
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########

    expired_regs = []
    # pour chaque inscription non payée (qui est un tuple stud_number, year, registration_date)
    for reg in unpaid_registrations:
        # la date d'inscription est le troisième élément (index 2)
        registration_date_str = reg[2]
        # on utilise la fonction déjà faite pour vérifier si la date limite est dépassée
        if deadline_expired(registration_date_str):
            # si c'est expiré on ajoute cette inscription à la liste
            expired_regs.append(reg)
            
    # retourne la liste des inscriptions expirées
    return expired_regs

    ####################################################################################
    
def _late_payment_registrations(unpaid_registrations):
    """Returns the registrations for which the payment deadline is two days from the current date.

    Parameters
    ----------
    unpaid_registrations : list
        List of all the unpaid registrations. 
        This list is the one returned the function _unpaid_registrations().

    Returns
    -------
    list
        The list of all the registrations for which the payment deadline is two days from the current date.
        Each item of the list is  tuple (first_name, email_address, registration_date)
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ################

    late_payment_regs = []
    
    # on parcourt toutes les inscriptions non payées
    for stud_number, year, registration_date_str in unpaid_registrations:
        # on vérifie si la date limite approche (dans 2 jours) avec la fonction prédéfinie
        if deadline_aproaching(registration_date_str):
            
            # requête pour trouver le prénom de l'étudiant son email et la date d'inscription
            # on fait une jointure entre registration student has et emailaddress
            sql_query = """
                SELECT 
                    T1.first_name, 
                    T3.email,
                    T0.registration_date
                FROM 
                    Registration AS T0
                INNER JOIN 
                    Student AS T1 ON T0.stud_number = T1.stud_number
                INNER JOIN 
                    has AS T2 ON T1.stud_number = T2.stud_number
                INNER JOIN
                    EmailAddress AS T3 ON T2.email = T3.email
                WHERE 
                    T0.stud_number = ? AND T0.year = ? AND T0.registration_date = ?
            """
            
            try:
                # exécute la requête pour cet étudiant et cette inscription
                cursor.execute(sql_query, (stud_number, year, registration_date_str))
                result = cursor.fetchone()
                
                if result:
                    # si on trouve les informations on les ajoute à la liste
                    late_payment_regs.append(result)
                    
            except sqlite3.Error as e:
                # gestion d'erreur si la requête échoue
                print(f"erreur de base de données lors de la récupération des détails de paiement tardif: {e}")

    # retourne la liste des inscriptions nécessitant un rappel
    return late_payment_regs

    ####################################################################################


def _remove_expired_registrations(expired_registrations):
    """Removes all the expired registrations from the database.

    IMPORTANT:

    * You can use the function delete_registration() defined in the registration module (file mregistration.py)

    * There is likely to be more than one expired registration. 
    You should remove all the expired registrations within a transaction.
    If any registration could not be deleted for any reason (look at the delete_registration return value), 
    you should rollback the transaction. Only if all the registrations could be successfully removed, 
    you can commit the transaction.

    Parameters
    ----------
    expired_registrations : list
        List of all the expired registrations. 
        This list is the one returned by the function _expired_registrations().

    Returns
    -------
    A tuple.
        The return value of the function mreg.delete_registration.
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ################

    successful_deletion = True
    
    # pour chaque inscription expirée on tente de la supprimer
    for stud_number, year, _ in expired_registrations:
        # on appelle la fonction de suppression du module mregistration
        # on suppose qu'elle renvoie (vrai/faux, code_erreur, données)
        res = mreg.delete_registration(stud_number, year, cursor, conn)
        
        # si la suppression a échoué (res[0] est faux)
        if not res[0]:
            successful_deletion = False
            # on arrête la boucle
            break
            
    # gestion de la transaction
    if successful_deletion:
        # si toutes les suppressions ont réussi on sauvegarde les changements
        conn.commit()
        # on retourne succès
        return (True, None, None) 
    else:
        # si une suppression a échoué on annule toutes les suppressions de la transaction
        conn.rollback()
        # on retourne le résultat de l'échec
        return res

    ####################################################################################

def _send_late_payment_reminder(late_payment_registrations):
    """Sends an automatic email to all students having late registrations.

    Parameters
    ----------
    _late_payment_registrations : list
        List of all the late registrations. 
        This list is the one returned by the function _late_payment_registrations().
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ###############

    # configuration smtp (à ajuster)
    smtp_server = "smtp.example.com"
    smtp_port = 587 
    sender_email = "skisatiresa@example.com"
    sender_password = "your_app_password" 

    try:
        # se connecter au serveur smtp en utilisant tls pour la sécurité
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            # pour chaque étudiant à qui envoyer un rappel
            for first_name, recipient_email, registration_date_str in late_payment_registrations:
                
                # charger le modèle de message de rappel
                # on suppose ici que load_config et load_messages_bundle sont définis
                config = utils.load_config()
                messages_bundle = utils.load_messages_bundle(config["bundle"] + config["lang"])
                
                body = messages_bundle["payment_reminder_email"].format(
                    first_name=first_name,
                    registration_date=registration_date_str,
                    deadline=deadline(utils.get_date(registration_date_str))
                )
                
                # créer l'email
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = "rappel de paiement pour votre inscription skisatiresa"
                msg.attach(MIMEText(body, 'plain'))

                # envoyer l'email
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print(f"rappel envoyé avec succès à {recipient_email} ({first_name})")
                
    except Exception as e:
        # si il y a une erreur lors de l'envoi d'email
        print(f"erreur lors de l'envoi d'email: {e}")

    ####################################################################################
     
def deadline_management():
    """Function invoked periodically to manage the unpaid registrations.
    
    * Retrieves the unpaid registrations
    * Identifies in the unpaid registrations those that are expired.
    * Identifies in the unpaid registrations those that are late.
    * Removes the expired registrations.
    * Sends a reminder to the students who have late registrations.

    This function is first invoked in the function  open_main_window in file 
    ./gui/mainwindow.py.
    The function is then  invoked once a day. 

    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ################

    print("--- lancement de la gestion des délais ---")
    
    # 1 récupère toutes les inscriptions non payées
    unpaid_regs = _unpaid_registrations()
    
    if not unpaid_regs:
        print("aucune inscription non payée trouvée arrêt")
        return

    # 2 identifie celles qui sont expirées
    expired_regs = _expired_registrations(unpaid_regs)
    
    # 3 identifie celles dont le paiement est en retard (rappel à envoyer)
    late_payment_regs = _late_payment_registrations(unpaid_regs)
    
    # 4 supprime les inscriptions expirées
    if expired_regs:
        print(f"suppression de {len(expired_regs)} inscriptions expirées...")
        res = _remove_expired_registrations(expired_regs)
        if res[0]:
            print("inscriptions expirées supprimées avec succès")
        else:
            print(f"échec de la suppression des inscriptions expirées: {res[1]}")
    else:
        print("aucune inscription expirée à supprimer")

    # 5 envoie un rappel pour les paiements en retard
    if late_payment_regs:
        print(f"envoi de rappels à {len(late_payment_regs)} étudiants pour paiement tardif...")
        _send_late_payment_reminder(late_payment_regs)
    else:
        print("aucun rappel de paiement tardif à envoyer")
        
    print("--- gestion des délais terminée ---")
    ####################################################################################
  