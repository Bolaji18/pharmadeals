from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Pharma, Categories, cart, popular, buyerinfo, boughtitem

# pharma/test_tests.py

class TestSetUpMethod(TestCase):
    def setUp(self):
        # Recreate the setup from PharmaDealsTestCase
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.category = Categories.objects.create(category='Test Category')
        self.pharma = Pharma.objects.create(name='Test Product', price=100, user=self.user, categor=self.category, Approval=True, shipping=1, stock=10, description='Test Description')
        self.popular_item = popular.objects.create(name=self.pharma, views=10)
        self.cart_item = cart.objects.create(user=self.user, name=self.pharma, quantity=2)
        self.buyer_info = buyerinfo.objects.create(user=self.user, name='Test Buyer', email='buyer@example.com')
        self.bought_item = boughtitem.objects.create(
            email='seller@example.com',
            name='Seller Name',
            users=self.user.username,
            product_name=self.pharma.name,
            quantity=2,
            total_earned=200,
            order_id=1,
            buyer_info=self.buyer_info
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_category_creation(self):
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(self.category.category, 'Test Category')

    def test_pharma_creation(self):
        self.assertEqual(Pharma.objects.count(), 1)
        self.assertEqual(self.pharma.name, 'Test Product')
        self.assertEqual(self.pharma.price, 100)
        self.assertEqual(self.pharma.stock, 10)
        self.assertTrue(self.pharma.Approval)

    def test_popular_creation(self):
        self.assertEqual(popular.objects.count(), 1)
        self.assertEqual(self.popular_item.name, self.pharma)
        self.assertEqual(self.popular_item.views, 10)

    def test_cart_creation(self):
        self.assertEqual(cart.objects.count(), 1)
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.name, self.pharma)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_buyerinfo_creation(self):
        self.assertEqual(buyerinfo.objects.count(), 1)
        self.assertEqual(self.buyer_info.name, 'Test Buyer')
        self.assertEqual(self.buyer_info.email, 'buyer@example.com')

    def test_boughtitem_creation(self):
        self.assertEqual(boughtitem.objects.count(), 1)
        self.assertEqual(self.bought_item.email, 'seller@example.com')
        self.assertEqual(self.bought_item.product_name, self.pharma.name)
        self.assertEqual(self.bought_item.total_earned, 200)
# Create your tests here.
