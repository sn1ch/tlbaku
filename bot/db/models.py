from tortoise import Tortoise, fields
from tortoise.models import Model


class Botbakuadmin_category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    slug_name = fields.CharField(max_length=64)

    def __repr__(self):
        return self.name


class Botbakuadmin_subcategory(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    slug_name = fields.CharField(max_length=64)
    category: fields.ForeignKeyRelation[Botbakuadmin_category] = fields.ForeignKeyField("models.Botbakuadmin_category",
                                                                                        related_name="subcategory")
    product: fields.ReverseRelation["Botbakuadmin_product"]

    def __repr__(self):
        return self.name


class Botbakuadmin_beer(Model):
    style = fields.CharField(max_length=64)
    ibu = fields.SmallIntField()
    abv = fields.FloatField()
    og = fields.SmallIntField()
    country = fields.CharField(max_length=64)
    manufacturer = fields.CharField(max_length=64)
    size = fields.FloatField()

    # def __repr__(self):
    # return self.name


class Botbakuadmin_eat(Model):
    text = fields.TextField()
    size = fields.SmallIntField()


class Botbakuadmin_product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    slug_name = fields.CharField(max_length=64)
    img = fields.CharField(max_length=256)
    price = fields.SmallIntField()
    in_stock = fields.BooleanField(default=True)
    subcategory: fields.ForeignKeyRelation[Botbakuadmin_subcategory] = fields.ForeignKeyField(
        'models.Botbakuadmin_subcategory', on_delete=fields.CASCADE)
    beer: fields.OneToOneRelation[Botbakuadmin_beer] = fields.OneToOneField('models.Botbakuadmin_beer',
                                                                            on_delete=fields.CASCADE)
    eat: fields.OneToOneRelation[Botbakuadmin_eat] = fields.OneToOneField('models.Botbakuadmin_eat',
                                                                          on_delete=fields.CASCADE)

    def __repr__(self):
        return self.name


class Botbakuadmin_text(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32)
    slug_name = fields.CharField(max_length=32)
    text = fields.TextField()

    def __repr__(self):
        return self.name


class Botbakuadmin_tguser(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    name = fields.CharField(max_length=64)
    phone = fields.CharField(max_length=20)
    register_date = fields.DatetimeField(auto_now_add=True)
    last_date = fields.DatetimeField(auto_now=True)

    def __repr__(self):
        return self.name


class Botbakuadmin_casino(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField(verbose_name='Текст конкурса', default='Не за')

    def __repr__(self):
        return self.text[0:7]


class Botbakuadmin_casinouser(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    user_id = fields.IntField(verbose_name='ID')
    register_date = fields.DatetimeField(auto_now_add=True)

    def __repr__(self):
        return self.name
