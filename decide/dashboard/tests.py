from base.tests import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from django.utils import timezone
from voting.models import Voting, Question, QuestionOption
from census.models import Census
from store.models import Vote
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from selenium.webdriver.common.action_chains import ActionChains
from voting.models import Voting
from pathlib import Path
import time
import datetime
import os.path

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




# Create your tests here.
class DashBoard_test_case(StaticLiveServerTestCase):

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

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()



    def test_vote_dashboard_user_positive(self):
        q = Question(desc='test questcccion')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()
        response = self.driver.get(f'{self.live_server_url}/dashboard')
        percentages_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="noadmin"))
        self.assertEqual(percentages_selector.text,"noadmin")



    def test_vote_dashboard_user_negative(self):
        q = Question(desc='test questcccion')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()
        response = self.driver.get(f'{self.live_server_url}/dashboard')
        percentages_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="noadmin"))
        self.assertNotEqual(percentages_selector.text,"adminadmin")



    
    def test_vote_dashboard_census_positive(self):
        q = Question(desc='test questionnn')
        q.save()

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
        self.driver.find_element(By.LINK_TEXT, "Auths").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(self.live_server_url)
        self.driver.find_element(By.ID, "id_url").click()
        self.driver.find_element(By.ID, "id_url").send_keys(self.live_server_url)
        self.driver.find_element(By.NAME, "_save").click()

        #añadir censo
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_voting_id").send_keys("2")
        self.driver.find_element(By.ID, "id_voter_id").click()
        self.driver.find_element(By.ID, "id_voter_id").send_keys("4")
        self.driver.find_element(By.NAME, "_save").click()


        #crear votación
        self.driver.find_element(By.LINK_TEXT, "Inicio").click()
        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_name").send_keys("voting test")
        self.driver.find_element(By.ID, "id_desc").click()
        self.driver.find_element(By.ID, "id_desc").send_keys("voting desc")
        dropdown = self.driver.find_element(By.ID, "id_question")
        dropdown.find_element(By.XPATH, "//option[. = 'test questionnn']").click()
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
        dropdown.find_element(By.XPATH, "//option[. = '"+self.live_server_url+"']").click()
        self.driver.find_element(By.NAME, "_save").click()
        self.driver.find_element(By.NAME, "_selected_action").click()
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()
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
        v=Voting.objects.get(name='voting test')

        self.driver.get(f'{self.live_server_url}/dashboard/')
        percentages_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value=v.pk))
        self.assertNotEqual(percentages_selector.text, "0%")

 
        

        
        
    def test_vote_dashboard_census_negative(self):
        q = Question(desc='test questcccion')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()
        response = self.driver.get(f'{self.live_server_url}/dashboard')
        percentages_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="noadmin"))
        self.assertEqual(percentages_selector.text, "noadmin")

    def test_vote_dashboard_user_negative(self):
        q = Question(desc='test questcccion')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()
        response = self.driver.get(f'{self.live_server_url}/dashboard')
        percentages_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="noadmin"))
        self.assertNotEqual(percentages_selector.text, "adminadmin")

    def test_vote_dashboard_census_negative(self):
        q = Question(desc='test questionnn')
        q.save()

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
        self.driver.find_element(By.LINK_TEXT, "Auths").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(self.live_server_url)
        self.driver.find_element(By.ID, "id_url").click()
        self.driver.find_element(By.ID, "id_url").send_keys(self.live_server_url)
        self.driver.find_element(By.NAME, "_save").click()

        # añadir censo
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_voting_id").send_keys("2")
        self.driver.find_element(By.ID, "id_voter_id").click()
        self.driver.find_element(By.ID, "id_voter_id").send_keys("4")
        self.driver.find_element(By.NAME, "_save").click()

        # crear votación
        self.driver.find_element(By.LINK_TEXT, "Inicio").click()
        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_name").send_keys("voting test")
        self.driver.find_element(By.ID, "id_desc").click()
        self.driver.find_element(By.ID, "id_desc").send_keys("voting desc")
        dropdown = self.driver.find_element(By.ID, "id_question")
        dropdown.find_element(By.XPATH, "//option[. = 'test questionnn']").click()
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
        dropdown.find_element(By.XPATH, "//option[. = '" + self.live_server_url + "']").click()
        self.driver.find_element(By.NAME, "_save").click()

        v=Voting.objects.get(name='voting test')


        self.driver.find_element(By.NAME, "_selected_action").click()
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Eliminar votings seleccionado/s']").click()
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


        self.driver.get(f'{self.live_server_url}/dashboard/')
        percentages_selector =""
        try:
            percentages_selector = self.driver.find_element(by=By.ID, value=v.pk)
        except:

            self.assertEqual(len(percentages_selector), 0)

    def test_download_pdf(self):
        self.driver.get(f'{self.live_server_url}/dashboard/')
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(7)").click()
        time.sleep(10)
        path = str(Path.cwd())
        self.assertEqual(True,os.path.isfile(path+"/record.pdf"))
        os.remove(path+"/record.pdf")


class DashBoard2TestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


    def test_get_to_dashboard(self):

        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 301)


class Dashboard_votTestCase(BaseTestCase):

    def setUp(self):

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

    def test_positive_model_data_normal_no_start(self):

        q = Question(questionType="normal",desc = "TestQ")
        q.save()
        qo1 = QuestionOption(question=q, number = 1, option = "Tortilla")
        qo2 = QuestionOption(question=q, number = 2, option = "Arroz")
        qo1.save()
        qo2.save()
        q.save()
        v = Voting(name='test v', question=q)
        v.save()
        v.create_pubkey()
        v.save()
        rq = self.client.get("/dashboard/"+str(v.id)+"/")
        self.assertEqual(rq.status_code,200)
        self.assertEqual(rq.context.get('time'),'Aún no ha comenzado')
        self.assertEqual(rq.context.get('description'),q.desc)
        self.assertEqual(rq.context.get('questionType'),q.questionType)
        self.assertEqual(rq.context.get('numberOfVotes'),0)
        self.assertEqual(rq.context.get('labels'),[qo1.option,qo2.option])
        self.assertEqual(rq.context.get('values'),[0,0])
        self.assertEqual(rq.context.get('labels2'),["Votaron","No votaron"])
        self.assertEqual(rq.context.get('values2'),[0,0])
        self.assertEqual(rq.context.get('parity'),True)
        self.assertEqual(list(rq.context.get('labels3')),['Hombre','Mujer','Otros'])
        self.assertEqual(rq.context.get('values3'),[0,0,0])
        self.assertEqual(rq.context.get('mayor'),'')
        self.assertEqual(rq.context.get('menor'),'')
    
    def test_positive_model_data_normal_no_finish(self):

        q = Question(questionType="normal",desc = "TestQ")
        q.save()
        qo1 = QuestionOption(question=q, number = 1, option = "Tortilla")
        qo2 = QuestionOption(question=q, number = 2, option = "Arroz")
        qo1.save()
        qo2.save()
        q.save()
        v = Voting(name='test v', question=q)
        v.save()
        v.create_pubkey()
        v.save()
        v.start_date = timezone.now()
        v.save()
        rq = self.client.get("/dashboard/"+str(v.id)+"/")
        self.assertEqual(rq.status_code,200)
        self.assertEqual(rq.context.get('time'),'Aún no ha terminado')
        self.assertEqual(rq.context.get('description'),q.desc)
        self.assertEqual(rq.context.get('questionType'),q.questionType)
        self.assertEqual(rq.context.get('numberOfVotes'),0)
        self.assertEqual(rq.context.get('labels'),[qo1.option,qo2.option])
        self.assertEqual(rq.context.get('values'),[0,0])
        self.assertEqual(rq.context.get('labels2'),["Votaron","No votaron"])
        self.assertEqual(rq.context.get('values2'),[0,0])
        self.assertEqual(rq.context.get('parity'),True)
        self.assertEqual(list(rq.context.get('labels3')),['Hombre','Mujer','Otros'])
        self.assertEqual(rq.context.get('values3'),[0,0,0])
        self.assertEqual(rq.context.get('mayor'),'')
        self.assertEqual(rq.context.get('menor'),'')

    def test_positive_model_data_normal_no_tally(self):

        q = Question(questionType="normal",desc = "TestQ")
        q.save()
        qo1 = QuestionOption(question=q, number = 1, option = "Tortilla")
        qo2 = QuestionOption(question=q, number = 2, option = "Arroz")
        qo1.save()
        qo2.save()
        q.save()
        v = Voting(name='test v', question=q)
        v.save()
        v.create_pubkey()
        v.save()
        v.start_date = timezone.now()
        v.end_date = timezone.now()
        v.save()
        rq = self.client.get("/dashboard/"+str(v.id)+"/")
        self.assertEqual(rq.status_code,200)

        time = v.end_date-v.start_date
        duracion = str(time - datetime.timedelta(microseconds=time.microseconds))

        self.assertEqual(rq.context.get('time'),duracion)
        self.assertEqual(rq.context.get('description'),q.desc)
        self.assertEqual(rq.context.get('questionType'),q.questionType)
        self.assertEqual(rq.context.get('numberOfVotes'),0)
        self.assertEqual(rq.context.get('labels'),[qo1.option,qo2.option])
        self.assertEqual(rq.context.get('values'),[0,0])
        self.assertEqual(rq.context.get('labels2'),["Votaron","No votaron"])
        self.assertEqual(rq.context.get('values2'),[0,0])
        self.assertEqual(rq.context.get('parity'),True)
        self.assertEqual(list(rq.context.get('labels3')),['Hombre','Mujer','Otros'])
        self.assertEqual(rq.context.get('values3'),[0,0,0])
        self.assertEqual(rq.context.get('mayor'),'')
        self.assertEqual(rq.context.get('menor'),'')



        """
        user1 = User(username = "usuario1")
        user1.set_password('Constraseñaa11')
        user1.save()
        user2 = User(username = "usuario2")
        user2.set_password('Constraseñaa22')
        user2.save()
        user3 = User(username = "usuario3")
        user3.set_password('Constraseñaa33')
        user3.save()

        us = User.objects.filter(username="usuario2")
        self.assertEqual(user2,us[0])

        census1 = Census(voting_id = v.id, voter_id=user1.id)
        census2 = Census(voting_id = v.id, voter_id=user2.id)
        census3 = Census(voting_id = v.id, voter_id=user3.id)
        census1.save()
        census2.save()
        census3.save()

        cens = Census.objects.filter(voting_id = v.id, voter_id = user2.id)
        self.assertEqual(census2,cens[0])

        
        vote = self.client.post("/store/",request ={'voting' : v, 'voter' : user1, 'vote' : {'a' : 1, 'b' : 2}})
        self.assertEqual(vote.status_code,200)
        voteAux = Vote.objects.filter(voting_id = v.id, voter_id = user1.id)
        print(voteAux)
        """