from django.test import TestCase
from rest_framework.views import APIView

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.response import Response
from .views import d_hondt

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_complete_borda(self):
        data = {
            'type': 'IDENTITY', 
            'options': [{'option': 'Respuesta 1', 'number': 1, 'votes': 3}, {'option': 'Respuesta 2', 'number': 2, 'votes': 3}, {'option': 'Respuesta 3', 'number': 3, 'votes': 3}], 
            'extra': [1, 3, 2, 3, 2, 1, 1, 3, 2], 
            'questionType': 'borda'}

        expected_result = [
            { 'option': 'Respuesta 1', 'number': 1, 'votes': 3, 'postproc': 7 },
            { 'option': 'Respuesta 3', 'number': 3, 'votes': 3, 'postproc': 7 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 3, 'postproc': 4 },
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_same_order_borda(self):
        data = {
            'type': 'IDENTITY', 
            'options': [{'option': 'Respuesta 1', 'number': 1, 'votes': 3}, {'option': 'Respuesta 2', 'number': 2, 'votes': 3}, {'option': 'Respuesta 3', 'number': 3, 'votes': 3}], 
            'extra': [1, 3, 2, 1, 3, 2, 1, 3, 2], 
            'questionType': 'borda'}

        expected_result = [
            { 'option': 'Respuesta 1', 'number': 1, 'votes': 3, 'postproc': 9 },
            { 'option': 'Respuesta 3', 'number': 3, 'votes': 3, 'postproc': 6 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 3, 'postproc': 3 }    
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_same_results_borda(self):
        data = {
            'type': 'IDENTITY', 
            'options': [{'option': 'Respuesta 1', 'number': 1, 'votes': 3}, {'option': 'Respuesta 2', 'number': 2, 'votes': 3}, {'option': 'Respuesta 3', 'number': 3, 'votes': 3}], 
            'extra': [1, 3, 2, 3, 2, 1, 2, 1, 3], 
            'questionType': 'borda'}

        expected_result = [
            { 'option': 'Respuesta 1', 'number': 1, 'votes': 3, 'postproc': 6 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 3, 'postproc': 6 },
            { 'option': 'Respuesta 3', 'number': 3, 'votes': 3, 'postproc': 6 }    
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_wrong_data_borda(self):
        data = {
            'type': 'IDENTITY', 
            'options': [{'option': 'Respuesta 1', 'number': 1, 'votes': 3}, {'option': 'Respuesta 2', 'number': 2, 'votes': 3}, {'option': 'Respuesta 3', 'number': 3, 'votes': 3}], 
            'extra': [1, 3, 2, 3, 2, 1, 1, 3, 2], 
            'questionType': 'borda'}

        expected_result = [
            { 'option': 'Respuesta 1', 'number': 10, 'votes': 3, 'postproc': 7 },
            { 'option': 'Respuesta 3', 'number': 310, 'votes': 3, 'postproc': 7 },
            { 'option': 'Respuesta 2', 'number': 2123123, 'votes': 3, 'postproc': 4 },
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEquals(values, expected_result)

    def test_wrong_postproc_borda(self):
        data = {
            'type': 'IDENTITY', 
            'options': [{'option': 'Respuesta 1', 'number': 1, 'votes': 3}, {'option': 'Respuesta 2', 'number': 2, 'votes': 3}, {'option': 'Respuesta 3', 'number': 3, 'votes': 3}], 
            'extra': [1, 3, 2, 3, 2, 1, 1, 3, 2], 
            'questionType': 'borda'}

        expected_result = [
            { 'option': 'Respuesta 1', 'number': 1, 'votes': 3, 'postproc': 6 },
            { 'option': 'Respuesta 3', 'number': 3, 'votes': 3, 'postproc': 56388 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 3, 'postproc': 6 },
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEquals(values, expected_result)

    def test_wrong_votes_borda(self):
        data = {
            'type': 'IDENTITY', 
            'options': [{'option': 'Respuesta 1', 'number': 1, 'votes': 3}, {'option': 'Respuesta 2', 'number': 2, 'votes': 3}, {'option': 'Respuesta 3', 'number': 3, 'votes': 3}], 
            'extra': [1, 3, 2, 3, 2, 1, 1, 3, 2], 
            'questionType': 'borda'}

        expected_result = [
            { 'option': 'Respuesta 1', 'number': 1, 'votes': 3, 'postproc': 6 },
            { 'option': 'Respuesta 3', 'number': 3, 'votes': 1000, 'postproc': 6 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 3, 'postproc': 6 },
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEquals(values, expected_result)

    def test_no_data_borda(self):
        data = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.data, Response([]).data)

    def test_more_votes_borda(self):
        data = {
            'type': 'IDENTITY', 
            'options': [{'option': 'Respuesta 1', 'number': 1, 'votes': 3}, {'option': 'Respuesta 2', 'number': 2, 'votes': 3}, {'option': 'Respuesta 3', 'number': 3, 'votes': 3}], 
            'extra': [1, 3, 2, 3, 2, 1, 1, 3, 2, 8], 
            'questionType': 'borda'}

        with self.assertRaises(KeyError):
            self.client.post('/postproc/', data, format='json')

    #DHONDT API TESTS
    def test_positive_dhondt(self):
        data = {
            'type': 'IDENTITY',
            'seats': 15, 
            'options': [
                { 'option': 'Respuesta 1', 'number': 1, 'votes': 3 },
                { 'option': 'Respuesta 2', 'number': 2, 'votes': 7 },
                { 'option': 'Respuesta 3', 'number': 3, 'votes': 3 }, 
            ],
            'extra': [3,1,1,1,2,1,1,3,1,3,2,2,1], 
            'questionType': 'dhondt'}

        expected_result = [
            { 'option': 'Respuesta 1', 'number': 1, 'votes': 3, 'postproc': 9 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 7, 'postproc': 3 },
            { 'option': 'Respuesta 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_negative_dhondt_wrong_seats_valute(self):
        data_negative = {
            'type': 'IDENTITY',
            'seats': -7, 
            'options': [
                { 'option': 'Respuesta 1', 'number': 1, 'votes': 3 },
                { 'option': 'Respuesta 2', 'number': 2, 'votes': 7 },
                { 'option': 'Respuesta 3', 'number': 3, 'votes': 3 }, 
            ],
            'extra': [3,1,1,1,2,1,1,3,1,3,2,2,1], 
            'questionType': 'dhondt'}

        data_zero = {
            'type': 'IDENTITY',
            'seats': 0, 
            'options': [
                { 'option': 'Respuesta 1', 'number': 1, 'votes': 3 },
                { 'option': 'Respuesta 2', 'number': 2, 'votes': 7 },
                { 'option': 'Respuesta 3', 'number': 3, 'votes': 3 }, 
            ],
            'extra': [3,1,1,1,2,1,1,3,1,3,2,2,1], 
            'questionType': 'dhondt'}

        data_no_seats = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Respuesta 1', 'number': 1, 'votes': 3 },
                { 'option': 'Respuesta 2', 'number': 2, 'votes': 7 },
                { 'option': 'Respuesta 3', 'number': 3, 'votes': 3 }, 
            ],
            'extra': [3,1,1,1,2,1,1,3,1,3,2,2,1], 
            'questionType': 'dhondt'}

        with self.assertRaises(ValueError):
            self.client.post('/postproc/', data_negative, format='json')

        with self.assertRaises(ValueError):
            self.client.post('/postproc/', data_zero, format='json')

        with self.assertRaises(TypeError):
            self.client.post('/postproc/', data_no_seats, format='json')


class PostProcUnitTestCase(TestCase):

    def test_unit_positive_dhondt(self):
        seats = 15
        tally = [0,1,1,1,2,1,1,0,1,0,2,2,1]
        opts = [
            { 'option': 'Respuesta 1', 'number': 0, 'votes': 3 },
            { 'option': 'Respuesta 3', 'number': 1, 'votes': 7 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 3 }, 
        ]
        result = d_hondt(tally, seats, opts)

        self.assertEqual(result[0], 3)
        self.assertEqual(result[1], 9)
        self.assertEqual(result[2], 3)

    def test_unit_negative_dhondt(self):
        seats_negative = -2
        seats_zero = 0
        tally = [0,1,1,1,2,1,1,0,1,0,2,2,1]
        opts = [
            { 'option': 'Respuesta 1', 'number': 0, 'votes': 3 },
            { 'option': 'Respuesta 3', 'number': 1, 'votes': 7 },
            { 'option': 'Respuesta 2', 'number': 2, 'votes': 3 }, 
        ]

        with self.assertRaises(ValueError):
            d_hondt(tally, seats_negative, opts)
        
        with self.assertRaises(ValueError):
            d_hondt(tally, seats_zero, opts)
