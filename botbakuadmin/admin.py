from django.contrib import admin
from botbakuadmin.models import Category, SubCategory, Beer, Eat, Product, Text, TgUser, CasinoUser, Casino


# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Product
    extra = 1
    prepopulated_fields = {"slug_name": ("name",)}
    fields = ['in_stock', 'name', 'slug_name', 'price', 'subcategory', ]
    # fieldsets = [
    #     ('Наличие', {'fields': ['in_stock']}),
    #     ('2', {'fields': ['price']}),
    # ]


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug_name": ("name",)}


class SubCategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug_name": ("name",)}


class ProductModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug_name": ("name",)}


class BeerModelAdmin(admin.ModelAdmin):
    inlines = [ProductInline, ]
    list_display = ['__str__', 'get_subcategory', 'get_instock', 'get_price']
    list_filter = ['product__subcategory__name', 'product__in_stock']
    search_fields = ['product__name']
    fieldsets = [
        ('ХАРАКТЕРИСТИКИ', {'fields': ['style', 'abv', 'ibu', 'og', 'size', 'manufacturer', 'country']})
    ]

    def get_subcategory(self, obj):
        return obj.product.subcategory.name.upper()

    def get_instock(self, obj):
        return obj.product.in_stock

    def get_price(self, obj):
        return obj.product.price

    get_subcategory.short_description = 'Подкатегория'
    get_instock.short_description = 'Вналичии'
    get_instock.boolean = True
    get_price.short_description = 'Цена'


class EatModelAdmin(admin.ModelAdmin):
    inlines = [ProductInline, ]
    list_display = ['__str__', 'get_subcategory', 'get_instock', 'get_price']
    list_filter = ['product__subcategory__name', 'product__in_stock']
    search_fields = ['product__name']

    def get_subcategory(self, obj):
        return obj.product.subcategory.name.upper()

    def get_instock(self, obj):
        return obj.product.in_stock

    def get_price(self, obj):
        return obj.product.price

    get_instock.short_description = 'Вналичии'
    get_instock.boolean = True
    get_price.short_description = 'Цена'

    get_subcategory.short_description = 'Подкатегория'


class TextModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug_name": ("name",)}


class TgUserModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'register_date', 'last_date']
    readonly_fields = ['name', 'phone', 'user_id']


class CasinoModelAdmin(admin.ModelAdmin):
    pass


class CasinoUserModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryModelAdmin)
admin.site.register(SubCategory, SubCategoryModelAdmin)
admin.site.register(Beer, BeerModelAdmin)
admin.site.register(Eat, EatModelAdmin)
admin.site.register(Text, TextModelAdmin)
admin.site.register(TgUser, TgUserModelAdmin)
admin.site.register(Casino, CasinoModelAdmin)
admin.site.register(CasinoUser, CasinoUserModelAdmin)
admin.site.site_header = 'Управление ботом'
