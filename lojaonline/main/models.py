from django.conf import settings
from django.db import models
from django.utils.text import slugify 

# Create your models here.

ESCOLHA_CATEGORIAS = (

    (1, ("Mouse")),
    (2, ("Teclado")),
    (3, ("Mousepad")),
    (4, ("Fone")),
    (5, ("Monitor")),
)


STATUS_PEDIDO = (

    (1, ("Aguardando envio")),
    ( 2, ("Enviado")),
    ( 3, ("Entregue")),

)

class Marca(models.Model):
    nome = models.CharField(max_length=50)
    origem = models.CharField(max_length=50, default='BR')

    def __str__(self):
        return self.nome     

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    marca = models.ForeignKey(Marca, default=None,  on_delete=models.CASCADE )
    categoria = models.IntegerField(choices=ESCOLHA_CATEGORIAS)
    preco = models.FloatField(max_length=20, default=0)
    slug = models.SlugField( default='')
    descricao = models.TextField(default='')
    estoque = models.IntegerField(default=0)
    foto = models.ImageField( default='image-cap.png')
    data_pub = models.DateTimeField('Data de publicacao')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{ESCOLHA_CATEGORIAS[self.categoria-1][1]} {self.nome} '
    
    
    
class Pedido(models.Model):
    status = models.IntegerField(choices=STATUS_PEDIDO, default = 1)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    preco_total = models.FloatField(default=0)
    data_pub = models.DateTimeField('Data do pedido')


    def __str__(self):
        return f'Pedido id = {self.id}'
    
    def getStatus(self):
        return  self.status
    


class Venda(models.Model):
    quantidade = models.PositiveIntegerField()
    produto = models.ForeignKey(Produto, on_delete = models.PROTECT)
    pedido = models.ForeignKey(Pedido, on_delete = models.PROTECT)
    preco= models.FloatField(default=0)
    preco_total = models.FloatField(default=0)

    


    def __str__(self):
        return f'{self.produto} / Pedido id = {self.pedido.id}'
    
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
    


