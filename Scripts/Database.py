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

    # Tag table get,add,edit and remove

    def get_tag(self, tag_id=None):

        # Check if id is null, if it's null return all records in the table.
        if tag_id is None:
            command = f"""id,name from tag"""
        else:
            command = f"""Select id,name from tag where id = {tag_id}"""
        result = pd.read_sql_query(command, self.connection)
        header = ["Nazwa"]
        result.rename(columns={"name": header[0]}, inplace=True)
        return result

    # to edit
    def add_tag(self, name):
        cursor = self.connection.cursor()
        try:
            command = f"INSERT INTO tag(name,isActive) VALUES('{name}',{1})"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    # To edit
    def edit_tag(self, name, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE income SET name='{name}' WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def remove_tag(self, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE tag SET isActive=0 WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()

        except:
            result = False
        finally:
            result = True
        return result

    # subcategory table get,add,edit and remove

    def get_subcategory(self, subcategory_id=None):

        # Check if id is null, if it's null return all records in the table.
        if subcategory_id is None:
            command = f"""Select subcategory.id, subcategory.name, category.name from subcategory inner join category on 
            subcategory.id_category = sub.id """
        else:
            command = f"""Select subcategory.id, subcategory.name, category.name from subcategory inner join category on 
            subcategory.id_category = sub.id where id = {subcategory_id}"""
        result = pd.read_sql_query(command, self.connection)
        header = ["Podkategoria", "Kategoria"]
        result.rename(columns={"name": header[0], "name": header[1]}, inplace=True)
        return result

    # to edit
    def add_subcategory(self, name, id_category):
        cursor = self.connection.cursor()
        try:
            command = f"INSERT INTO subcategory(name, id_category, isActive) VALUES('{name}',{id_category},{1})"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    # To edit
    def edit_subcategory(self, name, id_category, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE subcategory SET name='{name}', id_category={id_category} WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def remove_subcategory(self, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE subcategory SET isActive=0 WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()

        except:
            result = False
        finally:
            result = True
        return result

    # category table get,add,edit and remove

    def get_category(self, category_id=None):

        # Check if id is null, if it's null return all records in the table.
        if category_id is None:
            command = f"Select id, name from category"
        else:
            command = f"Select id, name from category where id = {category_id}"
        result = pd.read_sql_query(command, self.connection)
        header = ["Kategoria"]
        result.rename(columns={"name": header[0]}, inplace=True)
        return result

    # to edit
    def add_category(self, name):
        cursor = self.connection.cursor()
        try:
            command = f"INSERT INTO category(name) VALUES('{name}')"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    # To edit
    def edit_category(self, name, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE category SET name='{name}',WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def remove_category(self, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE category SET isActive=0 WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()

        except:
            result = False
        finally:
            result = True
        return result

    # product table get,add,edit and remove

    def get_product(self, product_id=None):

        # Check if id is null, if it's null return all records in the table.
        if product_id is None:
            command = f"""Select product.id, product.name, category.name, subcategory.name from product
             inner join category on product.id_category = category.id
             inner join subcategory on product.id_subcategory = subcategory id"""
        else:
            command = f"""Select product.id, product.name, category.name, subcategory.name from product
             inner join category on product.id_category = category.id
             inner join subcategory on product.id_subcategory = subcategory id where id= {product_id}"""
        result = pd.read_sql_query(command, self.connection)
        header = ["Produkt", "Kategoria", "Podkategoria"]
        result.rename(columns={"name": header[0], "name": header[1], "name": header[2]}, inplace=True)
        return result

    # to edit
    def add_product(self, name, id_category, id_subcategory):
        cursor = self.connection.cursor()
        try:
            command = f"""Insert INTO product(name,id_category,id_subcategory,isActive Values ('{name}',
{id_category},{id_subcategory},1) """
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    # To edit
    def edit_product(self, name, id_category, id_subcategory):
        cursor = self.connection.cursor()
        try:
            command = f"""UPDATE product SET name='{name}', id_category={id_category}, id_subcategory={id_subcategory}"
                       WHERE id={id}"""
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def remove_product(self, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE product SET isActive=0 WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()

        except:
            result = False
        finally:
            result = True
        return result

    # record table get,add,edit and remove

    def get_record(self, record_id=None):

        # Check if id is null, if it's null return all records in the table.
        if record_id is None:
            command = f"""
                    SELECT product.name, record.price, person.first_name, person.last_name, record.date FROM record
                    INNER JOIN product ON record.id_product = product.id
                    INNER JOIN person ON record.id_person = person.id
                    """
        else:
            command = f"""
                    SELECT product.name, record.price, person.first_name, person.last_name, record.date FROM record
                    INNER JOIN product ON record.id_product = product.id
                    INNER JOIN person ON record.id_person = person.id
                    WHERE id = {record_id}
                    """
        result = pd.read_sql_query(command, self.connection)
        header = ["Produkt", "Cena", "Imię", "Nazwisko", "Data"]
        result.rename(columns={"name": header[0], "price": header[1], "first_name": header[2], "last_name": header[3],
                               "date": header[4]}, inplace=True)
        return result

    # to edit
    def add_record(self, id_product, id_person, price, date):
        cursor = self.connection.cursor()
        try:
            command = f"""Insert INTO record(id_product,id_person,price,date Values ({id_product},
            {id_person},{price},'{date}',1) """
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    # To edit
    def edit_record(self, id_product, id_person, price, date, id):
        cursor = self.connection.cursor()
        try:
            command = f"""UPDATE record SET id_product={id_product}, id_person={id_person},price={price},date='{date}'
            Where id={id}"""
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
        except:
            return False
        finally:
            return True

    def remove_record(self, id):
        cursor = self.connection.cursor()
        try:
            command = f"UPDATE record SET isActive=0 WHERE id={id}"
            cursor.execute(command)
            cursor.close()
            self.connection.commit()

        except:
            result = False
        finally:
            result = True
        return result
