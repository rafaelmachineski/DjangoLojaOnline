from datetime import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate,  login

from .cart import Cart




from .models import Marca, Pedido, Venda, Produto

from .forms import AdicionarCarrinhoForm, AtualizarCadastroForm, LoginForm, RegisterForm




class BaseView(View):

    pedidos_pendentes = Pedido.objects.filter(status = 1).__len__()


    def get(self, request):



        cart = Cart(request)
        product_list = Produto.objects.order_by()
        template = loader.get_template("main/index.html")
        context = {"product_list": product_list,  'cart': cart, 'pedidos_pendentes': self.pedidos_pendentes}
        return HttpResponse(template.render(context, request))
    
class ProductTypeView(BaseView):
    product_type=''
    cat_number = 0

    def get(self, request):
        cart = Cart(request)
        product_list = Produto.objects.filter(categoria = self.cat_number).order_by()
        marca_list = Marca.objects.all()
        template = loader.get_template(f"main/{self.product_type}.html") 
        context = {"product_list": product_list, "marca_list": marca_list,  'cart': cart}
        return HttpResponse(template.render(context, request))
    
class MonitorView(ProductTypeView):
    product_type='monitor'
    cat_number=5

class FoneView(ProductTypeView):
    product_type='fone'
    cat_number=4

class MousepadView(ProductTypeView):
    product_type='mousepad'
    cat_number=3

class TecladoView(ProductTypeView):
    product_type='teclado'
    cat_number=2

class MouseView(ProductTypeView):
    product_type='mouse'
    cat_number=1

class BuscarView(BaseView):

    
    def get(self, request):
        cart = Cart(request)
        search_query = request.GET.get('search_query')
        product_list = Produto.objects.filter(nome__contains=search_query)
        template = loader.get_template("main/busca.html")
        context = {"product_list": product_list,  'cart': cart}
        return HttpResponse(template.render(context, request))
    

class LogarView(BaseView):

    def get(self, request):
        cart = Cart(request)
        form = LoginForm()

        if request.user.is_authenticated:
            return HttpResponse('Usuário já logado! Saia da conta para fazer novo login')
        else:
            return render(request, 'main/login.html', {'form': form, 'cart': cart})




    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                    password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                print('login sucesso')
                return HttpResponseRedirect('/')
        else:
            return HttpResponse('Usuário não existe ou senha incorreta!')


class CadastroView(BaseView):

    def get(self, request):
        cart = Cart(request)
        form = RegisterForm()
        return render(request, 'main/cadastro.html', {'form': form, 'cart': cart})
    def post(self, request):
        cart = Cart(request)
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso!.')
            return redirect('/')
        else:
            return render(request, 'main/cadastro.html', {'form': form})

    
class CarrinhoView(BaseView):

    def get(self, request):
        cart = Cart(request)
        template = loader.get_template("main/carrinho.html")
        context = {'cart': cart}
        return HttpResponse(template.render(context, request))
    def post(self, request):
        cart = Cart(request)
        product = get_object_or_404(Produto, id = request.POST['id'])
        form = AdicionarCarrinhoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantidade'],
            update_quantity=cd['update'])
        else:
            print('fail')
        return redirect("/carrinho")
    
class LimparCarrinhoView(BaseView):

    def post(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect("/carrinho")


class ProcutoView(BaseView):

    def get(self, request, slug):
        cart = Cart(request)
        product= Produto.objects.get(slug=slug)
        template = loader.get_template("main/produto.html")
        context = {"product": product,  'cart': cart}
        return HttpResponse(template.render(context, request))
    
class RemoverProdutoView(BaseView):

    def post(self, request):
        cart = Cart(request)
        product = get_object_or_404(Produto, id = request.POST['id'])
        cart.remove(product)
        return redirect("/carrinho")

class FinalizarCompraView(BaseView):

    def post(self, request):
        if request.user.is_authenticated:
            cart = Cart(request)
            pedido = Pedido.objects.create(usuario = request.user, data_pub = datetime.now())
            pedido_preco_total = 0
            for item in cart:
                Venda.objects.create(quantidade = item['quantidade'], produto = item['product'], pedido = pedido,
                                     preco = item['preco'],
                                      preco_total = item['preco_total'] )
                pedido_preco_total += item['preco_total']
            pedido.preco_total = pedido_preco_total
            pedido.save()

            cart.clear()
            return redirect("/pedidos")
        else:
            return redirect("/logar")

class MinhaContaView(BaseView):

    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart(request)
            form = AtualizarCadastroForm(user=request.user) 
            template = loader.get_template("main/minha-conta.html")
            context = {'cart': cart, 'form': form}
            return HttpResponse(template.render(context, request))
        else:
            return redirect("/logar")
    
    def post(self, request):
        return HttpResponse('post')

class PedidosView(BaseView):

    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart(request)
            pedidos = reversed(Pedido.objects.filter(usuario = request.user).values())
            context = {'pedidos': pedidos, 'cart': cart}
            template = loader.get_template("main/pedidos.html")
            return HttpResponse(template.render(context, request))
        return redirect("/logar")

class PedidoView(BaseView):

    def get(self, request, pedido_id):

        pedido = Pedido.objects.filter(id = pedido_id).values()
        user_id = pedido[0]['usuario_id']
        if request.user.id == user_id:
            cart = Cart(request)
            template = loader.get_template("main/pedido.html")
            vendas = Venda.objects.filter(pedido=pedido_id)
            context = {'pedido': pedido[0], 'vendas': vendas, 'cart': cart}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseForbidden()




