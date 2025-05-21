from django.contrib import admin
from .models import Customer, Order,Blog,Author,Todo


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'pincode', 'create_at']
    search_fields = ('name', 'email','pincode')
    list_filter = ('name', 'email')
    ordering = ('create_at',)

# Register your models here.
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order)
admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Todo)