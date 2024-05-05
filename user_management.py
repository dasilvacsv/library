import tkinter as tk
from tkinter import messagebox
from user import User, UserManager

class UserManagementFrame(tk.Frame):
    def __init__(self, master, user_manager, current_user):
        super().__init__(master)
        self.user_manager = user_manager
        self.current_user = current_user
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for user management
        self.user_listbox = tk.Listbox(self)
        self.user_listbox.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.user_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.user_listbox.yview)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        create_user_button = tk.Button(button_frame, text="Crear usuario", command=self.create_user)
        create_user_button.pack(side=tk.LEFT, padx=5)

        edit_user_button = tk.Button(button_frame, text="Editar usuario", command=self.edit_user)
        edit_user_button.pack(side=tk.LEFT, padx=5)

        delete_user_button = tk.Button(button_frame, text="Eliminar usuario", command=self.delete_user)
        delete_user_button.pack(side=tk.LEFT, padx=5)

        self.update_user_list()

    def create_user(self):
        if self.current_user.role != "superuser":
            messagebox.showinfo("Acceso denegado", "Solo los superusuarios pueden crear usuarios.")
            return

        create_user_window = tk.Toplevel(self)
        create_user_window.title("Crear usuario")

        tk.Label(create_user_window, text="Nombre de usuario:").grid(row=0, column=0)
        username_entry = tk.Entry(create_user_window)
        username_entry.grid(row=0, column=1)

        tk.Label(create_user_window, text="Contraseña:").grid(row=1, column=0)
        password_entry = tk.Entry(create_user_window, show="*")
        password_entry.grid(row=1, column=1)

        tk.Label(create_user_window, text="Rol:").grid(row=2, column=0)
        role_var = tk.StringVar(create_user_window)
        role_var.set("regular")
        role_dropdown = tk.OptionMenu(create_user_window, role_var, "regular", "superuser")
        role_dropdown.grid(row=2, column=1)

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()

            self.user_manager.create_user(username, password, role)
            create_user_window.destroy()
            self.update_user_list()

        save_button = tk.Button(create_user_window, text="Guardar", command=save_user)
        save_button.grid(row=3, column=0, columnspan=2)

    def edit_user(self):
        if self.current_user.role != "superuser":
            messagebox.showinfo("Acceso denegado", "Solo los superusuarios pueden editar usuarios.")
            return

        selected_user_index = self.user_listbox.curselection()
        if selected_user_index:
            user_index = selected_user_index[0]
            user = self.user_manager.get_all_users()[user_index]

            edit_user_window = tk.Toplevel(self)
            edit_user_window.title("Editar usuario")

            tk.Label(edit_user_window, text="Nombre de usuario:").grid(row=0, column=0)
            username_entry = tk.Entry(edit_user_window)
            username_entry.insert(tk.END, user.username)
            username_entry.grid(row=0, column=1)

            tk.Label(edit_user_window, text="Contraseña:").grid(row=1, column=0)
            password_entry = tk.Entry(edit_user_window, show="*")
            password_entry.grid(row=1, column=1)

            tk.Label(edit_user_window, text="Rol:").grid(row=2, column=0)
            role_var = tk.StringVar(edit_user_window)
            role_var.set(user.role)
            role_dropdown = tk.OptionMenu(edit_user_window, role_var, "regular", "superuser")
            role_dropdown.grid(row=2, column=1)

            def save_changes():
                new_username = username_entry.get()
                new_password = password_entry.get()
                new_role = role_var.get()

                user.username = new_username
                user.role = new_role

                if new_password:
                    user.password = new_password

                edit_user_window.destroy()
                self.update_user_list()

            save_button = tk.Button(edit_user_window, text="Guardar cambios", command=save_changes)
            save_button.grid(row=3, column=0, columnspan=2)

    def delete_user(self):
        if self.current_user.role != "superuser":
            messagebox.showinfo("Acceso denegado", "Solo los superusuarios pueden eliminar usuarios.")
            return

        selected_user_index = self.user_listbox.curselection()
        if selected_user_index:
            user_index = selected_user_index[0]
            user = self.user_manager.get_all_users()[user_index]

            self.user_manager.users.remove(user)
            self.update_user_list()

    def update_user_list(self):
        self.user_listbox.delete(0, tk.END)
        users = self.user_manager.get_all_users()
        for user in users:
            self.user_listbox.insert(tk.END, f"{user.username} - {user.role}")