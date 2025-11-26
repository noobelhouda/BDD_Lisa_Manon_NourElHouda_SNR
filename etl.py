"""The ETL module.

Look at the instructions after the statement if __name__ == "__main__":

* First, we extract the data from the input CSV files into a collection of Pandas dataframes.
  Each dataframe corresponds to a table in the target relational database.
* Then, we transform the data in the dataframes.
* Finally, we load the data into the database.

"""

import pandas as pd
import sqlite3
import os
import db
import utils

from datetime import datetime


def extract():
    """Implementation of the extraction submodule.

    Returns
    -------
    dictionary
        The collection of dataframes containing the data of the input CSV files.
        You should have as many dataframes as tables in your relational database.
        Each dataframe corresponds to a table in the relational database.
        The dictionary contains a set of key-value pairs where
            * the value is a dataframe. 
            * the key is the name of the table corresponding to the dataframe  (e.g., "Student", "EmailAddress"...)
            
    """

    # This is the dictonary containing the collection of dataframes.
    # Each item of this dictionary is a key-value pair; the key is the name of a database table;
    # the value is a Pandas dataframe with the content of the table.
    dataframes = {}

    print("Extracting the data from the input CSV files...")

    ################## TODO: COMPLETE THE CODE OF THIS FUNCTION  #####################

    # Lire les CSV
    registrations_df = pd.read_csv("./data/student_registrations.csv", delimiter=";")
    memberships_df   = pd.read_csv("./data/student_memberships.csv", delimiter=";")

    #Construire les dataframes
    students_from_reg = registrations_df[["stud_number", "first_name", "last_name", "gender"]]
    students_from_mem = memberships_df[["stud_number", "first_name", "last_name", "gender"]]
    student_df = pd.concat([students_from_reg, students_from_mem], ignore_index=True)

    emails_from_reg = registrations_df[["stud_number", "email"]]
    emails_from_mem = memberships_df[["stud_number", "email"]]
    email_df = pd.concat([emails_from_reg, emails_from_mem], ignore_index=True)

    association_df = memberships_df[["asso_name", "asso_desc"]]
    membership_df  = memberships_df[["stud_number", "asso_name", "stud_role"]]

    skisati_df = registrations_df[["year", "registration_fee"]]
    registration_df = registrations_df[
        ["stud_number", "year", "registration_date", "payment_date", "registration_fee"]
    ]

    # Remplir le dictionnaire
    dataframes = {
        "Student": student_df,
        "EmailAddress": email_df,
        "Association": association_df,
        "Membership": membership_df,
        "SkisatiEdition": skisati_df,
        "Registration": registration_df,
    }

    ##################################################################################

    # Return the dataframe collection.
    return dataframes
    
def transform(dataframes):
    """Implementation of the transformation submodule.

    Parameters
    ----------
    dataframes : dictionary
        This is the dictionary returned by the function load()
    
    Returns 
    -------
    The input dictionary (after the transformations).
    """

    print("Transforming the data...")

    ################## TODO: COMPLETE THE CODE OF THIS FUNCTION  #####################
    #Implementation of the transformation submodule
    #On enlève d'abord les doublons

    #Student : un étudiant par stud_number
    student_df = dataframes["Student"]
    student_df = student_df.drop_duplicates(subset=["stud_number"])
    dataframes["Student"] = student_df

    #EmailAddress : un couple (stud_number, email) unique
    email_df = dataframes["EmailAddress"]
    email_df = email_df.drop_duplicates(subset=["stud_number", "email"])
    dataframes["EmailAddress"] = email_df

    #Association : une association par nom
    asso_df = dataframes["Association"]
    asso_df = asso_df.drop_duplicates(subset=["asso_name"])
    dataframes["Association"] = asso_df

    #SkisatiEdition : une ligne par année
    skisati_df = dataframes["SkisatiEdition"]
    skisati_df = skisati_df.drop_duplicates(subset=["year"])
    dataframes["SkisatiEdition"] = skisati_df

    #Membership et Registration : on ne supprime pas de lignes (les tailles attendues sont déjà OK)
    membership_df = dataframes["Membership"]
    dataframes["Membership"] = membership_df

    registration_df = dataframes["Registration"]

    #Normaliser la colonne gender dans Student : M / F
    student_df["gender"] = (
        student_df["gender"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    student_df["gender"] = student_df["gender"].replace({
        "m": "M",
        "h": "M",
        "homme": "M",
        "garçon": "M",
        "garcon": "M",
        "f": "F",
        "w": "F",
        "fille": "F",
        "woman": "F"
    })

    dataframes["Student"] = student_df

    #On remet les dates registration_date et payment_date en dd-mm-yyyy
    for col in ["registration_date", "payment_date"]:
        #conversion
        dt_series = pd.to_datetime(registration_df[col], errors="coerce")
        #format dd-mm-yyyy
        registration_df[col] = dt_series.dt.strftime("%d-%m-%Y")
        #remplacer NaN par chaîne vide
        registration_df[col] = registration_df[col].fillna("")

    dataframes["Registration"] = registration_df
    
    ##################################################################################

    # Returns the dataframe collection after the transformations.
    return dataframes

def load(dataframes):
    """Implementation of the load submodule.

    Parameters:
    ----------
    dataframes : dictionary
        The dictionary returned by the function extract()
    """
    # Loads the application configuration.
    app_config = utils.load_config()

    # Gets the path to the database file.
    database_file = app_config["db"]

    # You might bump into some errors while debugging your code which 
    # This might result in a database that is partially filled with some data.
    # Each time you rerun the ETL module, you want the database to be in the same state as when
    # you first created. 
    # The simpler solution here is to remove the database and recreate the tables back again.
    if os.path.exists(database_file):
        # If the database file already exists, we remove it.
        # In order to test the existence of a file, and to remove it, we use functions that are 
        # available in a Python module called "os".
        os.remove(database_file)
    
    # We open a connection to the database.
    conn = sqlite3.connect(database_file)

    # We get the cursor to query the database.
    cursor = conn.cursor()

    # We create the tables in the database, by using the function create_database that you implemented in the module
    # db.
    db.create_database(conn, cursor)

    print("Loading the data into the database...")
    
    ################## TODO: COMPLETE THE CODE OF THIS FUNCTION  #####################
    
    
    ##################################################################################

    print("Done!")
    
    # We close the connection to the database.
    cursor.close()
    conn.close()

# Entry point of the ETL module.
if __name__ == "__main__":

    ################## TODO: COMPLETE THE CODE OF THIS FUNCTION  #####################
    
    # Appeler extract()
    dataframes = extract()

    # Afficher les dataframes
    for name, df in dataframes.items():
        print(f"\n===== {name} =====")
        print(df)

    print("\n--- Before transformation (shapes) ---")
    for name, df in dataframes.items():
        print(f"{name}: {df.shape}")

    #Transformation
    dataframes = transform(dataframes)

    print("\n--- After transformation (shapes) ---")
    for name, df in dataframes.items():
        print(f"{name}: {df.shape}")

    #Afficher le contenu
    for name, df in dataframes.items():
        print(f"\n===== {name} =====")
        print(df)
    
    ##################################################################################
    