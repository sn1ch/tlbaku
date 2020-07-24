from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Имя Категория', unique=True)
    slug_name = models.SlugField()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name='Имя Категория', unique=True)
    slug_name = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    slug_name = models.SlugField(verbose_name='slug name(заполняется автоматически)')
    img = models.CharField(max_length=264,
                           default='AgACAgIAAxkBAAILT18XUe6mdD-g1arbv20TP8Tl00qSAALTrjEbtuu5SF6v994XcN50pXjrki4AAwEAAwIAA3kAAy4MBAABGgQ')
    price = models.SmallIntegerField(verbose_name='Цена')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    beer = models.OneToOneField('Beer', on_delete=models.CASCADE, null=True)
    eat = models.OneToOneField('Eat', on_delete=models.CASCADE, null=True)
    in_stock = models.BooleanField(verbose_name='Вналичии', default=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукт'

    def __str__(self):
        return self.name


class Beer(models.Model):
    style = models.CharField(max_length=128, verbose_name='Стиль', default='ipa')
    ibu = models.SmallIntegerField(verbose_name='IBU', null=True)
    abv = models.FloatField(max_length=3, verbose_name='ABV')
    og = models.SmallIntegerField(verbose_name='OG', null=True)
    country = models.CharField(max_length=3, verbose_name='Страна', default='RU')
    size = models.FloatField(verbose_name='Объем(литры)')
    manufacturer = models.CharField(max_length=64, verbose_name='Производитель(пивоварня)', null=True,
                                    default='БАКУНИН')

    class Meta:
        verbose_name = 'Пиво'
        verbose_name_plural = 'Пиво'

    def __str__(self):
        return self.product.name


class Eat(models.Model):
    text = models.TextField(verbose_name='Описание')
    size = models.SmallIntegerField(verbose_name='Размер порции(грамм)')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Еда'
        verbose_name_plural = 'Еда'


class Text(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название текста')
    slug_name = models.SlugField(verbose_name='slug name(заполняется автоматически)', null=True)
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тексты'
        verbose_name_plural = 'Тексты'


class TgUser(models.Model):
    user_id = models.IntegerField(verbose_name='ID')
    name = models.CharField(max_length=64, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=20)
    register_date = models.DateField(auto_now_add=True, verbose_name='Дата первого заказа')
    last_date = models.DateField(auto_now=True, verbose_name='Дта последнего заказа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Casino(models.Model):
    text = models.TextField(verbose_name='Текст конкурса',
                            default='Не забудь, удалить всех пользователей из таблицы "Участники конкурса", '
                                    'перед созданием нового конкурса')

    def __str__(self):
        return f'{self.text[:7]}...'

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурс'


class CasinoUser(models.Model):
    name = models.CharField(max_length=64, verbose_name='Имя')
    user_id = models.IntegerField(verbose_name='ID')
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Участники конкурса'
        verbose_name_plural = 'Участники конкурса'
