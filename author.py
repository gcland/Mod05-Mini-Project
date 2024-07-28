class Author:
    def __init__(self, auth_name, biography):
        self.auth_name = auth_name
        self.biography = biography
        
    def get_auth_name(self):
        return self.auth_name

    def add_biography(self, auth_name):
        while True:
            bio_add = input(f"Enter book by {auth_name} to add to biography ('end' to finish.): ")
            if bio_add.lower() == "end":
                break
            else:
                self.biography.append(bio_add)
        return self.biography
                
    def get_biography(self):
        print(f"{self.auth_name} Biography:")
        for book in self.biography:
            print(book)
        return self.biography