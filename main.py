import sqlite3

#Generates the DB and cursor objects as well as connecting to/initialising the ebookstore database object.
def db_generator():
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    return cursor, db # These used frequently so returned for passing into all later database related functions

#generates the books
def initial_table_data(cursor, db):
    cursor.execute(f"""CREATE TABLE books(id Integer PRIMARY KEY, Title TEXT, Author TEXT, QTY Integer)""")
    #inputting raw data
    id1 = 3001
    Title1 = "A Tale of Two Cities"
    Author1 = "Charles Dickens"
    Qty1 = 30

    id2 = 3002
    Title2 = "Harry Potter and the Philosophers Stone"
    Author2 = "J.K. Rowling"
    Qty2 = 40

    id3 = 3003
    Title3 = "The Lion, the Witch and the Wardrobe"
    Author3 = "C.S Lewis"
    Qty3 = 25

    id4 = 3004
    Title4 = "The Lord of the Rings"
    Author4 = "J.R.R Tolkien"
    Qty4 = 37

    id5 = 3005
    Title5 = "Alice in Wonderland"
    Author5 = "Lewis Carroll"
    Qty5 = 12

    #populating table with raw data
    book_entries = [(id1, Title1, Author1, Qty1),(id2, Title2, Author2, Qty2),(id3, Title3, Author3, Qty3),(id4, Title4, Author4, Qty4),(id5, Title5, Author5, Qty5),]
    cursor.executemany(f"""INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)""", book_entries)

    db.commit()

#useful to be able to immediadtley see changes to database, used more than once so func created.
def database_preview(cursor, db):
    readme = cursor.execute("SELECT * FROM books")
    for row in readme:
        print(row)

#Searching for a specific book
def search_for_book(cursor, db):
    search_by = input("\nWould you like to search by:"
                        "\n1.ID"
                        "\n2.Title"
                        "\n3.Author"
                        "\n4.Qty\n\n\t")

    #casting as int for synatx security
    if int(search_by) == 1:
        id_input_error = True

        #making sure the id number is as expected and ensuring correct with use of loop
        while id_input_error == True:
            search_id = input("Please enter the ID you wish to search for:")
            if search_id.isdigit() and len(search_id) == 4:
                id_input_error = False
            else:
                print("Please try that bit again.")

        #adding a try loop so the database doesnt crash out if no record is found.
        try:
            result = cursor.execute("SELECT * FROM books WHERE id =? ",(search_id,))

            #printing the selected item to console
            for row in result:
                print(row)
        except:
            print("that ID was not found.")

    elif int(search_by) == 2:
        search_title = input("Please enter the Title you wish to search for:")
        try:
            result = cursor.execute("SELECT * FROM books WHERE Title =? ",(search_title,))
            for row in result:
                print(row)
        except:
            print("that Title was not found.")


    elif int(search_by) == 3:
        search_author = input("Please enter the Title you wish to search for:")
        try:
            result = cursor.execute("SELECT * FROM books WHERE Author =? ",(search_author,))
            for row in result:
                print(row)
        except:
            print("that Author was not found.")

    elif int(search_by) == 4:
        search_qty = input("Please enter the Title you wish to search for:")
        qty_error = True
        while qty_error == True:
            if search_qty.isdigit():
                try:
                    result = cursor.execute("SELECT * FROM books WHERE Qty =? ",(search_qty,))
                    for row in result:
                        print(row)
                except:
                    print("that Author was not found.")

    else:
        print("Input not recognised - exiting to main menu")

#Checking the table exists
def check_for_table(cursor, db):
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books' ''')
    return cursor.fetchone()[0]

#function to enter new book details
def enter_book(cursor, db):
    id_input_error = True

    #while loop to ensure the book id matches the form of other book ID's
    while id_input_error == True:
        try:
            id = input("Please enter id:")
            if id.isdigit() and len(id) == 4:
                id_input_error = False
        except:
            print("Please try that bit again.")

    # no formatting check for title as it could be anything
    Title = input("Please enter book Title:")

    # no formatting check for author as it could be anything
    Author = input("Please enter book Author:")

    # while loop to ensure the book QTY is a number
    QTY_input_error = True
    while QTY_input_error == True:
        try:
            Qty = input("Please enter Qty:")
            if Qty.isdigit():
                QTY_input_error = False
        except:
            print("Please try that bit again.")

    #object ensures new data is passed to the table
    cursor.execute("INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)", (id,Title, Author, Qty))

    #commiting new objevt data to database
    db.commit()

#function to update existing book details
def update_book(cursor, db):

    #will be identifying books by ids
    existing_ids = []
    updating_error = True

    #generating a list of ids
    id_existing = cursor.execute("SELECT id FROM books")
    for row in id_existing:
        id = str(row).strip(",()")
        existing_ids.append(id)

    #UX improvement to show what options currently are
    print("\nID's currently available are:", existing_ids)

    # while loop to ensure the updating of book properties is in line with books properties
    while updating_error == True:
        update_id = input("Please Type the ID of the book you would like to update:")
        selected = cursor.execute("SELECT * FROM books WHERE id = ?", (update_id,))
        for row in selected:
            print(row)

        #ensuring we are selecting availabe IDS so as not to crash.
        if update_id in existing_ids:
            update_type = input("\nWould you like to update by:"
                                "\n1.ID"
                                "\n2.Title"
                                "\n3.Author"
                                "\n4.Qty\n\n\t")

            if int(update_type) == 1:
                new_id = input("Please enter the new ID CODE")

                #checking if new_id is a number and it is not longer than 4 and it doesnt not already assigned elsewhere
                if new_id.isdigit() and len(new_id) == 4 and new_id not in existing_ids:
                    cursor.execute(f"UPDATE books SET id = ? WHERE id = ?",(new_id,update_id))
                    db.commit()
                    updating_error = False # successful update, exit error loop
                else:
                    print("An error has occurred, please try again")


            elif int(update_type) == 2:
                new_title = input("Please enter the new Title")
                cursor.execute(f"UPDATE books SET Title = ? WHERE id = ?",(new_title,update_id))
                db.commit()
                updating_error = False # successful update, exit error loop

            elif int(update_type) == 3:
                new_author = input("Please enter the new Author")
                cursor.execute(f"UPDATE books SET Author = ? WHERE id = ?",(new_author,update_id))
                db.commit()
                updating_error = False # successful update, exit error loop

            elif int(update_type) == 4:
                new_qty = input("Please enter the new QTY")
                if new_qty.isdigit():
                    cursor.execute(f"UPDATE books SET Qty = ? WHERE id = ?",(new_qty,update_id))
                    db.commit()
                    updating_error = False # successful update, exit error loop
                else:
                    print("An error has occurred, please try again")

            #if a character other than 1,2,3,4 are selected, request retry as there is not other option.
            else:
                print("Input not recognised, please try again.")

        #if id input that is not currently in the list of ids, this message shows
        else:
            print("ID not currently assigned")

#small func to break to the large delete_book func for better troubleshooting
def id_list(cursor, db):
    existing_ids = []
    id_existing = cursor.execute("SELECT id FROM books")
    for row in id_existing:
        id = str(row).strip(",()")
        existing_ids.append(id)
    return existing_ids

#small func to break to the large delete_book func for better troubleshooting
def title_list(cursor, db):
    existing_titles = []
    id_existing = cursor.execute("SELECT Title FROM books")
    for row in id_existing:
        id = str(row).strip(",()")
        existing_titles.append(id)
    return existing_titles

#function to delete book details
def delete_book(cursor, db):

    delete_by_error = True

    #generating list objects to ensure we are not trying to delete item that do not exist
    existing_ids = []
    existing_titles = []

    # Starting a circular loop to require the correct user input for progression
    while delete_by_error == True:
        delete_by_type = input("Would you like to delete by:"
                               "\n1.ID"
                               "\n2.Title")

        if int(delete_by_type) == 1:
            existing_ids = id_list(cursor, db)

            #showcasing the current ID's as a UX upgrade
            print("ID's currently available are:", existing_ids)
            delete_id = input("Please enter ID you wish to delete:")

            #only attempt to delete if the id is currently in the datbase
            if delete_id in existing_ids:
                cursor.execute(f"DELETE FROM books WHERE id = '{delete_id}'")
                delete_by_error = False
                db.commit()
            else:
                print("ID not recognised")


        elif int(delete_by_type) == 2:
            existing_titles = title_list(cursor, db)

            # showcasing the current Titles as a UX upgrade
            print("Titles currently available are:", existing_titles)
            delete_title = input("Please enter Title you wish to delete:")

            # only attempt to delete if the id is currently in the database
            if delete_title in existing_titles:
                cursor.execute(f"DELETE FROM books WHERE Title = '{delete_title}'")
                delete_by_error = False
                db.commit()
            else:
                print("Title not recognised")


        else:
            print("Invalid selection, please try again")


if __name__ == "__main__":
    #generate db if not exist, or link database to sqlite3
    cursor, db = db_generator()

    #check if there is data in the table, if there is, do not re-try to add as there will be error
    table_present = check_for_table(cursor, db)
    if table_present == 0:
        initial_table_data(cursor, db)
    print("Welcome to the eBookstore Data Management Systems.")

    #activity loop to enable the user to keep using software until they decide to exit
    activity_loop = True
    while activity_loop == True:

        #action error is to help avoid crashing out due to input errors when making first choice
        action_error = True
        while action_error == True:

        #inputting action choice:
            try:
                action = int(input("\nPlease enter from the following choices:"
                                   "\n1. Enter Book"
                                   "\n2. Update Book"
                                   "\n3. Delete Book"
                                   "\n4. Search Books"
                                   "\n0. Exit\n\n\t"))

                if action < 5 and len(str(action)) == 1:
                    action_error = False
            except:
                pass


        if action == 0:
            print("Exiting now")
            #allowing activity loop to end and closing the program
            activity_loop = False


        elif action == 1:
            print("\nEntering book Details:")
            #all data entry is held inside function to nothing needs to be returned or input
            enter_book(cursor, db)


        elif action == 2:
            # all data entry is held inside function to nothing needs to be returned or input
            update_book(cursor, db)
            print("Following your changes, the Table now shows:")
            #Helpful to confirm the changes that have been made and allow user to see if other changes are required
            database_preview(cursor, db)


        elif action == 3:
            # all action is acheived inside function to nothing needs to be returned or input
            delete_book(cursor, db)


        elif action == 4:
            search_error = True
            while search_error == True:

                # inputting action choice:
                try:
                    search = int(input("\nWould you like to search for a specific or view all entries:"
                                       "\n1. Search"
                                       "\n2. View All"))

                    if search == 1 or search == 2:
                        search_error = False
                except:
                    pass
            if search == 1:
                search_for_book(cursor, db)
                # allowing activity loop to end and closing the program



            elif search == 2:
                print("\nEntering book Details:")
                # returning all table data
                database_preview(cursor, db)
                # allowing activity loop to end and closing the program



        else:
            print("Selection not recognised, Please try again.")











