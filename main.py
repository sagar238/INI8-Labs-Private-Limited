import sqlite3
from datetime import datetime

class RegistrationManager:
    def __init__(self, db_path='registration.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Registration (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Email TEXT NOT NULL,
                DateOfBirth DATE
                -- Add additional fields as needed
            )
        ''')
        self.conn.commit()

    def create_record(self, name, email, date_of_birth):
        try:
            self.cursor.execute('''
                INSERT INTO Registration (Name, Email, DateOfBirth)
                VALUES (?, ?, ?)
            ''', (name, email, date_of_birth))
            self.conn.commit()
            print("Record created successfully.")
        except sqlite3.Error as e:
            print("Error creating record:", e)

    def read_records(self):
        try:
            self.cursor.execute('SELECT * FROM Registration')
            records = self.cursor.fetchall()
            return records
        except sqlite3.Error as e:
            print("Error reading records:", e)

    def update_record(self, record_id, name=None, email=None, date_of_birth=None):
        update_params = {}
        if name is not None:
            update_params['Name'] = name
        if email is not None:
            update_params['Email'] = email
        if date_of_birth is not None:
            update_params['DateOfBirth'] = date_of_birth

        try:
            if update_params:
                update_params['ID'] = record_id
                self.cursor.execute('''
                    UPDATE Registration
                    SET Name = COALESCE(:Name, Name),
                        Email = COALESCE(:Email, Email),
                        DateOfBirth = COALESCE(:DateOfBirth, DateOfBirth)
                    WHERE ID = :ID
                ''', update_params)
                self.conn.commit()
                print("Record updated successfully.")
            else:
                print("No updates provided.")
        except sqlite3.Error as e:
            print("Error updating record:", e)

    def delete_record(self, record_id):
        try:
            self.cursor.execute('DELETE FROM Registration WHERE ID = ?', (record_id,))
            self.conn.commit()
            print("Record deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting record:", e)

    def __del__(self):
        self.conn.close()

# Example Usage:
if __name__ == "__main__":
    manager = RegistrationManager()

    # Create a new record
    manager.create_record("John Doe", "john@example.com", "1990-01-01")

    # Read all records
    records = manager.read_records()
    print("All Records:")
    for record in records:
        print(record)

    # Update a record
    manager.update_record(record_id=1, email="john.doe@example.com")

    # Delete a record
    manager.delete_record(record_id=1)
