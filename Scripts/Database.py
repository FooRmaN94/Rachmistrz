import sqlite3
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
        amount INTEGER NOT NULL,
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
        );'''
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

    def get_person(self, id=None):
		
		# Check if id is null, if it's null return all records in the table. 
		
		if id==None:
			command = "Select first_name,last_name,id from person"
		else:
			command = f"Select first_name,last_name,id from person where id = {id}"
        result = pd.read_sql_query(command,self.connection)
        print(result)

    def add_person(self, first_name, last_name):
	
		# Add new record to the person table
		
        cursor = self.connection.cursor()
        command = f"INSERT INTO person(first_name,last_name,isActive) VALUES('{first_name}','{last_name}',{1})"
        print("such command will be executed:",command)
        cursor.execute(command)
        cursor.close()
        self.connection.commit()

    def edit_person(self, first_name, last_name, id):
        cursor = self.connection.cursor()
        command = f"INSERT INTO person(first_name,last_name) VALUES('{first_name}','{last_name}' WHERE id={id})"
        print("such command will be executed:", command)
        cursor.execute(command)
        cursor.close()
        self.connection.commit()

    def remove_person(self, id):
        cursor = self.connection.cursor()
        command = f"INSERT INTO person(isActive) VALUES({1}) WHERE id={id}"
        cursor.execute(command)
        cursor.close()
        self.connection.commit()
