from database import create_connection
from user import User
from book import Book

class Loan:
    def __init__(self, book, user, loan_date=None, return_date=None, loan_id=None):
        self.id = loan_id
        self.book = book
        self.user = user
        self.loan_date = loan_date
        self.return_date = return_date


class LoanManager:
    def __init__(self):
        self.conn = create_connection()

    def create_loan(self, loan):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?)", (loan.book.id, loan.user.id, loan.loan_date))
        self.conn.commit()

    def return_loan(self, loan_id, return_date):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE loans SET return_date = ? WHERE id = ?", (return_date, loan_id))
        self.conn.commit()

    def get_all_loans(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM loans")
        results = cursor.fetchall()
        loans = []
        for loan_id, book_id, user_id, loan_date, return_date in results:
            book = self.get_book_by_id(book_id)
            user = self.get_user_by_id(user_id)
            loan = Loan(book, user, loan_date, return_date, loan_id)
            loans.append(loan)
        return loans

    def get_book_by_id(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        result = cursor.fetchone()
        if result:
            _, title, author, isbn = result
            return Book(title, author, isbn, book_id)
        return None

    def get_user_by_id(self, user_id):
        if isinstance(user_id, User):
            return user_id
        else:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                user_id, username, password, role = result
                return User(username, password, role, user_id)
        return None
