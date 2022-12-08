from base.tests import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from django.utils import timezone
from voting.models import Voting, Question, QuestionOption
from census.models import Census
from voting import tests
from django.contrib.auth.models import User
from mixnet.models import Auth
from django.contrib.auth import get_user_model
from selenium.webdriver.common.action_chains import ActionChains
from voting.models import Voting
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

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


'''

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
'''

class Dashboard_TestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

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

    
    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

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
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

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
        time = v.end_date-v.start_date
        duracion = str(time - datetime.timedelta(microseconds=time.microseconds))

        rq = self.client.get("/dashboard/"+str(v.id)+"/")
        self.assertEqual(rq.status_code,200)

        self.assertEqual(rq.context.get('time'),duracion)
        self.assertEqual(rq.context.get('description'),"No hay una descripción asociada a esta votación ni a esta pregunta")
        '''
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
        self.assertEqual(response.context.get(''))
        '''


        




