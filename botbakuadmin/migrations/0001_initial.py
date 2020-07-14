# Generated by Django 3.0.7 on 2020-06-29 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ibu', models.SmallIntegerField(null=True, verbose_name='IBU')),
                ('abv', models.FloatField(max_length=3, verbose_name='ABV')),
                ('og', models.SmallIntegerField(null=True, verbose_name='OG')),
                ('country', models.CharField(default='RU', max_length=3, verbose_name='Страна')),
                ('size', models.FloatField(verbose_name='Объем(литры)')),
                ('manufacturer', models.CharField(default='БАКУНИН', max_length=64, null=True, verbose_name='Производитель(пивоварня)')),
            ],
            options={
                'verbose_name': 'Пиво',
                'verbose_name_plural': 'Пиво',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Имя Категория')),
                ('slug_name', models.SlugField()),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Eat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Описание')),
                ('size', models.SmallIntegerField(verbose_name='Размер порции(грамм)')),
            ],
            options={
                'verbose_name': 'Еда',
                'verbose_name_plural': 'Еда',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Имя Категория')),
                ('slug_name', models.SlugField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botbakuadmin.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('slug_name', models.SlugField()),
                ('img', models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Изображение')),
                ('price', models.SmallIntegerField(verbose_name='Цена')),
                ('in_stock', models.BooleanField(default=True, verbose_name='Вналичии')),
                ('beer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='botbakuadmin.Beer')),
                ('eat', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='botbakuadmin.Eat')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botbakuadmin.SubCategory', verbose_name='Подкатегория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукт',
            },
        ),
    ]
