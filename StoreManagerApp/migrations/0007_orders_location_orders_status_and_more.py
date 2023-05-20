# Generated by Django 4.1.7 on 2023-05-16 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagerApp', '0006_remove_orders_orderedproducts_orderitem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='Location',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='orders',
            name='Status',
            field=models.CharField(choices=[('Preparing', 'Preparing'), ('OnDelivery', 'OnDelivery'), ('Delivered', 'Delivered')], default='Preparing', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='Decription',
            field=models.TextField(max_length=255),
        ),
    ]