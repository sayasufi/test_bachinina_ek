from django.db import models


class Currency(models.Model):
    char_code = models.CharField(max_length=10, unique=True, verbose_name="Код валюты")
    name = models.CharField(max_length=255, verbose_name="Название валюты")

    class Meta:
        unique_together = ('char_code', 'name')
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return f"{self.char_code} - {self.name}"


class CurrencyRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="rates", verbose_name="Валюта")
    date = models.DateField(verbose_name="Дата")
    value = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Значение курса")

    class Meta:
        unique_together = ('currency', 'date')
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"

    def __str__(self):
        return f"{self.currency.char_code} {self.date} {self.value}"
