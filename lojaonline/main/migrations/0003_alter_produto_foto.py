# Generated by Django 4.2.6 on 2023-10-18 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_produto_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='foto',
            field=models.ImageField(default='image-cap.png', upload_to=''),
        ),
    ]