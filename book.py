from database import create_connection

class Book:
    def __init__(self, title, author, isbn, book_id=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn

class BookManager:
    def __init__(self):
        self.conn = create_connection()

    def add_book(self, book):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (book.title, book.author, book.isbn))
        self.conn.commit()

    def remove_book(self, book):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book.id,))
        self.conn.commit()

    def update_book(self, book, title, author, isbn):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE books SET title = ?, author = ?, isbn = ? WHERE id = ?", (title, author, isbn, book.id))
        self.conn.commit()

    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()
        books = [Book(title, author, isbn, book_id) for book_id, title, author, isbn in results]
        return books
    
    def get_book_by_id(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        result = cursor.fetchone()
        if result:
            _, title, author, isbn = result
            return Book(title, author, isbn, book_id)
        return None
