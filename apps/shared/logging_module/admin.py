from django.contrib import admin
from .models import ApiActionLog


# Modelni admin panelda ro'yxatdan o'tkazish uchun maxsus sinf yaratamiz.
# Bu admin panelini ancha qulay va informativ qiladi.
@admin.register(ApiActionLog)
class ApiActionLogAdmin(admin.ModelAdmin):
    """
    ApiActionLog modeli uchun admin panel sozlamalari.
    """
    # Admin panelidagi ro'yxatda ko'rinadigan ustunlar
    list_display = ('api_name', 'status_code', 'user', 'created_at')

    # O'ng tomonda paydo bo'ladigan filtrlar
    list_filter = ('api_name', 'status_code', 'created_at')

    # Qidiruv maydoni qaysi ustunlar bo'yicha ishlashi
    search_fields = ('request_payload', 'response_data', 'user__username')

    # Faqat o'qish uchun mo'ljallangan maydonlar (tahrirlab bo'lmaydi)
    readonly_fields = ('created_at',)

    # Sana bo'yicha tezkor navigatsiya
    date_hierarchy = 'created_at'