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
        create_table_person = '''CREATE TABLE person(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
        isActive 
        );'''
        create_table_category = '''CREATE TABLE category(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
        );'''
        create_table_subcategory = '''CREATE TABLE sub_category(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        id_category INTEGER 
        '''
        create_table_product = '''CREATE TABLE product(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category 
        '''
        cursor = self.connection.cursor()

        return

