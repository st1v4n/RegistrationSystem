import mysql.connector

"""За да се използват тези команди, трябва да има създадена база от данни на име Form и таблица в нея на име FormTable"""

def insert_new_user(data):
    database = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="password123",
        database = "Form"
    )
    cursor = database.cursor()
    sqlCommand = "INSERT INTO FormTable (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)"
    values = (data['firstNameText'], data['lastNameText'], data['emailText'], data['passwordText'])
    cursor.execute(sqlCommand, values)
    database.commit()
    database.close()

def get_password_from_email(email):
    database = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="password123",
        database = "Form"
    )
    cursor = database.cursor()
    sqlCommand = f"SELECT Password FROM FormTable WHERE Email = '{email}';"
    cursor.execute(sqlCommand)
    result = cursor.fetchall()
    database.close()
    return result

def check_if_exists(email, password): # проверява дали има такива имейл и парола в базата данни при Login
    result = get_password_from_email(email)
    if len(result) == 0:
        return False
    result = ' '.join(result[0])
    if result == password:
        return True
    return False

def check_already_registered(email): # проверява дали вече има такава регистрация с този имейл
    result = get_password_from_email(email)
    if len(result) == 0:
        return False
    return True

def update_value_by_email(field, value, email):
    database = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="password123",
        database = "Form"
    )
    cursor = database.cursor()
    sqlCommand = f"UPDATE FormTable SET {field} = '{value}' WHERE Email = '{email}'"
    cursor.execute(sqlCommand)
    database.commit()
    database.close()