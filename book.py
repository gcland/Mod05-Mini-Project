class Book:
    def __init__(self, title, author, isbn, publish_date):
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__publish_date = publish_date
        self.__is_available = True

    def get_title(self):
        return self.__title

    def get_status(self):
        return self.__is_available
    
    def borrow_book(self):
        if self.__is_available:
            self.__is_available = False
            return True
        else:
            return False
    
    def return_book(self):
        self.__is_available = True
    
    def get_author(self):
        return self.__author
    
    def get_isbn(self):
        return self.__isbn
    
    def get_publish_date(self):
        return self.__publish_date

    def get_book_details(self):
        print(f"\nTitle: {self.__title}.")
        print(f"Author: {self.__author}.")
        print(f"ISBN: {self.__isbn}.")
        print(f"Publish date: {self.__publish_date}.")
        if self.__is_available == False:
            print("Availability: Checked-out.")
        else: 
            print("Availability: Checked-in.")
        

class NonFiction(Book):
    def __init__(self, title, author, isbn, publish_date, category, description):
        super().__init__(title, author, isbn, publish_date)
        self.category = category
        self.description = description
        self.fict = 'Nonfiction'

    def get_genrebook_details(self):
        print(f"\nTitle: {self.get_title()}.")
        print(f"{self.fict} book.") #added genre feature
        print(f"Category: {self.category}.") #added genre feature
        print(f"Author: {self.get_author()}.")
        print(f"Description: {self.description}.") #added genre feature
        print(f"ISBN: {self.get_isbn()}.")
        print(f"Publish date: {self.get_publish_date()}.")
        if self.get_status() == False:
            print("Availability: Checked-out.")
        else: 
            print("Availability: Checked-in.")

class Fiction(Book):
    def __init__(self, title, author, isbn, publish_date, category, description):
        super().__init__(title, author, isbn, publish_date)
        self.category = category
        self.description = description
        self.fict = 'Fiction'

    def get_genrebook_details(self):
        print(f"\nTitle: {self.get_title()}.")
        print(f"{self.fict} book.") #added genre feature
        print(f"Category: {self.category}.") #added genre feature
        print(f"Author: {self.get_author()}.")
        print(f"Description: {self.description}.") #added genre feature
        print(f"ISBN: {self.get_isbn()}.")
        print(f"Publish date: {self.get_publish_date()}.")
        if self.get_status() == False:
            print("Availability: Checked-out.")
        else: 
            print("Availability: Checked-in.")
