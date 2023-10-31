
from django.contrib import admin
from django.urls import include, path

from main import views



app_name = 'main'



urlpatterns = [
    path('', views.BaseView.as_view(), name='index'),
    path('', include('django.contrib.auth.urls')),
    path("logar/", views.LogarView.as_view(), name="logar"),
    path("cadastro/", views.CadastroView.as_view(), name="cadastro"),
    path("minha-conta/", views.MinhaContaView.as_view(), name="minha-conta"),
    path("pedidos/", views.PedidosView.as_view(), name="pedidos"),
    path("pedidos/<int:pedido_id>/", views.PedidoView.as_view(), name="pedido"),
    path("carrinho/", views.CarrinhoView.as_view(), name="carrinho"),
    path("finalizar-compra/", views.FinalizarCompraView.as_view(), name="finalizar-compra"),
    path("limpar-carrinho/", views.LimparCarrinhoView.as_view(), name="limpar-carrinho"),
    path("remover/", views.RemoverProdutoView.as_view(), name="remover"),
    path("produto/<slug:slug>/", views.ProcutoView.as_view(), name="produto"),
    path("categoria/mouse/",  views.MouseView.as_view(), name="mouse"),
    path("categoria/teclado/",  views.TecladoView.as_view(), name="teclado"),
    path("categoria/mousepad/", views.MousepadView.as_view(), name="mousepad"),
    path("categoria/fone/", views.FoneView.as_view(), name="fone"),
    path("categoria/monitor/", views.MonitorView.as_view(), name="monitor"),
    path('buscar/', views.BuscarView.as_view(), name='buscar'),
    path("admin/", admin.site.urls),
    
]