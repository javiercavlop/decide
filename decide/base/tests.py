from django.contrib.auth.models import User
from postproc.models import UserProfile
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from base import mods

import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from urllib3.connectionpool import log as urllibLogger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.token = None
        mods.mock_query(self.client)

        user_noadmin = User(username='noadmin', is_staff=False)
        user_noadmin.set_password('qwerty')
        user_noadmin.save()

        user_admin = User(username='admin', is_staff=True, is_superuser = True)
        user_admin.set_password('qwerty')
        user_admin.save()

        LOGGER.setLevel(logging.WARNING)
        urllibLogger.setLevel(logging.WARNING)

    def tearDown(self):
        self.client = None
        self.token = None

    def login(self, user='admin', password='qwerty'):
        data = {'username': user, 'password': password}
        response = mods.post('authentication/login', json=data, response=True)
        self.assertEqual(response.status_code, 200)
        self.token = response.json().get('token')
        self.assertTrue(self.token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def logout(self):
        self.client.credentials()

class MainPageTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        super().setUp()       
        self.base.login()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_access_mainpage_as_staff(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID,'id_username').send_keys("admin")
        self.driver.find_element(By.ID,'id_password').send_keys("qwerty",Keys.ENTER)
        self.driver.get(f'{self.live_server_url}/')
        self.assertTrue(len(self.driver.find_elements(By.ID,'id-admin-panel')) == 1)

    def test_access_mainpage_as_no_staff(self):
        self.driver.set_window_size(1920,1080)
        self.driver.get(f'{self.live_server_url}/authentication/signin')
        self.driver.find_element(By.NAME,'username').send_keys('noadmin')
        self.driver.find_element(By.NAME,'password').send_keys('qwerty')
        self.driver.find_element(By.ID,'id-signin-btn').click()
        self.driver.get(f'{self.live_server_url}/')
        self.assertTrue(len(self.driver.find_elements(By.ID,'id-admin-panel')) == 0)
        
class MainpageTranslationCase(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()
        
        self.test_user = User.objects.create_user(username='test_user', password='test_user_password')
        
        self.driver.get('{}/authentication/signin'.format(self.live_server_url))
        username_field = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="id_username"))
        username_field.send_keys('test_user')
        password_field = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="id_password"))
        password_field.send_keys('test_user_password')
        
        submit_login_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="id-signin-btn"))
        submit_login_button.click()
        
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def test_french_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(4)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#header > h1"))
        self.assertEqual(header_text.text, "Benvenue à Decide")
        
    def test_german_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(3)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#header > h1"))
        self.assertEqual(header_text.text, "Willkommen zu Decide")
        
    def test_spanish_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(2)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#header > h1"))
        self.assertEqual(header_text.text, "Bienvenido a Decide")

    def test_english_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(1)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#header > h1"))
        self.assertEqual(header_text.text, "Welcome to Decide")

class BaseTranslationCase(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()
        
        self.test_user = User.objects.create_user(username='test_user', password='test_user_password')
        
        self.driver.get('{}/authentication/signin'.format(self.live_server_url))
        username_field = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="id_username"))
        username_field.send_keys('test_user')
        password_field = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="id_password"))
        password_field.send_keys('test_user_password')
        
        submit_login_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="id-signin-btn"))
        submit_login_button.click()
        
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def test_french_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}/'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(4)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#navbarSupportedContent > ul > li:nth-child(1) > a"))
        self.assertEqual(header_text.text, "PANNEAU DE COMMANDE")
        
    def test_german_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(3)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#navbarSupportedContent > ul > li:nth-child(1) > a"))
        self.assertEqual(header_text.text, "BEDIENFELD")
        
    def test_spanish_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(2)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#navbarSupportedContent > ul > li:nth-child(1) > a"))
        self.assertEqual(header_text.text, "PANEL DE CONTROL")

    def test_english_translation(self):

        self.driver.set_window_size(1920,1080)
        self.driver.get('{}'.format(self.live_server_url))
        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(1)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#navbarSupportedContent > ul > li:nth-child(1) > a"))
        self.assertEqual(header_text.text, "PANNEAU DE COMMANDE")