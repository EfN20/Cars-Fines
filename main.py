# imports
import sqlite3 as sql


class Person:
    def __init__(self, iin=0, name=None):
        self.__iin = iin
        self.__name = name

    def set_iin(self, new_iin):
        self.__iin = new_iin

    def get_iin(self):
        return self.__iin

    def set_name(self, new_name):
        self.__name = new_name

    def get_name(self):
        return self.__name

    def __str__(self):
        return f"IIN: {self.get_iin()} | Name: {self.get_name()}"


class Car:
    def __init__(self, car_reg_number=None, car_owner=None):
        self.__car_reg_number = car_reg_number
        self.__car_owner = car_owner

    def set_car_reg_number(self, new_car_reg_number):
        self.__car_reg_number = new_car_reg_number

    def get_car_reg_number(self):
        return self.__car_reg_number

    def set_car_owner(self, new_car_owner):
        self.__car_owner = new_car_owner

    def get_car_owner(self):
        return self.__car_owner


class Fine:
    def __init__(self, fine_id=None, car_owner=None, car_reg_number=None):
        self.__fine_id = fine_id
        self.__car_owner = car_owner
        self.__car_reg_number = car_reg_number

    def set_fine_id(self, new_fine_id):
        self.__fine_id = new_fine_id

    def get_fine_id(self):
        return self.__fine_id

    def set_car_owner(self, new_car_owner):
        self.__car_owner = new_car_owner

    def get_car_owner(self):
        return self.__car_owner

    def set_car_reg_number(self, new_car_reg_number):
        self.__car_reg_number = new_car_reg_number

    def get_car_reg_number(self):
        return self.__car_reg_number

    def __str__(self):
        return f"Fine ID: {self.get_fine_id()} | Car Owner: {self.get_car_owner()} | " \
               f"Car Reg Number: {self.get_car_reg_number()}"


""" Here we searching Fine(s) by Person's iin """

def fines_by_iin():
    while True:
        iin = input("Please, enter IIN to search: ")

        if iin == "" or iin.strip() == "":  # If person enter blank line, then he must re-enter
            print("Please, enter correct IIN!")

        else:
            sql_fines = "Select * from Fine where car_owner = ?"  # Sql query with prepared parameter
            cursor.execute(sql_fines, (iin,))
            rows_fines = cursor.fetchall()
            for row in rows_fines:
                searched_fine = Fine(row[0], row[1], row[2])  # Creating Fine by getting data from each row
                print(searched_fine)
            break


def fines_by_car_number():
    while True:
        car_number = input("Please, enter car register number to search: ")

        if car_number == "" or car_number.strip() == "":
            print("Please, enter correct car number!")

        else:
            sql_fines = "Select * from Fine where car_reg_number = ?"
            cursor.execute(sql_fines, (car_number,))
            rows_fines = cursor.fetchall()
            for row in rows_fines:
                searched_fine = Fine(row[0], row[1], row[2])
                print(searched_fine)
            break


def add_fine_by_iin():
    while True:
        iin = input("Please, enter IIN to search: ")

        if iin == "" or iin.strip() == "":
            print("Please, enter correct IIN!")

        else:
            sql_cars = "Select * from Car where car_owner = ?"
            cursor.execute(sql_cars, (iin,))
            rows_car = cursor.fetchall()
            sql_fines = "Insert into Fine(car_owner, car_reg_number) values (?, ?)"
            choice_car = 0
            if len(rows_car) > 1:  # If length of all rows more than 1
                print("Owners cars: ")  # Give options to choose which car
                for row in rows_car:
                    print(row[0])
                choice_car = input("Please, choose a car to attach fine: ")
            else:
                row = rows_car[0]
                choice_car = row[0]
            cursor.execute(sql_fines, (iin, choice_car))
            conn.commit()
            break


def add_fine_by_car_number():
    while True:
        car_number = input("Please, enter car register number to search: ")

        if car_number == "" or car_number.strip() == "":
            print("Please, enter correct car number!")

        else:
            sql_cars = "Select * from Car where car_reg_number = ?"
            cursor.execute(sql_cars, (car_number,))
            row_car = cursor.fetchone()
            sql_fines = "Insert into Fine(car_owner, car_reg_number) values (?, ?)"
            cursor.execute(sql_fines, (row_car[1], row_car[0]))
            conn.commit()
            break


def erase_fine_by_id():
    while True:
        fine_id = int(input("Please, enter fine ID to erase: "))

        if fine_id < 1:
            print("Please, enter correct fine ID!")

        else:
            sql_erase = "Delete from Fine where fine_id = ?"
            cursor.execute(sql_erase, (fine_id,))
            conn.commit()
            break


def get_all_fines():
    sql_all = "Select * from Fine"
    cursor.execute(sql_all)
    rows_fines = cursor.fetchall()
    for row in rows_fines:
        fine = Fine(row[0], row[1], row[2])
        print(fine)


def get_all_persons():
    sql_persons = "Select * from Person"
    sql_all = "Select * from Fine"
    cursor.execute(sql_all)
    rows_fines = cursor.fetchall()
    cursor.execute(sql_persons)
    rows_persons = cursor.fetchall()
    for row_person in rows_persons:  # Here, we iterate throw all persons and if this person contain any Fine
        has_fine = False
        for row_fine in rows_fines:
            if row_fine[1] == row_person[0]:
                has_fine = True

        if not has_fine:
            person = Person(row_person[0], row_person[1])
            print(person)


if __name__ == '__main__':
    # DATABASE INITIAL BLOCK
    # setting connection to Final.db (will be created if doesn't exist)
    conn = sql.connect("Final.db")

    # cursor object for manipulations with db
    cursor = conn.cursor()

    # Uncomment block below to generate tables and inserts
    # # create tables
    # tables = ["CREATE TABLE IF NOT EXISTS Person(iin TEXT PRIMARY KEY, name TEXT);",
    #           """CREATE TABLE IF NOT EXISTS Car(car_reg_number TEXT PRIMARY KEY,
    #                                           car_owner TEXT NOT NULL, FOREIGN KEY (car_owner)
    #                                           REFERENCES Person ON UPDATE CASCADE ON DELETE CASCADE);""",
    #           """CREATE TABLE IF NOT EXISTS Fine(fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                                           car_owner TEXT NOT NULL,
    #                                           car_reg_number TEXT NOT NULL,
    #                                           FOREIGN KEY (car_owner)
    #                                           REFERENCES Person ON UPDATE CASCADE ON DELETE CASCADE,
    #                                           FOREIGN KEY (car_reg_number)
    #                                           REFERENCES Car ON UPDATE CASCADE ON DELETE CASCADE);"""
    #           ]
    #
    # # executing table creation
    # [cursor.execute(i) for i in tables]
    #
    # # commiting creation of tables
    # conn.commit()
    #
    # # data to fill up the Person table
    # users = [("990112300326", "John"),
    #          ("950326987456", "Adam"),
    #          ("960815654789", "Anne"),
    #          ("780930457147", "Isabelle")
    #          ]
    #
    # # data to fill up the Cars table
    # cars = [("987ASD01", "990112300326"),
    #         ("111KKK02", "950326987456"),
    #         ("666ZLO06", "960815654789"),
    #         ("999OLZ06", "960815654789"),
    #         ("123ABC01", "780930457147")
    #         ]
    #
    # # data to fill up the Finetable
    # fines = [("960815654789", "666ZLO06"),
    #          ("990112300326", "987ASD01"),
    #          ("960815654789", "999OLZ06"),
    #          ("960815654789", "666ZLO06"),
    #          ("960815654789", "666ZLO06"),
    #          ("950326987456", "111KKK02")
    #          ]
    #
    # # running the sql statments for population of tables
    # cursor.executemany("INSERT INTO Person VALUES(?,?)", users)
    # cursor.executemany("INSERT INTO Car VALUES(?,?)", cars)
    # cursor.executemany("INSERT INTO Fine(car_owner, car_reg_number) VALUES(?,?)",
    #                    fines)
    #
    # # commiting changes to db
    # conn.commit()

    # cheking the db content
    # cursor.execute("SELECT * from Fine")
    # print(cursor.fetchall())

    # DATABASE INITIAL BLOCK

    while True:
        print("1. See fines by user ID")
        print("2. See fines by car registration number")
        print("3. Add fine by user ID")
        print("4. Add fine by car registration number")
        print("5. Erase fine by fine ID")
        print("6. See all fines")
        print("7. See people without fines")
        print("8. Exit")
        choice_1 = 0
        try:
            choice_1 = int(input("Select operation: "))
        except TypeError:
            print("Please, enter number of operation!")

        if choice_1 == 1:
            fines_by_iin()

        elif choice_1 == 2:
            fines_by_car_number()

        elif choice_1 == 3:
            add_fine_by_iin()

        elif choice_1 == 4:
            add_fine_by_car_number()

        elif choice_1 == 5:
            erase_fine_by_id()

        elif choice_1 == 6:
            get_all_fines()

        elif choice_1 == 7:
            get_all_persons()

        else:
            # closing streams
            cursor.close()
            conn.close()
            break
