from os.path import pathsep

from django.db.models.expressions import result
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cafe.models import Order


class OrderAPITestCase(APITestCase):
    fixtures = ['orders.json']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getOrders(self):
        path = reverse('orders-list')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 9)

    def test_postOrders(self):
        data = {
            "table_number": 90,
            "items": {
                "example": 100
            }
        }
        path = reverse('orders-list')
        response = self.client.post(path, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['table_number'], data['table_number'])
        self.assertEqual(response.data['items'], data['items'])

    def test_getDetailOrder(self):
        path = reverse('orders-detail', kwargs={'pk': 3})
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 3)

    def test_deleteDetailOrder(self):
        path = reverse('orders-detail', kwargs={'pk': 3})
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.filter(pk=3).count(), 0)

    def test_updateDetailOrder(self):
        data = {
            "items": {
                "new_data": 9999
            }
        }
        path = reverse('orders-detail', kwargs={'pk': 3})
        response = self.client.patch(path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items'], data['items'])

    def test_getOrderItems(self):
        path = reverse('orders-items', kwargs={'pk': 3})
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, Order.objects.get(pk=3).items)

    def test_patchOrderItems(self):
        path = reverse('orders-items', kwargs={'pk': 3})
        data = {
            "items": {
                "new_data": 101010
            }
        }
        response = self.client.patch(path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data['items'])
        self.assertEqual(Order.objects.get(pk=3).items, data['items'])
