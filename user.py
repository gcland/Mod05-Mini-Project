class User:
    def __init__(self, user_name, library_ID, borrowed_books):
        self.user_name = user_name
        self.library_ID = library_ID
        self.borrowed_books = borrowed_books

    def get_user_name(self):
        return self.user_name
    
    def get_library_ID(self):
        return self.library_ID

    def view_books(self):
        print(f"{self.user_name} borrowed books:")
        for book in self.borrowed_books:
            print(book)
        # return self.borrowed_books
    
    def get_user_details(self):
        print(f"\nUser name: {self.user_name}.")
        print(f"Library ID: {self.library_ID}.")
        self.view_books()
        
    def get_borrowed_books(self):
        return self.borrowed_books

    def borrow_book(self, borrowed_book):
        self.borrowed_books.append(borrowed_book)
        return self.borrowed_books
    
    def return_book(self, borrowed_book):
        self.borrowed_books.remove(borrowed_book)
        return self.borrowed_books