import mysql.connector

"""За да се използват тези команди, трябва да има създадена база от данни на име Form и таблица в нея на име FormTable"""

def insert_new_user(data): # при регистрация, да се запише новия потребител в базата от данни (като разбира се преди това програмата е проверила за валидност на входните данни)
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

def get_password_from_email(email): # взима паролата на потребителя, за да я сравнява с подадена
    database = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="password123",
        database = "Form"
    )
    cursor = database.cursor()
    sqlCommand = f"SELECT DISTINCT Password FROM FormTable WHERE Email = '{email}';"
    cursor.execute(sqlCommand)
    result = cursor.fetchall()
    database.close()
    return result

def check_if_exists(email, password): # проверява дали има такива имейл и парола в базата данни при Login
    result = get_password_from_email(email)
    if len(result) == 0:
        return False
    result = ' '.join(result[0]) # защото е list от tuple-ли, а ние искаме само стринга
    if result == password:
        return True
    return False

def check_already_registered(email): # проверява дали вече има такава регистрация с този имейл (всеки потребител е с гарантиран имейл)
    result = get_password_from_email(email)
    if len(result) == 0:
        return False
    return True

def update_value_by_email(field, value, email): # променяме стойността във съответната колона за съответния потребител (всеки потребител е с гарантиран уникален имейл)
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

def clean_up_database(email): # функция, която се използва от unit тестовете, за да почисти базата от данни от входовете, които и задават
    database = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="password123",
        database = "Form"
    )
    cursor = database.cursor()
    sqlCommand = f"DELETE FROM FormTable WHERE Email = '{email}'"
    cursor.execute(sqlCommand)
    database.commit()
    database.close()