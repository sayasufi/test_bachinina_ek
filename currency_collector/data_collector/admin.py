from django.contrib import admin

from .models import Currency, CurrencyRate


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('char_code', 'name')
    search_fields = ('char_code', 'name')


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'value')
    list_filter = ('currency', 'date')
    search_fields = ('currency__char_code', 'currency__name')


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
