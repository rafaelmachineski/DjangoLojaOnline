# Generated by Django 4.2.6 on 2023-10-26 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_pedido_pedidoproduto'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PedidoProduto',
            new_name='ConjuntoProduto',
        ),
        migrations.AlterModelOptions(
            name='conjuntoproduto',
            options={'verbose_name': 'Produto associado a pedido', 'verbose_name_plural': 'Produtos associados a pedido '},
        ),
    ]