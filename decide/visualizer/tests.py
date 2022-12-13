from django.test import TestCase

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


from base.tests import BaseTestCase
from voting.models import Question, Voting

class VisualizerTestCase(StaticLiveServerTestCase):


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
        data = {'action': 'start'}
        response1 = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response1.status_code, 401)
        data = {'action': 'stop'}
        response1 = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response1.status_code, 401)
        response =self.driver.get(f'{self.live_server_url}/visualizer/{v.pk}/')
        vState = self.driver.find_element(By.TAG_NAME,"h2").text
        self.assertTrue(vState, "Resultados:")
    