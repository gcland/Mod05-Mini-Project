from connect_mysql import connect_database
from mysql.connector import Error
import re
import random

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

        def add_book(title, auth_id, genre_name, publish_date):
            isbn_set = {10}
            for i in range(1, 5):
                a = random.randint(1, 9)
                isbn_set.add(a)    
            isbn = random.choice(list(isbn_set))
            view_genre = (genre_name, )
            query = "Select * from Genres\nWHERE name = %s"
            cursor.execute(query, view_genre)
            conn.commit()
            for row in cursor.fetchall():
                genre_id = row[0]
            book_add = (title, auth_id, genre_id, isbn, publish_date)
            query = "Insert into Books (title, author_id, genre_id, isbn, publication_date) values (%s, %s, %s, %s, %s)"
            cursor.execute(query, book_add)
            conn.commit()
            print(f"New book: {title}, added successfully.")

        def book_search_name(title):
            view_book = (title, )
            query = "Select * from Books\nWHERE title = %s"
            cursor.execute(query, view_book)
            conn.commit()
            s = 0
            for row in cursor.fetchall():
                s+=1
                print(f"\nBook title: '{title}' found: ")
                print(f"Book ID#: {row[0]}, Book Title: {row[1]}, Author ID#: {row[2]}, Genre ID#: {row[3]}, ISBN: {row[4]}, Publication Date: {row[5]}")
                if row[6] == 1:
                    print("Availability: Checked-In")
                else:
                    print("Availability: Checked-Out")
            if s == 0:
                print(f"No book with name: {title} found.")

        def book_search_id(book_id):
            view_book = (book_id, )
            query = "Select * from Books\nWHERE id = %s"
            cursor.execute(query, view_book)
            conn.commit()
            s = 0
            for row in cursor.fetchall():
                s+=1
                print(f"\nBook ID#: {book_id} found: ")
                print(f"Book ID#: {row[0]}, Book Title: {row[1]}, Author ID#: {row[2]}, Genre ID#: {row[3]}, ISBN: {row[4]}, Publication Date: {row[5]}")
                if row[6] == 1:
                    print("Availability: Checked-In")
                else:
                    print("Availability: Checked-Out")
            if s == 0:
                print(f"No book with ID: {book_id} found.")

        def display_all_books():
            query = f"Select * from Books"
            cursor.execute(query)
            print(f"\nBooks table:")
            for row in cursor.fetchall():
                print(f"Book ID#: {row[0]}, Book Title: {row[1]}, Author ID#: {row[2]}, Genre ID#: {row[3]}, ISBN: {row[4]}, Publication Date: {row[5]}")

                if row[6] == 1:
                    print("Availability: Checked-In")
                else:
                    print("Availability: Checked-Out")

        def view_genre_name(genre_name):
            view_genre = (genre_name, )
            query = "Select * from Genres\nWHERE name = %s"
            cursor.execute(query, view_genre)
            conn.commit()
            s = 0
            for row in cursor.fetchall():
                s+=1
                print(f"Genre '{genre_name}' found: ")
                print(f"Genre ID#: {row[0]}, Genre Name: {row[1]}, Genre Category: {row[3]}\nGenre Description: {row[2]}.")
            if s == 0:
                print(f"No genre, '{genre_name}' found.")

        def view_genre_id(genre_id):
            view_genre = (genre_id, )
            query = "Select * from Genres\nWHERE id = %s"
            cursor.execute(query, view_genre)
            conn.commit()
            s = 0
            for row in cursor.fetchall():
                s+=1
                print(f"Genre ID#: {genre_id} found: ")
                print(f"Genre ID#: {row[0]}, Genre Name: {row[1]}, Genre Category: {row[3]}\nGenre Description: {row[2]}.")
            if s == 0:
                print(f"No genre with ID: {genre_id} found.")

        def view_genre_category(genre_category):
            view_genre = (genre_category, )
            query = "Select * from Genres\nWHERE category = %s"
            cursor.execute(query, view_genre)
            conn.commit()
            s = 0
            for row in cursor.fetchall():
                s+=1
                print(f"Genre '{genre_category}' found: ")
                print(f"Genre ID#: {row[0]}, Genre Name: {row[1]}, Genre Category: {row[3]}\nGenre Description: {row[2]}.")
            if s == 0:
                print(f"No genres with category: '{genre_category}' found.")
        
        def add_genre(genre_name, genre_details, genre_category):
            genre_add = (genre_name, genre_details, genre_category)
            query = "Insert into Genres (name, description, category) values (%s, %s, %s)"
            cursor.execute(query, genre_add)
            conn.commit()
            print(f"New Genre: '{genre_name}', added successfully.")
            
        def view_all_genres():
            query = f"Select * from Genres"
            cursor.execute(query)
            print(f"\nGenres table:")
            for row in cursor.fetchall():
                print(f"Genre ID#: {row[0]}, Genre Name: {row[1]}, Genre Category: {row[3]}\nGenre Description: {row[2]}.")
                
        def checkout_book():
            isbn = int(input("Enter ISBN of the book to check out: "))
            checkout_book = (isbn, )
            if type(isbn) is not int:
                raise TypeError(f"ISBN must be an integer.")
            query = "UPDATE Books\nSET\navailability = 0 WHERE ISBN = %s"
            cursor.execute(query, checkout_book)
            conn.commit()
            print(f"Book ISBN: {isbn} now checked out.")

        def checkin_book():
            isbn = int(input("Enter ISBN of the book to check in: "))
            checkin_book = (isbn, )
            if type(isbn) is not int:
                raise TypeError(f"ISBN must be an integer.")
            query = "UPDATE Books\nSET\navailability = 1 WHERE ISBN = %s"
            cursor.execute(query, checkin_book)
            conn.commit()
            print(f"Book ISBN: {isbn} now checked in.")

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

        def view_user(user_name): 
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
                print("\n1. User Operations\n2. Book Operations\n3. Author Operations\n4. Genre Operations\n5. Quit")
                choice_main = input("\nEnter selection: ")
                try:
                    if choice_main == '3':
                        while True:
                            print("\nAuthor Operations Menu:")
                            print("1. Add a new author\n2. View author details\n3. Display all authors\n4. Return")
                            choice = input("\nEnter selection: ")
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
                            print("1. Add a book\n2. Check-out a book\n3. Check-in a book\n4. Search for a book\n5. Display all books\n6. Return")
                            choice = input("\nEnter selection: ")
                            try: 
                                if choice == '1':
                                    title = input("Enter book title: ")
                                    auth_name = input("Enter book author: ")
                                    if type(auth_name) is int:
                                        raise TypeError(f"Name cannot be an integer.")
                                    view_auth = (auth_name, )
                                    query = "Select * from authors\nWHERE name = %s"
                                    cursor.execute(query, view_auth)
                                    conn.commit()
                                    s = 0
                                    for row in cursor.fetchall():
                                        s+=1
                                        print(f"\nAuthor '{auth_name}' found: ")
                                        print(f"Author ID#: {row[0]}, Author Name: {row[1]}, Biography: {row[2]}.")
                                    if s == 0:
                                        print(f"No author, '{auth_name}' found. Continue to add '{auth_name}' to database.")
                                        add_bio_choice = input(f"Add more books to {auth_name} biography? (yes/no) ")
                                        if add_bio_choice.lower() == "yes":
                                            biography = []
                                            print(f"\n{title}' added to {auth_name} biography.")
                                            biography.append(title)
                                            while True:
                                                bio_add = input(f"Enter books by {auth_name} to add to biography ('end' to finish.): ")
                                                if bio_add.lower() == "end":
                                                    break
                                                else:
                                                    biography.append(bio_add)
                                            add_author(auth_name, biography)
                                        else:
                                            biography = []
                                            biography.append(title)
                                            add_author(auth_name, biography)
                                    view_auth = (auth_name, )
                                    query = "Select * from authors\nWHERE name = %s"
                                    cursor.execute(query, view_auth)
                                    conn.commit()
                                    for row in cursor.fetchall():
                                        auth_id = row[0]
                                    while True:
                                        try:
                                            publish_date = input("Enter book publication date (YYYY-MM-DD): ")
                                            pattern_str = r'^\d{4}-\d{2}-\d{2}$'
                                            if re.match(pattern_str, publish_date):
                                                if int(publish_date[5]+publish_date[6]) > 12:
                                                    print("Incorrect date format (YYYY-MM-DD).")
                                                else:
                                                    break
                                            else:
                                                print("Incorrect date format (YYYY-MM-DD)")
                                        except Error as e:
                                            print(f"{e}.")
                                    print("\nChoose a genre for the book from the following list:\n(Genres can be added from the Main Menu, Genre Operations Menu) ")
                                    genre_name_table = []
                                    query = f"Select * from Genres"
                                    cursor.execute(query)
                                    conn.commit()
                                    print(f"\nGenres table:")
                                    for row in cursor.fetchall():
                                        print(row[1])
                                        genre_name_table.append(row[1])
                                    genre_input = input("\nEnter selection: ")
                                    if genre_input not in genre_name_table:
                                        raise Error ("Genre not in list of genres. Please add this genre in the genre menu.")
                                    else:
                                        add_book(title, auth_id, genre_input, publish_date)
                                elif choice =='2':
                                    checkout_book()
                                elif choice == '3':
                                    checkin_book()
                                elif choice =='4':
                                    print("\nChoose one of the following to search by: ")
                                    print("\n1. Book ID\n2. Book Title\n3. Return")
                                    book_choice = input("\nEnter selection: ")
                                    if book_choice == '1':
                                        book_id = input("Enter Book ID#: ")
                                        book_search_id(book_id)
                                    if book_choice == '2':
                                        book_title = input("Enter book title: ")
                                        book_search_name(book_title)
                                    else:
                                        break
                                elif choice == '5':
                                    display_all_books()
                                elif choice == '6':
                                    break
                            except Exception as e:
                                print(f"Error: {e}.")
                    elif choice_main == '1':
                        while True:
                            print("\nUser Operations Menu:")
                            print("1. Add a new user\n2. Search for user and details\n3. Display all users and details\n4. Return")
                            choice = input("\nEnter selection: ")
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
                        while True:
                            print("\nGenre Operations Menu:")
                            print("1. Add a new genre\n2. Search for a genre\n3. Display all genres\n4. Return")
                            choice = input("\nEnter selection: ")
                            try: 
                                if choice == '1':
                                    genre_name = input("Enter genre name: ")
                                    genre_details = input("Enter genre description: ")
                                    genre_category = input("Enter general category of genre: ")
                                    add_genre(genre_name, genre_details, genre_category)
                                elif choice =='2':
                                    print("\nChoose one of the following to search by: ")
                                    print("\n1. Genre ID\n2. Genre name\n3. Genre category\n4. Return")
                                    genre_choice = input("Enter selection: ")
                                    if genre_choice == '1':
                                        genre_id = input("Enter genre ID#: ")
                                        view_genre_id(genre_id)
                                    if genre_choice == '2':
                                        genre_name = input("Enter genre name: ")
                                        view_genre_name(genre_name)
                                    if genre_choice == '3':
                                        genre_category = input("Enter genre category: ")
                                        view_genre_category(genre_category)
                                    else:
                                        break
                                elif choice == '3':
                                    view_all_genres()
                                elif choice =='4':
                                    break
                            except Exception as e:
                                print(f"Error: {e}.")
                    elif choice_main == '5':
                        break
                except Exception as e:
                    print(f'Error: {e}.')
                finally:
                    print("\nThank you for using the Library Management System!")

        main()

    except Error as db_err:
        print(f"Error: {db_err}") 
    
    except Exception as e:
        print(f"Error: {e}") 
    
    finally:
        cursor.close()
        conn.close()
        print("MySQL connection is closed.")