from Scripts import Database as database
import sqlite3

print(r"Hi! I'll try to create database")
db = database.Database('database.db')

db.create_database()

