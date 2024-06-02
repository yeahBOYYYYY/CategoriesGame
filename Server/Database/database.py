import re
import sqlite3


class Database:
    """
    Database class for handling sqlite3 database operations.
    """

    def __init__(self, database_file: str = 'Server/Database/database.db'):
        # connect to the database that will be created in this folder
        self.conn = sqlite3.connect(database_file, check_same_thread=False)

        self.cursor = self.conn.cursor()

        # set a new table for the users information
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            email TEXT,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        );""")

        self.conn.commit()

    def __str__(self):
        """
        String representation of the Database class.
        """

        # get all users from table
        self.cursor.execute("SELECT * FROM users")
        items = self.cursor.fetchall()

        return "\n".join([str(item) for item in items])

    def __del__(self):
        """
        Destructor for the Database class, closes the connection to the database.
        """

        self.conn.close()

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Check if the email is a valid format.
        """

        # Regular expression for validating an Email
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # If the string matches the regex, it is a valid email
        if re.match(regex, email):
            return True
        else:
            return False

    def is_valid_user(self, username: str, password: str) -> bool:
        """
        Check if a user exists in the database.
        :param username: the username of the user.
        :param password: the password of the user.
        :return: True if the user exists, False otherwise.
        """

        try:
            # check if the user exists
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?;", (username, password))
            user = self.cursor.fetchone()
            return user is not None
        except:
            return False

    def add_user(self, username: str, password: str, email: str) -> bool:
        """
        Add a new user to the database.
        :param username: the username of the user.
        :param password: the password of the user.
        :param email: the email of the user.
        :return: True if the user was added successfully, False otherwise.
        """

        # check if the email is valid
        if not self.is_valid_email(email):
            return False

        try:
            # create a new user in the database
            self.cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?);",
                                (username, password, email))

            # commit changes to the database
            self.conn.commit()
            return True
        except:
            return False

    def get_score(self, username: str) -> tuple[int, int]:
        """
        Get the score of a user, tuple of wins and losses.
        :param username: the username of the user.
        :return: the score of the user.
        """

        try:
            # get the score of the user
            self.cursor.execute("SELECT wins, losses FROM users WHERE username = ?;", (username,))
            score = self.cursor.fetchone()

            # extract first and only user found.
            return score[0]
        except:
            return -1, -1

    def set_score(self, username: str, score: tuple[int, int]) -> bool:
        """
        Set the score of a user.
        :param username: the username of the user.
        :param score: the score of the user.
        :return: True if the score was set successfully, False otherwise.
        """

        if (score[0] < 0) or (score[1] < 0):
            return False

        try:
            # set the score of the user
            self.cursor.execute("UPDATE users SET wins = ?, losses = ? WHERE username = ?;",
                                (score[0], score[1], username))

            # commit changes to the database
            self.conn.commit()
            return True
        except:
            return False


if __name__ == '__main__':
    db = Database('database.db')
    print(db.add_user("user1", "password1", "ron@gmail.com"))
    print(db.add_user("user8", "nigga!", "bulbul@yahoo.org"))
    print(db.add_user("user69", "nigga?!", "bulbul"))
    print(db)
    del db

    print(Database.is_valid_email("w@gmail.com"))
    print(Database.is_valid_email("lol@yahho.org"))
    print(Database.is_valid_email("@edu.co.il"))
    print(Database.is_valid_email("mikhelman.ron@israel.giv.il"))
    print(Database.is_valid_email("mikhelman.ron@edu"))
    print(Database.is_valid_email("shlomi.eat123@edu.co.il"))
    print(Database.is_valid_email("wgmail.com"))
    print(Database.is_valid_email("shlomi.eat123@edu.co2.il"))
    print(Database.is_valid_email("shlomi.eat123@edu.co2.il18"))