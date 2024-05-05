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
        self.geometry("2000x1000")
        self.user_manager = UserManager()
        self.book_manager = BookManager()
        self.loan_manager = LoanManager()
        self.current_user = None
        self.create_widgets()

    def create_widgets(self):
        self.create_menu()
        self.create_start_frame()

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
            height=1000,
            width=795,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        print("Canvas created successfully")  # Add this line

       
        image_image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(397, 251, image=image_image_1, anchor="nw")
        
        print("Loading image_2.png")
        image_image_2 = tk.PhotoImage(file=relative_to_assets("image_2.png"))
        print("image_2.png loaded successfully")
        image_2 = canvas.create_image(397.0, 97.0, image=image_image_2)

        print("Loading button_1.png")
        button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        print("button_1.png loaded successfully")
        button_1 = tk.Button(
            canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        button_1.place(x=287.0, y=432.0, width=219.0, height=52.0)

        print("Loading image_3.png")
        image_image_3 = tk.PhotoImage(file=relative_to_assets("image_3.png"))
        print("image_3.png loaded successfully")
        image_3 = canvas.create_image(378.0, 157.0, image=image_image_3)
        canvas.create_rectangle(0, 0, 795, 502, outline="red")

        self.resizable(False, False)

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