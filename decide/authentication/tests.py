from base import mods
from base.tests import BaseTestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from postproc.models import UserProfile


REGISTER_URL = '/authentication/api/register/'

LOGIN_URL = '/authentication/api/login/'

EDIT_URL = '/authentication/api/edit-user/'

DELETE_URL = '/authentication/api/delete-user/'


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

class AuthTestSelenium(StaticLiveServerTestCase):

    def setUp(self):
        # Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='leslie', email='leslie@us.es')
        u.set_password('contraseña1')
        u.save()
        super().setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
    def tearDown(self):
    
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()
    
    
    def test_login_by_username(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie")
        self.driver.find_element_by_id("id_password").send_keys("contraseña1")
        self.driver.find_element_by_id("submit").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/hello/")

    def test_login_by_email(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie@us.es")
        self.driver.find_element_by_id("id_password").send_keys("contraseña1")
        self.driver.find_element_by_id("submit").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/hello/")

    def test_fail_password_login_by_username(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie")
        self.driver.find_element_by_id("id_password").send_keys("no es mi contraseña")
        self.driver.find_element_by_id("submit").click()
        error = self.driver.find_element_by_id("error")
        self.assertEqual(error.text, "Username or password is incorrect")

    def test_fail_password_login_by_email(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie@us.es")
        self.driver.find_element_by_id("id_password").send_keys("no es mi contraseña")
        self.driver.find_element_by_id("submit").click()
        error = self.driver.find_element_by_id("error")
        self.assertEqual(error.text, "Username or password is incorrect")

    def test_fail_username_login_by_username(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("niidea")
        self.driver.find_element_by_id("id_password").send_keys("contraseña1")
        self.driver.find_element_by_id("submit").click()
        error = self.driver.find_element_by_id("error")
        self.assertEqual(error.text, "Username or password is incorrect")

    def test_fail_email_login_by_email(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("nosequieneres@us.es")
        self.driver.find_element_by_id("id_password").send_keys("contraseña1")
        self.driver.find_element_by_id("submit").click()
        error = self.driver.find_element_by_id("error")
        self.assertEqual(error.text, "Username or password is incorrect")


    def test_empty_username_login(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("")
        self.driver.find_element_by_id("id_password").send_keys("contraseña1")
        self.driver.find_element_by_id("submit").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/signin/")

    def test_empty_password_login_by_username(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie")
        self.driver.find_element_by_id("id_password").send_keys("")
        self.driver.find_element_by_id("submit").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/signin/")

    def test_empty_password_login_by_username(self):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("leslie@us.es")
        self.driver.find_element_by_id("id_password").send_keys("")
        self.driver.find_element_by_id("submit").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/signin/")

    def test_empty_username_and_password_login(self):

        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("")
        self.driver.find_element_by_id("id_password").send_keys("")
        self.driver.find_element_by_id("submit").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/signin/")

class RegisterTestSelenium(StaticLiveServerTestCase):


    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='test', email='test@test.com')
        u.set_password('testpass1')
        u.save()
        
        super().setUp()
        
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        
    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()
        
    def test_fail_register_by_blank(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_class_name("btn").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/signup/")

    def test_fail_register_username(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("iamleslie1")
        self.driver.find_element_by_id("id_password2").send_keys("iamleslie1")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Username already exists")

    def test_fail_register_email(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("test@test.com")
        self.driver.find_element_by_id("id_password1").send_keys("iamleslie1")
        self.driver.find_element_by_id("id_password2").send_keys("iamleslie1")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Email already exists")

    def test_fail_register_password(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("iamleslie1")
        self.driver.find_element_by_id("id_password2").send_keys("iamleslie2")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Passwords don't match")

    def test_fail_register_min_password(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("leslie1")
        self.driver.find_element_by_id("id_password2").send_keys("leslie1")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Password must be at least 8 characters")

    def test_fail_register_num_password(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("iamleslie")
        self.driver.find_element_by_id("id_password2").send_keys("iamleslie")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Password must contain at least one number")
        
    def test_fail_register_let_password(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("12345678")
        self.driver.find_element_by_id("id_password2").send_keys("12345678")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Password must contain at least one letter")
    
    def test_fail_register_first_name(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("iamleslie1")
        self.driver.find_element_by_id("id_password2").send_keys("iamleslie1")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Name must be capitalized")
    
    def test_fail_register_last_name(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("iamleslie1")
        self.driver.find_element_by_id("id_password2").send_keys("iamleslie1")
        self.driver.find_element_by_class_name("btn").click()
        error = self.driver.find_element_by_class_name("alert")
        self.assertEqual(str(error.text).strip(), "Surname must be capitalized")
        
    def test_register(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.driver.find_element_by_id("id_username").send_keys("new_leslie")
        self.driver.find_element_by_id("id_first_name").send_keys("Leslie")
        self.driver.find_element_by_id("id_last_name").send_keys("Acme")
        self.driver.find_element_by_id("id_email").send_keys("leslie@acme.com")
        self.driver.find_element_by_id("id_password1").send_keys("contraseña1")
        self.driver.find_element_by_id("id_password2").send_keys("contraseña1")
        self.driver.find_element_by_class_name("btn").click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/hello/")
        
    def test_register_authorise(self):
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/signup/")
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_password").send_keys("testpass1")
        self.driver.find_element_by_id("submit").click()
        self.driver.get(f"{self.live_server_url}/authentication/signup/")
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/hello/")

class UpdateTestSelenium(StaticLiveServerTestCase):


    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        self.client = APIClient()
        mods.mock_query(self.client)
        u1 = User(username='test', email='test@test.com')
        u1.set_password('testpass1')
        u1.save()
        u2 = User(username='test2', email='test2@test.com')
        u2.set_password('testpass2')
        u2.save()

        super().setUp()
        
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        
    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def login(self, username, password):
        self.driver.get(f"{self.live_server_url}/authentication/signin/")
        self.driver.find_element_by_id("id_username").send_keys(username)
        self.driver.find_element_by_id("id_password").send_keys(password)
        self.driver.find_element_by_id("submit").click()

    def test_fail_update_by_blank(self):
        self.login('test', 'testpass1')
        self.driver.get(f"{self.live_server_url}/authentication/profile/")
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_first_name").clear()
        self.driver.find_element_by_id("id_last_name").clear()
        self.driver.find_element_by_id("id_email").clear()
        update_btn = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.container.py-5 > form > button"))
        update_btn.click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/profile/")

    def test_fail_update_username(self):
        self.login('test', 'testpass1')
        self.driver.get(f"{self.live_server_url}/authentication/profile/")
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_username").send_keys("test2")
        update_btn = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.container.py-5 > form > button"))
        update_btn.click()
        error = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.alert.alert-danger"))
        self.assertEqual(str(error.text).strip(), "Username already exists")

    def test_fail_update_email(self):
        self.login('test', 'testpass1')
        self.driver.get(f"{self.live_server_url}/authentication/profile/")
        self.driver.find_element_by_id("id_email").clear()
        self.driver.find_element_by_id("id_email").send_keys("test2@test.com")
        update_btn = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.container.py-5 > form > button"))
        update_btn.click()
        error = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.alert.alert-danger"))
        self.assertEqual(str(error.text).strip(), "Email already exists")
    
    def test_fail_update_first_name(self):
        self.login('test', 'testpass1')
        self.driver.get(f"{self.live_server_url}/authentication/profile/")
        self.driver.find_element_by_id("id_first_name").clear()
        self.driver.find_element_by_id("id_first_name").send_keys("leslie")
        update_btn = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.container.py-5 > form > button"))
        update_btn.click()
        error = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.alert.alert-danger"))
        self.assertEqual(str(error.text).strip(), "Name must be capitalized")
    
    def test_fail_update_last_name(self):
        self.login('test', 'testpass1')
        self.driver.get(f"{self.live_server_url}/authentication/profile/")
        self.driver.find_element_by_id("id_last_name").clear()
        self.driver.find_element_by_id("id_last_name").send_keys("acme")
        update_btn = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.container.py-5 > form > button"))
        update_btn.click()
        error = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.alert.alert-danger"))
        self.assertEqual(str(error.text).strip(), "Surname must be capitalized")
        
    def test_update(self):
        self.login('test', 'testpass1')
        self.driver.get(f"{self.live_server_url}/authentication/profile/")
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_username").send_keys("new_test")
        update_btn = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="body > div > div.container.py-5 > form > button"))
        update_btn.click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/authentication/hello/")
        

username_user = 'usuario'
email_user = 'perro@email.com'
first_name_user = 'Usuario'
last_name_user = 'Prueba'
username_admin = 'admin1'
password = 'password'

class ApiUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username=username_user)
        u.set_password(password)
        u.save()

        u2 = User(username=username_admin)
        u2.set_password(password)
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login_positive(self):
        data = {'username': username_user, 'password': password}
        response = self.client.post(LOGIN_URL, data,
                                    format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_negative(self):
        data = {'username': username_user + '_bad', 'password': password}
        response = self.client.post(LOGIN_URL, data,
                                    format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_positive(self):
        ## Register
        data_register = {'username': username_user + '_new',
                         'password': password,
                         'email': email_user,
                         'first_name': first_name_user,
                         'last_name': last_name_user}
        response_register = self.client.post(REGISTER_URL,
                                             data_register)

        self.assertEqual(response_register.status_code, 200)

        user = response_register.json().get('user')

        self.assertTrue(user.get('username') == data_register.get('username'))
        self.assertTrue(user.get('email') == data_register.get('email'))
        self.assertTrue(user.get('first_name') == data_register.get('first_name'))

        token = response_register.json().get('token')

        ## Login

        data_login = {'username': username_user + '_new',
                      'password': password}
        response = self.client.post(LOGIN_URL, data_login,
                                    format='json')
        self.assertEqual(response.status_code, 200)

        token_login = response.json()

        self.assertEqual(token_login.get('token'), token)

    def test_register_negative(self):
        data = {'username': username_user, 'password': password}
        response = self.client.post(REGISTER_URL, data)
        self.assertEqual(response.status_code, 400)

        data = {'username': username_user + '_new', 'password': password,
                'email': email_user, 'first_name': 'first_name_user',
                'last_name': 'last_name_user'}
        response = self.client.post(REGISTER_URL, data)
        self.assertEqual(response.status_code, 400)

    def test_edit_user_positive(self):

        data = {'username': username_user, 'password': password}

        response = self.client.post(LOGIN_URL, data)

        token = response.json().get('token')

        data = {'username': username_user, 'first_name': first_name_user,
                'token': token}
        response = self.client.put(EDIT_URL, data)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=username_user)

        self.assertTrue(user.first_name == first_name_user)

    def test_edit_user_negative(self):
        data = {'username': username_user + '_bad', 'last_name': last_name_user}
        response = self.client.put(EDIT_URL, data)
        self.assertEqual(response.status_code, 400)

        data = {'username': username_user, 'password': password}
        self.client.post(LOGIN_URL, data)

        token = 'abcd'

        data = {'username': username_user, 'last_name': last_name_user, 'token': token}
        response = self.client.put(EDIT_URL, data)
        self.assertEqual(response.status_code, 403)

    def test_delete_user_positive(self):
        data = {'username': 'prueba', 'password': password, 'email':'p@p.com',
                'first_name': 'Prueba', 'last_name': 'Prueba'}

        response = self.client.post(REGISTER_URL, data)

        self.assertEqual(response.status_code, 200)

        token = response.json().get('token')

        response = self.client.delete(f'{DELETE_URL}prueba', {'token': token})

        self.assertEqual(response.status_code, 200)

        user = User.objects.filter(username='prueba')
        self.assertFalse(user)

    def test_delete_user_negative(self):
        response = self.client.delete(f'{DELETE_URL}usuario')
        self.assertEqual(response.status_code, 400)

class GenreCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        up = UserProfile(user=u,genre="W")
        up.save()

        u2 = User(username='admin',email="d@gmail.com", is_staff=True)
        u2.set_password('qwerty')
        u2.is_superuser = True
        u2.save()

        up = UserProfile(user=u2,genre="W")
        up.save()

    def tearDown(self):
        self.client = None

    def test_signup(self):
        data = {'username': 'user2', 'password1': '1234','password2': '1234', 'first_name':'Nombre','last_name':'Apellido','email':'correo@gmail.com','genre':'M'}
        response = self.client.post('/authentication/signup/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        self.login()

        user = User.objects.get(username="admin")

        data = {'user':user,'genre':'W','email':'','first_name':'','last_name':'','username':'admin'}
        response = self.client.post('/authentication/profile/',data=data, follow=True)
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