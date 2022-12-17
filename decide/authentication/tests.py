from urllib.request import HTTPBasicAuthHandler
from base import mods
from base.tests import BaseTestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from postproc.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )
    
class TranslationCase(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp() 
        
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def test_french_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/authentication/signin'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(4)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        username_label = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value=".container > h1"))
        self.assertEqual(username_label.text, "Connexion")
        
    def test_german_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/authentication/signin'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(3)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        username_label = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value=".container > h1"))
        self.assertEqual(username_label.text, "Anmeldung")
        
    def test_spanish_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/authentication/signin'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(2)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        username_label = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value=".container > h1"))
        self.assertEqual(username_label.text, "Iniciar sesión")

    def test_english_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/authentication/signin'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(1)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        username_label = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value=".container > h1"))
        self.assertEqual(username_label.text, "Sign In") 

class GenreCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        up = UserProfile(user=u, genre="W")
        up.save()

        u2 = User(username='admin', email="d@gmail.com", is_staff=True)
        u2.set_password('qwerty')
        u2.is_superuser = True
        u2.save()

        up = UserProfile(user=u2, genre="W")
        up.save()

    def tearDown(self):
        self.client = None

    def test_signup(self):
        data = {'username': 'user2', 'password1': '1234', 'password2': '1234', 'first_name': 'Nombre',
                'last_name': 'Apellido', 'email': 'correo@gmail.com', 'genre': 'M'}
        response = self.client.post('/authentication/signup/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        self.login()

        user = User.objects.get(username="admin")

        data = {'user': user, 'genre': 'W', 'email': '', 'first_name': '', 'last_name': '', 'username': 'admin'}
        response = self.client.post('/authentication/profile/', data=data, follow=True)
        self.assertEqual(response.status_code, 200)

class AuthenticationViewsTestCase(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.base = BaseTestCase()
        self.base.setUp()
        super().setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_register(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/'.format(self.live_server_url))

        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'first_name').send_keys('Test')
        self.driver.find_element(By.NAME, 'last_name').send_keys('User')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@notexistsemail.com')
        self.driver.find_element(By.NAME, 'password1').send_keys('aQwAm4n2')
        self.driver.find_element(By.NAME, 'password2').send_keys('aQwAm4n2')

        self.driver.find_element(By.ID, 'id-signup-btn').click()
        self.assertEqual(self.driver.current_url, '{}/'.format(self.live_server_url))

    def test_login(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/signin/'.format(self.live_server_url))

        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('qwerty')

        self.driver.find_element(By.ID, 'id-signin-btn').click()
        self.assertEqual(self.driver.current_url, '{}/'.format(self.live_server_url))


class RegisterPageTranslationCase(StaticLiveServerTestCase):

    def setUp(self):
        # Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        mods.mock_query(self.client)
        u = User(username='leslie', email='leslie@us.es')
        u.set_password('contraseña1')
        u.save()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_french_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie")
        self.driver.find_element_by_id("id_password").send_keys("contraseña1")
        self.driver.get(f"{self.live_server_url}/authentication/profile/")

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(4)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="container-md > h1"))
        self.assertEqual(header_text.text, "Gérer votre profil")

    def test_german_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie")
        self.driver.find_element_by_id("id_password").send_keys("contraseña1")
        self.driver.get(f"{self.live_server_url}/authentication/profile/")

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(3)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="container-md > h1"))
        self.assertEqual(header_text.text, "Vorname:")

    def test_spanish_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/signup/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(1)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR,
                                                                                            value="body > div > div > form > div:nth-child(3) > div.fw-bold > label"))
        self.assertEqual(header_text.text, "Nombre:")

    def test_english_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/signup/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(2)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR,
                                                                                            value="body > div > div > form > div:nth-child(3) > div.fw-bold > label"))
        self.assertEqual(header_text.text, "First name:")


class LoginPageTranslationCase(StaticLiveServerTestCase):

    def setUp(self):
        # Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()
        super().setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_french_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/signin/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(4)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR,
                                                                                            value="body > div > form > div.row.mb-3 > div:nth-child(1) > label"))
        self.assertEqual(header_text.text, "Nom d'utilisateur:")

    def test_german_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/signin/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(3)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR,
                                                                                            value="body > div > form > div.row.mb-3 > div:nth-child(1) > label"))
        self.assertEqual(header_text.text, "Nutzername:")

    def test_spanish_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/signin/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(1)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR,
                                                                                            value="body > div > form > div.row.mb-3 > div:nth-child(1) > label"))
        self.assertEqual(header_text.text, "Nombre de usuario:")

    def test_english_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/signin/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(2)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR,
                                                                                            value="body > div > form > div.row.mb-3 > div:nth-child(1) > label"))
        self.assertEqual(header_text.text, "Username:")


class EditPageTranslationCase(StaticLiveServerTestCase):

    def setUp(self):
        # Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

        self.test_user = User.objects.create_user(username='test_user', password='test_user_password')

        self.driver.get(f'{self.live_server_url}/authentication/signin')
        username_field = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="id_username"))
        username_field.send_keys('test_user')
        password_field = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="id_password"))
        password_field.send_keys('test_user_password')

        submit_login_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="id-signin-btn"))
        submit_login_button.click()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_french_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/profile/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(4)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div.container-md > h1"))
        self.assertEqual(header_text.text, "Gérer votre profil")

    def test_german_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/profile/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(3)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div.container-md > h1"))
        self.assertEqual(header_text.text, "Verwalten Sie Ihr Profil")

    def test_spanish_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/profile/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(1)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div.container-md > h1"))
        self.assertEqual(header_text.text, "Gestiona tu perfil")

    def test_english_translation(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get('{}/authentication/profile/'.format(self.live_server_url))

        language_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(2)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div.container-md > h1"))
        self.assertEqual(header_text.text, "Manage your profile")