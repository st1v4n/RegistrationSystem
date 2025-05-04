import re

name_error_message = "Name: Invalid!"
email_error_message = "Email: Invalid!"
password_error_message = "Password should contain at least 8 characters, 1 of them upper-case and 1 of them lower-case"

def validate_email(email):
    # всеки email трябва да match-ва regex-a от вида <букви/цифри>@<букви/цифри>.<букви/цифри> Имейли от вида ivan.georgi@abv.bg ще считаме за невалидни заради . между ivan и georgi, нищо че всъщност са валидни в действителността
    if re.match(r'^\w+\@\w+\.\w+', email) is not None:
        return True
    return False
    
def validate_password(password):
    # Всяка парола трябва да е от поне 8 символа, да съдържа поне 1 малка и поне 1 главна буква
    containsSmall = False
    containsBig = False
    if len(password) < 8:
        return False
    for symbol in password:
        if symbol >= 'a' and symbol <= 'z':
            containsSmall = True
        if symbol >= 'A' and symbol <= 'Z':
            containsBig = True
    return containsSmall and containsBig

def validate_name(name):
    # Всяко име трябва да започва с главна буква, да съдържа само букви и да е с поне 2 букви
    if len(name) < 2:
        return False
    if name[0] < 'A' or name[0] > 'Z':
        return False
    for symbol in name[1:]:
        if symbol < 'a' or symbol > 'z':
            return False
    return True

def validate_registration(data): # Валидираме всички данни, нужни за регистрация, като ако има невалидни, добавяме като message, който после ще пратим обратно
    status = True # Ако всичко е минало успешно и това status остане на true, то ще върнем response 200
    message = dict()
    message['Email'] = ""
    message['Password'] = ""
    message['FirstName'] = ""
    message['LastName'] = ""
    if validate_email(data['emailText']) == False:
        status = False
        message['Email'] = email_error_message
    if validate_password(data['passwordText']) == False:
        status = False
        message['Password'] = password_error_message
    if validate_name(data['firstNameText']) == False:
        status = False
        message['FirstName'] = "First " + name_error_message
    if validate_name(data['lastNameText']) == False:
        status = False
        message['LastName'] = "Last " + name_error_message
    return status, message