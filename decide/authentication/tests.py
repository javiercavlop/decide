from base import mods
from base.tests import BaseTestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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

    # #New tests for the new urls

    # def test_login_user_by_mail(self):
    #     self.client = APIClient()
    #     mods.mock_query(self.client)
    #     u = User(username='josgarmar31', email='josgarmar31@alum.us.es')
    #     u.set_password('contraseña1')
    #     u.save()
    #     data = {'username': 'josgarmar31@alum.us.es', 'password': 'contraseña1'}
    #     response = self.client.post('/authentication/signin/', data, format='json')
    #     print(response)
    #     self.assertEqual(response.status_code, 200)

    #     token = response.json()
    #     self.assertTrue(token.get('token'))

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
        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/'.format(self.live_server_url))

        self.driver.find_element(By.NAME,'username').send_keys('testuser')
        self.driver.find_element(By.NAME,'first_name').send_keys('Test')
        self.driver.find_element(By.NAME,'last_name').send_keys('User')
        self.driver.find_element(By.NAME,'email').send_keys('testuser@notexistsemail.com')
        self.driver.find_element(By.NAME,'password1').send_keys('aQwAm4n2')
        self.driver.find_element(By.NAME,'password2').send_keys('aQwAm4n2')

        self.driver.find_element(By.ID,'id-signup-btn').click()
        self.assertEqual(self.driver.current_url,'{}/'.format(self.live_server_url))


    def test_login(self):
        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/authentication/signin/'.format(self.live_server_url))

        self.driver.find_element(By.NAME,'username').send_keys('admin')
        self.driver.find_element(By.NAME,'password').send_keys('qwerty')

        self.driver.find_element(By.ID,'id-signin-btn').click()
        self.assertEqual(self.driver.current_url,'{}/'.format(self.live_server_url))

    