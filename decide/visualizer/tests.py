from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select




from base.tests import BaseTestCase
from voting.models import Question, Voting


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
