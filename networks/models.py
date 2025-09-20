from django.db import models

from networks.validators import validate_all


class ElectronicsNetwork(models.Model):
    TYPE_CHOICES = (
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    )

    name = models.CharField(max_length=255, verbose_name="Название звена")
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name="Тип звена")
    level = models.IntegerField(default=0, verbose_name="Уровень в иерархии", editable=False)


    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    product_name = models.CharField(max_length=255, verbose_name="Название продукта")
    product_model = models.CharField(max_length=255, verbose_name="Модель продукта")
    product_release_date = models.DateField(
        verbose_name="Дата выхода продукта на рынок"
    )

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        related_name="children",
    )

    debt_to_supplier = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность перед поставщиком",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def clean(self):
        """Валидация данных перед сохранением с использованием внешних валидаторов"""
        super().clean()
        validate_all(self)

    def full_clean(self, *args, **kwargs):
        """Переопределяем full_clean чтобы гарантировать вызов нашего clean()"""
        super().full_clean(*args, **kwargs)
        self.clean()

    def save(self, *args, **kwargs):
        """Автоматически вычисляет уровень иерархии"""
        if self.type == 0:
            self.level = 0
        else:
            if self.supplier is None:
                self.level = 0
            else:
                if self.supplier.pk is None:
                    self.supplier.save()
                self.level = self.supplier.level + 1

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
