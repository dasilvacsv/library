import tkinter as tk
from tkinter import messagebox
from book import BookManager, Book
from loan import LoanManager, Loan
from user import UserManager
from datetime import datetime

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Bibliotecas")
        self.geometry("800x600")
        
        self.book_manager = BookManager()
        self.loan_manager = LoanManager()
        self.user_manager = UserManager()

        self.create_widgets()

    def create_widgets(self):
        # Crear los widgets principales de la aplicación
        self.create_menu()
        self.create_login_frame()

    def create_menu(self):
        # Crear el menú principal de la aplicación
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

    def create_main_frame(self):
        # Crear el marco principal de la aplicación
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sección de manejo de libros
        book_list_frame = tk.Frame(main_frame)
        book_list_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.book_listbox = tk.Listbox(book_list_frame)
        self.book_listbox.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(book_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.book_listbox.yview)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        add_button = tk.Button(button_frame, text="Agregar libro", command=self.add_book)
        add_button.pack(pady=5)

        edit_button = tk.Button(button_frame, text="Editar libro", command=self.edit_book)
        edit_button.pack(pady=5)

        delete_button = tk.Button(button_frame, text="Eliminar libro", command=self.delete_book)
        delete_button.pack(pady=5)

        # Manejo de préstamo de libros
        loan_frame = tk.Frame(main_frame)
        loan_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.loan_listbox = tk.Listbox(loan_frame)
        self.loan_listbox.pack(side=tk.LEFT)

        loan_scrollbar = tk.Scrollbar(loan_frame)
        loan_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.loan_listbox.config(yscrollcommand=loan_scrollbar.set)
        loan_scrollbar.config(command=self.loan_listbox.yview)

        loan_button_frame = tk.Frame(loan_frame)
        loan_button_frame.pack(pady=10)

        create_loan_button = tk.Button(loan_button_frame, text="Crear préstamo", command=self.create_loan)
        create_loan_button.pack(side=tk.LEFT, padx=5)

        return_loan_button = tk.Button(loan_button_frame, text="Devolver préstamo", command=self.return_loan)
        return_loan_button.pack(side=tk.LEFT, padx=5)

        self.update_loan_list()
        self.update_book_list()

    # Autenticación
    def create_login_frame(self):
        login_frame = tk.Frame(self)
        login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(login_frame, text="Nombre de usuario:").pack()
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.pack()

        tk.Label(login_frame, text="Contraseña:").pack()
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.pack()

        login_button = tk.Button(login_frame, text="Iniciar sesión", command=self.login)
        login_button.pack()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.user_manager.authenticate_user(username, password)

        if user:
            self.current_user = user
            self.create_main_frame()
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales inválidas")

    # Métodos libros
    def add_book(self):
        add_book_window = tk.Toplevel(self)
        add_book_window.title("Agregar libro")

        tk.Label(add_book_window, text="Título:").grid(row=0, column=0)
        title_entry = tk.Entry(add_book_window)
        title_entry.grid(row=0, column=1)

        tk.Label(add_book_window, text="Autor:").grid(row=1, column=0)
        author_entry = tk.Entry(add_book_window)
        author_entry.grid(row=1, column=1)

        tk.Label(add_book_window, text="ISBN:").grid(row=2, column=0)
        isbn_entry = tk.Entry(add_book_window)
        isbn_entry.grid(row=2, column=1)

        def save_book():
            title = title_entry.get()
            author = author_entry.get()
            isbn = isbn_entry.get()

            book = Book(title, author, isbn)
            self.book_manager.add_book(book)

            add_book_window.destroy()
            self.update_book_list()

        save_button = tk.Button(add_book_window, text="Guardar", command=save_book)
        save_button.grid(row=3, column=0, columnspan=2)

    def edit_book(self):
        selected_index = self.book_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            book = self.book_manager.get_all_books()[index]

            edit_book_window = tk.Toplevel(self)
            edit_book_window.title("Editar libro")

            tk.Label(edit_book_window, text="Título:").grid(row=0, column=0)
            title_entry = tk.Entry(edit_book_window)
            title_entry.insert(tk.END, book.title)
            title_entry.grid(row=0, column=1)

            tk.Label(edit_book_window, text="Autor:").grid(row=1, column=0)
            author_entry = tk.Entry(edit_book_window)
            author_entry.insert(tk.END, book.author)
            author_entry.grid(row=1, column=1)

            tk.Label(edit_book_window, text="ISBN:").grid(row=2, column=0)
            isbn_entry = tk.Entry(edit_book_window)
            isbn_entry.insert(tk.END, book.isbn)
            isbn_entry.grid(row=2, column=1)

            def save_changes():
                title = title_entry.get()
                author = author_entry.get()
                isbn = isbn_entry.get()

                self.book_manager.update_book(book, title, author, isbn)

                edit_book_window.destroy()
                self.update_book_list()

            save_button = tk.Button(edit_book_window, text="Guardar cambios", command=save_changes)
            save_button.grid(row=3, column=0, columnspan=2)

    def delete_book(self):
        selected_index = self.book_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            book = self.book_manager.get_all_books()[index]

            self.book_manager.remove_book(book)
            self.update_book_list()

    def update_book_list(self):
        self.book_listbox.delete(0, tk.END)
        books = self.book_manager.get_all_books()
        for book in books:
            self.book_listbox.insert(tk.END, book.title)

    # Funciones para el préstamo de libros
    def create_loan(self):
        selected_book_index = self.book_listbox.curselection()
        if selected_book_index:
            book_index = selected_book_index[0]
            book = self.book_manager.get_all_books()[book_index]

            loan_date = datetime.now().strftime("%Y-%m-%d")
            loan = Loan(book, self.current_user, loan_date)
            self.loan_manager.create_loan(loan)

            self.update_loan_list()


    def return_loan(self):
        selected_loan_index = self.loan_listbox.curselection()
        if selected_loan_index:
            loan_index = selected_loan_index[0]
            loan = self.loan_manager.get_all_loans()[loan_index]

            if loan.return_date is None:
                return_date = datetime.now().strftime("%Y-%m-%d")
                self.loan_manager.update_loan(loan, return_date)
                self.update_loan_list()
            else:
                messagebox.showinfo("Devolución de préstamo", "Este préstamo ya ha sido devuelto.")

    def update_loan_list(self):
        self.loan_listbox.delete(0, tk.END)
        loans = self.loan_manager.get_all_loans()
        for loan in loans:
            status = "Devuelto" if loan.return_date else "Pendiente"
            self.loan_listbox.insert(tk.END, f"{loan.book.title} - {loan.user.username} - {status}")
        
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()