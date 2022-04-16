from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from knox.models import AuthToken


class LoginTest(TestCase):
    """ Test login functionality. """

    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number='+201012345600', password='p123P123')
        self.user.save()


    def tearDown(self):
        """ Delete the user after test. """

        self.user.delete()


    def test_correct(self):
        user = authenticate(phone_number='+201012345600', password='p123P123')
        self.assertTrue((user is not None) and user.is_authenticated)


    def test_wrong_phone_number(self):
        user = authenticate(phone_number='wrong', password='p123P123')
        self.assertFalse(user is not None and user.is_authenticated)


    def test_wrong_pssword(self):
        user = authenticate(phone_number='+201012345600', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class LoginViewTest(TestCase):
    """ Test login endpoint functionality. """

    def setUp(self):
        """ Create a test user, and set correct and wrong credentials to be passed. """

        self.user = get_user_model().objects.create_user(
            phone_number='+201012345600', 
            password='p123P123'
        )
        self.valid_credentials = {
            'phone_number': '+201012345600', 
            'password': 'p123P123'
        }
        self.wrong_phone_number = {
            'phone_number': 'wrong', 
            'password': 'p123P123'
        }
        self.wrong_phone_password = {
            'phone_number': 'wrong', 
            'password': 'p123P123'
        }


    def tearDown(self):
        """ Delete the user after test. """

        self.user.delete()


    def test_correct(self):
        response = self.client.post('/users/login/', self.valid_credentials)
        self.assertEqual(response.status_code, 200)


    def test_wrong_phone_number(self):
        response = self.client.post('/users/login/', self.wrong_phone_number)
        self.assertNotEqual(response.status_code, 200)


    def test_wrong_pssword(self):
        response = self.client.post('/users/login/', self.wrong_phone_password )
        self.assertNotEqual(response.status_code, 200)


class RegisterViewTest(TestCase):
    """ Test register endpoint functionality. """

    def setUp(self):
        """ Setup valid and invalid parametars to be passed. """

        self.all_fields = {
            'phone_number': '+201012345600',
            "first_name":"Ahmed",
            "last_name":"Mohamed",
            "country_code":"eg",
            "gender":"1",
            "birthdate":"2008-8-8",
            "avatar":"",
            "email":"example@mail.com",
            'password': 'p123P123'
        }

        self.required_fields = {
            'phone_number': '+201012345600',
            'password': 'p123P123'
        }

        self.fields_with_invalid_phone_number = {
            'phone_number': '+201012345',
            'password': 'p123P123'
        }

        self.fields_with_invalid_first_name = {
            'phone_number': '+201012345600',
            'password': 'p123P123',
            "first_name":"Ahmedaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        }
        self.fields_with_invalid_last_name = {
            'phone_number': '+201012345600',
            'password': 'p123P123',
            "last_name":"Mohameddaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        }
        self.fields_with_invalid_country_code = {
            'phone_number': '+201012345600',
            'password': 'p123P123',
            "country_code":"egg",
        }
        self.fields_with_invalid_gender = {
            'phone_number': '+201012345600',
            'password': 'p123P123',
            "gender":"3",
        }
        self.fields_with_invalid_birthdate = {
            'phone_number': '+201012345600',
            'password': 'p123P123',
            "birthdate":"1-1-2008",
        }
        self.fields_with_invalid_email = {
            'phone_number': '+201012345600',
            'password': 'p123P123',
            "email":"examplemail.com",
        }
        self.fields_with_invalid_password = {
            'phone_number': '+201012345600',
            'password': 'p123P123',
            "password":"",
        }


    def tearDown(self):
        """ Try to delete the created user if it has been created. """
        try:
            self.user = get_user_model().objects.get(phone_number=self.all_fields.get('phone_number'))
            self.user.delete()
        except:
            pass


    def test_register_with_all_fields(self):
        response = self.client.post('/users/register/', self.all_fields)
        self.assertEqual(response.status_code, 201)


    def test_register_with_required_fields(self):
        response = self.client.post('/users/register/', self.required_fields)
        self.assertEqual(response.status_code, 201)


    def test_register_invalid_phone_number(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_phone_number)
        self.assertNotEqual(response.status_code, 201)


    def test_register_invalid_first_name(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_first_name)
        self.assertNotEqual(response.status_code, 201)


    def test_register_invalid_last_name(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_last_name)
        self.assertNotEqual(response.status_code, 201)


    def test_register_invalid_country_code(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_country_code)
        self.assertNotEqual(response.status_code, 201)


    def test_register_invalid_gender(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_gender)
        self.assertNotEqual(response.status_code, 201)


    def test_register_invalid_birthdate(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_birthdate)
        self.assertNotEqual(response.status_code, 201)


    def test_register_invalid_email(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_email)
        self.assertNotEqual(response.status_code, 201)


    def test_register_invalid_password(self):
        response = self.client.post('/users/register/', self.fields_with_invalid_password)
        self.assertNotEqual(response.status_code, 201)


class LogoutViewTest(TestCase):
    """ Test logout endpoint functionality. """

    def setUp(self):
        """ Create a test user, and create a token for it. """

        self.user = get_user_model().objects.create_user(
            phone_number='+201012345600', 
            password='p123P123'
        )
        
        self.token = AuthToken.objects.create(self.user)[1]


    def tearDown(self):
        """ Delete the user after test. """
        self.user.delete()


    def test_correct_logout(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + self.token
        response = self.client.post('/users/logout/')
        self.assertEqual(response.status_code, 204)


    def test_not_correct_logout(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + 'not_valid_token'
        response = self.client.post('/users/logout/')
        self.assertNotEqual(response.status_code, 204)


    def test_correct_logoutall(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + self.token
        response = self.client.post('/users/logoutall/')
        self.assertEqual(response.status_code, 204)


    def test_not_correct_logoutall(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + 'not_valid_token'
        response = self.client.post('/users/logoutall/')
        self.assertNotEqual(response.status_code, 204)
