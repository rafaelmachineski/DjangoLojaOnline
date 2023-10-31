from django.contrib import admin

from main.models import Pedido, Venda, Produto, Marca

class CompraAdmin(admin.ModelAdmin):
    list_display = ('produto', 'pedido', 'quantidade',  'preco_total') 

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_pub', 'status', 'preco_total', 'usuario' )

class ProdutoAdmin(admin.ModelAdmin):
    exclude = ('slug',)



# Register your models here.
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Marca)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Venda, CompraAdmin)

