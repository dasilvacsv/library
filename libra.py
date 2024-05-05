import tkinter as tk
from tkinter import messagebox
from user_management import UserManagementFrame
from user import UserManager
from book_management import BookManagementFrame
from book import BookManager
from loan_management import LoanManagementFrame
from loan import LoanManager
from database import create_tables
from main import StartupFrame

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        create_tables()
        self.title("Sistema de Gestión de Bibliotecas")
        self.geometry("800x600")
        self.user_manager = UserManager()
        self.book_manager = BookManager()
        self.loan_manager = LoanManager()
        self.current_user = None
        self.show_startup_frame()
        self.create_widgets()

    def create_widgets(self):
        self.create_menu()

    def show_startup_frame(self):
        self.startup_frame = StartupFrame(self, command=lambda: self.create_login_frame_callback())
        self.startup_frame.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

    def create_login_frame_callback(self):
        self.startup_frame.pack_forget()  # Hide the startup frame
        self.create_login_frame_widgets()

    def create_login_frame_widgets(self):
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

    def create_main_frame(self):
        # Create the main frames for each management section
        user_management_frame = UserManagementFrame(self, self.user_manager, self.current_user)
        user_management_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Add book and loan management frames here
        book_management_frame = BookManagementFrame(self, self.book_manager)
        book_management_frame.pack(side=tk.LEFT, padx=10, pady=10)

        loan_management_frame = LoanManagementFrame(self, self.loan_manager, self.book_manager, self.user_manager, self.current_user)
        loan_management_frame.pack(side=tk.LEFT, padx=10, pady=10)

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()