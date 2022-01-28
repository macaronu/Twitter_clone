from django.shortcuts import reverse
from django.test import TestCase

from .forms import SignupForm
from .models import CustomUser

# Create your tests here.
class CreateUserFormTests(TestCase):
    def test_phonenumber_input_is_string(self):
        # String inputs in phonenumber field raises error
        form = SignupForm(data={"phone": "hello I'm a string"})
        self.assertEqual(form.errors["phone"], ["Enter a valid phone number."])
    
    def test_invalid_phonenumber(self):
        # Invalid phonenumber raises error
        form = SignupForm(data={"phone": "080-8727"})
        self.assertEqual(form.errors["phone"], ["Enter a valid phone number."])

    def test_email_is_blank(self):
        # Blank email raises error
        form = SignupForm(data={"email": ""})
        self.assertEqual(form.errors["email"], ["This field is required."])


class HomeViewTests(TestCase):
    def test_get_signup_view(self):
        # GET method returns status code 200
        response = self.client.get(reverse('user:signup'))
        self.assertEqual(response.status_code, 200)


class PasswordViewTests(TestCase):
    def setUp(self):
        self.info_session_data = {
            'username': 'test', 
            'email': 'test@test.com', 
            'phone': '', 
            'date_of_birth_month': '1', 
            'date_of_birth_day': '1', 
            'date_of_birth_year': '1901'
        }

    def test_get_password_view(self):
        # GET method returns status code 200 with session data
        session = self.client.session
        session['info_form_data'] = self.info_session_data
        session.save()
        response = self.client.get(reverse('user:create_password'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_password_view_with_invalid_session(self):
        # Redirects to home view without session data
        response = self.client.get(reverse('user:create_password'))
        self.assertRedirects(response, reverse('user:signup'))


class ConfirmViewTests(TestCase):
    def setUp(self):
        self.password_session_data = {
            'username': 'test', 
            'email': 'test@test.com', 
            'phone': '', 
            'date_of_birth_month': '1', 
            'date_of_birth_day': '1', 
            'date_of_birth_year': '1901',
            'password1': 'testpassword', 
            'password2': 'testpassword'
        }
    def test_get_confirm_view(self):
        # GET method returns status code 200 with session data
        session = self.client.session
        session['password_form_data'] = self.password_session_data
        session.save()
        response = self.client.get(reverse('user:confirm'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_confirm_view_with_invalid_session(self):
        # Returns to home view without session data
        response = self.client.get(reverse('user:confirm'))
        self.assertRedirects(response, reverse('user:signup'))


class ValidSignupTests(TestCase):
    def setUp(self):
        self.valid_info_data = {
            'username': 'test', 
            'email': 'test@test.com', 
            'phone': '', 
            'date_of_birth_month': '1', 
            'date_of_birth_day': '1', 
            'date_of_birth_year': '1901'
        }
        self.valid_password_data = {
            'username': 'test', 
            'email': 'test@test.com', 
            'phone': '', 
            'date_of_birth_month': '1', 
            'date_of_birth_day': '1', 
            'date_of_birth_year': '1901',
            'password1': 'testpassword', 
            'password2': 'testpassword'
        }
    
    def test_info_post(self):
        # Valid post redirects to password view without saving data
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(reverse('user:signup'), self.valid_info_data)
        self.assertFalse(CustomUser.objects.filter(username='test').exists())
        self.assertRedirects(response, reverse('user:create_password'))

    def test_password_post(self):
        # Valid post redirects to confirmation view without saving data
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session['password_form_data'] = self.valid_password_data
        session.save()
        response = self.client.post(reverse('user:create_password'), self.valid_password_data)
        self.assertFalse(CustomUser.objects.filter(username='test').exists())
        self.assertRedirects(response, reverse('user:confirm'))

    def test_confirm_post(self):
        # Valid post saves data and redirects to thanks view
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session['password_form_data'] = self.valid_password_data
        session.save()
        response = self.client.post(reverse('user:confirm'), self.valid_password_data)
        self.assertTrue(CustomUser.objects.filter(username='test').exists())
        self.assertRedirects(response, reverse('user:thanks'))


class InvalidSignupTests(TestCase):
    def setUp(self):
        self.valid_info_data = {
            'username': 'test', 
            'email': 'test@test.com', 
            'phone': '', 
            'date_of_birth_month': '1', 
            'date_of_birth_day': '1', 
            'date_of_birth_year': '1901'
        }
        self.valid_password_data = {
            'username': 'test', 
            'email': 'test@test.com', 
            'phone': '', 
            'date_of_birth_month': '1', 
            'date_of_birth_day': '1', 
            'date_of_birth_year': '1901',
            'password1': 'testpassword', 
            'password2': 'testpassword'
        }
    
    def test_blank(self):
        # Blank data brings you back to the form, raises errors, and is not saved
        blank_data = {
            'username': '', 
            'email': '', 
            'phone': '', 
            'date_of_birth_month': '', 
            'date_of_birth_day': '', 
            'date_of_birth_year': '',
            'password1': '', 
            'password2': ''
        }
        session = self.client.session
        session['password_form_data'] = blank_data
        session.save()
        response = self.client.post(reverse('user:confirm'), blank_data )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context.get('form').errors)
        self.assertFalse(CustomUser.objects.filter(username='test').exists())
    
    def test_username_is_blank(self):
        # Posting a blank username brings you back to the form and raises errors
        self.valid_info_data['username'] = ''
        response = self.client.post(reverse('user:signup'), self.valid_info_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
    
    def test_email_is_blank(self):
        # Posting a blank email brings you back to the form and raises errors
        self.valid_info_data['email'] = ''
        response = self.client.post(reverse('user:signup'), self.valid_info_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'This field is required.')
    
    def test_password_is_blank(self):
        # Posting a blank password brings you back to the form and raises errors
        self.valid_password_data['password1'] = ''
        self.valid_password_data['password2'] = ''
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(reverse('user:create_password'), self.valid_password_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password1', 'This field is required.')
        self.assertFormError(response, 'form', 'password2', 'This field is required.')
    
    def test_username_taken(self):
        # An existing username brings you back to the form and raises errors
        CustomUser.objects.create(username="test", email='test@test.com', date_of_birth='2001-12-31')
        response = self.client.post(reverse('user:signup'), self.valid_info_data)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')
        self.assertEquals(response.status_code, 200)
    
    def test_invalid_email(self):
        # An invalid email brings you back to the form and raises errors
        self.valid_info_data['email'] = 'test'
        response = self.client.post(reverse('user:signup'), self.valid_info_data)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        self.assertEquals(response.status_code, 200)
    
    def test_invalid_password(self):
        # Short or similar passwords are invalid.
        self.valid_password_data['password1'] = 'test'
        self.valid_password_data['password2'] = 'test'
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(reverse('user:create_password'), self.valid_password_data)
        self.assertFormError(response, 'form', 'password2', 'This password is too short. It must contain at least 8 characters.')
        self.assertFormError(response, 'form', 'password2', 'The password is too similar to the email.')
        self.assertFormError(response, 'form', 'password2', 'The password is too similar to the username.')
        self.assertEquals(response.status_code, 200)

    def test_invalid_password(self):
        # Passwords with only numbers are invalid.
        self.valid_password_data['password1'] = '12345678'
        self.valid_password_data['password2'] = '12345678'
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(reverse('user:create_password'), self.valid_password_data)
        self.assertFormError(response, 'form', 'password2', 'This password is entirely numeric.')
        self.assertEquals(response.status_code, 200)

    def test_mismatching_password(self):
        # Two passwords do not match
        self.valid_password_data['password1'] = 'testtest'
        self.valid_password_data['password2'] = 'hogehoge'
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(reverse('user:create_password'), self.valid_password_data)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")
        self.assertEquals(response.status_code, 200)
