import sqlite3

class Database:
    """
    Database class for handling database operations
    """

    def __init__(self):
        # connect to the database
        self.conn = sqlite3.connect('database.db')

        self.cursor = self.conn.cursor()

        # set a new table for the users information
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            email TEXT,
            identity INTEGER,
            score INTEGER
        );""")

        self.conn.commit()

    def __del__(self):
        """
        Destructor for the Database class, closes the connection to the database.
        """

        self.conn.close()

if __name__ == '__main__':
    db = Database()
    del db