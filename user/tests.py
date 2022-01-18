from django.test import TestCase

from .forms import SignupForm

# Create your tests here.
class CreateUserFormTest(TestCase):
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
