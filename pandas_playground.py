"""In this file, you'll find some code that showcases the main functionalities of the 
Pandas library.

All student should play with the code in order to get a proper understanding of the library 
and use it correctly while implementing the ETL module.

When you run this file as a Python script, the Python interpreter 
executes the instructions after the 
statement if __name__ == "__main__": that you find at the bottom of the file.
"""

import pandas as pd
import sqlite3

#The Python module datetime defines the necessary types for manipulating 
# dates and times.
# Among these types, we find one called datetime (the same name as the module) 
# that is used to express a combination of date and time. 
from datetime import datetime

def get_right_date(input_date):
    """Gets a date as a string in the format mm/dd/yyyy and 
    returns that date as a string in the format "dd/mm/yyyy".

    Parameters
    ----------
        input_date : string
            The input date (in the format mm/dd/yyyy)

    Returns
    -------
        A string
            The input date in the format dd/mm/yyyy, or None if the input date is null.
    """
    
    # In case we have an empty string we return None
    if pd.isnull(input_date):
        return None

    # In order to convert the input date into the right format, we can use 
    # a function that is called "strftime() that is defined in the 
    # Python module datetime.
    # Unfortunately, this function cannot directly convert a string to another string;
    # but it can convert a variable of type "datetime" to a string.
    # Therefore, we must first convert the input_date from a string to a datetime object;
    # then, we can apply the function strftime() 
    # 
    # In order to turn the input date into a datetime object, the type "datetime" provides a function
    # called strptime() that takes in two arguments:
    # 
    # * First argument: a string containing a date.
    # * Second argumnet: a string describing the format of the date given in the first argument.
    # The format must be expressed according to a well-defined code.
    # For instance:
    # * %m indicates a month as a zero-padded decimal number (01, 02, ....);
    # * %y indicates a year without century as a zero-padded decimal number (19, 20, ...99);
    # * %Y indicates a year as a decimal number (2019, 2020)...
    # 
    # The complete list of the format codes can be found at the following address:
    # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    #
    # In the code below, the format "%m/%d/%Y" indicates that the date 
    # given in the first argument must be mm/dd/yyyy. 
    # If the date is not in this format  or the date is not valid (for instance, 
    # in the input file we find 11/31/2000), a ValueError exception is raised. 
    try:
        input_date = datetime.strptime(input_date, "%m/%d/%Y")
    except ValueError:
        return None
    
    # Now input_date is an object of type datetime.
    #  We finally convert the date to a string, enforcing the format that we want
    # that is dd/mm/yyyy.
    return input_date.strftime("%d/%m/%Y")

#
# Entry point of this module
#
if __name__ == "__main__" :

    ################### STEP 1: read a CSV file into a Pandas dataframe ###################

    # The function read_csv defined in the Pandas library takes as a parameter 
    # the path to a CSV file and loads its content into a dataframe.
    # It then returns that dataframe.
    # We can think of a dataframe as an in-memory table.
    # As a sample file, we use books.csv, an CSV file that you'll find in the directory
    # ./data.
    input_df = pd.read_csv("./data/books.csv", delimiter=';')

    # TODO: uncomment this line to print the dataframe input_df and execute the code.
    # In the output, the first column contains values that are not in the input CSV file.
    # It contains a row identifier added by Pandas that is called index.
    #print(input_df)

    ################### STEP 2: slicing ###################

    # We want to create a new dataframe called "books" that only contains the data in the columns
    # (bookID, title, authors, language_code, publication_date).
    # This operation is called SLICING.
    books = input_df[['bookID', 'title', 'authors', 'language_code', 'publication_date']]

    # TODO: uncomment this line to print the dataframe books and execute the code.
    #print(books)

    ################### STEP 3: find and replace ###################

    # If we look at the column language_code, the code for "English" is either "eng"
    # or "en-US". We want to replace both values with the code "en".
    # To this purpose, we invoked on the dataframe books the function "replace".
    # Let's see how we use this function.
    # 
    # We first create a dictionary, where:
    # * the keys are the words to replace (in our case, "eng" and "en-US");
    # * the values are the new words (in our case, "en").
    find_replace = {
    "eng": "en",
    "en-US": "en"
    }

    # Then, we create another dictionary, where:
    # * the key is the name of the column on which the function "replace" must be applied (in our case, "language_code")
    # * the value is the dictionary "find_replace" that we created before.
    columns_to_replace = {
    "language_code": find_replace
    }

    # Finally, we call the function replace on the dataframe books
    # The function replace takes as an argument the dictionary columns_to_replace.
    books = books.replace(columns_to_replace)

    # TODO: uncomment this line to print the dataframe
    # and execute the code to verify that we correctly replaced the intended values.
    #print(books)

    ################### STEP 4: removing duplicates ###################

    # We apply slicing to get a new dataframe "publishers" by only extracting the 
    # values in column "publisher" of the original dataframe.
    # Since a publisher may have published several books, its name appears 
    # multiple times in this dataframe.
    publishers = input_df['publisher']

    # TODO: uncomment the following line to see that 
    # publisher names are indeed repeated.
    # print(publishers)

    # We invoke the function drop_duplicates() on the dataframe
    # publishers to eliminate the redundant data.
    publishers = publishers.drop_duplicates()

    # TODO: uncomment the following line to see that 
    # publisher names are not repeated anymore.
    #print(publishers)

    ################### STEP 5: working with dates ###################
    
    # Looking at the input file, we notice that the dates in the publication_date column 
    # are in the format mm/dd/yyyy; we want to convert them into the format 
    # dd/mm/yyyy. 
    # To this extent, we need to iterate over all values in column publication_date and 
    # apply the conversion function get_right_date() that is defined in this Python file.
    # Dataframes provide a very useful function that is called map() that takes in a 
    # function (in our case, get_right_date), iterates over all values in the given 
    # dataframe portion (in our case, the column publication_date) and applies 
    # that function to each value. 
    # TODO: DON'T FORGET to read the comments of function get_right_date() defined above in this file
    # in order to understand how the dates are converted.
    books["publication_date"] = books["publication_date"].map(get_right_date)

    # TODO: uncomment the following line and verify that the dates respect the format 
    # dd/mm/yyyy
    #print(books['publication_date'])

    ################## STEP 6: importing into a database ###################

    # In order to import the values of one or more dataframes, we can use the Pandas function 
    # to_sql().
    # We first need to open a connection to a database.
    # If the database doesn't exist, it is created!
    database_file = "./data/books.db"
    conn = sqlite3.connect(database_file)
    print("Importing the data to the database")

    # Then, we need to call the function to_sql for each dataframe that we want to import.
    # Here we import the dataframe books and publishers that we created before:
    # The function to_sql takes in many parameters, but here we use only four:
    # * The name of the database table to which the dataframe will be imorted.
    # * The object used to connect to the database (conn).
    # * if_exists="append" means that if the target database table already exists, the data is appended
    # * to the existing content.
    # * index=False means that we don't want to import the Pandas row identifiers to our database.
    # 
    # TODO: uncomment the two following lines and execute the code
    #books.to_sql('Book', conn, if_exists="append", index=False)
    #publishers.to_sql('Publisher', conn, index=False)

    print("Done!")

    # TODO: after executing the code, open the file ./data/books.db with the DB Browser
    # for SQLite to verify that the two tables and the data are there.
    
    # We close the connection.
    conn.close()
