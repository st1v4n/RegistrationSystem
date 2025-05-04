import unittest
import validation
import databaseHandle

class Testing(unittest.TestCase):

    def test_email_validation(self):
        email1 = "ivan@abv.bg"
        email2 = "mitkoabv.bg"
        email3 = "georgi@a"
        email4 = "petur@gmail.com"
        email5 = "@."
        email6 = "@a.a"
        email7 = "qvor.ivan@abv"
        self.assertTrue(validation.validate_email(email1))
        self.assertFalse(validation.validate_email(email2))
        self.assertFalse(validation.validate_email(email3))
        self.assertTrue(validation.validate_email(email4))
        self.assertFalse(validation.validate_email(email5))
        self.assertFalse(validation.validate_email(email6))
        self.assertFalse(validation.validate_email(email7))

    def test_name_validation(self):
        name1 = "Ivan"
        name2 = "georgi"
        name3 = "IvanGeorgi"
        name4 = "ivangeorgi"
        name5 = "I"
        name6 = "Ivan georgi"
        name7 = "Qvor@abv"
        self.assertTrue(validation.validate_name(name1))
        self.assertFalse(validation.validate_name(name2))
        self.assertFalse(validation.validate_name(name3))
        self.assertFalse(validation.validate_name(name4))
        self.assertFalse(validation.validate_name(name5))
        self.assertFalse(validation.validate_name(name6))
        self.assertFalse(validation.validate_name(name7))

    def test_password_validation(self):
        password1 = "Ivan5789"
        password2 = "Ivan578"
        password3 = "ivanivanivan"
        password4 = "Ivanivanivan"
        password5 = "qwertYoup"
        password6 = "123IVANIVANIVAN"
        password7 = "***************"
        self.assertTrue(validation.validate_password(password1))
        self.assertFalse(validation.validate_password(password2))
        self.assertFalse(validation.validate_password(password3))
        self.assertTrue(validation.validate_password(password4))
        self.assertTrue(validation.validate_password(password5))
        self.assertFalse(validation.validate_password(password6))
        self.assertFalse(validation.validate_password(password7))

    def test_validate_registration(self):
        test_dict1 = {
            'emailText' : "ivan@abv.bg",
            'passwordText' : "vanko123Vanko",
            'firstNameText' : "Ivan",
            'lastNameText' : "Ivanov"
        }
        result1 = validation.validate_registration(test_dict1)
        self.assertTrue(result1[0]) # това е статуса, дали е валидна или не
        for key in result1[1].keys():
            self.assertEqual(result1[1][key], "")
        test_dict2 = {
            'emailText' : "ivangeorgiev@abv.bg",
            'passwordText' : "vanko123Vanko",
            'firstNameText' : "ivan",
            'lastNameText' : "Georgiev"
        }
        result2 = validation.validate_registration(test_dict2)
        self.assertFalse(result2[0])
        for key in result2[1].keys():
            if key == 'FirstName':
                left = str(result2[1][key])
                right = str("First " + validation.name_error_message)
                self.assertTrue(left == right)
                continue
            self.assertEqual(result2[1][key], "")

    def test_insert_new_user(self):
        test_dict1 = {
            'emailText' : "ivan@abv.bg",
            'passwordText' : "vanko123Vanko",
            'firstNameText' : "Ivan",
            'lastNameText' : "Ivanov"
        }
        databaseHandle.insert_new_user(test_dict1)
        self.assertTrue(databaseHandle.check_if_exists("ivan@abv.bg", "vanko123Vanko"))
        self.assertTrue(databaseHandle.check_already_registered("ivan@abv.bg"))
        databaseHandle.clean_up_database("ivan@abv.bg")

    def test_get_password_from_email(self):
        test_dict1 = {
            'emailText' : "ivan@abv.bg",
            'passwordText' : "vanko123Vanko",
            'firstNameText' : "Ivan",
            'lastNameText' : "Ivanov"
        }
        databaseHandle.insert_new_user(test_dict1)
        result = databaseHandle.get_password_from_email(test_dict1['emailText'])
        result = ' '.join(result[0])
        self.assertTrue(result == "vanko123Vanko")
        invalid_email = "aaa"
        result = databaseHandle.get_password_from_email(invalid_email) 
        self.assertTrue(len(result) == 0)
        databaseHandle.clean_up_database("ivan@abv.bg")

    def test_check_if_exists(self):
        test_dict1 = {
            'emailText' : "ivan@abv.bg",
            'passwordText' : "vanko123Vanko",
            'firstNameText' : "Ivan",
            'lastNameText' : "Ivanov"
        }
        databaseHandle.insert_new_user(test_dict1)
        email1 = "ivan@abv.bg"
        password1 = "vanko123Vanko"
        self.assertTrue(databaseHandle.check_if_exists(email1, password1))
        email2 = "invalidEmail"
        password2 = "invalid-password"
        self.assertFalse(databaseHandle.check_if_exists(email2, password2))
        password3 = "invalid-password-for-email1"
        self.assertFalse(databaseHandle.check_if_exists(email1, password3))
        databaseHandle.clean_up_database("ivan@abv.bg")
    
    def test_check_already_registered(self):
        test_dict1 = {
            'emailText' : "ivan@abv.bg",
            'passwordText' : "vanko123Vanko",
            'firstNameText' : "Ivan",
            'lastNameText' : "Ivanov"
        }
        databaseHandle.insert_new_user(test_dict1)
        email1 = "ivan@abv.bg"
        self.assertTrue(databaseHandle.check_already_registered(email1))
        email2 = "invalid-email"
        self.assertFalse(databaseHandle.check_already_registered(email2))
        databaseHandle.clean_up_database("ivan@abv.bg")

    def test_update_value_by_email(self):
        test_dict1 = {
            'emailText' : "ivan@abv.bg",
            'passwordText' : "vanko123Vanko",
            'firstNameText' : "Ivan",
            'lastNameText' : "Ivanov"
        }
        databaseHandle.insert_new_user(test_dict1)
        result = databaseHandle.get_password_from_email("ivan@abv.bg")
        result = ' '.join(result[0])
        self.assertTrue(result, "vanko123Vanko")
        databaseHandle.update_value_by_email("Password", "NewPassword123", "ivan@abv.bg")
        result = databaseHandle.get_password_from_email("ivan@abv.bg")
        result = ' '.join(result[0])
        self.assertTrue(result, "NewPassword123")
        databaseHandle.clean_up_database("ivan@abv.bg")











if __name__ == '__main__':
    unittest.main()