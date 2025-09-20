from django.contrib import admin
from django.utils.html import format_html
from .models import ElectronicsNetwork
from django.core.exceptions import ValidationError


@admin.register(ElectronicsNetwork)
class ElectronicsNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'city', 'supplier_link', 'debt_to_supplier', 'created_at')
    list_filter = ('city',)
    list_display_links = ('name',)
    actions = ('clear_debt',)

    def save_model(self, request, obj, form, change):
        print(f"DEBUG: save_model called for {obj.name}, supplier: {obj.supplier}")
        try:
            obj.full_clean()
            print("DEBUG: Validation passed")
        except ValidationError as e:
            print(f"DEBUG: Validation failed: {e}")


    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/networks/electronicsnetwork/{obj.supplier.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = 'Поставщик'


    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt_to_supplier=0.00)
        self.message_user(request, f'Задолженность очищена для {updated_count} объектов.')

    clear_debt.short_description = 'Очистить задолженность перед поставщиком'
