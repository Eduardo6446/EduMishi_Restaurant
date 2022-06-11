# Generated by Django 3.0.7 on 2022-06-09 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Extras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Introduce el nombre del extra', max_length=64)),
                ('price', models.DecimalField(decimal_places=2, default=0, help_text='Introduzca el precio del extra', max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Menu_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('Pizza', 'Pizza'), ('Pasta', 'Pasta'), ('Subs', 'Subs'), ('Salad', 'Salad'), ('Dinner_Platter', 'Dinner_Platter'), ('Topping', 'Topping'), ('Extra', 'Extra'), ('Dessert', 'Dessert'), ('Pastry', 'Pastry'), ('Main', 'Main'), ('Appetizer', 'Appetizer'), ('Side', 'Side'), ('Miscellaneous', 'Miscellaneous')], help_text='Categoría del elemento del menú.', max_length=36, null=True)),
                ('name', models.CharField(help_text='Nombre del elemento del menú', max_length=128)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True)),
                ('sizes', models.CharField(blank=True, choices=[('Sm', 'Small'), ('Md', 'Medium'), ('Lg', 'Large'), ('XL', 'Extra_Large')], help_text='Ingrese el tamaños                                             del elemento del menú', max_length=4, null=True)),
                ('toppings', models.CharField(blank=True, help_text='Introducir ingredientes', max_length=400, null=True)),
                ('num_toppings', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topping_name', models.CharField(max_length=36)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_items', models.ManyToManyField(blank=True, to='orders.Menu_Item')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('date_ordered', models.DateTimeField(null=True)),
                ('is_topping', models.BooleanField(default=False)),
                ('num_extras', models.IntegerField(blank=True, default=0)),
                ('extras', models.CharField(blank=True, max_length=400, null=True)),
                ('extras_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('ptoppings', models.CharField(blank=True, max_length=400, null=True)),
                ('menu_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Menu_Item')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(blank=True, max_length=15)),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(auto_now=True)),
                ('ordered_items', models.ManyToManyField(to='orders.OrderItem')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Profile')),
            ],
        ),
    ]