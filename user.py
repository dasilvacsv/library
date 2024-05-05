from database import create_connection

class User:
    def __init__(self, username, password, role, user_id=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role

class UserManager:
    def __init__(self):
        self.conn = create_connection()

    def create_user(self, username, password, role):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        self.conn.commit()

    def authenticate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        if result:
            user_id, username, password, role = result
            return User(username, password, role, user_id)
        return None

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        users = [User(username, password, role, user_id) for user_id, username, password, role in results]
        return users
