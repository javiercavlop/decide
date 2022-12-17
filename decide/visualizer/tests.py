from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from base.tests import BaseTestCase
from voting.models import Question, Voting, QuestionOption
import time
from django.contrib.auth.models import User



class VisualizerTestCase(StaticLiveServerTestCase):

    def setUp(self):
        # Load base test functionality for decide

        self.base = BaseTestCase()
        self.base.setUp()
        User = get_user_model()
        user = User.objects.get(username="admin")
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()

        options = webdriver.ChromeOptions()
        options.headless = True
        path = Path.cwd()
        prefs = {"download.default_directory": str(path)}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
        super().setUp()
            
    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
        

    def test_StopedVotingVisualizer(self):
        q = Question(desc='test question')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        data = {'action': 'stop'}
        response1 = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response1.status_code, 401)
        response =self.driver.get(f'{self.live_server_url}/visualizer/{v.pk}/')
        vState = self.driver.find_element(By.TAG_NAME,"h2").text
        self.assertTrue(vState, "Resultados:")
    

    def test_NoStartedVotingVisualizer(self):
        q = Question(desc='test question')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        self.driver.get(f'{self.live_server_url}/visualizer/{v.pk}/')
        vState= self.driver.find_element(By.TAG_NAME,"h2").text
        self.assertTrue(vState, "Votación no comenzada")


    def test_StartedVotingVisualizer(self):
        q = Question(desc='test question')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        data = {'action': 'start'}
        response1 = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response1.status_code, 401)
        self.driver.get(f'{self.live_server_url}/visualizer/{v.pk}/')
        vState= self.driver.find_element(By.TAG_NAME,"h2").text
        self.assertTrue(vState, "Votación en curso")

    def test_DeletedVotingVisualizer(self):
        q = Question(desc='test question')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()

        self.driver.get(f'{self.live_server_url}/admin/')
        user_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="id_username"))

        user_selector.send_keys('admin')
        pass_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="id_password"))

        pass_selector.send_keys('qwerty')
        submit_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element_by_xpath('//*[@id="login-form"]/div[3]/input'))
        submit_selector.click()
        self.driver.get(f'{self.live_server_url}')
        self.driver.set_window_size(1450, 873)
        dropdown = Select(self.driver.find_element(By.NAME, "language"))
        dropdown.select_by_visible_text("español (es)")
        self.driver.find_element(By.ID, "change-language-button").click()
        self.driver.get(f'{self.live_server_url}/admin/')


        self.driver.find_element(By.LINK_TEXT, "Auths").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(self.live_server_url)
        self.driver.find_element(By.ID, "id_url").click()
        self.driver.find_element(By.ID, "id_url").send_keys(self.live_server_url)
        self.driver.find_element(By.NAME, "_save").click()
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_name").send_keys("voting test")
        self.driver.find_element(By.ID, "id_desc").click()
        self.driver.find_element(By.ID, "id_desc").send_keys("voting desc")
        dropdown = self.driver.find_element(By.ID, "id_question")
        dropdown.find_element(By.XPATH, "//option[. = 'test question']").click()
        element = self.driver.find_element(By.ID, "id_question")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.ID, "id_question")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.ID, "id_question")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        dropdown = self.driver.find_element(By.ID, "id_auths")
        print(self.live_server_url)
        dropdown.find_element(By.XPATH, "//option[. = '" + self.live_server_url + "']").click()
        self.driver.find_element(By.NAME, "_save").click()

        v=Voting.objects.get(name='voting test')
        
        self.driver.find_element(By.NAME, "_selected_action").click()
        dropdown = Select(self.driver.find_element(By.NAME, "action"))

        dropdown.select_by_visible_text("Eliminar votings seleccionado/s")
        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.NAME, "index").click()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(4)").click()
        response = self.client.get(f'{self.live_server_url}/visualizer/{v.pk}/')        
        self.assertEqual(response.status_code, 404)

class CensusPageTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        u = User(username='Enrique', is_staff=True)
        u.set_password('qwerty')
        u.save()

        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        v.create_pubkey()
        v.start_date = timezone.now()
        time.sleep(5)
        v.end_date = timezone.now()
        v.save()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()
        self.census = None
        self.user = None

    def test_visualizer_detail(self):
        self.driver.get(f'{self.live_server_url}/admin')
        self.driver.find_element(By.ID, "id_username").send_keys('Enrique')
        self.driver.find_element(By.ID, "id_password").send_keys('qwerty',Keys.ENTER)

        time.sleep(5)
        self.driver.get(f'{self.live_server_url}/visualizer/1')
        time.sleep(5)
        self.assertTrue(len(self.driver.find_elements(By.ID,'app-visualizer'))==1)
        self.assertTrue(len(self.driver.find_elements(By.ID,'visualizer-table')) == 1)

class visualizerTranslationCase(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        self.voting = Voting.objects.create(name='test voting', question=q)
        self.voting.save()
        

        self.voting.create_pubkey()
        self.voting.start_date = timezone.now()
        time.sleep(5)
        self.voting.end_date = timezone.now()
        self.voting.save()

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
        id_voting = Voting.objects.get(name='test voting')
        self.driver.get('{}/visualizer/{}'.format(self.live_server_url, id_voting))        
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(4)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#app-visualizer > div > h1"))
        self.assertEqual(header_text.text, "Votement {}".format(id_voting))
        
    def test_german_translation(self):
        self.driver.set_window_size(1920,1080)
        id_voting = Voting.objects.get(name='test voting')
        self.driver.get('{}/visualizer/{}'.format(self.live_server_url, id_voting))  
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(3)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#app-visualizer > div > h1"))
        self.assertEqual(header_text.text, "Abstimmung {}".format(id_voting))
    
    def test_spanish_translation(self):
        self.driver.set_window_size(1920,1080)
        id_voting = Voting.objects.get(name='test voting')
        self.driver.get('{}/visualizer/{}'.format(self.live_server_url, id_voting))  
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(1)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#app-visualizer > div > h1"))
        self.assertEqual(header_text.text, "Votación {}".format(id_voting))

    def test_english_translation(self):
        self.driver.set_window_size(1920,1080)
        id_voting = Voting.objects.get(name='test voting')
        self.driver.get('{}/visualizer/{}'.format(self.live_server_url, id_voting))  
        language_selector = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.NAME, value="language"))
        language_selector.click()
        selected_language = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="select > option:nth-child(2)"))
        selected_language.click()
        change_language_button = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="change-language-button"))
        change_language_button.click()
        header_text = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="#app-visualizer > div > h1"))
        self.assertEqual(header_text.text, "Voting {}".format(id_voting))
