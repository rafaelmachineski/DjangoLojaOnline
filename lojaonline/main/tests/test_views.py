
import os



from django import setup
from django.urls import reverse


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lojaonline.settings")
setup()


from django.test import Client, TestCase


class IndexTests(TestCase):
    databases = '__all__'

    def setUp(self):
        self.client = Client()

    def test_page_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

class CarrinhoTests(TestCase):
    databases = '__all__'

    def setUp(self):
        self.client = Client()

    def test_page_works(self):
        response = self.client.get("/carrinho/")
        self.assertEqual(response.status_code, 200)

class CategoriaTests(TestCase):
    databases = '__all__'

    def setUp(self):
        self.client = Client()

    def test_page_works(self):

        options = ['mouse', 'teclado', 'mousepad', 'fone', 'monitor']
        
        for option in options:
            response = self.client.get(f"/categoria/{option}/")
            self.assertEqual(response.status_code, 200)


class BuscarTests(TestCase):
    databases = '__all__'

    def setUp(self):
        self.client = Client()

    def test_page_works(self):
        response = self.client.get('/buscar/', {'search_query': ''})
        self.assertEqual(response.status_code, 200)

class ProdutoTests(TestCase):
    databases = '__all__'

    def setUp(self):
        self.client = Client()

    def test_page_works(self):
        response = self.client.get('/produto/mouse-razer-viper/', args=('mouse-razer-viper'))
        self.assertEqual(response.status_code, 200)

