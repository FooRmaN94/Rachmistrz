import sqlite3
import sys
import pandas as pd


class Database:
    connection = None

    # zrobić isActive
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        return

    def __del__(self):
        self.connection.close()
        return

    def create_database(self):
        tables = []
        create_table_person = '''CREATE TABLE IF NOT EXISTS person(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        isActive INTEGER NOT NULL
        );'''
        tables.append(create_table_person)
        create_table_category = '''CREATE TABLE IF NOT EXISTS category(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        isActive INTEGER NOT NULL
        );'''
        tables.append(create_table_category)
        create_table_subcategory = '''CREATE TABLE IF NOT EXISTS sub_category(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        id_category INTEGER,
        isActive INTEGER NOT NULL
        );
        '''
        tables.append(create_table_subcategory)
        create_table_product = '''CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        id_category INTEGER NOT NULL,
        id_sub_category INTEGER,
        isActive INTEGER NOT NULL,
        FOREIGN KEY(id_category) REFERENCES category(id),
        FOREIGN KEY(id_sub_category)REFERENCES sub_category(id)
        );
        '''
        tables.append(create_table_product)
        create_table_income = '''CREATE TABLE IF NOT EXISTS income(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_person INTEGER NOT NULL,
        amount REAL NOT NULL,
        isActive INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(id_person) REFERENCES person(id)
        );
        '''
        tables.append(create_table_income)
        create_table_tag = '''CREATE TABLE IF NOT EXISTS tag(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        isActive INTEGER NOT NULL
        );'''
        tables.append(create_table_tag)
        create_table_product_tag = '''CREATE TABLE IF NOT EXISTS product_tag(
        id_product INTEGER NOT NULL,
        id_tag INTEGER NOT NULL,
        FOREIGN KEY(id_product) REFERENCES product(id),
        FOREIGN KEY(id_tag) REFERENCES tag(id)
        );
        '''
        tables.append(create_table_product_tag)
        create_table_record = '''CREATE TABLE IF NOT EXISTS record(
        id_product INTEGER NOT NULL,
        id_person INTEGER NOT NULL,
        price REAL NOT NULL,
        date TEXT NOT NULL,
        isActive INTEGER NOT NULL,
        FOREIGN KEY(id_product) REFERENCES product(id),
        FOREIGN KEY(id_person) REFERENCES person(id)
        );
        '''
        tables.append(create_table_record)
        cursor = self.connection.cursor()

        for x in tables:
            cursor.execute(x)
        cursor.close()

    # Person table get,add,edit and remove

    def get_person(self, person_id=None):

        # Check if id is null, if it's null return all records in the table.
        if person_id is None:
            command = "Select id, first_name, last_name from person where isActive == 1"
        else:
            command = f"Select id, first_name,last_name from person where id = {person_id}"
        result = pd.read_sql_query(command, self.connection)
        header = ["Imię", "Nazwisko"]
        result.rename(columns={"first_name": header[0], "last_name": header[1]}, inplace=True)

        return result

    def add_person(self, first_name, last_name):
        cursor = self.connection.cursor()
        try:
            command = f"INSERT INTO person(first_name,last_name,isActive) VALUES('{first_name}','{last_name}',{1})"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def edit_person(self, first_name, last_name, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE person SET first_name='{first_name}', last_name='{last_name}' WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def remove_person(self, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE person SET isActive=0 WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()

        except:
            result = False
        finally:
            result = True
        return result

    # Income table get,add,edit and remove

    def get_income(self, income_id=None):

        # Check if id is null, if it's null return all records in the table.
        if income_id is None:
            command = f"""Select income.id, person.first_name, person.last_name, income.amount, income.date from income
             inner join person on income.id_person = person.id"""
        else:
            command = f"""Select income.id, person.first_name, person.last_name, income.amount, income.date from income
             inner join person on income.id_person = person.id where id = {income_id}"""
        result = pd.read_sql_query(command, self.connection)
        header = ["Imię", "Nazwisko", "Wpływ", "Data"]
        result.rename(columns={"first_name": header[0], "last_name": header[1], "amount": header[2], "date": header[3]},
                      inplace=True)
        return result

    # to edit
    def add_income(self, id_person, amount, date):
        cursor = self.connection.cursor()
        try:
            command = f"INSERT INTO income(id_person,amount,date,isActive) VALUES('{id_person}',{amount},'{date}',{1})"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    # To edit
    def edit_income(self, id_person, amount, date, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE income SET id_person={id_person}, amount={amount}, date='{date}' WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def remove_income(self, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE income SET isActive=0 WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()

        except:
            result = False
        finally:
            result = True
        return result
