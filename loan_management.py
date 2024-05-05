import tkinter as tk
from tkinter import messagebox
from loan import Loan, LoanManager
from datetime import datetime

class LoanManagementFrame(tk.Frame):
    def __init__(self, master, loan_manager, book_manager, user_manager, current_user):
        super().__init__(master)
        self.loan_manager = loan_manager
        self.book_manager = book_manager
        self.user_manager = user_manager
        self.current_user = current_user
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for loan management
        self.loan_listbox = tk.Listbox(self)
        self.loan_listbox.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.loan_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.loan_listbox.yview)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        create_loan_button = tk.Button(button_frame, text="Crear préstamo", command=self.create_loan)
        create_loan_button.pack(side=tk.LEFT, padx=5)

        return_loan_button = tk.Button(button_frame, text="Devolver préstamo", command=self.return_loan)
        return_loan_button.pack(side=tk.LEFT, padx=5)

        self.update_loan_list()

    def create_loan(self):
        create_loan_window = tk.Toplevel(self)
        create_loan_window.title("Crear préstamo")

        tk.Label(create_loan_window, text="Libro:").grid(row=0, column=0)
        book_var = tk.StringVar(create_loan_window)
        book_dropdown = tk.OptionMenu(create_loan_window, book_var, *[book.title for book in self.book_manager.get_all_books()])
        book_dropdown.grid(row=0, column=1)

        def save_loan():
            book_title = book_var.get()
            book = next((b for b in self.book_manager.get_all_books() if b.title == book_title), None)
            if book:
                loan_date = datetime.now().strftime("%Y-%m-%d")
                loan = Loan(book, self.current_user, loan_date)
                self.loan_manager.create_loan(loan)
                create_loan_window.destroy()
                self.update_loan_list()
            else:
                messagebox.showerror("Error", "Libro no válido")

    def return_loan(self):
        selected_loan_index = self.loan_listbox.curselection()
        if selected_loan_index:
            loan_index = selected_loan_index[0]
            loan = self.loan_manager.get_all_loans()[loan_index]
            return_date = datetime.now().strftime("%Y-%m-%d")
            self.loan_manager.return_loan(loan.id, return_date)
            self.update_loan_list()

    def update_loan_list(self):
        self.loan_listbox.delete(0, tk.END)
        loans = self.loan_manager.get_all_loans()
        for loan in loans:
            book = loan.book
            user = self.loan_manager.get_user_by_id(loan.user)
            self.loan_listbox.insert(tk.END, f"{book.title} - {user.username}")