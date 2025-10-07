from django.db import models
from django.conf import settings

class ApiActionLog(models.Model):
    """
    Har bir tashqi API so'rovi va uning javobini xom holatda saqlaydigan universal model.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Foydalanuvchi",
        help_text="So'rovni yuborgan tizim foydalanuvchisi (agar mavjud bo'lsa)"
    )
    api_name = models.CharField(
        "API nomi",
        max_length=100,
        help_text="So'rov yuborilgan API nomi (masalan, 'notary', 'tax')",
        db_index=True # Bu maydon bo'yicha qidiruvni tezlashtiradi
    )
    request_payload = models.JSONField(
        "So'rov tanasi (Request Payload)",
        help_text="Tashqi API'ga yuborilgan ma'lumotlar"
    )
    response_data = models.JSONField(
        "Javob tanasi (Response Data)",
        help_text="Tashqi API'dan qaytgan javob",
        null=True, blank=True
    )
    status_code = models.PositiveIntegerField(
        "HTTP Status Kodi",
        help_text="So'rovning HTTP statusi (masalan, 200)",
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        "Yaratilgan vaqti",
        auto_now_add=True,
        help_text="So'rov jo'natilgan vaqt"
    )

    def __str__(self):
        # Admin panelida tushunarli ko'rinishi uchun
        user_info = f" by {self.user.username}" if self.user else ""
        return f"API: {self.api_name}{user_info} - Status: {self.status_code} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "API So'rov Logi"
        verbose_name_plural = "API So'rovlari Loglari"
        ordering = ['-created_at'] # Eng yangilari birinchi bo'lib ko'rinadi
        db_table = 'shared_api_action_log'

