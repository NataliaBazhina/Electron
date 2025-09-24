from django.core.exceptions import ValidationError


def validate_all(instance):
    """
    Комплексная валидация для объекта ElectronicsNetwork
    """
    is_factory = instance.type == 0

    if is_factory:
        real_level = 0
    else:
        if instance.supplier is None:
            real_level = 0
        else:
            if instance.supplier.pk is None:
                instance.supplier.save()
            real_level = instance.supplier.level + 1

    if real_level > 2:
        raise ValidationError(
            {"supplier": "Максимальная глубина иерархии в сети - 3 уровня"}
        )

    if is_factory and instance.supplier is not None:
        raise ValidationError({"supplier": "Завод не может иметь поставщика"})

    if is_factory and float(instance.debt_to_supplier) != 0:
        raise ValidationError({"debt_to_supplier": "Завод не может иметь задолженности"})

    if (instance.supplier and
            hasattr(instance, 'id') and
            instance.id is not None and
            instance.supplier.id == instance.id):
        raise ValidationError({"supplier": "Объект не может быть своим поставщиком"})

    if not is_factory and instance.supplier:
        supplier_level = instance.supplier.level

        if supplier_level == 0 and real_level != 1:
            raise ValidationError({"supplier": "Только уровень 1 может ссылаться на завод"})

        if supplier_level >= real_level:
            raise ValidationError({"supplier": "Уровень должен быть выше уровня поставщика"})