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

def check_if_exists(data):
    database = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="password123",
        database = "Form"
    )
    cursor = database.cursor()
    sqlCommand = "SELECT Password FROM FormTable WHERE Email == " + data['emailText']
    cursor.execute(sqlCommand)
    result = cursor.fetchall()
    if data['passwordText'] == result:
        database.close()
        return True
    database.close()
    return False

