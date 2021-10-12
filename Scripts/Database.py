import sqlite3

class Database:
    connection=None
# zrobić isActive
    def __init__(self,path):
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
        return
    def add_person(self,first_name,last_name):
        return
