import os
from base.tests import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.utils import timezone
from voting.models import Voting, Question, QuestionOption
from census.models import Census

from postproc.models import UserProfile
from django.contrib.auth.models import User
from mixnet.models import Auth
from django.contrib.auth import get_user_model
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
from django.conf import settings
import time
import datetime
from rest_framework.authtoken.models import Token
import random
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
import itertools
from base import mods

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select




import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from urllib3.connectionpool import log as urllibLogger






# Create your tests here.
class DashBoard_test_case(StaticLiveServerTestCase):

    def setUp(self):
        # Load base test functionality for decide
        LOGGER.setLevel(logging.WARNING)
        urllibLogger.setLevel(logging.WARNING)
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
        self.driver.set_window_size(1920,1080)

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
        response = self.driver.get(f'{self.live_server_url}/dashboard/dashboard')
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
        response = self.driver.get(f'{self.live_server_url}/dashboard/dashboard')
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
        self.driver.get(f'{self.live_server_url}/admin/')
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

        self.driver.get(f'{self.live_server_url}/dashboard/dashboard')
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
        response = self.driver.get(f'{self.live_server_url}/dashboard/dashboard')
        percentages_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="noadmin"))
        self.assertEqual(percentages_selector.text, "noadmin")

    def test_vote_dashboard_user_negative_2(self):
        q = Question(desc='test questcccion')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()
        response = self.driver.get(f'{self.live_server_url}/dashboard/dashboard')
        percentages_selector = WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(by=By.ID, value="noadmin"))
        self.assertNotEqual(percentages_selector.text, "adminadmin")

    def test_vote_dashboard_census_negative_2(self):
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

        # añadir censo
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_voting_id").send_keys("2")
        self.driver.find_element(By.ID, "id_voter_id").click()
        self.driver.find_element(By.ID, "id_voter_id").send_keys("4")
        self.driver.find_element(By.NAME, "_save").click()

        # crear votación
        self.driver.get(f'{self.live_server_url}/admin/')
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


        self.driver.get(f'{self.live_server_url}/dashboard/dashboard')
        percentages_selector =""
        try:
            percentages_selector = self.driver.find_element(by=By.ID, value=v.pk)
        except:

            self.assertEqual(len(percentages_selector), 0)

    def test_download_pdf(self):

        self.driver.get(f'{self.live_server_url}/dashboard/dashboard')
        self.driver.find_element_by_xpath('//*[@id="descargar"]').click()
        time.sleep(10)
        path = str(Path.cwd())
        self.assertEqual(True,os.path.isfile(path+"/record.pdf"))
        os.remove(path+"/record.pdf")


class DashBoard2TestCase(BaseTestCase):

    def setUp(self):
        LOGGER.setLevel(logging.WARNING)
        urllibLogger.setLevel(logging.WARNING)
        super().setUp()

    def tearDown(self):
        super().tearDown()


    def test_get_to_dashboard(self):

        response = self.client.get('/dashboard/dashboard')
        self.assertEqual(response.status_code, 200)

    
class Dashboard_TestCase(StaticLiveServerTestCase):

    def setUp(self):
        LOGGER.setLevel(logging.WARNING)
        urllibLogger.setLevel(logging.WARNING)
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
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

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
        rq = self.client.get("/dashboard/dashboard/"+str(v.id)+"/")
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

        self.driver.get(f'{self.live_server_url}/dashboard/dashboard/{v.id}/')
        tim = self.driver.find_element(By.CLASS_NAME, "time").text
        self.assertEqual(tim,"No comenzada")

    
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
        rq = self.client.get("/dashboard/dashboard/"+str(v.id)+"/")
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

        self.driver.get(f'{self.live_server_url}/dashboard/dashboard/{v.id}/')
        tim = self.driver.find_element(By.CLASS_NAME, "time").text
        self.assertEqual(tim,"No finalizada")


    def test_positive_model_data_normal_no_tally_and_voting_desc(self):

        q = Question(questionType="normal",desc = "TestQ")
        q.save()
        qo1 = QuestionOption(question=q, number = 1, option = "Tortilla")
        qo2 = QuestionOption(question=q, number = 2, option = "Arroz")
        qo1.save()
        qo2.save()
        q.save()
        v = Voting(name='test v', desc = "Votación de prueba", question=q)
        v.save()
        v.create_pubkey()
        v.save()
        v.start_date = timezone.now()
        v.end_date = timezone.now()
        v.save()
        rq = self.client.get("/dashboard/dashboard/"+str(v.id)+"/")
        self.assertEqual(rq.status_code,200)

        time = v.end_date-v.start_date
        duracion = str(time - datetime.timedelta(microseconds=time.microseconds))

        self.assertEqual(rq.context.get('time'),duracion)
        self.assertEqual(rq.context.get('description'),v.desc)
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


        self.driver.get(f'{self.live_server_url}/dashboard/dashboard/{v.id}/')
        tim = self.driver.find_element(By.CLASS_NAME, "time").text
        self.assertEqual(tim,"0:00:00")

        dsc = self.driver.find_element(By.CLASS_NAME, "description").text
        self.assertEqual(dsc,"Votación de prueba")

    
    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question()
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    
    def create_voters_m(self, v):

        for i in range(40):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            
    
            u.save()

            if i%3 == 0:
                a = UserProfile(genre = 'W', user = u)
                a.save()
            else:
                a = UserProfile(genre = 'M', user = u)
                a.save()

            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    
    def create_voters_w(self, v):
        for i in range(40):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            if i%3 == 0:
                a = UserProfile(genre = 'M', user = u)
                a.save()
            else:
                a = UserProfile(genre = 'W', user = u)
                a.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def create_voters(self, v):
        for i in range(40):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()


    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.genre = 'M'
        user.save()
        return user
    
    def create_voting_dhondt(self):
        q = Question(desc='test question', questionType="dhondt")
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.base.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear
    

    def test_complete_voting_normal(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.base.login()  # set token
        v.tally_votes(self.base.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

        v.end_date = timezone.now()
      
        v.do_postproc()
        v.tally_votes()
        v.save()
        time = v.end_date - v.start_date
        duracion = str(time - datetime.timedelta(microseconds = time.microseconds))

        rq = self.client.get("/dashboard/dashboard/" + str(v.id) + "/")
        self.assertEqual(rq.status_code, 200)

        #"Check that the data assigned to the model is correct"
        self.assertEqual(rq.context.get('time'), duracion)
        self.assertEqual(rq.context.get('description'),"No hay una descripción asociada a esta votación ni a esta pregunta")
        self.assertEqual(rq.context.get('questionType'),'normal')

        postpro = v.postproc
        options = ['option 1', 'option 2', 'option 3', 'option 4', 'option 5']
        values = []
        numberOfVotes = 0
        numberOfPeople = len(Census.objects.filter(voting_id = v.id))
        #'Como se generan de forma aleatoria hay que calcularlo aquí'
        for vote in postpro:
            values.append(vote['votes'])
            numberOfVotes = numberOfVotes + vote['votes']

        self.assertEqual(rq.context.get('numberOfVotes'), numberOfVotes)
        
        self.assertListEqual(sorted(rq.context.get('labels')), sorted(options))
        self.assertEqual(rq.context.get('values'), values)

        self.assertEqual(rq.context.get('labels2'),["Votaron","No votaron"])
        self.assertEqual(rq.context.get('values2'),[numberOfVotes,numberOfPeople-numberOfVotes])
        self.assertEqual(rq.context.get('parity'),True)

        #"Get the HTML elements to check if the data from the model is processed correctly"
        self.driver.get(f'{self.live_server_url}/dashboard/dashboard/{v.id}/')
        numeroVotos = self.driver.find_element(By.CLASS_NAME, "numervotes").text
        tipoPregunta = self.driver.find_element(By.CLASS_NAME, "questionType").text
        desc_nav = self.driver.find_element(By.CLASS_NAME, "description").text
        parity = self.driver.find_element(By.CLASS_NAME, "parity").text
        chart = self.driver.find_element(By.ID, "myChart")
        chart2 = self.driver.find_element(By.ID, "my2Chart")
        chart3 = self.driver.find_element(By.ID, "my3Chart")

        self.assertEqual(tipoPregunta, "normal")
        self.assertEqual(desc_nav,"No hay una descripción asociada a esta votación ni a esta pregunta")
        self.assertEqual(numeroVotos,str(numberOfVotes))
        self.assertEqual(parity,'Se ha cumplido la paridad para esta votación')
        #"Check that the charts are displayed"
        self.assertTrue(chart != None)
        self.assertTrue(chart2 != None)
        self.assertTrue(chart3 != None)


    
    def test_voting_normal_more_woman(self):

        v = self.create_voting()
        self.create_voters_w(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.base.login()  # set token
        v.tally_votes(self.base.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])
        
        v.end_date = timezone.now()
      
        v.do_postproc()
        v.tally_votes()
        censo = list(Census.objects.filter(voting_id = v.id))
        user_id_list = []
        for id in censo:
            user_id_list.append(id.voter_id)
        v.get_paridad(user_id_list)
        v.save()

        rq = self.client.get("/dashboard/dashboard/" + str(v.id) + "/")
        self.assertEqual(rq.status_code, 200)

        postpro = v.postproc

        values = []
        numberOfVotes = 0

        'Como se generan de forma aleatoria hay que calcularlo aquí'
        for vote in postpro:
            values.append(vote['votes'])
            numberOfVotes = numberOfVotes + vote['votes']

        self.assertEqual(rq.context.get('numberOfVotes'), numberOfVotes)

        self.assertEqual(rq.context.get('parity'),False)

        self.assertEqual(list(rq.context.get('labels3')),['Hombre','Mujer','Otros'])
        self.assertEqual(rq.context.get('values3'),[v.num_votes_M, v.num_votes_W, numberOfVotes - (v.num_votes_M+v.num_votes_W)])
        self.assertEqual(rq.context.get('mayor'),'mujeres')
        self.assertEqual(rq.context.get('menor'),'hombres')

        numDif = abs(v.num_votes_M - v.num_votes_W)
        "Get the HTML elements to check if the data from the model is processed correctly"
        self.driver.get(f'{self.live_server_url}/dashboard/dashboard/{v.id}/')
        numeroVotos = self.driver.find_element(By.CLASS_NAME, "numervotes").text
        tipoPregunta = self.driver.find_element(By.CLASS_NAME, "questionType").text
        desc_nav = self.driver.find_element(By.CLASS_NAME, "description").text
        parity = self.driver.find_element(By.CLASS_NAME, "parity").text
        chart = self.driver.find_element(By.ID, "myChart")
        chart2 = self.driver.find_element(By.ID, "my2Chart")
        chart3 = self.driver.find_element(By.ID, "my3Chart")

        self.assertEqual(tipoPregunta, "normal")
        self.assertEqual(desc_nav,"No hay una descripción asociada a esta votación ni a esta pregunta")
        self.assertEqual(numeroVotos,str(numberOfVotes))
        if(numDif == 1):
            self.assertEqual(parity,'No se ha cumplido la paridad para esta votación, hay ' + str(numDif) + ' voto más de mujeres que de hombres')
        else:
            self.assertEqual(parity,'No se ha cumplido la paridad para esta votación, hay ' + str(numDif) + ' votos más de mujeres que de hombres')
        
        "Check that the charts are displayed"
        self.assertTrue(chart != None)
        self.assertTrue(chart2 != None)
        self.assertTrue(chart3 != None)
   

    def test_voting_normal_more_man(self):

        v = self.create_voting()
        self.create_voters_m(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.base.login()  # set token
        v.tally_votes(self.base.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])
        
        v.end_date = timezone.now()
      
        v.do_postproc()
        v.tally_votes()
        censo = list(Census.objects.filter(voting_id = v.id))
        user_id_list = []
        for id in censo:
            user_id_list.append(id.voter_id)
        v.get_paridad(user_id_list)
        v.save()

        rq = self.client.get("/dashboard/dashboard/" + str(v.id) + "/")
        self.assertEqual(rq.status_code, 200)

        postpro = v.postproc

        values = []
        numberOfVotes = 0

        'Como se generan de forma aleatoria hay que calcularlo aquí'
        for vote in postpro:
            values.append(vote['votes'])
            numberOfVotes = numberOfVotes + vote['votes']

        self.assertEqual(rq.context.get('numberOfVotes'), numberOfVotes)

        self.assertEqual(rq.context.get('parity'),False)

        self.assertEqual(list(rq.context.get('labels3')),['Hombre','Mujer','Otros'])
        self.assertEqual(rq.context.get('values3'),[v.num_votes_M, v.num_votes_W, numberOfVotes - (v.num_votes_M+v.num_votes_W)])
        self.assertEqual(rq.context.get('mayor'),'hombres')
        self.assertEqual(rq.context.get('menor'),'mujeres')

        numDif = abs(v.num_votes_M - v.num_votes_W)
        "Get the HTML elements to check if the data from the model is processed correctly"
        self.driver.get(f'{self.live_server_url}/dashboard/dashboard/{v.id}/')
        numeroVotos = self.driver.find_element(By.CLASS_NAME, "numervotes").text
        tipoPregunta = self.driver.find_element(By.CLASS_NAME, "questionType").text
        desc_nav = self.driver.find_element(By.CLASS_NAME, "description").text
        parity = self.driver.find_element(By.CLASS_NAME, "parity").text
        chart = self.driver.find_element(By.ID, "myChart")
        chart2 = self.driver.find_element(By.ID, "my2Chart")
        chart3 = self.driver.find_element(By.ID, "my3Chart")

        self.assertEqual(tipoPregunta, "normal")
        self.assertEqual(desc_nav,"No hay una descripción asociada a esta votación ni a esta pregunta")
        self.assertEqual(numeroVotos,str(numberOfVotes))
        if(numDif == 1):
            self.assertEqual(parity,'No se ha cumplido la paridad para esta votación, hay ' + str(numDif) + ' voto más de hombres que de mujeres')
        else:
            self.assertEqual(parity,'No se ha cumplido la paridad para esta votación, hay ' + str(numDif) + ' votos más de hombres que de mujeres')
        
        "Check that the charts are displayed"
        self.assertTrue(chart != None)
        self.assertTrue(chart2 != None)
        self.assertTrue(chart3 != None)

    
    def test_complete_voting_dhondt(self):

        v = self.create_voting_dhondt()
        self.create_voters(v)
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.base.login()  # set token
        v.tally_votes(self.base.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

        v.end_date = timezone.now()
      
        v.do_postproc()
        v.tally_votes()
        v.save()
        rq = self.client.get("/dashboard/dashboard/" + str(v.id) + "/")
        self.assertEqual(rq.status_code, 200)

        postpro = v.postproc
        options = ['option 1', 'option 2', 'option 3', 'option 4', 'option 5']
        values = []
        numberOfVotes = 0
        numberOfPeople = len(Census.objects.filter(voting_id = v.id))
        'Como se generan de forma aleatoria hay que calcularlo aquí'

        for vote in postpro:
            options.append(vote['option'])
            values.append(vote['postproc'])
            numberOfVotes = numberOfVotes + vote['votes']

        self.assertEqual(rq.context.get('numberOfVotes'), numberOfVotes)
        
        self.assertEqual(set(rq.context.get('labels')), set(options))
        self.assertEqual(rq.context.get('values'), values)

        self.assertEqual(rq.context.get('labels2'),["Votaron","No votaron"])
        self.assertEqual(rq.context.get('values2'),[numberOfVotes,numberOfPeople-numberOfVotes])
        self.assertEqual(rq.context.get('parity'),True)

        "Get the HTML elements to check if the data from the model is processed correctly"
        self.driver.get(f'{self.live_server_url}/dashboard/dashboard/{v.id}/')
        numeroVotos = self.driver.find_element(By.CLASS_NAME, "numervotes").text
        tipoPregunta = self.driver.find_element(By.CLASS_NAME, "questionType").text
        desc_nav = self.driver.find_element(By.CLASS_NAME, "description").text
        parity = self.driver.find_element(By.CLASS_NAME, "parity").text
        chart = self.driver.find_element(By.ID, "myChart")
        chart2 = self.driver.find_element(By.ID, "my2Chart")
        chart3 = self.driver.find_element(By.ID, "my3Chart")

        self.assertEqual(parity,'Se ha cumplido la paridad para esta votación')
        self.assertEqual(tipoPregunta, "dhondt")
        self.assertEqual(desc_nav,"test question")
        self.assertEqual(numeroVotos,str(numberOfVotes))
        
        "Check that the charts are displayed"
        self.assertTrue(chart != None)
        self.assertTrue(chart2 != None)
        self.assertTrue(chart3 != None)
    



