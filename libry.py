import tkinter as tk
from tkinter import messagebox
from user_management import UserManagementFrame
from user import UserManager
from book_management import BookManagementFrame
from book import BookManager
from loan_management import LoanManagementFrame
from loan import LoanManager
from database import create_tables
from pathlib import Path

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        create_tables()
        self.title("Sistema de Gestión de Bibliotecas")
        self.geometry("795x502")
        self.user_manager = UserManager()
        self.book_manager = BookManager()
        self.loan_manager = LoanManager()
        self.current_user = None
        self.create_widgets()

    def create_widgets(self):
        self.create_menu()
        self.create_start_frame()
        self.create_login_frame()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

    def create_start_frame(self):
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path("Inicio/build/assets/frame0")

        def relative_to_assets(path):
            return ASSETS_PATH / Path(path)

        self.configure(bg="#000000")
        canvas = tk.Canvas(
            self,
            bg="#000000",
            height=502,
            width=795,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        image_image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(397.0, 251.0, image=image_image_1)

        image_image_2 = tk.PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(397.0, 97.0, image=image_image_2)

        button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(
            canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login_frame,
            relief="flat"
        )
        button_1.place(x=287.0, y=432.0, width=219.0, height=52.0)

        image_image_3 = tk.PhotoImage(file=relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(378.0, 157.0, image=image_image_3)

        self.resizable(False, False)

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

    def create_main_frame(self):
        # Create the main frames for each management section
        user_management_frame = UserManagementFrame(self, self.user_manager, self.current_user)
        user_management_frame.pack(side=tk.LEFT, padx=10, pady=10)

        book_management_frame = BookManagementFrame(self, self.book_manager)
        book_management_frame.pack(side=tk.LEFT, padx=10, pady=10)

        loan_management_frame = LoanManagementFrame(self, self.loan_manager, self.book_manager, self.user_manager, self.current_user)
        loan_management_frame.pack(side=tk.LEFT, padx=10, pady=10)

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()