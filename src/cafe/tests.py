from django.db.models import Q, Sum
from django.test import TestCase
from django.urls import reverse

from cafe.models import Order


class OrderTestCase(TestCase):
    fixtures = ['orders.json']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_home_page(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/home.html')
        self.assertQuerySetEqual(response.context_data['orders'], Order.objects.all()[:4])
        response = self.client.get(path + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/home.html')
        self.assertQuerySetEqual(response.context_data['orders'], Order.objects.all()[4:8])

    def test_search(self):
        q = '1'
        path = reverse('search')
        response = self.client.get(path + f'?q={q}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/home.html')
        self.assertQuerySetEqual(response.context_data['orders'],
                                 Order.objects.filter(Q(table_number__iregex=q) | Q(status__iregex=q)))

    def test_total(self):
        total = Order.objects.filter(status="Оплачено").aggregate(total=Sum('total_price'))['total']
        path = reverse('total')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/home.html')
        self.assertEqual(response.context_data['total_price'], total)

    def test_detail(self):
        id = 3
        path = reverse('detail', kwargs={'order_id': id})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/detail.html')
        self.assertEqual(response.context_data['object'], Order.objects.get(id=id))

    def test_detail_delete(self):
        id = 3
        path = reverse('detail', kwargs={'order_id': id})
        response = self.client.post(path, {'delete': ''})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Order.objects.filter(id=id).count(), 0)

    def test_detail_update(self):
        update_data = {
            "status": "Оплачено"
        }
        id = 3
        path = reverse('detail', kwargs={'order_id': id})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/detail.html')
        self.assertEqual(response.context_data['object'].status, "В ожидании")
        response = self.client.post(path, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.get(id=id).status, update_data['status'])

    def test_create(self):
        data = {
            "table_number": "20",
            "items": "example 200\r\nexample 500.00",
        }
        path = reverse('create')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/create.html')
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Order.objects.first().id, 10)