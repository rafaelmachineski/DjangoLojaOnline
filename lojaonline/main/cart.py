from decimal import Decimal
from .models import Produto



class Cart(object):
    def __init__(self, request):

        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantidade': 0,
                                     'preco': str(product.preco)}
        if update_quantity:
            self.cart[product_id]['quantidade'] = quantity
        else:
            self.cart[product_id]['quantidade'] += quantity
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Produto.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['preco'] = Decimal(item['preco'])
            item['preco_total'] = item['preco'] * item['quantidade']
            yield item
        
    def __len__(self):
        return sum(item['quantidade'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['preco'])*item['quantidade'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.session.modified = True
