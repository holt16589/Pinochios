from django.contrib import admin

# Register your models here.
from .models import regularPizza, sicilianPizza, toppings, subs, pasta, dinnerPlatters, order, order_items, categories, salad

admin.site.register(regularPizza)
admin.site.register(sicilianPizza)
admin.site.register(toppings)
admin.site.register(salad)
admin.site.register(subs)
admin.site.register(pasta)
admin.site.register(dinnerPlatters)
admin.site.register(order)
admin.site.register(order_items)
admin.site.register(categories)
