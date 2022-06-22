from django.contrib.auth import SESSION_KEY
from django.core.files.images import ImageFile
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


class SignupViewTests(TestCase):
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
        response = self.client.post(
            reverse('user:signup'), self.valid_info_data)
        self.assertFalse(CustomUser.objects.filter(username='test').exists())
        self.assertRedirects(response, reverse('user:create_password'))

    def test_password_post(self):
        # Valid post redirects to confirmation view without saving data
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session['password_form_data'] = self.valid_password_data
        session.save()
        response = self.client.post(
            reverse('user:create_password'), self.valid_password_data)
        self.assertFalse(CustomUser.objects.filter(username='test').exists())
        self.assertRedirects(response, reverse('user:confirm'))

    def test_confirm_post(self):
        # Valid post saves data and redirects to thanks view
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session['password_form_data'] = self.valid_password_data
        session.save()
        response = self.client.post(
            reverse('user:confirm'), self.valid_password_data)
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
        response = self.client.post(reverse('user:confirm'), blank_data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context.get('form').errors)
        self.assertFalse(CustomUser.objects.filter(username='test').exists())

    def test_username_is_blank(self):
        # Posting a blank username brings you back to the form and raises errors
        self.valid_info_data['username'] = ''
        response = self.client.post(
            reverse('user:signup'), self.valid_info_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'username',
                             'This field is required.')

    def test_email_is_blank(self):
        # Posting a blank email brings you back to the form and raises errors
        self.valid_info_data['email'] = ''
        response = self.client.post(
            reverse('user:signup'), self.valid_info_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'email',
                             'This field is required.')

    def test_password_is_blank(self):
        # Posting a blank password brings you back to the form and raises errors
        self.valid_password_data['password1'] = ''
        self.valid_password_data['password2'] = ''
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(
            reverse('user:create_password'), self.valid_password_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password1',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')

    def test_username_taken(self):
        # An existing username brings you back to the form and raises errors
        CustomUser.objects.create(
            username="test", email='test@test.com', date_of_birth='2001-12-31')
        response = self.client.post(
            reverse('user:signup'), self.valid_info_data)
        self.assertFormError(response, 'form', 'username',
                             'A user with that username already exists.')
        self.assertEquals(response.status_code, 200)

    def test_invalid_email(self):
        # An invalid email brings you back to the form and raises errors
        self.valid_info_data['email'] = 'test'
        response = self.client.post(
            reverse('user:signup'), self.valid_info_data)
        self.assertFormError(response, 'form', 'email',
                             'Enter a valid email address.')
        self.assertEquals(response.status_code, 200)

    def test_common_invalid_password(self):
        # Short or similar passwords are invalid.
        self.valid_password_data['password1'] = 'test'
        self.valid_password_data['password2'] = 'test'
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(
            reverse('user:create_password'), self.valid_password_data)
        self.assertFormError(response, 'form', 'password2',
                             'This password is too short. It must contain at least 8 characters.')
        self.assertFormError(response, 'form', 'password2',
                             'This password is too common.')
        self.assertFormError(response, 'form', 'password2',
                             'The password is too similar to the username.')
        self.assertEquals(response.status_code, 200)

    def test_numeric_invalid_password(self):
        # Passwords with only numbers are invalid.
        self.valid_password_data['password1'] = '12345678'
        self.valid_password_data['password2'] = '12345678'
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(
            reverse('user:create_password'), self.valid_password_data)
        self.assertFormError(response, 'form', 'password2',
                             'This password is entirely numeric.')
        self.assertEquals(response.status_code, 200)

    def test_mismatching_password(self):
        # Two passwords do not match
        self.valid_password_data['password1'] = 'testtest'
        self.valid_password_data['password2'] = 'hogehoge'
        session = self.client.session
        session['info_form_data'] = self.valid_info_data
        session.save()
        response = self.client.post(
            reverse('user:create_password'), self.valid_password_data)
        self.assertFormError(response, 'form', 'password2',
                             "The two password fields didn’t match.")
        self.assertEquals(response.status_code, 200)


class SigninTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            username="test",
            email="test@test.com",
            phone='',
            date_of_birth='1901-01-01'
        )
        user.set_password('12345')
        user.save()

        self.signin_url = reverse('user:signin')

    def test_get_signin_view(self):
        response = self.client.get(self.signin_url)
        self.assertEquals(response.status_code, 200)

    def test_valid_signin(self):
        response = self.client.post(
            self.signin_url, {'username': 'test', 'password': '12345'})
        self.assertEquals(response.status_code, 302)
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertRedirects(response, reverse('user:home'))

    def test_nonexistent_user_signin(self):
        response = self.client.post(
            self.signin_url, {'username': 'LeonardoDaVinci', 'password': '12345'})
        self.assertEquals(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertFormError(response, 'form', '__all__',
                             'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_null_password_signin(self):
        response = self.client.post(
            self.signin_url, {'username': 'test', 'password': ''})
        self.assertEquals(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertFormError(response, 'form', 'password',
                             'This field is required.')

    def test_invalid_password_signin(self):
        response = self.client.post(
            self.signin_url, {'username': 'test', 'password': '23456'})
        self.assertEquals(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertFormError(response, 'form', '__all__',
                             'Please enter a correct username and password. Note that both fields may be case-sensitive.')


class SignoutTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            username="test",
            email="test@test.com",
            phone='',
            date_of_birth='1901-01-01'
        )
        user.set_password('12345')
        user.save()

    def test_signout(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(reverse('user:home'))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse('user:signout'))
        self.assertEquals(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)


class GetViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="test",
            email="test@test.com",
            phone='',
            date_of_birth='1901-01-01'
        )
        self.user.set_password('12345')
        self.user.save()

        self.another_user = CustomUser.objects.create(
            username="test2",
            email="test2@test.com",
            phone='',
            date_of_birth='1901-01-01'
        )
        self.another_user.set_password('12345')
        self.another_user.save()

        self.signin_url = reverse('user:signin')

    def test_authenticated_get_home_view(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(reverse('user:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/home.html')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_unauthenticated_get_home_view(self):
        response = self.client.get(reverse('user:home'))
        redirect_url = self.signin_url + '?next=' + reverse('user:home')
        self.assertRedirects(response, redirect_url, status_code=302)
        self.assertNotIn(SESSION_KEY, self.client.session)

    # Get tests for user profile views
    def test_authenticated_get_my_user_profile_view(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(
            reverse('user:user_profile', kwargs={'pk': self.user.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile/user_profile.html')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_unauthenticated_get_my_user_profile_view(self):
        response = self.client.get(
            reverse('user:user_profile', kwargs={'pk': self.user.id}))
        redirect_url = self.signin_url + '?next=' + \
            reverse('user:user_profile', kwargs={'pk': self.user.id})
        self.assertRedirects(response, redirect_url, status_code=302)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_authenticated_get_another_users_profile_view(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(
            reverse('user:user_profile', kwargs={'pk': self.another_user.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile/user_profile.html')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_unauthenticated_get_another_users_profile_view(self):
        response = self.client.get(
            reverse('user:user_profile', kwargs={'pk': self.another_user.id}))
        redirect_url = self.signin_url + '?next=' + \
            reverse('user:user_profile', kwargs={'pk': self.another_user.id})
        self.assertRedirects(response, redirect_url, status_code=302)
        self.assertNotIn(SESSION_KEY, self.client.session)

    #  Get tests for profile editing views
    def test_authenticated_get_my_edit_profile_view(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(
            reverse('user:edit_profile', kwargs={'pk': self.user.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile/edit_profile.html')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_unauthenticated_get_my_edit_profile_view(self):
        response = self.client.get(
            reverse('user:edit_profile', kwargs={'pk': self.user.id}))
        self.assertRedirects(response, reverse('user:home'),
                             status_code=302, target_status_code=302)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_authenticated_get_another_users_edit_profile_view(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(
            reverse('user:edit_profile', kwargs={'pk': self.another_user.id}))
        self.assertRedirects(response, reverse('user:home'), status_code=302)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_unauthenticated_get_another_users_edit_profile_view(self):
        response = self.client.get(
            reverse('user:edit_profile', kwargs={'pk': self.another_user.id}))
        self.assertRedirects(response, reverse('user:home'),
                             status_code=302, target_status_code=302)
        self.assertNotIn(SESSION_KEY, self.client.session)


class EditProfileTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="test",
            email="test@test.com",
            phone='',
            date_of_birth='1901-01-01'
        )
        self.user.set_password('12345')
        self.user.save()

        self.another_user = CustomUser.objects.create(
            username="test2",
            email="test2@test.com",
            phone='',
            date_of_birth='1901-01-01'
        )
        self.another_user.set_password('12345')
        self.another_user.save()
        self.client.login(username="test", password="12345")

        self.context = {
            'username': 'test',
            'profile-TOTAL_FORMS': '1',
            'profile-INITIAL_FORMS': '1',
            'profile-MIN_NUM_FORMS': '0', 
            'profile-MAX_NUM_FORMS': '1', 
            'profile-0-user': self.user.id
            }

    def test_valid_username_and_bio_edit(self):
        url = reverse('user:edit_profile', kwargs={'pk': self.user.id})
        redirect_url = reverse('user:user_profile', kwargs={'pk': self.user.id})
        self.context['username'] = 'teste'
        self.context['profile-0-bio']= 'now testing'
        response = self.client.post(url, self.context)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.username, 'teste')
        self.assertEqual(self.user.profile.bio, 'now testing')
        self.assertIn(SESSION_KEY, self.client.session)

    # Make sure to delete /user_1/test_img.jpg every time you test this
    def test_valid_img_edit(self):
        url = reverse('user:edit_profile', kwargs={'pk': self.user.id})
        redirect_url = reverse('user:user_profile',
                               kwargs={'pk': self.user.id})
        path = './media/test/test_img.jpg'
        self.context['profile-0-profile_img']= ImageFile(open(path, 'rb'))
        response = self.client.post(url, self.context)
        self.user.profile.refresh_from_db()
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
        self.assertEqual(self.user.profile.profile_img.name,
                         f'profile/images/user_{self.user.id}/test_img.jpg')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_invalid_img_edit_with_pdf(self):
        url = reverse('user:edit_profile', kwargs={'pk': self.user.id})
        path = './media/test/test_pdf.pdf'
        self.context['profile-0-profile_img']= ImageFile(open(path, 'rb'))
        response = self.client.post(url, self.context)
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')
        self.assertEqual(self.user.profile.profile_img.name, '')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_invalid_img_edit_with_corr(self):
        url = reverse('user:edit_profile', kwargs={'pk': self.user.id})
        path = './media/test/test_corr.jpg'
        self.context['profile-0-profile_img']= ImageFile(open(path, 'rb'))
        response = self.client.post(url, self.context)
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')
        self.assertEqual(self.user.profile.profile_img.name, '')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_invalid_img_edit_with_txt(self):
        url = reverse('user:edit_profile', kwargs={'pk': self.user.id})
        path = './media/test/test_txt.txt'
        self.context['profile-0-profile_img']= ImageFile(open(path, 'rb'))
        response = self.client.post(url, self.context)
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')
        self.assertEqual(self.user.profile.profile_img.name, '')
        self.assertIn(SESSION_KEY, self.client.session)

    def test_nonexistent_profile_edit(self):
        url = reverse('user:edit_profile', kwargs={'pk': 5})
        context = {'username': 'teste', 'bio': 'now testing'}
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 404)
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.profile.bio, None)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_another_users_profile_edit(self):
        url = reverse('user:edit_profile', kwargs={'pk': self.another_user.id})
        context = {'username': 'teste', 'bio': 'now testing'}
        response = self.client.post(url, context)
        self.assertRedirects(response, reverse('user:home'), status_code=302)
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.profile.bio, None)
        self.assertIn(SESSION_KEY, self.client.session)
