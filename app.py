class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checked_out = False

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def checkout_book(self, book):
        if book.checked_out:
            print("This book is already checked out.")
        else:
            book.checked_out = True
            print("You have checked out {} by {}.".format(book.title, book.author))

    def return_book(self, book):
        if book.checked_out:
            book.checked_out = False
            print("You have returned {} by {}.".format(book.title, book.author))
        else:
            print("This book is already in the library.")

    def list_books(self):
        print("Library books:")
        for book in self.books:
            status = "available" if not book.checked_out else "checked out"
            print("- {} by {} ({})".format(book.title, book.author, status))

def main():
    library = Library()

    book1 = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "978-0345391803")
    book2 = Book("Pride and Prejudice", "Jane Austen", "978-0141439518")
    book3 = Book("To Kill a Mockingbird", "Harper Lee", "978-0446310789")

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    library.list_books()

    library.checkout_book(book1)

    library.list_books()

    library.return_book(book1)

    library.list_books()

if __name__ == "__main__":
    main()