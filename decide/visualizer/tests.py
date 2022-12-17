from django.contrib.auth.models import User
from base.tests import BaseTestCase
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from django.test import Client
from voting.models import Voting, Question, QuestionOption

from selenium import webdriver
from selenium.webdriver.common.by import By

from base.tests import BaseTestCase
import time

# Create your tests here.
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