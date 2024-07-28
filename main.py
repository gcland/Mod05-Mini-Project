from connect_mysql import connect_database
from mysql.connector import Error
from book import Book
from book import NonFiction
from book import Fiction


conn = connect_database()
if conn is not None:
    try:
        cursor = conn.cursor(buffered=True)

        def add_author(auth_name, biography):   
            delimiter = ', '
            biog_string = delimiter.join(biography)
            new_author = (auth_name, biog_string)

            if type(auth_name) is int:
                raise TypeError(f"Name cannot be an integer.")
            
            query = "Insert into Authors (name, biography) values (%s, %s)"
            cursor.execute(query, new_author)
            conn.commit()
            print(f"New author: {auth_name}, added successfully. {auth_name} biography: {biog_string}.")

        def view_author(auth_name): 
            view_auth = (auth_name, )
            query = "Select * from authors\nWHERE name = %s"
            cursor.execute(query, view_auth)
            conn.commit()
            for row in cursor.fetchall():
                print(f"Author ID#: {row[0]}, Author Name: {row[1]}, Biography: {row[2]}.")
            update_choice = input(f"Would you like to update {auth_name} details? (yes/no) ")
            if update_choice.lower() == 'yes':
                name_bio = input("Update name or add to biography? ")
                if name_bio.lower() == "name":
                    auth_id = input("Enter author ID: ")
                    new_name = input("Enter new name: ")
                    if type(new_name) is int:
                        raise TypeError(f"Name cannot be an integer.")
                    updated_name = (new_name, auth_id)
                    query = "UPDATE Authors\nSET\nname = %sWHERE id = %s"
                    cursor.execute(query, updated_name)
                    conn.commit()
                    print(f"{auth_name} updated to: {new_name}.")

                if name_bio.lower() == "biography":
                    biography = ["", ]
                    while True:
                        bio_add = input(f"Enter book by {auth_name} to add to biography ('end' to finish.): ")
                        if bio_add.lower() == "end":
                            break
                        else:
                            biography.append(bio_add)
                    delimiter = ', '
                    biog_string = delimiter.join(biography)
                    query = "Select * from authors\nWHERE name = %s"
                    cursor.execute(query, view_auth)
                    conn.commit()
                    for row in cursor.fetchall():
                        new_bio = (row[2]+biog_string, auth_name)
                        query = "UPDATE Authors\nSET\nBiography = %s WHERE name = %s"
                        cursor.execute(query, new_bio)
                        conn.commit()
                        print(f"Author: {auth_name} biography updated with {biog_string[2]}.\nNew biography: {row[2]+biog_string}")
            

        def display_all_authors():  
            query = f"Select * from Authors"
            cursor.execute(query)
            print(f"\nAuthors table:")
            for row in cursor.fetchall():
                print(f"Author ID#: {row[0]}, Author Name: {row[1]}, Biography: {row[2]}.")

        def add_book(library):
            b = 0
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            publish_date = input("Enter book publication date: ")
            for a in library:
                b+=1
            isbn = b+1
            print(f"'{title}' ISBN: {isbn}.")
            genre_ask = input("Add genre details to this book? (yes/no) ")
            if genre_ask.lower() == "yes":
                fict = input("Is this book fiction or nonfiction? ")
                category = input("Enter genre of book: ")
                description = input("Enter a description of the book: ")
                if fict.lower() == 'fiction':
                    library[isbn] = Fiction(title, author, isbn, publish_date, category, description)
                    library[isbn].get_genrebook_details()
                elif fict.lower() == 'nonfiction':
                    library[isbn] = NonFiction(title, author, isbn, publish_date, category, description)
                    library[isbn].get_genrebook_details()
                else:
                    print("Invalid selection.")
            else:   
                library[isbn] = Book(title, author, isbn, publish_date)
                library[isbn].get_status()

        def book_search(library):
            try:
                choice = input("Search book by title or by ISBN? ")
                if choice.lower() == 'isbn':
                    isbn = int(input("Input book ISBN: "))
                    library[isbn].get_book_details()
                if choice.lower() == "title":
                    title = input("Input book title: ")
                    for isbn in library:
                        if title == library[isbn].get_title():
                            library[isbn].get_book_details()
            except Exception as e:
                print(f"Error: {e}.")

        def display_all_books(library, isbn, checked_out):
            int(isbn)
            print(f"\nTitle: {library[isbn].get_title()} by {library[isbn].get_author()}")
            print(f"Publish date: {library[isbn].get_publish_date()}")
            print(f"ISBN: {library[isbn].get_isbn()}")
            if library[isbn].get_status() == True:
                print(f"Availability: Checked-in")
            else:
                print(f"Availability: Checked-out with {checked_out[isbn]}")    

        def view_genre(library):
            for isbn in library:
                try:
                    library[isbn].get_genrebook_details()
                except:
                    library[isbn].get_book_details()

        def checkout_book(library, checked_out, users):
            isbn = int(input("Enter ISBN of the book to borrow: "))
            library_ID = int(input("Enter library ID: "))
            if isbn in library and library[isbn].borrow_book() and library_ID in users:
                users[library_ID].borrow_book(library[isbn].get_title())
                user_name = users[library_ID].get_user_name()
                checked_out[isbn] = user_name
                print(f"'{library[isbn].get_title()}' checked out with {user_name}.")
            else:
                print("Book checked-out, is not in library, or user ID incorrect.")

        def checkin_book(library, checked_out, users):
            isbn = int(input("Enter ISBN of the book to return: "))
            if isbn in library and isbn in checked_out:
                library[isbn].return_book()
                del checked_out[isbn]
                for library_ID in users:
                    if library[isbn].get_title() in users[library_ID].get_borrowed_books():
                        users[library_ID].return_book(library[isbn].get_title())
                print(f"Book '{library[isbn].get_title()}' checked-in.")
            else:
                print("Invalid ISBN or book is checked-in.")

        def add_user(user_name):
            library_ID = input("Enter library ID nickname: ")
            if type(library_ID) is int:
                raise TypeError(f"Library ID nickname cannot be an integer.")
            if type(user_name) is int:
                raise TypeError(f"Name cannot be an integer.")
            new_user = (user_name, library_ID)
            query = "Insert into Users (name, library_id) values (%s, %s)"
            cursor.execute(query, new_user)
            conn.commit()
            query = f"Select * from Users"
            cursor.execute(query)
            print(f"Users table:")
            for row in cursor.fetchall():
                print(f"User ID#: {row[0]}, User Name: {row[1]}, Library ID Nickname: {row[2]}.")

        def view_user(user_name): #Add option to search by Library_ID or user_ID?
            view_user = (user_name, )
            query = "Select * from Users\nWHERE name = %s"
            cursor.execute(query, view_user)
            conn.commit()
            for row in cursor.fetchall():
                print(f"User ID#: {row[0]}, User Name: {row[1]}, Library ID Nickname: {row[2]}.")
            update_choice = input(f"Would you like to update {user_name} details? (yes/no) ")
            if update_choice.lower() == 'yes':
                name_bio = input("Update name or library id nickname? ")
                if name_bio.lower() == "name":
                    user_id = input("Enter user ID: ")
                    new_name = input("Enter new name: ")
                    if type(new_name) is int:
                        raise TypeError(f"Name cannot be an integer.")
                    updated_name = (new_name, user_id)
                    query = "UPDATE Users\nSET\nname = %sWHERE id = %s"
                    cursor.execute(query, updated_name)
                    conn.commit()
                    print(f"{user_name} updated to: {new_name}.")
        
                if name_bio.lower() == "library id nickname" or name_bio.lower() == "id":
                    user_id = input("Enter user ID: ")
                    new_libID = input("Enter new Library ID Nickname: ")
                    if type(new_libID) is int:
                        raise TypeError(f"Name cannot be an integer.")
                    updated_name = (new_libID, user_id)
                    query = "UPDATE Users\nSET\nlibrary_id = %sWHERE id = %s"
                    cursor.execute(query, updated_name)
                    conn.commit()
                    print(f"{user_name}: Library ID Nickname updated to: {new_libID}.")

        def display_users():
            query = f"Select * from Users"
            cursor.execute(query)
            print(f"Users table:")
            for row in cursor.fetchall():
                print(f"User ID#: {row[0]}, User Name: {row[1]}, Library ID Nickname: {row[2]}.")

        def main():
            print("\nWelcome to the Library Management System!")
            while True:
                print("\nLibrary Management System Main Menu:")
                print("\n1. User Operations\n2. Book Operations\n3. Author Operations\n4. Quit")
                choice_main = input("Enter selection: ")
                try:
                    if choice_main == '3':
                        while True:
                            print("\nAuthor Operations Menu:")
                            print("1. Add a new author\n2. View author details\n3. Display all authors\n4. Return")
                            choice = input("Enter selection: ")
                            try: 
                                if choice == '1':
                                    auth_name = input("Enter author name: ")
                                    biography = []
                                    while True:
                                        bio_add = input(f"Enter book by {auth_name} to add to biography ('end' to finish.): ")
                                        if bio_add.lower() == "end":
                                            break
                                        else:
                                            biography.append(bio_add)
                                    add_author(auth_name, biography)
                                elif choice == '2':
                                    auth_name = input("Enter author name to search: ")
                                    view_author(auth_name)
                                elif choice == '3':
                                    display_all_authors()
                                elif choice =='4':
                                    break
                            except Exception as e:
                                print(f"Error: {e}.")
                    if choice_main == '2':
                        while True:
                            print("\nBook Operations Menu:")
                            print("1. Add a book\n2. Check-out a book\n3. Check-in a book\n4. Search for a book\n5. View genre details of all books\n6. Display all books\n7. Return")
                            choice = input("Enter selection: ")
                            try: 
                                if choice == '1':
                                    add_book(library)
                                elif choice =='2':
                                    checkout_book(library, checked_out, users)
                                elif choice == '3':
                                    checkin_book(library, checked_out, users)
                                elif choice =='4':
                                    book_search(library)
                                elif choice == '5':
                                    view_genre(library)
                                elif choice == '6':
                                    for isbn in library:
                                        display_all_books(library, isbn, checked_out)
                                elif choice == '7':
                                    break
                            except Exception as e:
                                print(f"Error: {e}.")
                    elif choice_main == '1':
                        while True:
                            print("\nUser Operations Menu:")
                            print("1. Add a new user\n2. Search for user and details\n3. Display all users and details\n4. Return")
                            choice = input("Enter selection: ")
                            try: 
                                if choice == '1':
                                    user_name = input("Enter user name: ")
                                    add_user(user_name)
                                elif choice =='2':
                                    user_name = input("Enter user name: ")
                                    view_user(user_name)
                                elif choice == '3':
                                    display_users()
                                elif choice =='4':
                                    break
                            except Exception as e:
                                print(f"Error: {e}.")
                    elif choice_main == '4':
                        break
                except Exception as e:
                    print(f'Error: {e}.')
                finally:
                    print("Thank you for using the Library Management System!")

        main()

    except Error as db_err:
        print(f"Error: {db_err}") 
    
    except Exception as e:
        print(f"Error: {e}") 
    
    finally:
        cursor.close()
        conn.close()
        print("\nMySQL connection is closed.")