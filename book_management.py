import tkinter as tk
from book import Book, BookManager

class BookManagementFrame(tk.Frame):
    def __init__(self, master, book_manager):
        super().__init__(master)
        self.book_manager = book_manager
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for book management
        self.book_listbox = tk.Listbox(self)
        self.book_listbox.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.book_listbox.yview)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        add_book_button = tk.Button(button_frame, text="Agregar libro", command=self.add_book)
        add_book_button.pack(side=tk.LEFT, padx=5)

        edit_book_button = tk.Button(button_frame, text="Editar libro", command=self.edit_book)
        edit_book_button.pack(side=tk.LEFT, padx=5)

        delete_book_button = tk.Button(button_frame, text="Eliminar libro", command=self.delete_book)
        delete_book_button.pack(side=tk.LEFT, padx=5)

        self.update_book_list()

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
        selected_book_index = self.book_listbox.curselection()
        if selected_book_index:
            book_index = selected_book_index[0]
            book = self.book_manager.get_all_books()[book_index]

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
                new_title = title_entry.get()
                new_author = author_entry.get()
                new_isbn = isbn_entry.get()

                self.book_manager.update_book(book.id, new_title, new_author, new_isbn)

                edit_book_window.destroy()
                self.update_book_list()

            save_button = tk.Button(edit_book_window, text="Guardar cambios", command=save_changes)
            save_button.grid(row=3, column=0, columnspan=2)

    def delete_book(self):
        selected_book_index = self.book_listbox.curselection()
        if selected_book_index:
            book_index = selected_book_index[0]
            book = self.book_manager.get_all_books()[book_index]

            self.book_manager.remove_book(book.id)
            self.update_book_list()

    def update_book_list(self):
        self.book_listbox.delete(0, tk.END)
        books = self.book_manager.get_all_books()
        for book in books:
            self.book_listbox.insert(tk.END, book.title)