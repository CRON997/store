from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from products.models import Product
class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'ElectroHub')
        self.assertTemplateUsed(response, 'products/index.html')
        
        
class ProductListViewTestCase(TestCase):
    fixtures = ['products.json', 'categories.json']  # Load test data from fixtures
    def test_products_list_view(self):
        path = reverse('products:index')
        response = self.client.get(path)
        
        products = Product.objects.all()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'ElectroHub - Catalog')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['object_list'].count(), products.count())
        