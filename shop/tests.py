from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product
from django.contrib.auth.models import User

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.slug, 'electronics')
        self.assertEqual(str(self.category), 'Electronics')

    def test_get_absolute_url(self): #
        self.assertEqual(self.category.get_absolute_url(), reverse('shop:product_list_by_category', args=['electronics']))

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Smartphone',
            slug='smartphone',
            description='A smartphone description',
            price=299.99,
            available=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Smartphone')
        self.assertEqual(self.product.slug, 'smartphone')
        self.assertEqual(self.product.price, 299.99)
        self.assertEqual(self.product.description, 'A smartphone description')
        self.assertTrue(self.product.available)
        self.assertEqual(str(self.product), 'Smartphone')

    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), reverse('shop:product_detail', args=[self.product.id, self.product.slug]))

class ShopViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Smartphone',
            slug='smartphone',
            description='A smartphone description',
            price=299.99,
            available=True
        )

    def test_product_list_view(self):
        url = reverse('shop:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_product_list_by_category_view(self):
        url = reverse('shop:product_list_by_category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_product_detail_view(self):
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')
        self.assertTemplateUsed(response, 'shop/product/detail.html')
